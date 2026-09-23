#!/usr/bin/env python3
"""
Awesome Global AI Vault - Terminal CLI Search & Leaderboard Explorer
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
    parser.add_argument("--top", type=int, default=None, help="Display Top N global projects by ranking (e.g. --top 10)")
    parser.add_argument("--region", "-r", type=str, default=None, help="Filter by region (us, cn, eu, jp, 북미, 중국, 유럽, 일본)")
    parser.add_argument("--model", "-m", type=str, default=None, help="Filter by compatible model keyword")
    parser.add_argument("--category", "-c", type=str, default=None, help="Filter by category")
    parser.add_argument("--query", "-q", type=str, default=None, help="General keyword search (name, summary, use_case)")
    parser.add_argument("--list-regions", action="store_true", help="List all regions and counts")
    parser.add_argument("--list-categories", action="store_true", help="List all categories and counts")

    args = parser.parse_args()
    data = load_data()

    if args.list_regions:
        print("\n🌍 [등록된 전세계 권역 목록]")
        counts = {}
        for it in data:
            reg = it.get("region", "기타")
            counts[reg] = counts.get(reg, 0) + 1
        for reg, cnt in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {reg}: {cnt}개 프로젝트")
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
            reg = it.get("region", "").split("(")[0].strip()
            stars = format_number(it.get("stars", 0))
            score = it.get("score", 0.0)
            summary = it.get("summary", "")
            gh = it.get("github", "")
            print(f"#{rank:02d} | {status} | {name:<20} | {reg:<6} | ⭐ {stars:<8} | 점수 {score:<5} | {gh}")
            print(f"     👉 {summary}")
            print("-" * 85)
        print()
        return

    # Filter logic
    results = []
    region_aliases = {
        "us": "북미",
        "usa": "북미",
        "america": "북미",
        "cn": "중국",
        "china": "중국",
        "eu": "유럽",
        "europe": "유럽",
        "jp": "일본",
        "japan": "일본"
    }

    target_region = None
    if args.region:
        target_region = region_aliases.get(args.region.lower(), args.region.lower())

    for item in data:
        if target_region:
            if target_region not in item.get("region", "").lower():
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

    # Sort results by global rank
    results.sort(key=lambda x: x.get("rank_global", 999))

    print(f"\n🔍 검색 결과: {len(results)}건 / 총 {len(data)}건")
    print("=" * 80)
    for it in results:
        rank = it.get("rank_global", "-")
        reg_rank = it.get("rank_regional", "-")
        status = it.get("status", "⚡ Active")
        stars = format_number(it.get("stars", 0))
        forks = format_number(it.get("forks", 0))
        score = it.get("score", 0.0)

        print(f"[#{rank:02d} | 권역 #{reg_rank}] {it.get('name')} ({it.get('execution_type')}) - {status}")
        print(f"  • 권역/국가 : {it.get('region')}")
        print(f"  • 카테고리  : {it.get('category')}")
        print(f"  • 개발/조직 : {it.get('author')}")
        print(f"  • 호환 모델 : {it.get('model_affinity')}")
        print(f"  • 메트릭    : ⭐ {stars} stars | 🍴 {forks} forks | 점수: {score}")
        print(f"  • 저장소    : {it.get('github')}")
        print(f"  • 핵심 설명 : {it.get('summary')}")
        print(f"  • 실무 활용 : {it.get('use_case')}")
        print("-" * 80)
    print()

if __name__ == "__main__":
    main()
