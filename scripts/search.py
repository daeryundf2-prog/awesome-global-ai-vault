#!/usr/bin/env python3
"""
Awesome Global AI Vault - Terminal CLI Search & Leaderboard Explorer
Supports Country-by-Country Top 20 (US, CN, KR, EU, JP) & Global Top 100 Search
"""

import os
import sys
import json
import argparse

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "global_creations.json")

def load_data():
    if not os.path.exists(DATA_PATH):
        print(f"Error: Data file not found at {DATA_PATH}")
        sys.exit(1)
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
        return raw if isinstance(raw, list) else raw.get("items", [])

def format_number(val):
    if isinstance(val, (int, float)):
        return f"{int(val):,}"
    return str(val)

def main():
    parser = argparse.ArgumentParser(description="Awesome Global AI Vault & Leaderboard Search")
    parser.add_argument("--top", type=int, nargs="?", const=100, default=None, help="Display Top N global projects (default: 100)")
    parser.add_argument("--country", "-C", type=str, default=None, help="Filter by country (us, cn, kr, eu, jp, 미국, 중국, 한국, 유럽, 일본)")
    parser.add_argument("--region", "-r", type=str, default=None, help="Filter by region/country")
    parser.add_argument("--model", "-m", type=str, default=None, help="Filter by compatible model keyword")
    parser.add_argument("--category", "-c", type=str, default=None, help="Filter by category")
    parser.add_argument("--query", "-q", type=str, default=None, help="General keyword search (name, summary, use_case)")
    parser.add_argument("--list-countries", action="store_true", help="List all countries and counts")
    parser.add_argument("--list-categories", action="store_true", help="List all categories and counts")

    args = parser.parse_args()
    data = load_data()

    if args.list_countries:
        print("\n🌍 [등록된 5대 주요국 및 프로젝트 수]")
        counts = {}
        for it in data:
            c = it.get("country", it.get("region", "기타"))
            counts[c] = counts.get(c, 0) + 1
        for c, cnt in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {c}: {cnt}개 프로젝트")
        print()
        return

    if args.list_categories:
        print("\n📂 [등록된 카테고리 목록]")
        counts = {}
        for it in data:
            cat = it.get("category", "기타")
            counts[cat] = counts.get(cat, 0) + 1
        for cat, cnt in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {cat}: {cnt}개 프로젝트")
        print()
        return

    # Country filter aliases
    country_aliases = {
        "us": "미국",
        "usa": "미국",
        "america": "미국",
        "cn": "중국",
        "china": "중국",
        "kr": "대한민국",
        "korea": "대한민국",
        "한국": "대한민국",
        "대한민국": "대한민국",
        "eu": "유럽",
        "europe": "유럽",
        "jp": "일본",
        "japan": "일본"
    }

    target_country = None
    country_input = args.country or args.region
    if country_input:
        target_country = country_aliases.get(country_input.lower(), country_input.lower())

    # Country Top 20 mode
    if target_country and args.top is None:
        c_items = []
        for it in data:
            c_name = it.get("country", it.get("region", "")).lower()
            c_code = it.get("country_code", "").lower()
            if target_country in c_name or target_country == c_code:
                c_items.append(it)

        c_items.sort(key=lambda x: x.get("rank_country", x.get("rank_global", 999)))
        print(f"\n🗺️ [Top 20 Leaderboard: {target_country.upper()}] (총 {len(c_items)}개)")
        print("=" * 85)
        for it in c_items[:20]:
            c_rank = it.get("rank_country", "-")
            g_rank = it.get("rank_global", "-")
            status = it.get("status", "⚡ Active")
            name = it.get("name", "")
            stars = format_number(it.get("stars", 0))
            score = it.get("score", 0.0)
            summary = it.get("summary", "")
            gh = it.get("github", "")
            print(f"#{c_rank:02d} (전세계 #{g_rank:02d}) | {status} | {name:<22} | ⭐ {stars:<8} | 점수 {score:<5} | {gh}")
            print(f"     👉 {summary}")
            print("-" * 85)
        print()
        return

    # Top N mode
    if args.top is not None:
        data.sort(key=lambda x: x.get("rank_global", 999))
        results = data[:args.top]
        print(f"\n🏆 [Global AI Leaderboard Top {args.top}] (총 {len(data)}개 중)")
        print("=" * 85)
        for it in results:
            rank = it.get("rank_global", "-")
            status = it.get("status", "⚡ Active")
            name = it.get("name", "")
            cntry = it.get("country", it.get("region", "")).split("(")[0].strip()
            stars = format_number(it.get("stars", 0))
            score = it.get("score", 0.0)
            summary = it.get("summary", "")
            gh = it.get("github", "")
            print(f"#{rank:02d} | {status} | {name:<22} | {cntry:<8} | ⭐ {stars:<8} | 점수 {score:<5} | {gh}")
            print(f"     👉 {summary}")
            print("-" * 85)
        print()
        return

    # General query filtering
    results = []
    for item in data:
        if target_country:
            c_name = item.get("country", item.get("region", "")).lower()
            c_code = item.get("country_code", "").lower()
            if target_country not in c_name and target_country != c_code:
                continue

        if args.model:
            if args.model.lower() not in item.get("model_affinity", "").lower():
                continue

        if args.category:
            if args.category.lower() not in item.get("category", "").lower():
                continue

        if args.query:
            q = args.query.lower()
            text_corpus = f"{item.get('name', '')} {item.get('summary', '')} {item.get('use_case', '')} {item.get('author', '')}".lower()
            if q not in text_corpus:
                continue

        results.append(item)

    results.sort(key=lambda x: x.get("rank_global", 999))

    print(f"\n🔍 검색 결과: {len(results)}건 / 총 {len(data)}건")
    print("=" * 80)
    for it in results:
        g_rank = it.get("rank_global", "-")
        c_rank = it.get("rank_country", "-")
        status = it.get("status", "⚡ Active")
        stars = format_number(it.get("stars", 0))
        forks = format_number(it.get("forks", 0))
        score = it.get("score", 0.0)

        print(f"[전세계 #{g_rank:02d} | 국가 #{c_rank:02d}] {it.get('name')} ({it.get('execution_type')}) - {status}")
        print(f"  • 국가/권역 : {it.get('country', it.get('region'))}")
        print(f"  • 카테고리  : {it.get('category')}")
        print(f"  • 개발/조직 : {it.get('author')}")
        print(f"  • 메트릭    : ⭐ {stars} stars | 🍴 {forks} forks | 점수: {score}")
        print(f"  • 저장소    : {it.get('github')}")
        print(f"  • 핵심 설명 : {it.get('summary')}")
        print(f"  • 실무 활용 : {it.get('use_case')}")
        print("-" * 80)
    print()

if __name__ == "__main__":
    if sys.stdout:
        sys.stdout.reconfigure(encoding="utf-8")
    main()
