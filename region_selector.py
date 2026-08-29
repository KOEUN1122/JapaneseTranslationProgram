"""캡처할 영역(게임 대사창)을 드래그로 선택해 config.json에 저장한다."""

import json
import os
import tkinter as tk

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")


def select_region():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)
    root.attributes("-topmost", True)
    root.configure(bg="gray")

    canvas = tk.Canvas(root, cursor="cross", bg="gray", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_text(
        20, 20, anchor="nw",
        text="드래그해서 게임 대사창 영역을 선택하세요  (Esc: 취소)",
        fill="white", font=("Malgun Gothic", 16),
    )

    state = {"cancelled": False}
    rect_id = None

    def on_press(event):
        nonlocal rect_id
        state["x0"], state["y0"] = event.x, event.y
        rect_id = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="red", width=2)

    def on_drag(event):
        canvas.coords(rect_id, state["x0"], state["y0"], event.x, event.y)

    def on_release(event):
        state["x1"], state["y1"] = event.x, event.y
        root.quit()

    def on_cancel(event):
        state["cancelled"] = True
        root.quit()

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)
    root.bind("<Escape>", on_cancel)

    root.mainloop()
    root.destroy()

    if state["cancelled"] or "x1" not in state:
        return None

    left = min(state["x0"], state["x1"])
    top = min(state["y0"], state["y1"])
    width = abs(state["x1"] - state["x0"])
    height = abs(state["y1"] - state["y0"])
    if width < 5 or height < 5:
        return None
    return {"left": left, "top": top, "width": width, "height": height}


def save_region(region):
    config = {}
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    config["region"] = region
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    region = select_region()
    if region:
        save_region(region)
        print(f"저장됨: {region}")
    else:
        print("취소됨")
