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
    updated_count = 0

    for i, item in enumerate(items):
        repo_url = item.get("github", item.get("github_url", ""))
        # Extract owner/repo from https://github.com/owner/repo
        if "github.com/" in repo_url:
            parts = repo_url.rstrip("/").split("github.com/")[-1].split("/")
            if len(parts) >= 2:
                repo_full_name = f"{parts[0]}/{parts[1]}"
                print(f"[{i+1}/{len(items)}] Fetching {repo_full_name}...", end=" ", flush=True)
                info = fetch_repo_data(repo_full_name, token=token)
                if info:
                    item["stars"] = info["stars"]
                    item["forks"] = info["forks"]
                    item["open_issues"] = info["open_issues"]
                    item["pushed_at"] = info["pushed_at"]
                    item["archived"] = info["archived"]
                    updated_count += 1
                    print(f"Done (⭐{info['stars']:,}, 🍴{info['forks']:,})")
                else:
                    print("Skipped (retaining metrics)")
                # Polite rate pacing
                time.sleep(0.05)

        # Compute or recalculate score
        stars = item.get("stars", 1000)
        forks = item.get("forks", 100)
        pushed_at = item.get("pushed_at", "")
        score, days, status = calculate_activity_score(stars, forks, pushed_at, now_dt)
        item["score"] = score
        item["days_since_push"] = days
        item["status"] = status
        item["last_synced_at"] = now_dt.strftime("%Y-%m-%d %H:%M:%S UTC")

    # Compute Global Rankings
    items.sort(key=lambda x: x.get("score", 0), reverse=True)
    for rank, item in enumerate(items, start=1):
        prev_rank = item.get("rank_global", rank)
        item["rank_global"] = rank
        if prev_rank < rank:
            item["rank_delta"] = f"▼{rank - prev_rank}"
        elif prev_rank > rank:
            item["rank_delta"] = f"▲{prev_rank - rank}"
        else:
            item["rank_delta"] = "−"

    # Compute Country & Regional Rankings
    country_groups = {}
    for item in items:
        cntry = item.get("country", item.get("region", "Global"))
        country_groups.setdefault(cntry, []).append(item)

    for cntry, c_items in country_groups.items():
        c_items.sort(key=lambda x: x.get("score", 0), reverse=True)
        for c_rank, item in enumerate(c_items, start=1):
            item["rank_country"] = c_rank
            item["rank_regional"] = c_rank

    # Keep original list format or wrap
    output_data = items if is_list else {"items": items, "last_updated_at": now_dt.strftime("%Y-%m-%d %H:%M:%S UTC")}

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Successfully updated {updated_count}/{len(items)} repositories.")
    print(f"📊 Global Rankings and Scores assigned at {now_dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")

if __name__ == "__main__":
    main()
