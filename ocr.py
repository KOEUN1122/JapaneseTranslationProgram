"""manga-ocr 래퍼. 모델 로딩이 느리므로 최초 호출 시에만 로드한다."""

from PIL import Image

_mocr = None


def _get_model():
    global _mocr
    if _mocr is None:
        from manga_ocr import MangaOcr

        _mocr = MangaOcr()
    return _mocr


def recognize(image: Image.Image) -> str:
    model = _get_model()
    return model(image)


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")

    if len(sys.argv) != 2:
        print("usage: python ocr.py <image_path>")
        raise SystemExit(1)

    img = Image.open(sys.argv[1]).convert("RGB")
    print(recognize(img))
