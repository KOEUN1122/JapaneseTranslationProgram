"""지정된 화면 영역을 캡처해 PIL Image로 반환한다."""

import mss
from PIL import Image


def grab_region(region: dict) -> Image.Image:
    """region: {"left": int, "top": int, "width": int, "height": int}"""
    monitor = {
        "left": region["left"],
        "top": region["top"],
        "width": region["width"],
        "height": region["height"],
    }
    with mss.mss() as sct:
        shot = sct.grab(monitor)
        return Image.frombytes("RGB", shot.size, shot.rgb)
