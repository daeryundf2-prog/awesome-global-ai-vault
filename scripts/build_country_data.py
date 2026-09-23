#!/usr/bin/env python3
"""
Country-by-Country Top 20 AI Vault Dataset Generator
Generates 100 projects across 5 prominent AI powerhouse countries/blocs (20 each):
1. 🇺🇸 미국 (United States) - 20선
2. 🇨🇳 중국 (China) - 20선
3. 🇰🇷 대한민국 (South Korea) - 20선
4. 🇪🇺 유럽 (Europe - UK/France/Germany) - 20선
5. 🇯🇵 일본 (Japan) - 20선
"""

import os
import json

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "global_creations.json")

# 1. 🇺🇸 미국 (United States) - 20선
us_items = [
    {
        "name": "openclaw",
        "author": "openclaw",
        "github": "https://github.com/openclaw/openclaw",
        "category": "에이전트 하네스 & 자율 실행",
        "model_affinity": "Claude Opus 5.5 / GPT-6 Astra / Llama 3.3",
        "execution_type": "Agent Harness",
        "summary": "2026년 급부상한 범용 제너럴리스트 에이전트. 랍스터(Lobster) 아키텍처 기반 자율 태스크 분기",
        "use_case": "복잡한 웹 탐색, 코드 수정, 파일 시스템 조작을 단일 목표 지시로 자율 완결할 때"
    },
    {
        "name": "hermes-agent",
        "author": "NousResearch",
        "github": "https://github.com/nousresearch/hermes-agent",
        "category": "에이전트 하네스 & 자율 실행",
        "model_affinity": "Hermes 3 / Claude Code / Codex",
        "execution_type": "Adaptive Agent",
        "summary": "자율적인 스킬 학습 및 영구 누적을 특징으로 하는 적응형 에이전트 하네스",
        "use_case": "세션을 거듭할수록 팀의 특정 도메인 워크플로우에 맞춰 스스로 스킬을 학습하게 할 때"
    },
    {
        "name": "n8n",
        "author": "n8n.io",
        "github": "https://github.com/n8n-io/n8n",
        "category": "워크플로우 & 파이프라인 오케스트레이션",
        "model_affinity": "Multi-LLM / LangChain 연동",
        "execution_type": "Workflow Automation (⭐20만)",
        "summary": "수백 개의 SaaS와 데이터베이스를 AI 에이전트 노드로 연결하는 오픈소스 비주얼 워크플로우 플랫폼",
        "use_case": "슬랙, 노션, 세일즈포스, 이메일 간 복잡한 비즈니스 로직에 AI 판단 노드를 얹어 자동화할 때"
    },
    {
        "name": "AutoGPT",
        "author": "Significant-Gravitas",
        "github": "https://github.com/Significant-Gravitas/AutoGPT",
        "category": "에이전트 벤치마크 & 하네스",
        "model_affinity": "Multi-LLM",
        "execution_type": "Agent Platform (⭐18만)",
        "summary": "자율 에이전트의 시초이자 현재는 에이전트 빌더, 블록 기반 워크플로우, 벤치마킹을 아우르는 오픈 플랫폼",
        "use_case": "다양한 모델의 자율 문제 해결 성공률을 표준 벤치마크로 측정할 때"
    },
    {
        "name": "ollama",
        "author": "Ollama Official",
        "github": "https://github.com/ollama/ollama",
        "category": "로컬 인퍼런스 & 서빙 인프라",
        "model_affinity": "Llama, Qwen, DeepSeek, Mistral",
        "execution_type": "Local Model Runner (⭐18만)",
        "summary": "Mac, Linux, Windows에서 Llama, Qwen, DeepSeek 오픈 모델을 한 줄 명령으로 다운로드 및 실행하는 사실상 글로벌 표준",
        "use_case": "로컬 개발 환경에서 GPU 가속을 활용해 오프라인 LLM 서빙 및 로컬 에이전트 백엔드 구축"
    },
    {
        "name": "llama.cpp",
        "author": "Georgi Gerganov",
        "github": "https://github.com/ggerganov/llama.cpp",
        "category": "로컬 인퍼런스 & 서빙 인프라",
        "model_affinity": "GGUF Quantized Models",
        "execution_type": "C/C++ Core Engine (⭐12만)",
        "summary": "GGUF 양자화 포맷의 원조. 일반 CPU와 통합 메모리 GPU에서 대규모 모델을 돌릴 수 있게 만든 오픈 인프라",
        "use_case": "Ollama, Jan, LM Studio 등 전 세계 모든 로컬 AI 앱의 핵심 구동 엔진"
    },
    {
        "name": "ComfyUI",
        "author": "comfyanonymous",
        "github": "https://github.com/comfyanonymous/ComfyUI",
        "category": "생성형 미디어 & 노드 UI",
        "model_affinity": "Flux, SDXL, Video Diffusion",
        "execution_type": "Node-based GUI (⭐13만)",
        "summary": "가장 강력하고 모듈화된 노드 기반 생성형 이미지/비디오 워크플로우 런타임. 에이전트 API 연동 표준",
        "use_case": "AI 이미지/영상 생성 파이프라인을 완전 자동화된 백엔드 API로 래핑하여 에이전트와 결합할 때"
    },
    {
        "name": "browser-use",
        "author": "browser-use",
        "github": "https://github.com/browser-use/browser-use",
        "category": "브라우저 조작 & 웹 자동화",
        "model_affinity": "Claude 3.7 / Opus 5.5 / GPT-6 Astra",
        "execution_type": "Browser Agent (⭐11만)",
        "summary": "AI가 사람처럼 브라우저를 띄워 클릭, 스크롤, 양식 제출, 로그인, 데이터 수집을 완결하는 웹 에이전트",
        "use_case": "API가 없는 웹사이트 예약, 티켓팅, 경쟁사 가격 모니터링, 웹 기반 SaaS 자동 조작"
    },
    {
        "name": "vllm",
        "author": "UC Berkeley LMSYS",
        "github": "https://github.com/vllm-project/vllm",
        "category": "로컬 인퍼런스 & 서빙 인프라",
        "model_affinity": "All Open-weight LLMs",
        "execution_type": "High-Throughput Serving (⭐9.2만)",
        "summary": "PagedAttention 기반으로 메모리 낭비를 없애고 처리량을 최대 24배 끌어올린 오픈소스 프로덕션 서빙 엔진",
        "use_case": "대규모 사내 서빙 클러스터에서 수백 명의 동시 에이전트 요청을 고속 처리할 때"
    },
    {
        "name": "crewAI",
        "author": "CrewAI Official",
        "github": "https://github.com/crewAIInc/crewAI",
        "category": "워크플로우 & 파이프라인 오케스트레이션",
        "model_affinity": "Multi-LLM / Claude / OpenAI",
        "execution_type": "Role-playing Framework (⭐5.8만)",
        "summary": "기획자, 리서처, 작가 등 명확한 직책(Role)과 목표(Goal)를 부여해 가상의 팀을 조직하는 에이전트 프레임워크",
        "use_case": "시장 조사 보고서 작성, 뉴스레터 발행 파이프라인을 3~4명의 전문 가상 직원 팀으로 실행"
    },
    {
        "name": "mem0",
        "author": "Mem0 Official",
        "github": "https://github.com/mem0ai/mem0",
        "category": "에이전트 메모리 & 상태 관리",
        "model_affinity": "Multi-LLM / Graph + Vector",
        "execution_type": "Memory Layer (⭐6.5만)",
        "summary": "사용자의 과거 대화, 선호도, 사실 관계를 지속적으로 갱신하고 인덱싱하는 개인화 메모리 레이어",
        "use_case": "모든 에이전트 애플리케이션에 '사용자를 기억하는 영구 기억 장치'를 1줄 코드로 추가할 때"
    },
    {
        "name": "llama_index",
        "author": "LlamaIndex Official",
        "github": "https://github.com/run-llama/llama_index",
        "category": "데이터 인제스천 & RAG",
        "model_affinity": "Multi-LLM",
        "execution_type": "Data Framework (⭐5.2만)",
        "summary": "PDF, 노션, DB 등 방대한 비정형 데이터를 에이전트가 탐색 가능한 인덱스로 연결하는 RAG 표준",
        "use_case": "사내 위키, 고객지원 문서, API 문서를 에이전트의 지식 베이스로 공급할 때"
    },
    {
        "name": "whisper.cpp",
        "author": "Georgi Gerganov",
        "github": "https://github.com/ggerganov/whisper.cpp",
        "category": "로컬 인퍼런스 & 서빙 인프라",
        "model_affinity": "OpenAI Whisper",
        "execution_type": "C/C++ High Performance (⭐5.3만)",
        "summary": "C/C++로 밑바닥부터 재작성된 Whisper 추론 엔진. Apple Silicon Metal 가속으로 실시간 자막 전사 지원",
        "use_case": "맥북이나 경량 엣지 디바이스에서 100% 오프라인 고속 음성 인식"
    },
    {
        "name": "aider",
        "author": "Paul Gauthier (Aider)",
        "github": "https://github.com/Aider-AI/aider",
        "category": "에이전트 코딩 & 터미널",
        "model_affinity": "Claude Opus 5.5 / GPT-6 Astra / DeepSeek",
        "execution_type": "CLI Pair Programmer (⭐4.9만)",
        "summary": "터미널에서 Git과 완벽 연동되어 자동 커밋 메시지, diff 패치, 파일 맵을 관리하는 1위 코딩 도구",
        "use_case": "로컬 터미널에서 기존 Git 레포지토리를 직접 보며 페어 프로그래밍으로 기능 추가 및 디버깅"
    },
    {
        "name": "langgraph",
        "author": "LangChain Official",
        "github": "https://github.com/langchain-ai/langgraph",
        "category": "에이전트 하네스 & 상태 머신",
        "model_affinity": "Multi-LLM",
        "execution_type": "Stateful Graph Framework (⭐4.2만)",
        "summary": "상태(State)를 기반으로 순환 루프, 분기 조건, 인간 개입(Human-in-the-loop)을 정의하는 엔터프라이즈 에이전트 표준",
        "use_case": "승인 단계가 필요한 결재 시스템, 실패 시 재시도하는 복합 에이전트 워크플로우 개발"
    },
    {
        "name": "dspy",
        "author": "Stanford NLP",
        "github": "https://github.com/stanfordnlp/dspy",
        "category": "프롬프트 최적화 & 컴파일러",
        "model_affinity": "Multi-LLM / Open Models",
        "execution_type": "Algorithmic Optimizer (⭐3.8만)",
        "summary": "휴리스틱 프롬프트 대신 알고리즘으로 모델 가중치와 프롬프트를 자동 컴파일/최적화하는 스탠퍼드 프레임워크",
        "use_case": "RAG 파이프라인의 검색 정밀도와 답변 일관성을 수학적 평가 지표에 맞춰 자동 튜닝할 때"
    },
    {
        "name": "CopilotKit",
        "author": "CopilotKit Official",
        "github": "https://github.com/CopilotKit/CopilotKit",
        "category": "인앱 코파일럿 & UI 연동",
        "model_affinity": "Multi-LLM",
        "execution_type": "In-App Copilot Framework (⭐3.7만)",
        "summary": "기존 웹앱에 사이드바 코파일럿, 텍스트 인라인 편집, 프론트엔드 작업 제어 액션을 5분 만에 붙여주는 툴킷",
        "use_case": "사내 대시보드나 SaaS 앱에 사용자의 클릭/입력을 대신하는 인앱 AI 비서를 붙일 때"
    },
    {
        "name": "sglang",
        "author": "LMSYS Org",
        "github": "https://github.com/sgl-project/sglang",
        "category": "로컬 인퍼런스 & 서빙 인프라",
        "model_affinity": "DeepSeek / Llama / Qwen",
        "execution_type": "RadixAttention Inference (⭐3.6만)",
        "summary": "복잡한 에이전트 툴 호출과 다단계 추론에서 반복되는 KV 캐시를 Radix 트리로 공유해 레이턴시를 5배 단축",
        "use_case": "다단계 검색 및 CoT 추론을 반복하는 복잡한 에이전트의 응답 지연 극소화"
    },
    {
        "name": "diffusers",
        "author": "Hugging Face",
        "github": "https://github.com/huggingface/diffusers",
        "category": "생성형 미디어 & 노드 UI",
        "model_affinity": "PyTorch / Latent Diffusion",
        "execution_type": "Python Library (⭐3.4만)",
        "summary": "Stable Diffusion, Flux, ControlNet 등 최신 확산 모델을 통일된 파이썬 API로 다루는 표준 라이브러리",
        "use_case": "에이전트가 백엔드에서 이미지 인페인팅, 스타일 변환, 뎁스 기반 생성을 프로그래밍할 때"
    },
    {
        "name": "fastmcp",
        "author": "jlowin (Prefect)",
        "github": "https://github.com/jlowin/fastmcp",
        "category": "MCP & 도구 생태계",
        "model_affinity": "Claude Desktop / Claude Code / MCP",
        "execution_type": "Pythonic MCP Builder (⭐2.7만)",
        "summary": "FastAPI 스타일의 데코레이터 문법으로 고성능 Model Context Protocol(MCP) 서버를 10줄 만에 빌드",
        "use_case": "사내 파이썬 함수와 데이터베이스를 Claude의 외부 도구로 즉시 등록할 때"
    }
]

# 2. 🇨🇳 중국 (China) - 20선
cn_items = [
    {
        "name": "deepseek-harness",
        "author": "deepseek-ai",
        "github": "https://github.com/deepseek-ai/deepseek-harness",
        "category": "에이전트 하네스 & 자율 실행",
        "model_affinity": "Cordis Architecture / DeepSeek",
        "execution_type": "Modular Harness (⭐23만)",
        "summary": "Cordis 설계를 도입하여 모델, 툴, 세션, 루프 전부를 플러그인으로 갈아끼우는 프레임워크 독립형 하네스",
        "use_case": "DeepSeek 기반의 경량·모듈형 자율 코딩 에이전트 환경 구축"
    },
    {
        "name": "dify",
        "author": "LangGenius",
        "github": "https://github.com/langgenius/dify",
        "category": "워크플로우 & 에이전트 플랫폼",
        "model_affinity": "Multi-LLM / Plugin Architecture",
        "execution_type": "Agentic Platform (⭐15만)",
        "summary": "비주얼 오케스트레이션, RAG 파이프라인, 에이전트 워크플로우를 완성형 웹 앱으로 즉시 배포하는 글로벌 리딩 플랫폼",
        "use_case": "개발팀과 비개발팀이 협업하여 실서비스용 엔터프라이즈 AI 앱을 노코드로 운영할 때"
    },
    {
        "name": "DeepSeek-V3",
        "author": "deepseek-ai",
        "github": "https://github.com/deepseek-ai/DeepSeek-V3",
        "category": "최상위 추론 & 오픈 모델",
        "model_affinity": "MoE Architecture",
        "execution_type": "Foundation Model (⭐10만)",
        "summary": "671B 총 파라미터 중 37B만 활성화하는 초고효율 MoE 아키텍처. 상용 최상위 모델과 대등한 벤치마크 기록",
        "use_case": "사내 프라이빗 대규모 LLM 클러스터의 메인 범용 추론 백본"
    },
    {
        "name": "DeepSeek-R1",
        "author": "deepseek-ai",
        "github": "https://github.com/deepseek-ai/DeepSeek-R1",
        "category": "최상위 추론 & 오픈 모델",
        "model_affinity": "DeepSeek / Open-weight Frontier",
        "execution_type": "Reasoning Model (⭐9.1만)",
        "summary": "글로벌 AI 씬을 뒤흔든 오픈 가중치 최고봉 추론 모델. 강화학습을 통해 OpenAI o1 수준의 수학/코딩 추론 달성",
        "use_case": "복잡한 알고리즘 설계, 정밀 코드 디버깅 및 고난도 수학적 논리 전개"
    },
    {
        "name": "ragflow",
        "author": "Infiniflow",
        "github": "https://github.com/infiniflow/ragflow",
        "category": "엔터프라이즈 RAG 엔진",
        "model_affinity": "Deep Document Understanding",
        "execution_type": "RAG Engine (⭐9.1만)",
        "summary": "문서의 템플릿과 레이아웃을 깊이 이해하여 표와 단락이 엉키지 않도록 청킹하는 차세대 오픈소스 RAG",
        "use_case": "복잡한 서식의 매뉴얼과 정관에서 단 하나의 오류도 없이 정확한 조항을 검색할 때"
    },
    {
        "name": "PaddleOCR",
        "author": "Baidu Official",
        "github": "https://github.com/PaddlePaddle/PaddleOCR",
        "category": "광학 문자 인식 (OCR)",
        "model_affinity": "PaddlePaddle Engine",
        "execution_type": "Multilingual OCR (⭐9.0만)",
        "summary": "80개 이상 언어를 지원하는 초경량, 고정밀 산업용 OCR. 다단 표 및 영수증 텍스트 추출의 글로벌 최강자",
        "use_case": "스캔 공문서, 영수증, 송장 자동 입력 파이프라인의 핵심 전처리 엔진"
    },
    {
        "name": "MinerU",
        "author": "OpenDataLab",
        "github": "https://github.com/opendatalab/MinerU",
        "category": "문서 변환 & 구조화",
        "model_affinity": "All LLMs / RAG Platforms",
        "execution_type": "Document Extractor (⭐8.0만)",
        "summary": "복잡한 비정형 PDF, 오피스 문서, 학술 논문을 마크다운/JSON으로 완벽 추출하여 RAG 병목을 해결한 1위 도구",
        "use_case": "다단 레이아웃, 복합 표, 수식이 엉킨 논문/보고서를 LLM이 읽기 완벽한 포맷으로 변환"
    },
    {
        "name": "ChatTTS",
        "author": "2noise",
        "github": "https://github.com/2noise/ChatTTS",
        "category": "자연스러운 음성 합성",
        "model_affinity": "Speech Generation",
        "execution_type": "Conversational TTS (⭐3.9만)",
        "summary": "인터랙티브 대화에 특화된 혁신적 음성 합성 모델. 말하는 도중 자연스러운 웃음, 호흡, 억양 표현",
        "use_case": "대화형 AI 보이스 에이전트 및 오디오북, 팟캐스트 내레이션 제작"
    },
    {
        "name": "fish-speech",
        "author": "Fish Audio",
        "github": "https://github.com/fishaudio/fish-speech",
        "category": "자연스러운 음성 합성",
        "model_affinity": "Zero-shot TTS",
        "execution_type": "Audio Foundation Model (⭐3.2만)",
        "summary": "영어, 중국어, 일본어, 한국어를 완벽 지원하는 고품질 제로샷 텍스트-음성 변환 오픈 엔진",
        "use_case": "글로벌 타깃 버추얼 휴먼 및 게임 캐릭터의 고화질 음성 더빙"
    },
    {
        "name": "FastGPT",
        "author": "labring",
        "github": "https://github.com/labring/FastGPT",
        "category": "엔터프라이즈 RAG 플랫폼",
        "model_affinity": "Multi-LLM",
        "execution_type": "Knowledge Base Platform (⭐2.9만)",
        "summary": "데이터 전처리, 벡터 검색, 재순위화(Reranking)에 특화된 완성형 지식 베이스 질의응답 플랫폼",
        "use_case": "사내 CS 문의 응대 및 방대한 제품 매뉴얼 기반 고정밀 자동 답변봇"
    },
    {
        "name": "Qwen-Code",
        "author": "Alibaba Cloud QwenLM",
        "github": "https://github.com/QwenLM/Qwen-Code",
        "category": "코딩 에이전트 CLI",
        "model_affinity": "Qwen 2.5 Coder",
        "execution_type": "CLI Coding Agent (⭐2.8만)",
        "summary": "터미널에서 직접 실행되는 오픈소스 코딩 에이전트. Qwen-2.5-Coder의 최적화된 토크나이저와 도구 연동",
        "use_case": "오픈 모델 기반의 독립된 사내 전용 코딩 비서 환경 배포"
    },
    {
        "name": "CosyVoice",
        "author": "Alibaba NLP",
        "github": "https://github.com/FunAudioLLM/CosyVoice",
        "category": "제로샷 음성 복제",
        "model_affinity": "Multi-lingual Speech",
        "execution_type": "Voice Cloning (⭐2.3만)",
        "summary": "3초 오디오만으로 화자의 음색, 감정, 어투를 그대로 복제하고 다국어로 교차 발화하는 음성 모델",
        "use_case": "유튜브 영상의 다국어 더빙 시 원작자 본인의 목소리로 외국어 대사 생성"
    },
    {
        "name": "DB-GPT",
        "author": "eosphoros-ai",
        "github": "https://github.com/eosphoros-ai/DB-GPT",
        "category": "프라이빗 DB 에이전트",
        "model_affinity": "Multi-agent DB",
        "execution_type": "Private DB Agent (⭐2.0만)",
        "summary": "데이터와 메타데이터의 외부 유출 없이 로컬 DB에 직접 쿼리를 날리고 시각화하는 프라이빗 데이터 에이전트",
        "use_case": "사내 RDBMS, NoSQL, 웨어하우스에 대한 안전한 자연어 데이터 분석 및 보고서 작성"
    },
    {
        "name": "ktransformers",
        "author": "Tsinghua & KVCache AI",
        "github": "https://github.com/kvcache-ai/ktransformers",
        "category": "로컬 인퍼런스 가속",
        "model_affinity": "DeepSeek MoE",
        "execution_type": "Inference Acceleration (⭐1.9만)",
        "summary": "일반 데스크톱 GPU(예: RTX 4090) 1장으로 DeepSeek 671B MoE 모델을 실행시키는 혁신적인 CPU-GPU 오프로딩",
        "use_case": "수천만 원대 H100 서버 없이 일반 데스크톱에서 최고 스펙의 DeepSeek 모델을 로컬 구동"
    },
    {
        "name": "Qwen-Agent",
        "author": "Alibaba Cloud QwenLM",
        "github": "https://github.com/QwenLM/Qwen-Agent",
        "category": "다국어 & 코딩 에이전트",
        "model_affinity": "Qwen 2.5 / Qwen 3",
        "execution_type": "Official Agent Framework (⭐1.7만)",
        "summary": "8k부터 1M 컨텍스트까지 처리하는 알리바바 공식 에이전트. 펑션 콜링, 코드 인터프리터, 다중 툴 플래닝",
        "use_case": "대규모 책 한 권이나 초대형 소스코드 레포를 읽고 분석하는 문서 에이전트"
    },
    {
        "name": "InternVL",
        "author": "OpenGVLab",
        "github": "https://github.com/OpenGVLab/InternVL",
        "category": "멀티모달 시각 언어 모델",
        "model_affinity": "Vision-Language Model",
        "execution_type": "Multimodal Model (⭐1.0만)",
        "summary": "GPT-4V 수준의 시각 이해 벤치마크를 기록한 오픈소스 멀티모달. 고해상도 이미지 및 복합 도표 판독 특화",
        "use_case": "공학 도면 판독, 차트 분석, 스마트폰 UI 스크린샷 이해 에이전트"
    },
    {
        "name": "SenseVoice",
        "author": "Alibaba FunAudioLLM",
        "github": "https://github.com/FunAudioLLM/SenseVoice",
        "category": "초고속 음성 인식 & 감정 분석",
        "model_affinity": "Multi-lingual Speech",
        "execution_type": "Speech Understanding (⭐9.3K)",
        "summary": "Whisper 대비 5배 빠르고 감정, 음악, 웃음소리까지 감지하는 음성 인식 및 오디오 이해 모델",
        "use_case": "고객센터 통화 감정 분석 및 고속 실시간 회의록 전사"
    },
    {
        "name": "XAgent",
        "author": "OpenBMB",
        "github": "https://github.com/OpenBMB/XAgent",
        "category": "복합 자율 에이전트",
        "model_affinity": "Autonomous LLM",
        "execution_type": "Autonomous System (⭐8.5K)",
        "summary": "인간의 개입 없이 복잡한 목표를 하위 과제로 쪼개고 외부 도구를 탐색하며 실행하는 자율 문제 해결 시스템",
        "use_case": "복잡한 데이터 분석, 코드 작성, 인터넷 조사를 사람 없이 밤새 자율 실행시킬 때"
    },
    {
        "name": "GLM-4",
        "author": "Zhipu AI (THUDM)",
        "github": "https://github.com/THUDM/GLM-4",
        "category": "엔터프라이즈 멀티모달",
        "model_affinity": "1M Context / All-Tools",
        "execution_type": "Multimodal Foundation (⭐7.0K)",
        "summary": "칭화대 계열 Zhipu AI의 플래그십. 1M 장문 처리, 복합 도구 호출, 고정밀 웹 브라우징 능력 제공",
        "use_case": "긴 계약서 검토 및 대규모 데이터셋 크로스체크 에이전트"
    },
    {
        "name": "MindSearch",
        "author": "Shanghai AI Laboratory",
        "github": "https://github.com/InternLM/MindSearch",
        "category": "심층 웹 리서치 에이전트",
        "model_affinity": "InternLM 2.5 / Multi-Agent",
        "execution_type": "Deep Research Engine (⭐6.9K)",
        "summary": "인간 인지 과정을 모방해 다단계 병렬 검색과 지식 그래프를 구성하는 심층 연구 엔진 (Perplexity 대안)",
        "use_case": "복잡한 학술, 산업 리서치 주제에 대해 100개 이상의 웹페이지를 교차 검증해 레포트 작성"
    }
]

# 3. 🇰🇷 대한민국 (South Korea) - 20선
kr_items = [
    {
        "name": "KoAlpaca",
        "author": "Beomi (이준범)",
        "github": "https://github.com/Beomi/KoAlpaca",
        "category": "한국어 파운데이션 모델 & 파인튜닝",
        "model_affinity": "Llama / Polyglot-Ko",
        "execution_type": "Korean Instruction Tuning (⭐1.5K)",
        "summary": "한국어 인스트럭션 데이터셋 구축 및 라마/폴리글롯 파인튜닝의 시초가 된 대표 오픈소스",
        "use_case": "사내 한국어 비즈니스 지시 수행 모델 파인튜닝 데이터셋 및 학습 파이프라인 구축"
    },
    {
        "name": "soynlp",
        "author": "lovit (김현중)",
        "github": "https://github.com/lovit/soynlp",
        "category": "비지도학습 한국어 자연어처리",
        "model_affinity": "Unsupervised Korean NLP",
        "execution_type": "Python Library (⭐990+)",
        "summary": "사전 없이도 텍스트 데이터의 응집도(Cohesion)와 분기군(Branching Entropy)으로 단어를 자동 추출하는 비지도 토크나이저",
        "use_case": "신조어나 전문 용어가 가득한 고객 리뷰, 포럼 데이터에서 미등록 어휘를 자동 추출할 때"
    },
    {
        "name": "KoELECTRA",
        "author": "monologg (박장원)",
        "github": "https://github.com/monologg/KoELECTRA",
        "category": "한국어 임베딩 & 사전학습 모델",
        "model_affinity": "ELECTRA Architecture",
        "execution_type": "Pretrained Model (⭐640+)",
        "summary": "대규모 한국어 텍스트로 사전학습된 고성능 ELECTRA 모델. 한국어 감정분석, 문서분류, 질의응답 최고 벤치마크",
        "use_case": "사내 고객 상담 텍스트 분류, 악성 리뷰 필터링, RAG 리랭커로 활용"
    },
    {
        "name": "KoBART",
        "author": "SKT-AI",
        "github": "https://github.com/SKT-AI/KoBART",
        "category": "한국어 생성 & 요약 모델",
        "model_affinity": "BART Architecture",
        "execution_type": "Seq2Seq Model (⭐470+)",
        "summary": "SK텔레콤이 공개한 한국어 사전학습 BART 모델. 한국어 장문 기사 요약 및 문장 생성 표준",
        "use_case": "뉴스 기사 자동 3줄 요약, 사내 회의록 요약, 한국어 챗봇 생성 백본"
    },
    {
        "name": "kiwipiepy",
        "author": "bab2min (이민철)",
        "github": "https://github.com/bab2min/kiwipiepy",
        "category": "초고속 C++ 한국어 형태소 분석기",
        "model_affinity": "C++ Kiwi Engine",
        "execution_type": "Python Binding (⭐400+)",
        "summary": "C++로 작성된 초고속 고정밀 한국어 형태소 분석기. 띄어쓰기 오류가 있는 텍스트도 강력하게 교정 분석",
        "use_case": "초당 수만 건의 비정형 텍스트 색인 전처리, 한국어 검색엔진 형태소 인덱싱"
    },
    {
        "name": "polyglot",
        "author": "EleutherAI & 튜닙",
        "github": "https://github.com/EleutherAI/polyglot",
        "category": "다국어 & 한국어 대형 언어 모델",
        "model_affinity": "Polyglot-Ko 1.3B ~ 12.8B",
        "execution_type": "Open Weight Model (⭐480+)",
        "summary": "한국어 씬에서 가장 널리 쓰이는 비영어권 오픈 파운데이션 모델. 한국어 토크나이저 최적화",
        "use_case": "로컬 프라이빗 한국어 AI 비서 및 온프레미스 도메인 특화 모델 기반"
    },
    {
        "name": "korean-law-mcp",
        "author": "daeryundf2-prog",
        "github": "https://github.com/daeryundf2-prog/korean-law-mcp",
        "category": "법률 AI & MCP 도구 생태계",
        "model_affinity": "Claude 3.7 / Opus 5.5 / GPT-6",
        "execution_type": "Model Context Protocol Server",
        "summary": "대한민국 국가법령정보센터 및 대법원 종합법률정보 판례를 Claude/GPT에 실시간 연동하는 MCP 서버",
        "use_case": "법률 서면 작성, 조문 및 최신 대법원 판례 실시간 대조 검증"
    },
    {
        "name": "lazyforensic",
        "author": "daeryundf2-prog",
        "github": "https://github.com/daeryundf2-prog/lazyforensic",
        "category": "디지털 포렌식 & 증거 분석",
        "model_affinity": "Gemini 3.8 / Claude Code / Python",
        "execution_type": "Forensic CLI & Toolkit",
        "summary": "카카오톡 내보내기, SQLite DB, 타임라인 이벤트, 전자소송 서증 표찰을 통합 처리하는 포렌식 도구 모음",
        "use_case": "법원 제출용 디지털 증거 해시 감사, 무결성 증명서 발급 및 대화 분석"
    },
    {
        "name": "LAZYANTIGRAVITY",
        "author": "daeryundf2-prog",
        "github": "https://github.com/daeryundf2-prog/LAZYANTIGRAVITY",
        "category": "에이전트 오케스트레이션 프레임워크",
        "model_affinity": "Gemini 3.8 Flash / Claude Code",
        "execution_type": "Multi-Agent Orchestrator",
        "summary": "전지적 에이전트 실행, 2단계 공격적 오디팅(Adversarial Audit), 자율 태스크 분기를 지원하는 오케스트레이션 레이어",
        "use_case": "다중 에이전트 간 메모리 공유, 병렬 리서치 및 무인 코딩 파이프라인 가속"
    },
    {
        "name": "lumos",
        "author": "daeryundf2-prog",
        "github": "https://github.com/daeryundf2-prog/lumos",
        "category": "멀티모달 딥페이크 탐지 레이더",
        "model_affinity": "Multimodal Vision & Audio",
        "execution_type": "Forensic Detection Framework",
        "summary": "AI 생성 이미지/음성/영상의 위변조 흔적, EXIF 변조, FFT 주파수 이상 패턴을 감정하는 멀티모달 포렌식 레이더",
        "use_case": "법원 증거 감정, 가짜 뉴스 및 AI 생성 딥페이크 합성물 식별"
    },
    {
        "name": "deepfake-lens",
        "author": "daeryundf2-prog",
        "github": "https://github.com/daeryundf2-prog/deepfake-lens",
        "category": "멀티모달 딥페이크 탐지 레이더",
        "model_affinity": "Vision Foundation Models",
        "execution_type": "Visual Forensic Analyzer",
        "summary": "단일 프레임 수준에서 확산 모델(Diffusion) 및 생성형 AI 특유의 픽셀 아티팩트를 역추적하는 비전 포렌식 툴",
        "use_case": "위조된 인물 사진, 조작된 신분증 및 증거 사진의 진위 판정"
    },
    {
        "name": "frametrace",
        "author": "daeryundf2-prog",
        "github": "https://github.com/daeryundf2-prog/frametrace",
        "category": "영상 프레임 포렌식 & 채증",
        "model_affinity": "FFmpeg / Vision AI",
        "execution_type": "High-Throughput Video Pipeline",
        "summary": "CCTV, 블랙박스 고용량 동영상에서 핵심 이벤트 프레임을 초고속 추출하고 시계열 타임라인을 생성하는 도구",
        "use_case": "교통사고, 범죄 현장 CCTV 영상의 프레임별 나노초 타임스탬프 분석"
    },
    {
        "name": "kullm",
        "author": "NLPLabs-Korea-University",
        "github": "https://github.com/nlplabs-korea-university/KULLM",
        "category": "한국어 파운데이션 모델 & 파인튜닝",
        "model_affinity": "GPT-4 Distillation / Llama 2",
        "execution_type": "University Foundation (⭐1.1K)",
        "summary": "고려대학교 자연어처리 연구실과 HICA가 공동 제작한 한국어 인스트럭션 파인튜닝 모델 시리즈",
        "use_case": "학술 연구 및 한국어 상식 추론, 대화형 도메인 모델 프로토타이핑"
    },
    {
        "name": "Korpora",
        "author": "ko-nlp",
        "github": "https://github.com/ko-nlp/Korpora",
        "category": "한국어 코퍼스 & 데이터셋 툴킷",
        "model_affinity": "All Korean NLP Stacks",
        "execution_type": "Python Corpus Package (⭐600+)",
        "summary": "네이버 영화 리뷰, 국립국어원 등 대표적인 오픈 한국어 말뭉치를 한 줄 파이썬 코드로 다운로드/정제하는 툴킷",
        "use_case": "사내 한국어 NLP 모델 훈련을 위한 벤치마크 및 공개 말뭉치 신속 파이프라인 구성"
    },
    {
        "name": "py-hanspell",
        "author": "ssut",
        "github": "https://github.com/ssut/py-hanspell",
        "category": "한국어 맞춤법 & 오탈자 교정",
        "model_affinity": "Python Rule & API Wrapper",
        "execution_type": "Python Library (⭐800+)",
        "summary": "네이버 맞춤법 검사기 엔진을 파이썬에서 간편하게 호출하여 띄어쓰기와 맞춤법을 전처리하는 라이브러리",
        "use_case": "OCR 판독 결과물 교정 및 법률/공문서 초안의 오탈자 자동 검수 파이프라인"
    },
    {
        "name": "solar-10.7b",
        "author": "Upstage AI",
        "github": "https://github.com/UpstageAI/Upstage-Solar",
        "category": "한국어 프론티어 파운데이션 모델",
        "model_affinity": "Depth Up-Scaling (DUS)",
        "execution_type": "Enterprise Frontier Model",
        "summary": "DUS 기법으로 10.7B 크기에서 오픈LLM 리더보드 글로벌 1위를 달성한 한국 대표 스타트업 업스테이지의 모델",
        "use_case": "사내 온프레미스 고성능 문서 추출, 금융/법률 비즈니스 LLM 코어"
    },
    {
        "name": "rapid",
        "author": "daeryundf2-prog",
        "github": "https://github.com/daeryundf2-prog/rapid",
        "category": "로컬 퍼스트 포렌식 분석기",
        "model_affinity": "Fast Local Execution",
        "execution_type": "Local Engine",
        "summary": "인터넷 없는 폐쇄망 환경에서 현장 압수 단말기의 파일 메타데이터와 시스템 로그를 즉각 분석하는 로컬 도구",
        "use_case": "현장 압수수색 및 감사실 불시 점검 시 단말기 초기 트리아지"
    },
    {
        "name": "korean-doc-parser",
        "author": "daeryundf2-prog",
        "github": "https://github.com/daeryundf2-prog/lazyothers",
        "category": "한국 공문서 (HWP/HWPX) 파서",
        "model_affinity": "HWP, HWPX, PDF",
        "execution_type": "Document Ingestion Skill",
        "summary": "한컴오피스 무설치 환경에서 HWP, HWPX 바이너리를 마크다운 및 표 구조로 완전 복원하는 파서",
        "use_case": "공공기관 입찰 제안서, 판결문, 공문서의 RAG 색인 자동화"
    },
    {
        "name": "court-evidence-stamper",
        "author": "daeryundf2-prog",
        "github": "https://github.com/daeryundf2-prog/lazyothers",
        "category": "사법 증거 표찰 & Bates 날인",
        "model_affinity": "ECFS Standards",
        "execution_type": "Legal Forensic Automation",
        "summary": "대법원 전자소송 규격에 맞춘 갑/을호증 자동 표찰 및 고유 Bates 번호 날인, 증거설명서 자동 연동 도구",
        "use_case": "소송 증거 수천 장의 일괄 번호 부여 및 법원 제출 바인더 제작"
    },
    {
        "name": "financial-flow-tracer",
        "author": "daeryundf2-prog",
        "github": "https://github.com/daeryundf2-prog/lazyothers",
        "category": "금융 계좌 & 자금 흐름 추적기",
        "model_affinity": "Mermaid / Pandas Graph",
        "execution_type": "Financial Forensic Analyzer",
        "summary": "은행 거래내역 엑셀 파일로부터 입출금 상대방별 랭킹, 단기 순환 거래, 댕글링 자금 경로를 자동 시각화",
        "use_case": "횡령/배임 및 사기 사건의 자금 세탁 경로 다이어그램 생성"
    }
]

# 4. 🇪🇺 유럽 (Europe - UK/France/Germany) - 20선
eu_items = [
    {
        "name": "transformers",
        "author": "Hugging Face (France/US)",
        "github": "https://github.com/huggingface/transformers",
        "category": "모델 허브 & 표준 라이브러리",
        "model_affinity": "Every Open Model",
        "execution_type": "Python Core (⭐16만)",
        "summary": "현대 AI 오픈소스 생태계의 기틀. 전 세계 수십만 개의 사전학습 모델을 다운로드하고 추론하는 표준 라이브러리",
        "use_case": "새로 발표된 전 세계 최신 모델을 단 몇 줄의 파이썬 코드로 불러와 테스트할 때"
    },
    {
        "name": "unsloth",
        "author": "Unsloth AI (UK - Daniel Han)",
        "github": "https://github.com/unslothai/unsloth",
        "category": "초고속 모델 파인튜닝",
        "model_affinity": "Llama, Qwen, DeepSeek, Mistral",
        "execution_type": "Fine-Tuning Engine (⭐7.6만)",
        "summary": "파이토치 연산을 수작업으로 최적화하여 LLM 파인튜닝 속도를 5배 빠르게, VRAM 사용량을 80% 줄인 영국 명품 툴",
        "use_case": "일반 단일 GPU에서 70B 모델을 수 시간 만에 LoRA 파인튜닝할 때"
    },
    {
        "name": "AnythingLLM",
        "author": "Mintplex Labs",
        "github": "https://github.com/Mintplex-Labs/anything-llm",
        "category": "프라이버시 중심 올인원 AI",
        "model_affinity": "Multi-LLM / Multi-Vector",
        "execution_type": "Desktop & Server App (⭐6.6만)",
        "summary": "GDPR 및 완전 프라이버시를 보장하는 데스크톱/서버 AI 앱. 문서 드래그 앤 드롭 RAG, 다중 사용자 권한 관리",
        "use_case": "외부 클라우드 전송이 엄격히 금지된 법무법인, 회계법인의 사내 폐쇄망 AI 포털"
    },
    {
        "name": "LocalAI",
        "author": "mudler (Italy)",
        "github": "https://github.com/mudler/LocalAI",
        "category": "로컬 인퍼런스 서버",
        "model_affinity": "Drop-in OpenAI Replacement",
        "execution_type": "Inference Server (⭐4.9만)",
        "summary": "인터넷 없이 로컬 하드웨어에서 구동되는 오픈AI 규격 완벽 호환 REST API 서버 (텍스트, 음성, 이미지)",
        "use_case": "기존 상용 OpenAI API 코드를 단 한 줄도 수정하지 않고 사내 로컬 환경으로 교체할 때"
    },
    {
        "name": "ai-job-search",
        "author": "Mads Lorentzen (Denmark)",
        "github": "https://github.com/MadsLorentzen/ai-job-search",
        "category": "자율 채용 지원 에이전트",
        "model_affinity": "Claude Code / Codex / Gemini CLI",
        "execution_type": "CLI Framework (⭐4.3만)",
        "summary": "덴마크 개발자가 제작한 오픈소스. 채용공고 스크랩부터 이력서 맞춤 작성, 모의면접까지 자율 완결",
        "use_case": "구직자가 수십 개 타깃 기업에 맞춘 고품질 영문 커버레터와 CV를 자동 생성할 때"
    },
    {
        "name": "mindsdb",
        "author": "MindsDB (UK/US)",
        "github": "https://github.com/mindsdb/mindsdb",
        "category": "데이터베이스 AI 미들웨어",
        "model_affinity": "SQL-to-Model",
        "execution_type": "Database AI Layer (⭐3.9만)",
        "summary": "SQL 쿼리문 안에서 직접 AI 모델을 호출하고 실시간 예측 및 텍스트 분석을 수행하는 미들웨어",
        "use_case": "기존 DB 엔지니어가 파이썬 코드 없이 익숙한 SQL만으로 사내 데이터에 AI를 적용할 때"
    },
    {
        "name": "qdrant",
        "author": "Qdrant (Germany - Berlin)",
        "github": "https://github.com/qdrant/qdrant",
        "category": "Rust 기반 고성능 벡터 DB",
        "model_affinity": "Rust High Performance",
        "execution_type": "Vector DB Engine (⭐3.4만)",
        "summary": "Rust로 작성된 초고성능 벡터 검색 엔진. 풍부한 페이로드 필터링과 지연 없는 시맨틱 검색 지원",
        "use_case": "수백만 건의 문서에서 태그, 날짜, 카테고리 필터와 벡터 유사도 검색을 동시 초고속 처리할 때"
    },
    {
        "name": "smolagents",
        "author": "Hugging Face (France/US)",
        "github": "https://github.com/huggingface/smolagents",
        "category": "코드 기반 경량 에이전트",
        "model_affinity": "Any LLM / Open Weights",
        "execution_type": "Code-first Framework (⭐2.9만)",
        "summary": "복잡한 프레임워크 대신 에이전트의 모든 판단과 도구 호출을 파이썬 코드로 표현하는 미니멀리즘 에이전트",
        "use_case": "수천 줄의 복잡한 추상화 없이 몇 줄의 순수 파이썬 코드로 가볍고 강력한 에이전트를 조립할 때"
    },
    {
        "name": "haystack",
        "author": "deepset (Germany - Berlin)",
        "github": "https://github.com/deepset-ai/haystack",
        "category": "엔터프라이즈 RAG 오케스트레이터",
        "model_affinity": "Multi-LLM",
        "execution_type": "Enterprise Orchestrator (⭐2.6만)",
        "summary": "독일 특유의 견고한 엔지니어링으로 모듈화된 엔터프라이즈 RAG 및 에이전트 파이프라인 프레임워크",
        "use_case": "기업 보안과 유지보수성이 핵심인 엔터프라이즈 시맨틱 검색 및 문서 질의응답 시스템 구축"
    },
    {
        "name": "weaviate",
        "author": "Weaviate (Netherlands - Amsterdam)",
        "github": "https://github.com/weaviate/weaviate",
        "category": "클라우드 네이티브 벡터 DB",
        "model_affinity": "Go / Cloud Native",
        "execution_type": "Vector Search Engine (⭐1.6만)",
        "summary": "네덜란드 암스테르담에서 탄생한 클라우드 네이티브 벡터 데이터베이스. 멀티모달 검색 및 하이브리드 검색 특화",
        "use_case": "이미지와 텍스트가 섞인 멀티모달 이커머스 상품 시맨틱 검색 엔진"
    },
    {
        "name": "SubtitleEdit",
        "author": "Nikolaj Lynge Olsson (Denmark)",
        "github": "https://github.com/SubtitleEdit/subtitleedit",
        "category": "로컬 음성 전사 & 자막 도구",
        "model_affinity": "Local Whisper Integration",
        "execution_type": "Desktop App (⭐1.4만)",
        "summary": "덴마크에서 개발되어 전 세계 영상 전문가들이 사용하는 오픈소스 자막 편집기. 로컬 AI 모델 내장으로 오프라인 전사",
        "use_case": "방송국, 영상 제작사의 대용량 영상 로컬 자막 제작 및 다국어 싱크 수정"
    },
    {
        "name": "moshi",
        "author": "Kyutai Labs (France - Paris)",
        "github": "https://github.com/kyutai-labs/moshi",
        "category": "실시간 음성 대화 파운데이션",
        "model_affinity": "Helium 7B / Mimi Audio",
        "execution_type": "Speech-to-Speech Model (⭐1.1만)",
        "summary": "파리 비영리 연구소 Kyutai가 공개한 오픈소스 음성 대화 AI. STT/TTS 없이 200ms 지연으로 사람과 실시간 수다",
        "use_case": "중간 텍스트 변환 병목 없이 사람과 즉각 호흡을 주고받는 차세대 실시간 대화봇"
    },
    {
        "name": "text-generation-inference",
        "author": "Hugging Face (TGI)",
        "github": "https://github.com/huggingface/text-generation-inference",
        "category": "고성능 프로덕션 인퍼런스",
        "model_affinity": "Tensor Parallelism",
        "execution_type": "Production Serving (⭐1.0만)",
        "summary": "Hugging Face의 엔터프라이즈급 LLM 서빙 엔진. 텐서 병렬화, 토큰 스트리밍, 플래시 어텐션 지원",
        "use_case": "Kubernetes 환경에서 오픈 모델을 대규모 서비스 엔드포인트로 운영할 때"
    },
    {
        "name": "maka",
        "author": "Apache Maka Project (EU)",
        "github": "https://github.com/apache/maka",
        "category": "감사 가능한 로컬 실행 원장",
        "model_affinity": "Auditable Local Runs",
        "execution_type": "Execution Engine (⭐5.6K)",
        "summary": "에이전트가 내린 모든 툴 호출과 로컬 bash 명령어를 불변(Immutable) 원장에 기록해 법적 책임을 증명하는 엔진",
        "use_case": "자율 에이전트의 오작동 및 보안 사고 발생 시 원인 규명과 법적 감사 증빙"
    },
    {
        "name": "rhasspy",
        "author": "Michael Hansen (EU Open Source)",
        "github": "https://github.com/rhasspy/rhasspy",
        "category": "로컬 프라이빗 음성 비서",
        "model_affinity": "Offline Voice Stack",
        "execution_type": "Voice Assistant (⭐2.7K)",
        "summary": "클라우드 전송 없는 완전 오프라인 프라이빗 음성 비서 툴킷. 홈 오토메이션(Home Assistant) 완벽 연동",
        "use_case": "스마트홈 기기를 외부 서버 도청 걱정 없이 음성으로 제어할 때"
    },
    {
        "name": "hibiki",
        "author": "Kyutai Labs (France - Paris)",
        "github": "https://github.com/kyutai-labs/hibiki",
        "category": "실시간 다국어 음성 번역",
        "model_affinity": "Moshi Lineage",
        "execution_type": "Voice Translation (⭐1.5K)",
        "summary": "말하는 도중 실시간으로 다른 언어로 음성을 바꿔서 뱉어내는 엔드투엔드 동시통역 음성 모델",
        "use_case": "국제 컨퍼런스 실시간 음성 통역 및 다국어 실시간 화상 회의"
    },
    {
        "name": "Mistral-Large",
        "author": "Mistral AI (France)",
        "github": "https://github.com/mistralai/mistral-common",
        "category": "유럽 플래그십 파운데이션 모델",
        "model_affinity": "Mistral Architecture",
        "execution_type": "Frontier Model (⭐940+)",
        "summary": "프랑스 AI 대표주자 Mistral의 플래그십. 다국어(불어, 독어, 스페인어, 영어)와 복잡한 추론에서 최고 수준 성능",
        "use_case": "EU AI Act 및 데이터 주권(Sovereign AI) 규제를 준수하는 기업용 대규모 언어 모델"
    },
    {
        "name": "Codestral",
        "author": "Mistral AI (France)",
        "github": "https://github.com/mistralai/codestral-skills",
        "category": "코드 특화 파운데이션 모델",
        "model_affinity": "Codestral 22B",
        "execution_type": "Coding Intelligence",
        "summary": "80개 이상 프로그래밍 언어를 유창하게 구사하는 유럽 1위 오픈 코딩 모델. FIM(Fill-in-the-Middle) 완벽 지원",
        "use_case": "IDE 내 자동완성 및 Claude Code/Cursor의 유럽 현지 호스팅 백엔드"
    },
    {
        "name": "mistral-eval",
        "author": "Mistral AI (France)",
        "github": "https://github.com/mistralai/mistral-evals",
        "category": "유럽 환경 적응형 프롬프트 평가",
        "model_affinity": "Mistral Models",
        "execution_type": "Evaluation Suite",
        "summary": "유럽 각국 언어(프랑스어, 독일어, 이탈리아어 등)에서의 논리적 일관성과 규제 준수성을 측정하는 벤치마크",
        "use_case": "유럽 다국어 비즈니스 서비스 런칭 시 각 언어별 모델 응답 품질 보증"
    },
    {
        "name": "luminous",
        "author": "Aleph Alpha (Germany - Heidelberg)",
        "github": "https://github.com/Aleph-Alpha/luminous",
        "category": "유럽 독자 파운데이션 모델",
        "model_affinity": "Multimodal / Enterprise",
        "execution_type": "Sovereign AI",
        "summary": "독일 하이델베르크의 Aleph Alpha가 개발한 설명 가능성(Explainability) 중심의 유럽형 파운데이션 모델",
        "use_case": "답변의 근거가 되는 원본 문서의 위치를 정확히 역추적해야 하는 유럽 공공/의료 시스템"
    }
]

# 5. 🇯🇵 일본 (Japan) - 20선
jp_items = [
    {
        "name": "evolutionary-model-merge",
        "author": "Sakana AI (Tokyo)",
        "github": "https://github.com/SakanaAI/evolutionary-model-merge",
        "category": "진화 알고리즘 기반 모델 병합",
        "model_affinity": "Evolutionary Search / LLMs",
        "execution_type": "Evolutionary Merge Engine (⭐1.4K)",
        "summary": "도쿄 사카나 AI가 개발한 진화 알고리즘 기반 자동 모델 병합 도구. 교차 훈련 없이 고성능 하이브리드 LLM 탄생",
        "use_case": "수학 특화 모델과 일본어 특화 모델을 유전 알고리즘으로 자동 병합하여 새로운 모델 생성"
    },
    {
        "name": "mecab-ipadic-neologd",
        "author": "neologd",
        "github": "https://github.com/neologd/mecab-ipadic-neologd",
        "category": "일본어 신조어 & 맞춤형 사전",
        "model_affinity": "MeCab Dictionary",
        "execution_type": "Custom Dictionary (⭐2.7K)",
        "summary": "웹 문서와 SNS에서 매주 새로 등장하는 일본어 고유명사와 신조어를 자동 갱신하는 사실상 표준 사전",
        "use_case": "일본 서브컬처, 애니메이션, 최신 IT 유행어가 포함된 텍스트의 정확한 형태소 분리"
    },
    {
        "name": "voicevox",
        "author": "Hiroshiba (Japan)",
        "github": "https://github.com/VOICEVOX/voicevox",
        "category": "서브컬처 신경망 음성 합성",
        "model_affinity": "Japanese Neural TTS",
        "execution_type": "Desktop & Engine (⭐3.2K)",
        "summary": "일본 버추얼 유튜버 및 크리에이터 생태계의 절대적 1위 무료 음성 합성 소프트웨어 (즌다몬 등)",
        "use_case": "일본어 해설 영상, 서브컬처 게임, 버추얼 캐릭터 대사 자동 생성"
    },
    {
        "name": "voicevox_core",
        "author": "VOICEVOX Project",
        "github": "https://github.com/VOICEVOX/voicevox_core",
        "category": "음성 합성 코어 엔진",
        "model_affinity": "C++ / Python / Rust Binding",
        "execution_type": "Core Library (⭐1.1K)",
        "summary": "VOICEVOX의 고속 음성 합성 백엔드 C++ 코어. 파이썬과 러스트에서 경량 임베디드로 음성 출력",
        "use_case": "코딩 에이전트가 작업 완료 시 귀여운 일본어 보이스로 알림을 주도록 연동"
    },
    {
        "name": "kuromoji.js",
        "author": "takuyaa",
        "github": "https://github.com/takuyaa/kuromoji.js",
        "category": "자바스크립트 일본어 형태소 분석기",
        "model_affinity": "JavaScript / Node.js",
        "execution_type": "Pure JS Tokenizer (⭐1.5K)",
        "summary": "순수 자바스크립트로 브라우저나 Node.js 환경에서 C/바이너리 설치 없이 돌아가는 일본어 형태소 분석기",
        "use_case": "웹 브라우저 클라이언트 사이드에서 즉시 일본어 단어 분리 및 한자 읽기(후리가나) 생성"
    },
    {
        "name": "mecab-python3",
        "author": "SamuraiT",
        "github": "https://github.com/SamuraiT/mecab-python3",
        "category": "파이썬 MeCab 바인딩",
        "model_affinity": "Python 3 / C++",
        "execution_type": "Python Wrapper (⭐800+)",
        "summary": "일본어 자연어처리의 전설적인 MeCab 엔진을 현대 파이썬 3 환경에서 고속으로 호출하는 바인딩",
        "use_case": "일본어 대규모 말뭉치 전처리 및 검색엔진 토크나이저 구축"
    },
    {
        "name": "SudachiPy",
        "author": "Works Applications",
        "github": "https://github.com/WorksApplications/SudachiPy",
        "category": "기업용 고정밀 형태소 분석기",
        "model_affinity": "Sudachi Engine",
        "execution_type": "Multi-mode Analyzer (⭐440+)",
        "summary": "단어 분할 단위를 A(짧게), B(중간), C(길게) 3단계로 조절 가능한 엔터프라이즈 일본어 형태소 분석기",
        "use_case": "일본 대기업 사내 검색엔진 및 계약서 문서 색인 전처리"
    },
    {
        "name": "ELYZA-tasks-100",
        "author": "ELYZA (Tokyo University Startup)",
        "github": "https://github.com/elyza-inc/ELYZA-tasks-100",
        "category": "일본어 LLM 평가 벤치마크",
        "model_affinity": "Japanese LLMs",
        "execution_type": "Benchmark Suite",
        "summary": "일본 도쿄대 스타트업 ELYZA가 구축한 일본어 지시 수행 및 복합 문맥 이해 사실상 표준 벤치마크",
        "use_case": "새로 나온 글로벌 모델(Claude, GPT, Qwen)의 일본어 비즈니스 처리 능력 객관적 평가"
    },
    {
        "name": "llm-jp",
        "author": "LLM-jp (National Institute of Informatics)",
        "github": "https://github.com/llm-jp/llm-jp",
        "category": "일본 학술 파운데이션 모델",
        "model_affinity": "Japanese Academic LLM",
        "execution_type": "Open Foundation Model",
        "summary": "일본 국립정보학연구소(NII) 주도의 산학연 합동 오픈소스 일본어 파운데이션 모델 프로젝트",
        "use_case": "일본 전통 문화, 고유 한자, 법령 표현에 특화된 학술 연구 및 공공 서비스 구축"
    },
    {
        "name": "llm-jp-eval",
        "author": "LLM-jp",
        "github": "https://github.com/llm-jp/llm-jp-eval",
        "category": "일본어 자동 평가 하네스",
        "model_affinity": "Japanese LLMs",
        "execution_type": "Evaluation Harness",
        "summary": "일본어 독해, 번역, 수학, 추론 등 다양한 과제를 통일된 파이프라인으로 측정하는 공식 평가 도구",
        "use_case": "일본어 오픈소스 모델의 영역별 벤치마크 점수 자동 측정 및 리더보드 등재"
    },
    {
        "name": "japanese-stable-diffusion",
        "author": "Stability AI Japan",
        "github": "https://github.com/Stability-AI/japan-stable-diffusion",
        "category": "일본어 이미지 생성 디퓨전",
        "model_affinity": "Diffusion / Japanese Clip",
        "execution_type": "Image Generator",
        "summary": "일본어 텍스트 뉘앙스와 일본 서브컬처 스타일을 완벽하게 이해하도록 학습된 재팬 스테이블 디퓨전",
        "use_case": "일본 현지 감성의 애니메이션 풍 배경 및 캐릭터 일러스트레이션 생성"
    },
    {
        "name": "Swallow",
        "author": "Tokyo Tech Swallow Project",
        "github": "https://github.com/tokyotech-llm/Swallow",
        "category": "도쿄공대 일본어 대규모 모델",
        "model_affinity": "Llama 3 / Mistral Backbone",
        "execution_type": "Extended LLM",
        "summary": "도쿄공업대학과 산업기술총합연구소(AIST)가 Llama 가중치에 일본어 어휘 4만 개를 추가 확장 학습한 모델",
        "use_case": "자연스러운 일본어 비즈니스 경어체 구사 및 고난도 일본어 문해력 지원"
    },
    {
        "name": "open-calm",
        "author": "CyberAgent (Japan)",
        "github": "https://github.com/cyberagent/open-calm",
        "category": "일본 엔터프라이즈 언어 모델",
        "model_affinity": "Open-CALM Architecture",
        "execution_type": "Open Weight Model",
        "summary": "일본 대형 IT 기업 사이버에이전트가 자체 데이터로 사전학습해 공개한 오픈소스 일본어 모델 시리즈",
        "use_case": "일본 현지 웹 광고 카피라이팅 및 고객 상담 자동화"
    },
    {
        "name": "japanese-gpt-neox",
        "author": "rinna Co., Ltd. (Japan)",
        "github": "https://github.com/rinnakk/japanese-gpt-neox",
        "category": "대화형 감성 대화 모델",
        "model_affinity": "GPT-NeoX",
        "execution_type": "Conversational Model",
        "summary": "과거 MS 일본 법인에서 분사한 rinna의 고품질 대화형 일본어 모델. 친근한 대화체 구사",
        "use_case": "인터랙티브 스토리텔링 및 게임 캐릭터 롤플레잉 챗봇"
    },
    {
        "name": "kotoba-speech",
        "author": "Kotoba Technologies (Japan)",
        "github": "https://github.com/kotoba-tech/kotoba-speech",
        "category": "일본어 엔드투엔드 음성 모델",
        "model_affinity": "Japanese Speech AI",
        "execution_type": "Voice AI Model",
        "summary": "일본 스타트업 코토바 테크가 개발한 고속 고품질 일본어 음성인식 및 합성 통합 모델",
        "use_case": "사내 일본어 회의 음성 실시간 자막화 및 번역 파이프라인 연동"
    },
    {
        "name": "japanese-large-lm",
        "author": "LINE Corporation / LY Corp",
        "github": "https://github.com/line/japanese-large-lm",
        "category": "메신저 기반 일본어 대화 모델",
        "model_affinity": "LINE LLM",
        "execution_type": "Conversational Core",
        "summary": "라인(LINE)이 보유한 방대한 대화 데이터를 기반으로 학습된 일본어 대화 특화 대규모 언어 모델",
        "use_case": "라인 챗봇 및 비즈니스 고객 응대 자동화"
    },
    {
        "name": "seamless-m4t",
        "author": "Meta APAC Research",
        "github": "https://github.com/facebookresearch/seamless_communication",
        "category": "다국어 음성 번역 하네스",
        "model_affinity": "SeamlessM4T v2",
        "execution_type": "Universal Translator",
        "summary": "아시아-태평양 수십 개 언어 간의 실시간 음성-음성, 음성-텍스트 다자간 통번역을 지원하는 유니버설 모델",
        "use_case": "한-중-일-동남아 크로스보더 비즈니스 미팅 실시간 통역"
    },
    {
        "name": "dify-japan-recipes",
        "author": "Dify Japan User Group",
        "github": "https://github.com/dify-japan/recipes",
        "category": "AI 코딩 & 프롬프트 커뮤니티",
        "model_affinity": "Dify / Claude Code",
        "execution_type": "Workflow Recipes",
        "summary": "일본 현지 비즈니스(공문서, 비즈니스 메일 경어체 변환 등)에 맞춘 Dify 에이전트 실무 워크플로우 모음",
        "use_case": "일본 파트너사 협업 시 격식 있는 비즈니스 일본어 메일 및 보고서 자동 작성"
    },
    {
        "name": "sakura-cloud-ai",
        "author": "Sakura Internet (Japan)",
        "github": "https://github.com/sakura-internet/cloud-ai-stack",
        "category": "소버린 AI 인프라 스택",
        "model_affinity": "Sovereign Cloud AI",
        "execution_type": "Infrastructure Stack",
        "summary": "일본 정부가 인증한 소버린 클라우드 AI 인프라. 데이터 역외 유출 방지 및 안전한 LLM 파인튜닝 스택",
        "use_case": "일본 정부 및 금융기관 대상 역내 데이터 격리 에이전트 서비스 배포"
    },
    {
        "name": "fugumt",
        "author": "staka (FuguMT Project)",
        "github": "https://github.com/staka/fugumt",
        "category": "경량 일본어-영어 기계번역",
        "model_affinity": "MarianMT Architecture",
        "execution_type": "Local Translation Engine",
        "summary": "인터넷 없이 오프라인에서 매우 가볍게 구동되는 일본어-영어 쌍방향 고속 신경망 기계번역 엔진",
        "use_case": "로컬 문서 번역 및 개발자 터미널 영일 번역 파이프라인"
    }
]

def main():
    countries = [
        ("미국 (United States)", "US", us_items),
        ("중국 (China)", "CN", cn_items),
        ("대한민국 (South Korea)", "KR", kr_items),
        ("유럽 (Europe)", "EU", eu_items),
        ("일본 (Japan)", "JP", jp_items)
    ]

    all_items = []
    item_id = 1
    for country_name, country_code, items in countries:
        for idx, it in enumerate(items, start=1):
            it["id"] = item_id
            it["country"] = country_name
            it["country_code"] = country_code
            it["region"] = country_name
            it["rank_country"] = idx
            it["score"] = 0.0
            it["stars"] = 0
            it["forks"] = 0
            it["days_since_push"] = 999
            it["status"] = "💤 Stable"
            all_items.append(it)
            item_id += 1

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    print(f"✅ Generated {len(all_items)} items across 5 major countries (20 each).")
    print(f"📁 Saved to {DATA_PATH}")

if __name__ == "__main__":
    main()
