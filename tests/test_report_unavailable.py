"""report_unavailable.py 단위 테스트 — 404 레포 수집·분류·이슈 본문."""

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import report_unavailable as ru  # noqa: E402


def _item(name, status=None, streak=0, since=""):
    it = {"name": name, "github": f"https://github.com/owner/{name}", "country": "미국"}
    if status:
        it["status"] = status
        it["unavailable_since"] = since
        it["consecutive_unavailable"] = streak
    return it


def test_collect_splits_removal_and_watching():
    items = [
        _item("alive"),
        _item("gone3", "unavailable", 3, "2026-01-01"),
        _item("gone5", "unavailable", 5, "2025-12-01"),
        _item("watch1", "unavailable", 1, "2026-01-10"),
        _item("archived_ok", "unavailable", 0, ""),  # streak 0 → watching
    ]
    removal, watching = ru.collect_unavailable(items)
    assert [e["name"] for e in removal] == ["gone5", "gone3"]  # streak desc
    assert [e["name"] for e in watching] == ["archived_ok", "watch1"]


def test_render_issue_md_sections():
    removal = [{"name": "r1", "github": "g1", "country": "KR", "unavailable_since": "2026-01-01", "consecutive_unavailable": 4}]
    watching = [{"name": "w1", "github": "g2", "country": "US", "unavailable_since": "2026-01-05", "consecutive_unavailable": 1}]
    from datetime import datetime, timezone
    md = ru.render_issue_md(removal, watching, datetime(2026, 1, 15, tzinfo=timezone.utc))
    assert "제거 후보" in md and "r1" in md
    assert "관찰 대상" in md and "w1" in md
    assert "2026-01-15" in md


def test_main_writes_outputs_only_when_candidates(tmp_path):
    data = tmp_path / "data.json"
    data.write_text(json.dumps({"items": [_item("a")]}), encoding="utf-8")
    json_out = tmp_path / "candidates.json"
    md_out = tmp_path / "issue.md"
    assert ru.main(["--data", str(data), "--json-out", str(json_out), "--md-out", str(md_out)]) == 0
    assert not json_out.exists()  # 후보 없으면 JSON 미생성
    assert md_out.exists()        # 본문은 항상 생성 가능

    data.write_text(json.dumps({"items": [_item("dead", "unavailable", 3, "2026-01-01")]}), encoding="utf-8")
    assert ru.main(["--data", str(data), "--json-out", str(json_out), "--md-out", str(md_out)]) == 0
    payload = json.loads(json_out.read_text(encoding="utf-8"))
    assert payload["removal_candidates"][0]["name"] == "dead"
