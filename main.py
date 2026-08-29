"""단축키를 누르면 지정된 화면 영역을 캡처 -> OCR -> 후리가나 분석 -> 번역 -> 오버레이 표시."""

import json
import os
import queue
import sys
import tkinter as tk

sys.stdout.reconfigure(encoding="utf-8")

import keyboard

import capture
import furigana
import ocr
import overlay
import translate

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
DEFAULT_HOTKEY = "ctrl+shift+o"
DEFAULT_DURATION_MS = 6000


def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def do_capture(region, root, duration_ms):
    try:
        image = capture.grab_region(region)
        text = ocr.recognize(image)
        if not text.strip():
            print("텍스트를 인식하지 못했습니다.")
            return

        segments = furigana.annotate(text)
        translated = translate.translate_ja_to_ko(text)

        overlay.show_overlay(
            root, segments, translated,
            x=region["left"], y=region["top"],
            duration_ms=duration_ms,
        )
        print(f"[JP] {text}\n[KO] {translated}")
    except Exception as e:
        print(f"오류: {e}")


def main():
    config = load_config()
    region = config.get("region")
    if not region:
        print("먼저 region_selector.py를 실행해서 캡처 영역을 지정해주세요.")
        return

    hotkey = config.get("hotkey", DEFAULT_HOTKEY)
    duration_ms = config.get("overlay_duration_ms", DEFAULT_DURATION_MS)

    event_queue: queue.Queue = queue.Queue()
    keyboard.add_hotkey(hotkey, lambda: event_queue.put(True))
    print(f"준비 완료. [{hotkey}] 를 누르면 캡처합니다. (프로그램 종료: Ctrl+C)")

    root = tk.Tk()
    root.withdraw()

    def process_queue():
        try:
            while True:
                event_queue.get_nowait()
                do_capture(region, root, duration_ms)
        except queue.Empty:
            pass
        root.after(50, process_queue)

    root.after(50, process_queue)
    root.mainloop()


if __name__ == "__main__":
    main()
