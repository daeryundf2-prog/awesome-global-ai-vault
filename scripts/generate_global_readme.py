#!/usr/bin/env python3
"""
Dynamic Global AI Vault README Generator with Weekly Leaderboard
Renders Top 20 Global Leaderboard, Regional Division Tables, Emerging Radar Candidates,
and Automated Weekly Pipeline Badges.
"""

import os
import json
from datetime import datetime, timezone

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "global_creations.json")
CANDIDATES_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "emerging_candidates.json")
README_PATH = os.path.join(os.path.dirname(__file__), "..", "README.md")

def format_number(val):
    if isinstance(val, (int, float)):
        return f"{int(val):,}"
    return str(val)

def main():
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} not found.")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
        items = raw if isinstance(raw, list) else raw.get("items", [])

    candidates = []
    if os.path.exists(CANDIDATES_PATH):
        try:
            with open(CANDIDATES_PATH, "r", encoding="utf-8") as cf:
                cdata = json.load(cf)
                candidates = cdata.get("candidates", [])
        except Exception:
            pass

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Global items sorted by rank
    items_by_global_rank = sorted(items, key=lambda x: x.get("rank_global", 999))
    top_20 = items_by_global_rank[:20]

    # Partition by region
    region_map = {
        "북미": [],
        "중국": [],
        "유럽": [],
        "일본": []
    }

    for it in items:
        reg = it.get("region", "")
        if "북미" in reg or "North America" in reg:
            region_map["북미"].append(it)
        elif "중국" in reg or "China" in reg:
            region_map["중국"].append(it)
        elif "유럽" in reg or "Europe" in reg:
            region_map["유럽"].append(it)
        else:
            region_map["일본"].append(it)

    for reg_key in region_map:
        region_map[reg_key].sort(key=lambda x: x.get("rank_regional", x.get("rank_global", 999)))

    md = []
    md.append("# 🌐 Awesome Global AI Vault & Weekly Leaderboard")
    md.append("")
    md.append("> **전 세계 최상위 오픈소스 AI 생성물·에이전트·파운데이션 모델 100선 및 주간 자동 랭킹 레이더**")
    md.append("> 매주 월요일 09:00 KST, GitHub Actions가 100개 레포지토리의 실시간 Stars/Forks/최근 커밋일을 수집하여 동적 순위와 신규 급부상 프로젝트를 자동으로 최신화합니다.")
    md.append("")
    md.append("[![Weekly AI Vault & Leaderboard Sync](https://github.com/daeryundf2-prog/awesome-global-ai-vault/actions/workflows/weekly-sync.yml/badge.svg)](https://github.com/daeryundf2-prog/awesome-global-ai-vault/actions/workflows/weekly-sync.yml) ")
    md.append(f"![Last Synced](https://img.shields.io/badge/Last%20Synced-{now_utc.replace(' ', '%20')}-blue) ")
    md.append("![Tracked Repos](https://img.shields.io/badge/Tracked%20Repositories-100-success) ")
    md.append("![Weekly Cron](https://img.shields.io/badge/Sync%20Schedule-Every%20Monday%2009:00%20KST-orange)")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 🏆 1. Global AI Weekly Top 20 Leaderboard (실시간 글로벌 랭킹)")
    md.append("")
    md.append("GitHub 실시간 메트릭(Stars, Forks)과 최근 커밋 활동성(Recency Bonus)을 종합 반영한 글로벌 주간 랭킹입니다.")
    md.append("")
    md.append("| 순위 | 변동 | 상태 | 프로젝트명 | 권역 | 카테고리 | Stars | Forks | 활동 점수 | 핵심 특징 및 활용처 | 링크 |")
    md.append("|:---:|:---:|:---:|---|---|---|:---:|:---:|:---:|---|:---:|")

    for it in top_20:
        rank = it.get("rank_global", "-")
        delta = it.get("rank_delta", "-")
        status = it.get("status", "⚡ Active")
        name = it.get("name", "")
        reg = it.get("region", "").split("(")[0].strip()
        cat = it.get("category", "")
        stars = format_number(it.get("stars", 0))
        forks = format_number(it.get("forks", 0))
        score = it.get("score", 0.0)
        summary = it.get("summary", "")
        gh = it.get("github", "#")

        rank_badge = f"**#{rank:02d}**" if isinstance(rank, int) else f"**#{rank}**"
        md.append(f"| {rank_badge} | `{delta}` | {status} | **{name}** | {reg} | {cat} | ⭐ `{stars}` | 🍴 `{forks}` | **{score}** | {summary} | [GitHub]({gh}) |")

    md.append("")
    md.append("---")
    md.append("")

    if candidates:
        md.append("## 🛰️ 2. Weekly Radar Emerging Candidates (새롭게 포착된 유망 신규 AI)")
        md.append("")
        md.append("GitHub Search API를 통해 최근 1~2주간 스타 급증세가 포착된 미등록 신규 AI 오픈소스 프로젝트입니다:")
        md.append("")
        md.append("| 프로젝트명 | 언어 | Stars | Forks | 소개 | 저장소 링크 |")
        md.append("|---|:---:|:---:|:---:|---|:---:|")
        for c in candidates[:8]:
            c_name = c.get("name", "")
            c_lang = c.get("language", "Unknown")
            c_stars = format_number(c.get("stars", 0))
            c_forks = format_number(c.get("forks", 0))
            c_desc = c.get("description", "").replace("\n", " ")
            c_url = c.get("github", "#")
            md.append(f"| **{c_name}** | `{c_lang}` | ⭐ `{c_stars}` | 🍴 `{c_forks}` | {c_desc} | [GitHub]({c_url}) |")
        md.append("")
        md.append("---")
        md.append("")

    md.append("## 🌍 3. 전세계 4대 권역별 100선 랭킹 일람")
    md.append("")
    md.append("1. [🇺🇸 북미 / 글로벌 (North America & Global) (40선)](#reg-us)")
    md.append("2. [🇨🇳 중국권 (China & Greater Asia) (30선)](#reg-cn)")
    md.append("3. [🇪🇺 유럽권 (Europe) (20선)](#reg-eu)")
    md.append("4. [🇯🇵 일본 및 아태지역 (Japan & APAC) (10선)](#reg-jp)")
    md.append("")

    reg_sections = [
        ("reg-us", "🇺🇸 북미 / 글로벌 (North America & Global) (40선)", "북미"),
        ("reg-cn", "🇨🇳 중국권 (China & Greater Asia) (30선)", "중국"),
        ("reg-eu", "🇪🇺 유럽권 (Europe) (20선)", "유럽"),
        ("reg-jp", "🇯🇵 일본 및 아태지역 (Japan & APAC) (10선)", "일본")
    ]

    for anchor, title, key in reg_sections:
        sub_items = region_map[key]
        md.append(f"<a id=\"{anchor}\"></a>")
        md.append(f"### {title}")
        md.append("")
        md.append("| 권역순위 | 통합순위 | 상태 | 도구/프로젝트명 | 개발/조직 | 호환 모델 | Stars | 핵심 설명 및 실무 활용처 | 저장소 링크 |")
        md.append("|:---:|:---:|:---:|---|---|---|:---:|---|:---:|")

        for it in sub_items:
            reg_rank = it.get("rank_regional", "-")
            glob_rank = it.get("rank_global", "-")
            status = it.get("status", "⚡ Active")
            name = it.get("name", "")
            author = it.get("author", "")
            model = it.get("model_affinity", "")
            stars = format_number(it.get("stars", 0))
            summary = it.get("summary", "")
            use_case = it.get("use_case", "")
            gh = it.get("github", "#")

            desc = f"**{summary}**<br>👉 *{use_case}*"
            md.append(f"| **#{reg_rank}** | `#{glob_rank}` | {status} | **{name}** | {author} | `{model}` | ⭐ `{stars}` | {desc} | [GitHub]({gh}) |")

        md.append("")

    md.append("---")
    md.append("")
    md.append("## 🔎 4. 로컬 CLI 검색기 사용법 (`scripts/search.py`)")
    md.append("")
    md.append("저장소 내 `scripts/search.py`를 통해 터미널에서 순위별, 권역별, 모델별로 즉시 조회할 수 있습니다:")
    md.append("")
    md.append("""```bash
# 1. 글로벌 통합 랭킹 상위 Top 10 조회
python scripts/search.py --top 10

# 2. 특정 권역 필터링 (us / cn / eu / jp)
python scripts/search.py --region "cn"    # 중국권 30선 순위별 조회
python scripts/search.py --region "eu"    # 유럽권 20선 순위별 조회

# 3. 특정 모델 호환 도구 검색 (deepseek, qwen, mistral, opus, astra 등)
python scripts/search.py --model "deepseek"

# 4. 기능 키워드 검색 (agent, ocr, voice, memory, pdf 등)
python scripts/search.py --query "agent"

# 5. 등록된 권역 및 카테고리 통계 보기
python scripts/search.py --list-regions
python scripts/search.py --list-categories
```""")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## ⚙️ 5. 자동화 아키텍처 및 파이프라인")
    md.append("")
    md.append("""```mermaid
flowchart LR
    A[GitHub Actions Cron<br>매주 월요일 09:00 KST] --> B[scripts/update_metrics.py]
    B -->|GitHub REST API| C[(실시간 Stars / Forks / Commits)]
    C --> D[동적 가중치 랭킹 산정]
    A --> E[scripts/discover_trending.py]
    E -->|GitHub Search API| F[(신규 급부상 AI 레포 발굴)]
    D --> G[scripts/generate_global_readme.py]
    F --> G
    G --> H[README.md & Data 최신화]
    H --> I[Auto Git Commit & Push<br>skip-ci]
```""")
    md.append("")
    md.append("- **동적 가중치 산정 공식**:")
    md.append("  $$\\text{Activity Score} = \\log_{10}(\\text{Stars}) \\times 10 + \\text{Recency Bonus} + \\log_{10}(\\text{Forks}) \\times 2$$")
    md.append("  - 7일 이내 커밋: 가산점 +15 (🔥 Hot)")
    md.append("  - 30일 이내 커밋: 가산점 +8 (⚡ Active)")
    md.append("  - 90일 이내 커밋: 가산점 +3 (✨ Fresh)")
    md.append("  - 90일 초과: 가산점 0 (💤 Stable)")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 🤝 기여 및 건의")
    md.append("- 새로운 글로벌 오픈소스 AI 프로젝트나 획기적인 에이전트 도구가 발표되면 언제든 이슈(Issue)나 풀 리퀘스트(PR)를 남겨주세요.")
    md.append("- 관리 주체: [daeryundf2-prog](https://github.com/daeryundf2-prog)")

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    print(f"SUCCESS: Generated dynamic global README.md at {README_PATH}")

if __name__ == "__main__":
    main()
