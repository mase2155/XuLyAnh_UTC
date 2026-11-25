"""Gom CSV lưới thành trung bình, độ lệch chuẩn, min và max."""

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path


def summarize(rows: list[dict[str, str]], value_column: str = "psnr") -> list[dict[str, str]]:
    grouped: dict[tuple[str, str, str, str], list[float]] = defaultdict(list)
    for row in rows:
        key = (row["noise"], row["level"], row["method"], row.get("params", ""))
        grouped[key].append(float(row[value_column]))

    summary = []
    for key, values in grouped.items():
        count = len(values)
        mean = sum(values) / count
        if count > 1:
            variance = sum((value - mean) ** 2 for value in values) / (count - 1)
            spread = math.sqrt(variance)
            spread_text = f"{spread:.6f}"
        else:
            spread_text = ""
        noise, level, method, params = key
        summary.append(
            {
                "noise": noise,
                "level": level,
                "method": method,
                "params": params,
                "n": str(count),
                f"{value_column}_mean": f"{mean:.6f}",
                f"{value_column}_std": spread_text,
                f"{value_column}_min": f"{min(values):.6f}",
                f"{value_column}_max": f"{max(values):.6f}",
            }
        )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--value", default="psnr")
    args = parser.parse_args()
    with args.input.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    summary = summarize(rows, args.value)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = (
        "noise",
        "level",
        "method",
        "params",
        "n",
        f"{args.value}_mean",
        f"{args.value}_std",
        f"{args.value}_min",
        f"{args.value}_max",
    )
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary)
    print(f"Đã ghi {len(summary)} dòng vào {args.output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
