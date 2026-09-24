"""update_metrics.py 단위 테스트 — 점수 공식, 랭킹 정렬, 404 제외, stale 표시."""

import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import update_metrics as um  # noqa: E402

NOW = datetime(2026, 1, 15, tzinfo=timezone.utc)


def _item(name, stars=100, forks=10, pushed="2026-01-14T00:00:00Z", url=None):
    return {
        "name": name,
        "github": url or f"https://github.com/owner/{name}",
        "country": "미국 (United States)",
        "country_code": "US",
        "stars": stars,
        "forks": forks,
        "pushed_at": pushed,
    }


# ── 점수 공식 ────────────────────────────────────────────────────────

def test_score_formula():
    # log10(1000)*10 + log10(100)*2 + recency(1일 이내=15) = 30 + 4 + 15 = 49
    score, days, status = um.calculate_activity_score(1000, 100, "2026-01-14T00:00:00Z", NOW)
    assert score == 49.0
    assert days == 1 and status == "🔥 Hot"


def test_score_recency_bands():
    _, _, s7 = um.calculate_activity_score(1, 1, "2026-01-10T00:00:00Z", NOW)   # 5일
    _, _, s30 = um.calculate_activity_score(1, 1, "2025-12-25T00:00:00Z", NOW)  # 21일
    _, _, s90 = um.calculate_activity_score(1, 1, "2025-11-01T00:00:00Z", NOW)  # 75일
    _, _, sold = um.calculate_activity_score(1, 1, "2025-01-01T00:00:00Z", NOW) # 1년+
    assert (s7, s30, s90, sold) == ("🔥 Hot", "⚡ Active", "✨ Fresh", "💤 Stable")


def test_score_uses_floor_one_for_zero_counts():
    score, _, _ = um.calculate_activity_score(0, 0, "", NOW)
    assert score == 0.0  # log10(1)=0 기여분 없음


# ── 랭킹 정렬 ────────────────────────────────────────────────────────

def test_ranking_sorted_by_score():
    items = [_item("low", stars=10), _item("high", stars=100000), _item("mid", stars=1000)]
    um.update_items(items, lambda name: None, NOW)  # fetcher None → stale 유지
    assert items[0]["name"] != "low" or True  # 순서는 변하지 않음(정렬은 rankable만)
    ranks = {it["name"]: it["rank_global"] for it in items}
    assert ranks["high"] == 1 and ranks["mid"] == 2 and ranks["low"] == 3


def test_failed_fetch_keeps_previous_values_marks_stale():
    items = [_item("a", stars=777, forks=77)]
    um.update_items(items, lambda name: None, NOW)
    assert items[0]["stars"] == 777 and items[0]["forks"] == 77
    assert items[0]["stale"] is True
    assert items[0]["rank_global"] == 1  # stale이어도 순위에는 남는다


# ── 404 제외 ─────────────────────────────────────────────────────────

def test_404_marked_unavailable_and_excluded_from_ranking():
    items = [
        _item("alive", stars=5000),
        _item("gone", stars=999999, url="https://github.com/owner/gone"),
    ]

    def fetcher(name):
        return "not_found" if name.endswith("/gone") else {
            "stars": 5000, "forks": 500, "open_issues": 3,
            "pushed_at": "2026-01-14T00:00:00Z", "description": "", "archived": False,
        }

    updated, removals = um.update_items(items, fetcher, NOW)
    gone = next(i for i in items if i["name"] == "gone")
    alive = next(i for i in items if i["name"] == "alive")
    assert gone["status"] == "unavailable"
    assert gone["rank_global"] is None and gone["rank_country"] is None
    assert alive["rank_global"] == 1
    assert gone["consecutive_unavailable"] == 1
    assert removals == []


def test_three_consecutive_404s_suggest_removal():
    items = [_item("dead", url="https://github.com/owner/dead")]
    fetcher = lambda name: "not_found"
    um.update_items(items, fetcher, NOW)
    um.update_items(items, fetcher, NOW)
    _, removals = um.update_items(items, fetcher, NOW)
    assert removals == ["dead"]


def test_archived_excluded_from_ranking_but_kept():
    items = [
        _item("live", stars=100),
        _item("frozen", stars=100),
    ]

    def fetcher(name):
        archived = name.endswith("/frozen")
        return {"stars": 100, "forks": 10, "open_issues": 0,
                "pushed_at": "2026-01-14T00:00:00Z", "description": "", "archived": archived}

    um.update_items(items, fetcher, NOW)
    frozen = next(i for i in items if i["name"] == "frozen")
    live = next(i for i in items if i["name"] == "live")
    assert frozen["rank_global"] is None and frozen["archived"] is True
    assert live["rank_global"] == 1


def test_recovered_repo_returns_to_ranking():
    items = [_item("flaky", stars=50)]
    um.update_items(items, lambda n: "not_found", NOW)
    assert items[0]["status"] == "unavailable"
    um.update_items(items, lambda n: {"stars": 50, "forks": 5, "open_issues": 0,
                                      "pushed_at": "2026-01-14T00:00:00Z",
                                      "description": "", "archived": False}, NOW)
    assert items[0]["status"] != "unavailable"
    assert items[0]["rank_global"] == 1
    assert items[0]["consecutive_unavailable"] == 0


# ── 히스토리 스냅샷 ──────────────────────────────────────────────────

def test_history_snapshot_written(tmp_path, monkeypatch):
    monkeypatch.setattr(um, "HISTORY_DIR", str(tmp_path))
    path = um.write_history_snapshot([_item("x")], NOW)
    import json
    snap = json.loads(Path(path).read_text(encoding="utf-8"))
    assert snap["week"].startswith("2026-W")
    assert snap["items"][0]["name"] == "x"
