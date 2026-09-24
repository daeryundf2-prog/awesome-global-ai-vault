#!/usr/bin/env python3
"""
Dynamic Global AI Vault README Generator with Weekly Country-by-Country Top 20 & Global Top 100
Renders Global Top 100 Leaderboard, 5 Major Countries Top 20 Sections (US, CN, KR, EU, JP),
Emerging Radar Candidates, and Automated Weekly Pipeline Badges.
"""

import os
import sys
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

    # Global items sorted by rank — 404(unavailable)·archived는 랭킹에서 제외
    rankable = [it for it in items if it.get("status") != "unavailable" and not it.get("archived")]
    items_by_global_rank = sorted(rankable, key=lambda x: x.get("rank_global") or 9999)
    top_100 = items_by_global_rank[:100]

    # Partition by 5 prominent countries/blocs
    country_groups = {
        "US": {"title": "🇺🇸 미국 (United States) Top 20", "anchor": "cntry-us", "items": []},
        "CN": {"title": "🇨🇳 중국 (China) Top 20", "anchor": "cntry-cn", "items": []},
        "KR": {"title": "🇰🇷 대한민국 (South Korea) Top 20", "anchor": "cntry-kr", "items": []},
        "EU": {"title": "🇪🇺 유럽 (Europe - 영국/프랑스/독일 등) Top 20", "anchor": "cntry-eu", "items": []},
        "JP": {"title": "🇯🇵 일본 (Japan) Top 20", "anchor": "cntry-jp", "items": []},
    }

    for it in items:
        if it.get("status") == "unavailable":
            continue  # 사라진 레포는 표에 싣지 않는다
        code = it.get("country_code", "")
        cname = it.get("country", it.get("region", ""))
        if code in country_groups:
            country_groups[code]["items"].append(it)
        elif "미국" in cname or "North America" in cname:
            country_groups["US"]["items"].append(it)
        elif "중국" in cname or "China" in cname:
            country_groups["CN"]["items"].append(it)
        elif "한국" in cname or "대한민국" in cname or "Korea" in cname:
            country_groups["KR"]["items"].append(it)
        elif "유럽" in cname or "Europe" in cname:
            country_groups["EU"]["items"].append(it)
        elif "일본" in cname or "Japan" in cname:
            country_groups["JP"]["items"].append(it)
        else:
            country_groups["US"]["items"].append(it)

    for code in country_groups:
        country_groups[code]["items"].sort(key=lambda x: x.get("rank_country", x.get("rank_global", 999)))

    md = []
    md.append("# 🛰️ lazyradar: Global AI Tech Radar & 5-Nation Top 20")
    md.append("")
    md.append("> **레이지 시리즈 공식 글로벌 AI 기술 레이더 (Lazy Series Official Tech Radar)**")
    md.append("> 미국·중국·대한민국·유럽·일본 5대 주요국 Top 20 랭킹 분과 및 전 세계 100선 큐레이션 랭킹")
    md.append("> 매주 월요일 09:00 KST, GitHub Actions가 큐레이션된 100개 레포지토리의 Stars/Forks/최근 커밋 지표를 갱신해 순위를 다시 계산하고, Search API로 신규 후보를 제안합니다.")
    md.append("")
    md.append("[![Weekly lazyradar Sync & Leaderboard](https://github.com/daeryundf2-prog/lazyradar/actions/workflows/weekly-sync.yml/badge.svg)](https://github.com/daeryundf2-prog/lazyradar/actions/workflows/weekly-sync.yml) ")
    md.append(f"![Last Synced](https://img.shields.io/badge/Last%20Synced-{now_utc.replace(' ', '%20')}-blue) ")
    md.append("![Tracked Repos](https://img.shields.io/badge/Tracked%20Repositories-100-success) ")
    md.append("![5 Nations](https://img.shields.io/badge/Major%20Nations-US%20|%20CN%20|%20KR%20|%20EU%20|%20JP-purple) ")
    md.append("![Lazy Series](https://img.shields.io/badge/Lazy%20Series-Official%20Radar-orange) ")
    md.append("![Weekly Cron](https://img.shields.io/badge/Sync%20Schedule-Every%20Monday%2009:00%20KST-green)")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 🌍 5대 주요국별 바로가기")
    md.append("")
    md.append("1. [🇺🇸 미국 (United States) Top 20](#cntry-us)")
    md.append("2. [🇨🇳 중국 (China) Top 20](#cntry-cn)")
    md.append("3. [🇰🇷 대한민국 (South Korea) Top 20](#cntry-kr)")
    md.append("4. [🇪🇺 유럽 (Europe) Top 20](#cntry-eu)")
    md.append("5. [🇯🇵 일본 (Japan) Top 20](#cntry-jp)")
    md.append("6. [🏆 전 세계 100선 통합 랭킹 (Global Top 100)](#global-top-100)")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 🗺️ 1. 주요 5대국별 Top 20 랭킹 분과")
    md.append("")

    for code, group in country_groups.items():
        md.append(f"<a id=\"{group['anchor']}\"></a>")
        md.append(f"### {group['title']}")
        md.append("")
        md.append("| 국가순위 | 통합순위 | 상태 | 도구/프로젝트명 | 개발/조직 | 호환 모델 | Stars | Forks | 활동 점수 | 핵심 설명 및 실무 활용처 | 링크 |")
        md.append("|:---:|:---:|:---:|---|---|---|:---:|:---:|:---:|---|:---:|")

        for it in group["items"]:
            c_rank = it.get("rank_country")
            g_rank = it.get("rank_global")
            status = it.get("status", "⚡ Active")
            if it.get("archived"):
                status = "📦 Archived"
                c_rank = g_rank = None  # 순위 제외 — 데이터에 잔류 순위가 있어도 표시하지 않는다
            elif it.get("stale"):
                status = "⚠️ 갱신실패"
            name = it.get("name", "")
            author = it.get("author", "")
            model = it.get("model_affinity", "")
            stars = format_number(it.get("stars", 0))
            forks = format_number(it.get("forks", 0))
            score = it.get("score", 0.0)
            summary = it.get("summary", "")
            use_case = it.get("use_case", "")
            gh = it.get("github", "#")

            c_rank_s = f"**#{c_rank:02d}**" if isinstance(c_rank, int) else "**-**"
            g_rank_s = f"`#{g_rank:02d}`" if isinstance(g_rank, int) else "`-`"
            desc = f"**{summary}**<br>👉 *{use_case}*"
            md.append(f"| {c_rank_s} | {g_rank_s} | {status} | **{name}** | {author} | `{model}` | ⭐ `{stars}` | 🍴 `{forks}` | **{score}** | {desc} | [GitHub]({gh}) |")

        md.append("")

    md.append("---")
    md.append("")
    md.append("<a id=\"global-top-100\"></a>")
    md.append("## 🏆 2. Global AI Weekly Top 100 Leaderboard (글로벌 100선 종합 랭킹)")
    md.append("")
    md.append("GitHub 주간 갱신 메트릭(Stars, Forks)과 최근 커밋 활동성(Recency Bonus)을 종합 반영한 전 세계 100선 통합 랭킹입니다.")
    md.append("")
    md.append("| 순위 | 변동 | 상태 | 프로젝트명 | 국가 | 카테고리 | Stars | Forks | 활동 점수 | 핵심 특징 및 활용처 | 링크 |")
    md.append("|:---:|:---:|:---:|---|---|---|:---:|:---:|:---:|---|:---:|")

    for it in top_100:
        rank = it.get("rank_global") or "-"
        delta = it.get("rank_delta", "-")
        status = it.get("status", "⚡ Active")
        if it.get("archived"):
            status = "📦 Archived"
        elif it.get("stale"):
            status = "⚠️ 갱신실패"
        name = it.get("name", "")
        cntry = it.get("country", it.get("region", "")).split("(")[0].strip()
        cat = it.get("category", "")
        stars = format_number(it.get("stars", 0))
        forks = format_number(it.get("forks", 0))
        score = it.get("score", 0.0)
        summary = it.get("summary", "")
        gh = it.get("github", "#")

        rank_badge = f"**#{rank:02d}**" if isinstance(rank, int) else f"**#{rank}**"
        md.append(f"| {rank_badge} | `{delta}` | {status} | **{name}** | {cntry} | {cat} | ⭐ `{stars}` | 🍴 `{forks}` | **{score}** | {summary} | [GitHub]({gh}) |")

    md.append("")
    md.append("---")
    md.append("")

    if candidates:
        md.append("## 🛰️ 3. Weekly Radar Emerging Candidates (새롭게 포착된 유망 신규 AI)")
        md.append("")
        md.append("GitHub Search API 고정 토픽 쿼리로 포착된, 아직 추적 목록에 없는 AI 오픈소스 후보입니다:")
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

    md.append("## 🔎 4. 로컬 CLI 검색기 사용법 (`scripts/search.py`)")
    md.append("")
    md.append("저장소 내 `scripts/search.py`를 통해 터미널에서 국가별, 순위별, 모델별로 즉시 조회할 수 있습니다:")
    md.append("")
    md.append("""```bash
# 1. 국가별 Top 20 조회 (us, cn, kr, eu, jp)
python scripts/search.py --country "kr"    # 🇰🇷 대한민국 Top 20 조회
python scripts/search.py --country "us"    # 🇺🇸 미국 Top 20 조회
python scripts/search.py --country "cn"    # 🇨🇳 중국 Top 20 조회
python scripts/search.py --country "eu"    # 🇪🇺 유럽 Top 20 조회
python scripts/search.py --country "jp"    # 🇯🇵 일본 Top 20 조회

# 2. 글로벌 통합 랭킹 상위 Top 10 또는 전수(Top 100) 조회
python scripts/search.py --top 10
python scripts/search.py --top

# 3. 특정 모델 호환 도구 검색 (deepseek, qwen, mistral, opus, astra 등)
python scripts/search.py --model "deepseek"

# 4. 기능 키워드 검색 (agent, ocr, voice, memory, pdf 등)
python scripts/search.py --query "agent"

# 5. 등록된 국가 및 카테고리 통계 보기
python scripts/search.py --list-countries
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
    B -->|GitHub REST API| C[(100개 레포 주간<br>Stars / Forks / Commits)]
    C --> D[국가별 Top 20 &<br>글로벌 Top 100 랭킹 산정]
    A --> E[scripts/discover_trending.py]
    E -->|GitHub Search API| F[(신규 후보 레포 탐색)]
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
    md.append("- **방법론**:")
    md.append("  - **목록 선정 기준**: 추적 대상 100개는 관리자가 수동 선정한 큐레이션 목록입니다. 국가 분류는 조직/저자의 공개 정보에 따릅니다. 신규 항목은 자동으로 목록에 합류하지 않고 Emerging 후보에만 표시됩니다.")
    md.append("  - **Emerging 후보의 한계**: `discover_trending.py`는 고정 토픽 쿼리(`topic:mcp`, `topic:agent`, `deepseek`, `speech-to-speech`)의 누적 스타 상위 결과를 가져옵니다. 생성일/푸시일 필터와 주간 스타 증가분 지표가 없으므로 '급부상'이 아니라 '미등록 고스타 레포'로 해석해야 합니다.")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 🤝 기여 및 건의")
    md.append("- 새로운 글로벌 오픈소스 AI 프로젝트나 획기적인 에이전트 도구가 발표되면 언제든 이슈(Issue)나 풀 리퀘스트(PR)를 남겨주세요.")
    md.append("- 관리 주체: [daeryundf2-prog](https://github.com/daeryundf2-prog)")

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    print(f"SUCCESS: Generated country-by-country dynamic README.md at {README_PATH}")

if __name__ == "__main__":
    if sys.stdout:
        sys.stdout.reconfigure(encoding="utf-8")
    main()
