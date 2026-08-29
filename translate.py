"""Papago(네이버클라우드플랫폼) 번역 API 클라이언트.

.env 파일에 아래 두 값이 필요하다:
  PAPAGO_CLIENT_ID=...
  PAPAGO_CLIENT_SECRET=...

다른 번역 API로 바꾸고 싶다면 translate_ja_to_ko 함수 내부만 교체하면 된다.
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

_ENDPOINT = "https://papago.apigw.ntruss.com/nmt/v1/translation"


class TranslationError(RuntimeError):
    pass


def translate_ja_to_ko(text: str) -> str:
    client_id = os.environ.get("PAPAGO_CLIENT_ID")
    client_secret = os.environ.get("PAPAGO_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise TranslationError(
            ".env에 PAPAGO_CLIENT_ID / PAPAGO_CLIENT_SECRET을 설정해주세요."
        )

    headers = {
        "x-ncp-apigw-api-key-id": client_id,
        "x-ncp-apigw-api-key": client_secret,
        "Content-Type": "application/json",
    }
    data = {"source": "ja", "target": "ko", "text": text}

    resp = requests.post(_ENDPOINT, headers=headers, json=data, timeout=10)
    if resp.status_code != 200:
        raise TranslationError(f"Papago API 오류 ({resp.status_code}): {resp.text}")

    return resp.json()["message"]["result"]["translatedText"]


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")

    text = sys.argv[1] if len(sys.argv) > 1 else "今日は学校に行く"
    print(translate_ja_to_ko(text))
