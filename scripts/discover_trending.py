#!/usr/bin/env python3
"""
Emerging Trending AI Repository Discoverer for Awesome Global AI Vault
Searches GitHub Search API for newly surging AI repos (agents, reasoning models, MCP, voice)
that are not yet tracked in the main dataset, creating an emerging candidates watchlist.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone, timedelta

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "global_creations.json")
CANDIDATES_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "emerging_candidates.json")

def get_github_token():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    try:
        import subprocess
        res = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return None

def search_github(query, token=None, per_page=10):
    url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=stars&order=desc&per_page={per_page}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "lazyradar-Agent/1.0 (daeryundf2-prog/lazyradar)"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("items", [])
    except Exception as e:
        print(f"⚠️ Search error for query '{query}': {e}")
    return []

def main():
    existing_repos = set()
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
            items = raw if isinstance(raw, list) else raw.get("items", [])
            for it in items:
                url = it.get("github", "")
                if "github.com/" in url:
                    parts = url.rstrip("/").split("github.com/")[-1].lower()
                    existing_repos.add(parts)

    token = get_github_token()
    # "급부상" 근거: 최근 생성(14일) 또는 최근 푸시(7일) 필터를 쿼리에 포함한다.
    today = datetime.now(timezone.utc).date()
    created_after = (today - timedelta(days=14)).isoformat()
    pushed_after = (today - timedelta(days=7)).isoformat()
    queries = [
        f"(topic:llm OR topic:ai-agent) created:>{created_after} stars:>50",
        f"topic:mcp pushed:>{pushed_after} stars:>500",
        f"topic:llm pushed:>{pushed_after} stars:>200",
        f"deepseek pushed:>{pushed_after} stars:>1000",
        f"speech-to-speech created:>{created_after} stars:>50",
    ]

    discovered = {}
    print("🔍 Discovering emerging trending AI projects...")

    for q in queries:
        print(f"  • Searching: {q}...", end=" ", flush=True)
        results = search_github(q, token=token, per_page=5)
        print(f"found {len(results)} items")
        for item in results:
            full_name = item.get("full_name", "").lower()
            if full_name and full_name not in existing_repos:
                discovered[full_name] = {
                    "name": item.get("name", ""),
                    "full_name": item.get("full_name", ""),
                    "github": item.get("html_url", ""),
                    "stars": item.get("stargazers_count", 0),
                    "forks": item.get("forks_count", 0),
                    "description": item.get("description", "") or "No description provided.",
                    "language": item.get("language", "Unknown"),
                    "pushed_at": item.get("pushed_at", ""),
                    "discovered_at": datetime.now(timezone.utc).strftime("%Y-%m-%d")
                }

    # Sort candidates by stars
    candidates_list = sorted(discovered.values(), key=lambda x: x["stars"], reverse=True)[:15]

    output_payload = {
        "last_searched_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total_emerging": len(candidates_list),
        "candidates": candidates_list
    }

    with open(CANDIDATES_PATH, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, ensure_ascii=False, indent=2)

    print(f"✅ Discovered {len(candidates_list)} emerging AI projects. Saved to {CANDIDATES_PATH}")

if __name__ == "__main__":
    if sys.stdout:
        sys.stdout.reconfigure(encoding="utf-8")
    main()
