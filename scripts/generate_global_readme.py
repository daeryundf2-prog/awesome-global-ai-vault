import json
import os

data_path = os.path.join(os.path.dirname(__file__), "..", "data", "global_creations.json")
with open(data_path, "r", encoding="utf-8") as f:
    items = json.load(f)

# Group by Region
regions = {}
for it in items:
    reg = it["region"]
    if reg not in regions:
        regions[reg] = []
    regions[reg].append(it)

md = []
md.append("# 🌐 Awesome Global AI Creations & Tools Vault (전세계 100선)")
md.append("")
md.append("> **미국/북미(Silicon Valley)**, **중국(DeepSeek/Qwen/Alibaba)**, **유럽(Mistral/Kyutai/독일/영국)**, **일본 및 아태지역** 등 전 세계 주요 권역에서 활발히 개발·공개되고 실무에 쓰이는 최상위 오픈소스 AI 생성물, 에이전트 하네스, 서빙 인프라, 비전/음성 파운데이션 도구 100선을 집대성한 글로벌 보물창고입니다.")
md.append("")
md.append("---")
md.append("")
md.append("## 🌍 1. 전세계 권역별 AI 생태계 지형도 (2026)")
md.append("")
md.append("| 권역 | 핵심 주도 세력 | 생태계 핵심 특징 및 트렌드 | 대표 프로젝트 |")
md.append("|---|---|---|---|")
md.append("| **🇺🇸 북미 / 글로벌**<br>*(40선)* | OpenAI, Anthropic, Stanford, Berkeley, Meta, Vercel | • **자율 에이전트 하네스 & 컴퓨터 조작**: `openclaw`, `hermes-agent`, `aider`, `browser-use`<br>• **엔터프라이즈 프레임워크 & 서빙**: `vllm`, `ollama`, `langgraph`, `crewAI`, `dspy`, `fastmcp`<br>• **노드 미디어 & 생성형 UI**: `ComfyUI`, `Vercel AI SDK`, `CopilotKit` | `openclaw`, `vllm`, `ollama`, `aider`, `browser-use` |")
md.append("| **🇨🇳 중국권**<br>*(30선)* | DeepSeek, Alibaba Qwen, Zhipu GLM, OpenDataLab, Baidu, Tencent | • **오픈 가중치 최상위 추론 혁명**: `DeepSeek-R1`, `DeepSeek-V3`, `ktransformers`(단일 GPU 671B 구동)<br>• **RAG & 문서 파싱 병목 타파**: `MinerU`, `PaddleOCR`, `ragflow`<br>• **완성형 에이전트 플랫폼 & 초자연 음성**: `dify`, `FastGPT`, `ChatTTS`, `CosyVoice` | `DeepSeek-R1`, `Qwen-Agent`, `dify`, `MinerU`, `ChatTTS` |")
md.append("| **🇪🇺 유럽권**<br>*(20선)* | Mistral AI, Kyutai Labs, Hugging Face, Qdrant, deepset, Unsloth | • **유럽 독자 주권 AI & 실시간 음성**: `Mistral-Large`, `Codestral`, `Moshi`(200ms 보이스), `Hibiki`<br>• **Rust 기반 고성능 인프라 & 최적화**: `qdrant`, `unsloth`(VRAM 80% 절감 고속 파인튜닝)<br>• **GDPR 준수 & 로컬 프라이빗 런타임**: `LocalAI`, `AnythingLLM`, `Apache Maka`(감사 원장) | `Mistral-Large`, `Moshi`, `qdrant`, `smolagents`, `unsloth` |")
md.append("| **🇯🇵 일본 & 아태**<br>*(10선)* | ELYZA, NII (LLM-jp), VOICEVOX, CyberAgent, Sakura Internet | • **서브컬처 & 정밀 일본어 음성**: `VOICEVOX`(즌다몬 음성 코어), `Japanese Stable Diffusion`<br>• **현지화 LLM 평가 & 소버린 클라우드**: `ELYZA-tasks-100`, `llm-jp`, `open-calm`, `Sakura AI` | `VOICEVOX`, `ELYZA-tasks-100`, `llm-jp`, `dify-japan` |")
md.append("")
md.append("---")
md.append("")
md.append("## 🔎 2. 로컬 빠른 검색 CLI 도구 사용법")
md.append("")
md.append("저장소 내 `scripts/search.py`를 통해 터미널에서 권역별, 모델별, 키워드별로 즉시 도구를 조회할 수 있습니다:")
md.append("")
md.append("```bash")
md.append("# 1. 특정 권역 필터링 (us / cn / eu / jp 또는 북미 / 중국 / 유럽 / 일본)")
md.append("python scripts/search.py --region \"cn\"    # 중국권 30선 즉시 조회")
md.append("python scripts/search.py --region \"eu\"    # 유럽권 20선 즉시 조회")
md.append("python scripts/search.py --region \"us\"    # 북미 40선 즉시 조회")
md.append("")
md.append("# 2. 특정 모델 호환 도구 검색 (예: deepseek, qwen, mistral, opus, astra)")
md.append("python scripts/search.py --model \"deepseek\"")
md.append("")
md.append("# 3. 기능 키워드 검색 (예: agent, ocr, voice, memory, video)")
md.append("python scripts/search.py --query \"ocr\"")
md.append("")
md.append("# 4. 등록된 전체 권역 및 기능 카테고리 통계 보기")
md.append("python scripts/search.py --list-regions")
md.append("python scripts/search.py --list-categories")
md.append("```")
md.append("")
md.append("---")
md.append("")
md.append("## 📑 3. 권역별 100선 목차 바로가기")
md.append("")
for idx, reg in enumerate(regions.keys(), 1):
    count = len(regions[reg])
    anchor = f"reg-{idx}"
    md.append(f"{idx}. [{reg} ({count}선)](#{anchor})")

md.append("")
md.append("---")
md.append("")

reg_idx = 1
for reg, reg_items in regions.items():
    anchor = f"reg-{reg_idx}"
    md.append(f"<a id=\"{anchor}\"></a>")
    md.append(f"## 🌐 {reg_idx}. {reg} ({len(reg_items)}선)")
    md.append("")
    md.append("| No | 도구/프로젝트명 | 개발/조직 | 호환 모델 | 실행 형태 | 핵심 설명 및 실무 활용처 | 공식 저장소 / 링크 |")
    md.append("|:---:|---|---|---|:---:|---|:---:|")
    for it in reg_items:
        clean_desc = f"**{it['summary']}**<br>👉 *{it['use_case']}*"
        link_str = f"[{it['name']}]({it['github']})" if it['github'].startswith("http") else it['github']
        md.append(f"| `{it['id']:03d}` | **{it['name']}** | {it['author']} | `{it['model_affinity']}` | `{it['execution_type']}` | {clean_desc} | {link_str} |")
    md.append("")
    reg_idx += 1

md.append("---")
md.append("")
md.append("## 🤝 글로벌 기여 및 데이터 동기화")
md.append("- 새로운 글로벌 오픈소스 AI 프로젝트나 획기적인 에이전트 도구가 발표되면 `data/global_creations.json`에 추가하고 PR을 보내주세요.")
md.append("- 등재 기준: 깃허브 오픈소스 저장소 링크 필수, 실제 배포 가능한 코드/바이너리/스킬 형태, 검증된 프로덕션 활용도.")

out_readme = os.path.join(os.path.dirname(__file__), "..", "README.md")
with open(out_readme, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"SUCCESS: Generated global README.md with {len(items)} items at {out_readme}")
