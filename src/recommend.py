"""Khung khuyến nghị và một dòng đọc từ kết quả BSD68."""

import csv
from pathlib import Path

from src.pipeline import METHODS

NOISE_TYPES = ("gaussian", "salt_pepper", "poisson")
SUMMARY_PATH = Path(__file__).resolve().parents[1] / "results" / "bsd68_summary.csv"

_METHOD_NAME = {
    "mean": "trung bình",
    "gaussian": "Gauss",
    "median": "trung vị",
    "adaptive_median": "trung vị thích nghi",
    "bilateral": "song phương",
    "nlm": "NLM",
}

# Khung tạm. Chưa đọc kết quả BSD68, chưa có câu giải thích.
_FILTER_BY_NOISE = {
    "gaussian": "gaussian",
    "salt_pepper": "median",
    "poisson": "gaussian",
}


def recommend_filter(noise: str) -> str:
    """Trả về tên một bộ lọc trong pipeline cho loại nhiễu đã cho."""
    if noise not in _FILTER_BY_NOISE:
        raise ValueError(f"không có loại nhiễu {noise}")
    method = _FILTER_BY_NOISE[noise]
    if method not in METHODS:
        raise ValueError(f"không có bộ lọc {method}")
    return method


def _column(fieldnames: list[str], options: tuple[str, ...]) -> str | None:
    lookup = {name.strip().lower(): name for name in fieldnames}
    for option in options:
        if option in lookup:
            return lookup[option]
    return None


def _noise_key(value: str) -> str:
    text = value.strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "gauss": "gaussian",
        "gaussian": "gaussian",
        "saltpepper": "salt_pepper",
        "salt_pepper": "salt_pepper",
        "salt_and_pepper": "salt_pepper",
        "poisson": "poisson",
    }
    return aliases.get(text, text)


def _level_key(noise: str, value: str) -> float | None:
    text = value.strip()
    if text == "":
        return None
    number = float(text.replace("%", ""))
    if noise == "salt_pepper" and ("%" in value or number > 1):
        number /= 100.0
    return number


def _read_summary(path: Path) -> list[dict[str, str]]:
    sample = path.read_text(encoding="utf-8-sig")
    if not sample.strip():
        return []
    delimiter = ";" if sample.splitlines()[0].count(";") > sample.splitlines()[0].count(",") else ","
    return list(csv.DictReader(sample.splitlines(), delimiter=delimiter))


def _noise_phrase(noise: str, level: float | None) -> str:
    if noise == "gaussian" and level is not None:
        return f"Gauss σ = {level:g}"
    if noise == "salt_pepper" and level is not None:
        return f"muối tiêu {level * 100:g}%"
    if noise == "poisson":
        peak = 255 if level is None else level
        return f"Poisson peak = {peak:g}"
    if noise == "gaussian":
        return "Gauss"
    if noise == "salt_pepper":
        return "muối tiêu"
    return noise


def recommendation_line(
    noise: str,
    level: float | None = None,
    path: Path | None = None,
) -> str:
    """Một dòng khuyến nghị: bộ lọc có PSNR trung bình cao nhất trên BSD68.

    File ``results/bsd68_summary.csv`` cần cột noise, method và psnr
    (hoặc psnr_mean). Cột level và psnr_std là tùy chọn. Dấu phẩy hoặc
    chấm phẩy đều đọc được.
    """
    summary = SUMMARY_PATH if path is None else path
    if not summary.is_file():
        return "Chưa có results/bsd68_summary.csv nên chưa đọc được khuyến nghị từ BSD68."

    rows = _read_summary(summary)
    if not rows:
        return "results/bsd68_summary.csv chưa có dòng kết quả."
    fields = list(rows[0].keys())
    noise_col = _column(fields, ("noise", "noise_type"))
    method_col = _column(fields, ("method", "filter"))
    psnr_col = _column(fields, ("psnr_mean", "mean_psnr", "psnr"))
    std_col = _column(fields, ("psnr_std", "std_psnr", "std"))
    level_col = _column(fields, ("level", "sigma", "amount"))
    if noise_col is None or method_col is None or psnr_col is None:
        return "results/bsd68_summary.csv thiếu cột noise, method hoặc psnr."

    wanted = None if level is None else _level_key(noise, str(level))
    parsed = []
    for row in rows:
        if _noise_key(row[noise_col]) != noise:
            continue
        method = row[method_col].strip()
        if method not in METHODS:
            continue
        try:
            score = float(row[psnr_col])
        except ValueError:
            continue
        spread = None
        if std_col is not None and row[std_col].strip() != "":
            spread = float(row[std_col])
        row_level = None
        if level_col is not None:
            row_level = _level_key(noise, row[level_col])
        parsed.append((method, score, spread, row_level))

    if wanted is not None and any(item[3] is not None for item in parsed):
        known = [item[3] for item in parsed if item[3] is not None]
        if not any(item[3] is not None and abs(item[3] - wanted) <= 1e-6 for item in parsed):
            wanted = min(known, key=lambda item: abs(item - wanted))
        parsed = [item for item in parsed if item[3] is None or abs(item[3] - wanted) <= 1e-6]
        level = wanted

    grouped: dict[str, list[tuple[float, float | None]]] = {}
    for method, score, spread, _row_level in parsed:
        grouped.setdefault(method, []).append((score, spread))

    if not grouped:
        return f"BSD68 chưa có dòng cho nhiễu {_noise_phrase(noise, level)}."

    def mean_score(method: str) -> tuple[float, float | None]:
        values = grouped[method]
        scores = [item[0] for item in values]
        mean = sum(scores) / len(scores)
        spreads = [item[1] for item in values if item[1] is not None]
        if spreads:
            spread = sum(spreads) / len(spreads)
        elif len(scores) > 1:
            variance = sum((score - mean) ** 2 for score in scores) / (len(scores) - 1)
            spread = variance ** 0.5
        else:
            spread = None
        return mean, spread

    winner = max(grouped, key=lambda method: (mean_score(method)[0], -METHODS.index(method)))
    mean, spread = mean_score(winner)
    name = _METHOD_NAME.get(winner, winner)
    if spread is None:
        score_text = f"{mean:.2f} dB"
    else:
        score_text = f"{mean:.2f} ± {spread:.2f} dB"
    phrase = _noise_phrase(noise, level)
    return (
        f"Khuyến nghị từ BSD68: với nhiễu {phrase}, chọn {name} "
        f"vì PSNR trung bình cao nhất, {score_text}."
    )
