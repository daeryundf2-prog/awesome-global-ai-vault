#!/usr/bin/env python3
"""validate_data.py — global_creations.json 스키마 검증.

주간 갱신 워크플로가 커밋하기 전에 데이터 무결성을 확인한다.
[skip ci]만으로는 잘못된 데이터가 main에 들어가는 것을 막지 못한다.

Exit code: 0 유효 / 1 위반 / 2 실행 오류
"""

import json
import os
import sys

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "global_creations.json")

REQUIRED_FIELDS = {
    "name": str,
    "github": str,
    "country_code": str,
    "stars": (int, float),
    "forks": (int, float),
    "score": (int, float),
}
VALID_COUNTRY_CODES = {"US", "CN", "KR", "EU", "JP"}


def validate(items) -> list[str]:
    errors = []
    seen = set()
    for i, it in enumerate(items):
        name = it.get("name", f"<#{i}>")
        for field, types in REQUIRED_FIELDS.items():
            if field not in it:
                errors.append(f"{name}: 필수 필드 누락 '{field}'")
            elif not isinstance(it[field], types):
                errors.append(f"{name}: '{field}' 타입 오류 ({type(it[field]).__name__})")
        code = it.get("country_code", "")
        if code and code not in VALID_COUNTRY_CODES:
            errors.append(f"{name}: country_code '{code}' — {sorted(VALID_COUNTRY_CODES)} 중 하나여야 함")
        gh = it.get("github", "")
        if gh and "github.com/" in gh:
            key = gh.rstrip("/").split("github.com/")[-1].lower()
            if key in seen:
                errors.append(f"{name}: 중복 레포 '{key}'")
            seen.add(key)
        if it.get("status") == "unavailable" and it.get("rank_global") is not None:
            errors.append(f"{name}: unavailable인데 rank_global={it['rank_global']} — 랭킹 제외 원칙 위반")
    return errors


def main() -> int:
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} not found.", file=sys.stderr)
        return 2
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
    items = raw if isinstance(raw, list) else raw.get("items", [])

    errors = validate(items)
    if errors:
        print(f"❌ 데이터 검증 실패 ({len(errors)}건):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"✅ 데이터 검증 통과: {len(items)}개 항목")
    return 0


if __name__ == "__main__":
    if sys.stdout:
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
