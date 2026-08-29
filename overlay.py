"""후리가나 세그먼트 + 한국어 번역을 투명 오버레이 창에 그린다.

Windows 전용: -transparentcolor 로 특정 색상을 완전 투명하게 처리하는 트릭을 사용한다.
"""

import tkinter as tk
import tkinter.font as tkfont

_TRANSPARENT_KEY = "#010101"
_PAD = 16
_RUBY_GAP = 2
_LINE_GAP = 10


def _build_fonts():
    base_font = tkfont.Font(family="Yu Gothic UI", size=22, weight="bold")
    ruby_font = tkfont.Font(family="Yu Gothic UI", size=12)
    trans_font = tkfont.Font(family="Malgun Gothic", size=16)
    return base_font, ruby_font, trans_font


def show_overlay(root, segments, translation, x, y, duration_ms=6000):
    """root: 기존 tkinter Tk 인스턴스. 새 Toplevel을 만들어 duration_ms 후 자동으로 닫는다."""
    base_font, ruby_font, trans_font = _build_fonts()

    base_h = base_font.metrics("linespace")
    ruby_h = ruby_font.metrics("linespace")
    trans_h = trans_font.metrics("linespace")

    seg_widths = [base_font.measure(base) for base, _ in segments]
    jp_width = sum(seg_widths)
    trans_width = trans_font.measure(translation)
    content_width = max(jp_width, trans_width)

    ruby_y = _PAD
    base_y = ruby_y + ruby_h + _RUBY_GAP
    trans_y = base_y + base_h + _LINE_GAP

    win_w = content_width + _PAD * 2
    win_h = trans_y + trans_h + _PAD

    top = tk.Toplevel(root)
    top.overrideredirect(True)
    top.attributes("-topmost", True)
    top.attributes("-transparentcolor", _TRANSPARENT_KEY)
    top.geometry(f"{win_w}x{win_h}+{x}+{y}")

    canvas = tk.Canvas(top, width=win_w, height=win_h, bg=_TRANSPARENT_KEY, highlightthickness=0)
    canvas.pack()

    # 반투명 느낌을 주는 배경 박스 (완전 투명 배경 위에 짙은 사각형)
    canvas.create_rectangle(0, 0, win_w, win_h, fill="#1a1a1a", outline="")

    cx = _PAD + jp_width / 2 - content_width / 2 if content_width > jp_width else _PAD
    x_cursor = cx
    for (base, ruby), w in zip(segments, seg_widths):
        center = x_cursor + w / 2
        canvas.create_text(center, base_y, anchor="n", text=base, font=base_font, fill="white")
        if ruby:
            canvas.create_text(center, ruby_y, anchor="n", text=ruby, font=ruby_font, fill="#ffd866")
        x_cursor += w

    canvas.create_text(
        _PAD + content_width / 2, trans_y, anchor="n", text=translation, font=trans_font, fill="#8fd3ff"
    )

    top.after(duration_ms, top.destroy)
    top.bind("<Escape>", lambda e: top.destroy())
    top.bind("<Button-1>", lambda e: top.destroy())
    return top


if __name__ == "__main__":
    import furigana

    root = tk.Tk()
    root.withdraw()

    segs = furigana.annotate("今日は学校に行く")
    show_overlay(root, segs, "오늘은 학교에 간다", x=200, y=200, duration_ms=8000)
    root.after(8500, root.destroy)

    root.mainloop()
