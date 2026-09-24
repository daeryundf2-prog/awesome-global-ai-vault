#!/usr/bin/env python3
"""
GitHub Metrics & Ranking Updater for Awesome Global AI Vault
Fetches live GitHub metrics (stars, forks, open issues, pushed_at) for all repos,
calculates composite activity scores and assigns global and regional rankings.
"""

import os
import sys
import json
import math
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "global_creations.json")
HISTORY_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "history")

def get_github_token():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    # Try local gh auth token if available
    try:
        import subprocess
        res = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return None

def fetch_repo_data(repo_full_name, token=None):
    url = f"https://api.github.com/repos/{repo_full_name}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "lazyradar-Agent/1.0 (daeryundf2-prog/lazyradar)"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                return {
                    "stars": data.get("stargazers_count", 0),
                    "forks": data.get("forks_count", 0),
                    "open_issues": data.get("open_issues_count", 0),
                    "pushed_at": data.get("pushed_at", ""),
                    "description": data.get("description", ""),
                    "archived": data.get("archived", False)
                }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"⚠️  Repo not found (404): {repo_full_name}")
            return "not_found"
        elif e.code == 403:
            print(f"⚠️  Rate limit reached (403) while fetching {repo_full_name}")
        else:
            print(f"⚠️  HTTP Error {e.code} for {repo_full_name}")
    except Exception as e:
        print(f"⚠️  Error fetching {repo_full_name}: {e}")
    return None

def calculate_activity_score(stars, forks, pushed_at_str, now_dt):
    # Recency bonus based on days since last commit
    recency_bonus = 0
    days_since_push = 999
    if pushed_at_str:
        try:
            # Handles ISO format like '2025-06-27T08:35:54Z'
            pushed_dt = datetime.fromisoformat(pushed_at_str.replace("Z", "+00:00"))
            delta = now_dt - pushed_dt
            days_since_push = max(0, delta.days)
            if days_since_push <= 7:
                recency_bonus = 15
            elif days_since_push <= 30:
                recency_bonus = 8
            elif days_since_push <= 90:
                recency_bonus = 3
        except Exception:
            pass

    # Log-scaled score: Stars (weight 10) + Forks (weight 2) + Recency Bonus (max 15)
    stars_val = max(1, stars)
    forks_val = max(1, forks)
    score = (math.log10(stars_val) * 10.0) + (math.log10(forks_val) * 2.0) + recency_bonus
    score = round(score, 2)

    # Status indicator
    if days_since_push <= 7:
        status = "🔥 Hot"
    elif days_since_push <= 30:
        status = "⚡ Active"
    elif days_since_push <= 90:
        status = "✨ Fresh"
    else:
        status = "💤 Stable"

    return score, days_since_push, status

def update_items(items, fetcher, now_dt):
    """각 항목의 지표를 fetcher로 갱신하고 점수·순위를 재산정한다.

    fetcher(full_name) -> dict | "not_found" | None
      - dict: 정상 갱신
      - "not_found": 404 — status를 "unavailable"로 표시하고 랭킹에서 제외
      - None: 일시 오류 — 직전 지표 유지 + stale=True 표시

    반환: (updated_count, removal_candidates)
    """
    today_str = now_dt.strftime("%Y-%m-%d")
    updated_count = 0
    removal_candidates = []

    for i, item in enumerate(items):
        repo_url = item.get("github", item.get("github_url", ""))
        # Extract owner/repo from https://github.com/owner/repo
        if "github.com/" in repo_url:
            parts = repo_url.rstrip("/").split("github.com/")[-1].split("/")
            if len(parts) >= 2:
                repo_full_name = f"{parts[0]}/{parts[1]}"
                print(f"[{i+1}/{len(items)}] Fetching {repo_full_name}...", end=" ", flush=True)
                info = fetcher(repo_full_name)
                if info == "not_found":
                    # 사라진 레포 — 랭킹에서 제외하고 연속 미응답 주수를 누적한다.
                    item["status"] = "unavailable"
                    item["unavailable_since"] = item.get("unavailable_since") or today_str
                    item["consecutive_unavailable"] = int(item.get("consecutive_unavailable", 0)) + 1
                    if item["consecutive_unavailable"] >= 3:
                        removal_candidates.append(item.get("name", repo_full_name))
                elif info is None:
                    # 일시 조회 실패 — 직전 지표를 유지하고 stale로 표시한다.
                    item["stale"] = True
                    print("Skipped (retaining metrics, marked stale)")
                else:
                    item.pop("stale", None)
                    item.pop("unavailable_since", None)
                    item["consecutive_unavailable"] = 0
                    if item.get("status") == "unavailable":
                        del item["status"]  # 복구 — 아래 점수 산정이 상태를 다시 쓴다
                    item["stars"] = info["stars"]
                    item["forks"] = info["forks"]
                    item["open_issues"] = info["open_issues"]
                    item["pushed_at"] = info["pushed_at"]
                    item["archived"] = info["archived"]
                    updated_count += 1
                    print(f"Done (⭐{info['stars']:,}, 🍴{info['forks']:,})")
                # Polite rate pacing
                time.sleep(0.05)

        if item.get("status") == "unavailable":
            continue  # 점수·순위 재산정 대상이 아니다

        # Compute or recalculate score. 조회 실패 시 임의 기본값을 넣지 않고
        # 직전 값을 그대로 쓴다(없으면 0).
        stars = item.get("stars", 0)
        forks = item.get("forks", 0)
        pushed_at = item.get("pushed_at", "")
        score, days, status = calculate_activity_score(stars, forks, pushed_at, now_dt)
        item["score"] = score
        item["days_since_push"] = days
        item["status"] = status
        item["last_synced_at"] = now_dt.strftime("%Y-%m-%d %H:%M:%S UTC")

    # Compute Global Rankings — unavailable/archived는 순위에서 제외한다.
    rankable = []
    for item in items:
        if item.get("status") == "unavailable" or item.get("archived"):
            item["rank_global"] = None
            item["rank_country"] = None
            item["rank_regional"] = None
            item["rank_delta"] = "−"
            continue
        rankable.append(item)

    rankable.sort(key=lambda x: x.get("score", 0), reverse=True)
    for rank, item in enumerate(rankable, start=1):
        prev_rank = item.get("rank_global", rank)
        item["rank_global"] = rank
        if isinstance(prev_rank, int):
            if prev_rank < rank:
                item["rank_delta"] = f"▼{rank - prev_rank}"
            elif prev_rank > rank:
                item["rank_delta"] = f"▲{prev_rank - rank}"
            else:
                item["rank_delta"] = "−"
        else:
            item["rank_delta"] = "−"

    # Compute Country & Regional Rankings (rankable만 대상)
    country_groups = {}
    for item in rankable:
        cntry = item.get("country", item.get("region", "Global"))
        country_groups.setdefault(cntry, []).append(item)

    for cntry, c_items in country_groups.items():
        c_items.sort(key=lambda x: x.get("score", 0), reverse=True)
        for c_rank, item in enumerate(c_items, start=1):
            item["rank_country"] = c_rank
            item["rank_regional"] = c_rank

    return updated_count, removal_candidates


def write_history_snapshot(items, now_dt):
    """주간 스냅샷을 data/history/YYYY-WW.json에 누적한다(변동·Emerging 근거)."""
    iso = now_dt.isocalendar()
    week_id = f"{iso.year}-W{iso.week:02d}"
    snapshot = {
        "week": week_id,
        "generated_at": now_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "items": [
            {
                "name": it.get("name", ""),
                "github": it.get("github", ""),
                "stars": it.get("stars", 0),
                "forks": it.get("forks", 0),
                "score": it.get("score", 0.0),
                "rank_global": it.get("rank_global"),
                "status": it.get("status", ""),
            }
            for it in items
        ],
    }
    os.makedirs(HISTORY_DIR, exist_ok=True)
    path = os.path.join(HISTORY_DIR, f"{week_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    return path


def main():
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} not found.")
        sys.exit(1)

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    if isinstance(raw_data, list):
        items = raw_data
        is_list = True
    else:
        items = raw_data.get("items", [])
        is_list = False

    print(f"🚀 Loaded {len(items)} items from {DATA_PATH}")

    token = get_github_token()
    if token:
        print("🔑 GitHub Token detected. Rate limit: 5,000 req/hr.")
    else:
        print("⚠️ No GitHub Token found. Running unauthenticated (Rate limit: 60 req/hr).")

    now_dt = datetime.now(timezone.utc)
    fetcher = lambda name: fetch_repo_data(name, token=token)
    updated_count, removal_candidates = update_items(items, fetcher, now_dt)

    snap_path = write_history_snapshot(items, now_dt)

    # Keep original list format or wrap
    output_data = items if is_list else {"items": items, "last_updated_at": now_dt.strftime("%Y-%m-%d %H:%M:%S UTC")}

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Successfully updated {updated_count}/{len(items)} repositories.")
    print(f"📊 Global Rankings and Scores assigned at {now_dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"🗂  Weekly snapshot saved: {snap_path}")
    if removal_candidates:
        print(f"🗑️  3주 연속 미응답 — 목록 삭제 제안: {', '.join(removal_candidates)}")

if __name__ == "__main__":
    if sys.stdout:
        sys.stdout.reconfigure(encoding="utf-8")
    main()
