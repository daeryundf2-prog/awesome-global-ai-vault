#!/usr/bin/env python3
"""report_unavailable.py — 404(unavailable) 레포 정비 리포트 생성기.

주간 sync(update_metrics.py)가 3주 연속 미응답으로 표시한 레포를 수집해
워크플로가 GitHub 이슈로 올릴 본문(--md-out)과 후보 목록(--json-out)을 만든다.
제거 판단 자체는 update_metrics.py의 책임 — 이 스크립트는 리포트만 만든다.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "global_creations.json")
REMOVAL_STREAK = 3  # update_metrics.py의 removal_candidates 기준과 동일


def load_items(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return raw if isinstance(raw, list) else raw.get("items", [])


def collect_unavailable(items: list[dict]) -> tuple[list[dict], list[dict]]:
    """(제거 후보, 관찰 대상)으로 나눈다."""
    removal, watching = [], []
    for it in items:
        if it.get("status") != "unavailable":
            continue
        entry = {
            "name": it.get("name", ""),
            "github": it.get("github", it.get("github_url", "")),
            "country": it.get("country", it.get("region", "")),
            "unavailable_since": it.get("unavailable_since", ""),
            "consecutive_unavailable": int(it.get("consecutive_unavailable", 0)),
        }
        if entry["consecutive_unavailable"] >= REMOVAL_STREAK:
            removal.append(entry)
        else:
            watching.append(entry)
    removal.sort(key=lambda e: (-e["consecutive_unavailable"], e["name"]))
    watching.sort(key=lambda e: e["name"])
    return removal, watching


def render_issue_md(removal: list[dict], watching: list[dict], now_dt: datetime) -> str:
    lines = [
        "## lazyradar unavailable repositories",
        "",
        f"_Generated {now_dt.strftime('%Y-%m-%d %H:%M:%S UTC')} by weekly-sync + report_unavailable.py_",
        "",
    ]
    if removal:
        lines += [
            f"### 제거 후보 — {REMOVAL_STREAK}주 연속 GitHub 404 ({len(removal)}개)",
            "",
            "| Repo | GitHub | Country | Since | Streak |",
            "|---|---|---|---|---|",
        ]
        for e in removal:
            lines.append(
                f"| {e['name']} | {e['github']} | {e['country']} | {e['unavailable_since']} | {e['consecutive_unavailable']}주 |"
            )
        lines += [
            "",
            "삭제가 확정되면 `data/global_creations.json`에서 항목을 지우고 README를 재생성하면 된다.",
            "",
        ]
    if watching:
        lines += [
            f"### 관찰 대상 — unavailable, 미삭제 ({len(watching)}개)",
            "",
            "| Repo | GitHub | Since | Streak |",
            "|---|---|---|---|",
        ]
        for e in watching:
            lines.append(
                f"| {e['name']} | {e['github']} | {e['unavailable_since']} | {e['consecutive_unavailable']}주 |"
            )
        lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build unavailable-repo cleanup report for the weekly issue bot")
    parser.add_argument("--data", default=DATA_PATH, help="global_creations.json path")
    parser.add_argument("--json-out", default=None, help="Write removal candidates JSON here (skipped when empty)")
    parser.add_argument("--md-out", default=None, help="Write issue body markdown here")
    args = parser.parse_args(argv)

    items = load_items(args.data)
    removal, watching = collect_unavailable(items)

    print(f"🔎 unavailable repos: {len(removal) + len(watching)} total "
          f"({len(removal)} removal candidates, {len(watching)} watching)")

    if args.md_out:
        md = render_issue_md(removal, watching, datetime.now(timezone.utc))
        with open(args.md_out, "w", encoding="utf-8", newline="\n") as f:
            f.write(md)
        print(f"📝 issue body -> {args.md_out}")

    if not removal:
        print("✅ no removal candidates — no issue needed")
        return 0

    if args.json_out:
        payload = {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            "removal_candidates": removal,
            "watching": watching,
        }
        with open(args.json_out, "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"🗂 candidates -> {args.json_out}")
    return 0


if __name__ == "__main__":
    if sys.stdout:
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
