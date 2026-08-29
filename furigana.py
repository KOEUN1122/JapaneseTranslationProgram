"""일본어 문장을 (원문 조각, 후리가나 또는 None) 세그먼트 리스트로 변환한다.

한자가 포함된 부분에만 후리가나를 달고, 이미 가나인 부분(오쿠리가나 등)은
읽기와 겹치는 앞/뒤 구간을 잘라내어 제외한다.
"""

import fugashi

_tagger = fugashi.Tagger()


def _katakana_to_hiragana(text: str) -> str:
    return "".join(
        chr(ord(ch) - 0x60) if "ァ" <= ch <= "ヶ" else ch for ch in text
    )


def _is_kanji(ch: str) -> bool:
    return "一" <= ch <= "鿿" or ch in "々〆〇"


def _has_kanji(text: str) -> bool:
    return any(_is_kanji(ch) for ch in text)


def _split_okurigana(surface: str, reading: str):
    """surface/reading에서 공통 앞/뒤 가나를 잘라 (prefix, core_base, core_reading, suffix) 반환."""
    prefix_len = 0
    while (
        prefix_len < len(surface)
        and prefix_len < len(reading)
        and not _is_kanji(surface[prefix_len])
        and surface[prefix_len] == reading[prefix_len]
    ):
        prefix_len += 1

    suffix_len = 0
    while (
        suffix_len < len(surface) - prefix_len
        and suffix_len < len(reading) - prefix_len
        and not _is_kanji(surface[len(surface) - 1 - suffix_len])
        and surface[len(surface) - 1 - suffix_len] == reading[len(reading) - 1 - suffix_len]
    ):
        suffix_len += 1

    prefix = surface[:prefix_len]
    suffix = surface[len(surface) - suffix_len :] if suffix_len else ""
    core_base = surface[prefix_len : len(surface) - suffix_len]
    core_reading = reading[prefix_len : len(reading) - suffix_len]
    return prefix, core_base, core_reading, suffix


def annotate(text: str):
    """일본어 문장 -> [(base, ruby_or_None), ...]"""
    segments = []
    for token in _tagger(text):
        surface = token.surface
        if not _has_kanji(surface):
            segments.append((surface, None))
            continue

        kana = getattr(token.feature, "kana", None)
        if not kana:
            segments.append((surface, None))
            continue

        reading = _katakana_to_hiragana(kana)
        prefix, core_base, core_reading, suffix = _split_okurigana(surface, reading)

        if prefix:
            segments.append((prefix, None))
        if core_base:
            segments.append((core_base, core_reading or None))
        if suffix:
            segments.append((suffix, None))

    return segments


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")

    sample = "今日は学校に行く"
    for base, ruby in annotate(sample):
        print(f"{base!r:>8} -> {ruby!r}")
