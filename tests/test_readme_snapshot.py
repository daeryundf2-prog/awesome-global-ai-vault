"""generate_global_readme.py 스냅샷 — unavailable/archived/stale 렌더링 고정."""

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import generate_global_readme as gen  # noqa: E402


def _item(name, code="US", rank=1, **kw):
    base = {
        "name": name, "github": f"https://github.com/o/{name}",
        "country": "미국 (United States)", "country_code": code,
        "author": "o", "model_affinity": "M", "stars": 100, "forks": 10,
        "score": 10.0, "status": "⚡ Active", "summary": "s", "use_case": "u",
        "rank_global": rank, "rank_country": rank, "rank_delta": "−",
    }
    base.update(kw)
    return base


def _run_gen(tmp_path, monkeypatch, items):
    data = tmp_path / "global_creations.json"
    data.write_text(json.dumps({"items": items}, ensure_ascii=False), encoding="utf-8")
    readme = tmp_path / "README.md"
    monkeypatch.setattr(gen, "DATA_PATH", str(data))
    monkeypatch.setattr(gen, "CANDIDATES_PATH", str(tmp_path / "none.json"))
    monkeypatch.setattr(gen, "README_PATH", str(readme))
    gen.main()
    return readme.read_text(encoding="utf-8")


def test_unavailable_excluded_from_tables(tmp_path, monkeypatch):
    md = _run_gen(tmp_path, monkeypatch, [
        _item("alive"), _item("ghost", rank=None, status="unavailable"),
    ])
    assert "**alive**" in md and "**ghost**" not in md


def test_archived_shown_without_rank(tmp_path, monkeypatch):
    md = _run_gen(tmp_path, monkeypatch, [_item("frozen", rank=None, archived=True)])
    assert "**frozen**" in md and "📦 Archived" in md
    assert "**-**" in md  # 순위 칸은 대시


def test_stale_shows_refresh_failure(tmp_path, monkeypatch):
    md = _run_gen(tmp_path, monkeypatch, [_item("stale_repo", stale=True)])
    assert "⚠️ 갱신실패" in md


def test_no_realtime_claims_in_output(tmp_path, monkeypatch):
    md = _run_gen(tmp_path, monkeypatch, [_item("x")])
    assert "실시간" not in md and "Autonomous" not in md
    assert "큐레이션" in md
