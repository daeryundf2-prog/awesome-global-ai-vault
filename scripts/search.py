#!/usr/bin/env python3
"""
CLI search helper for Awesome Global AI Creations Vault (100 Curated World Tools)
Usage:
    python search.py --region "cn"
    python search.py --region "eu"
    python search.py --query "agent"
    python search.py --model "deepseek"
    python search.py --list-regions
    python search.py --list-categories
"""

import json
import argparse
import os
import sys

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "global_creations.json")

def load_data():
    if not os.path.exists(DATA_PATH):
        print(f"Error: Data file not found at {DATA_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def format_item(item):
    return f"""[{item['id']:03d}] {item['name']} ({item['execution_type']})
  • 권역/국가 : {item['region']}
  • 카테고리  : {item['category']}
  • 개발/조직 : {item['author']}
  • 호환 모델 : {item['model_affinity']}
  • 저장소    : {item['github']}
  • 핵심 설명 : {item['summary']}
  • 실무 활용 : {item['use_case']}
--------------------------------------------------------------------------------"""

def match_region(filter_val, region_str):
    fv = filter_val.lower().strip()
    rs = region_str.lower()
    if fv in ["us", "usa", "america", "global", "영어", "북미"]:
        return "north america" in rs or "북미" in rs
    if fv in ["cn", "china", "chinese", "중국"]:
        return "china" in rs or "중국" in rs
    if fv in ["eu", "europe", "european", "유럽", "france", "germany", "uk"]:
        return "europe" in rs or "유럽" in rs
    if fv in ["jp", "japan", "japanese", "apac", "일본", "아태"]:
        return "japan" in rs or "일본" in rs or "apac" in rs
    return fv in rs

def main():
    parser = argparse.ArgumentParser(description="전세계 글로벌 AI 생성물 & 도구 100선 검색기")
    parser.add_argument("-r", "--region", help="권역 검색 (예: us, cn, eu, jp, 북미, 중국, 유럽, 일본)")
    parser.add_argument("-q", "--query", help="이름, 설명, 실무활용 내 키워드 검색")
    parser.add_argument("-c", "--category", help="기능 카테고리 필터링")
    parser.add_argument("-m", "--model", help="호환 모델 검색 (예: deepseek, qwen, mistral, opus, astra)")
    parser.add_argument("--list-regions", action="store_true", help="등록된 권역 목록 표시")
    parser.add_argument("--list-categories", action="store_true", help="등록된 카테고리 목록 표시")
    parser.add_argument("-a", "--all", action="store_true", help="전체 100선 출력")

    args = parser.parse_args()
    data = load_data()

    if args.list_regions:
        regs = sorted(list(set(item["region"] for item in data)))
        print("🌐 등록된 권역/국가 목록:")
        for idx, reg in enumerate(regs, 1):
            count = sum(1 for item in data if item["region"] == reg)
            print(f"  {idx}. {reg} ({count}개 도구)")
        return

    if args.list_categories:
        cats = sorted(list(set(item["category"] for item in data)))
        print("📁 등록된 기능 카테고리 목록:")
        for idx, cat in enumerate(cats, 1):
            count = sum(1 for item in data if item["category"] == cat)
            print(f"  {idx}. {cat} ({count}개 도구)")
        return

    results = data

    if args.region:
        results = [item for item in results if match_region(args.region, item["region"])]

    if args.category:
        results = [item for item in results if args.category.lower() in item["category"].lower()]

    if args.model:
        results = [item for item in results if args.model.lower() in item["model_affinity"].lower()]

    if args.query:
        q = args.query.lower()
        results = [
            item for item in results
            if q in item["name"].lower()
            or q in item["summary"].lower()
            or q in item["use_case"].lower()
            or q in item["author"].lower()
            or q in item["execution_type"].lower()
            or q in item["region"].lower()
        ]

    if not args.all and not (args.query or args.region or args.category or args.model):
        print("💡 사용법:")
        print("  python search.py --region <us|cn|eu|jp|중국|유럽|일본>")
        print("  python search.py --query <검색어>")
        print("  python search.py --category <카테고리>")
        print("  python search.py --model <모델명(deepseek/qwen/mistral/opus/astra)>")
        print("  python search.py --list-regions")
        print("  python search.py --list-categories")
        print("  python search.py --all")
        print(f"\n현재 전세계 총 {len(data)}개의 엄선된 글로벌 AI 생성물/도구가 등록되어 있습니다.")
        return

    print(f"\n🔍 검색 결과: {len(results)}건 / 총 {len(data)}건\n" + "=" * 80)
    for item in results:
        print(format_item(item))

if __name__ == "__main__":
    main()
