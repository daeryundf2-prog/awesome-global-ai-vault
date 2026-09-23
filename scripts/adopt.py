#!/usr/bin/env python3
"""
lazyradar Technology Adoption & Integration Recipe Engine (실무 적용 & 무기화 엔진)
Transforms discovered global AI tools into instant, copy-paste production code recipes,
dependency specifications, and integration guides.
"""

import os
import sys
import json
import argparse

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "global_creations.json")
RECIPES_DIR = os.path.join(os.path.dirname(__file__), "..", "recipes")

RECIPE_TEMPLATES = {
    "donut": {
        "install": "pip install transformers torch pillow",
        "description": "네이버 Clova의 OCR-free 문서 이해 모델. 이미지에서 키-값 JSON 데이터를 단번에 추출합니다.",
        "code": """from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

# 1. 모델 및 프로세서 로드
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def extract_document_json(image_path: str):
    \"\"\"영수증/계약서/공문서 이미지에서 OCR 없이 JSON 엔티티 직접 추출\"\"\"
    image = Image.open(image_path).convert("RGB")
    pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)
    
    task_prompt = "<s_cord-v2>"
    decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids.to(device)
    
    outputs = model.generate(
        pixel_values,
        decoder_input_ids=decoder_input_ids,
        max_length=512,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        num_beams=1,
    )
    
    seq = processor.batch_decode(outputs.sequences)[0]
    seq = seq.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
    return processor.token2json(seq)

# 실행 예시:
# result = extract_document_json("sample_receipt.png")
# print(result)
"""
    },
    "kiwi": {
        "install": "pip install kiwipiepy",
        "description": "C++ 기반 지능형 한국어 형태소 분석기. 띄어쓰기 오류 자동 교정 및 초고속 토크나이징.",
        "code": """from kiwipiepy import Kiwi

# 1. Kiwi 인스턴스 초기화 (멀티스레드 지원)
kiwi = Kiwi(num_workers=4)

def sanitize_and_tokenize_korean(text: str):
    \"\"\"띄어쓰기가 망가진 비정형 한글 텍스트 정밀 교정 및 명사 추출\"\"\"
    # 띄어쓰기 자동 보정
    spaced_text = kiwi.space(text)
    
    # 형태소 분석 및 품사 태깅
    tokens = kiwi.tokenize(spaced_text)
    
    # 핵심 명사(NNG, NNP) 추출
    nouns = [t.form for t in tokens if t.tag in ('NNG', 'NNP')]
    return {
        "corrected_text": spaced_text,
        "tokens": [(t.form, t.tag) for t in tokens],
        "nouns": nouns
    }

# 실행 예시:
# text = "대법원판례에따르면이러한계약은무효로본다."
# print(sanitize_and_tokenize_korean(text))
"""
    },
    "mineru": {
        "install": "pip install magic-pdf[full] detectron2",
        "description": "복잡한 비정형 PDF, 다단 수식, 꼬인 표를 마크다운/JSON으로 무오류 변환하는 글로벌 1위 RAG 전처리 도구.",
        "code": """import os
from magic_pdf.pipe.UNIPipe import UNIPipe
from magic_pdf.rw.DiskReaderWriter import DiskReaderWriter

def parse_pdf_to_clean_markdown(pdf_path: str, output_dir: str):
    \"\"\"복잡한 공문서/논문/계약서 PDF를 KaTeX 수식 및 클린 마크다운 표로 변환\"\"\"
    os.makedirs(output_dir, exist_ok=True)
    reader = DiskReaderWriter(os.path.dirname(pdf_path))
    writer = DiskReaderWriter(output_dir)
    
    pdf_bytes = reader.read(os.path.basename(pdf_path), "rb")
    pipe = UNIPipe(pdf_bytes, {}, writer)
    pipe.pipe_classify()
    pipe.pipe_analyze()
    pipe.pipe_parse()
    
    md_content = pipe.pipe_mk_markdown(output_dir, drop_mode="none")
    return md_content

# 실행 예시:
# parse_pdf_to_clean_markdown("contract.pdf", "./output")
"""
    },
    "fastmcp": {
        "install": "pip install fastmcp",
        "description": "FastAPI 스타일 데코레이터로 Claude/Gemini용 MCP 서버를 10줄 만에 빌드하는 도구.",
        "code": """from fastmcp import FastMCP

# 1. MCP 서버 선언
mcp = FastMCP("Legal-Forensic-Assistant")

@mcp.tool()
def search_statute_or_case(keyword: str) -> str:
    \"\"\"대한민국 법령 조문 또는 대법원 판례를 검색합니다.\"\"\"
    # 실제 사내 법률 DB 또는 외부 API 연동
    return f"[{keyword}] 관련 대법원 판례 3건 검색 완료: ..."

@mcp.tool()
def verify_hash_integrity(file_path: str, expected_sha256: str) -> bool:
    \"\"\"포렌식 파일의 SHA-256 무결성을 실시간 검증합니다.\"\"\"
    import hashlib
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest().lower() == expected_sha256.lower()

if __name__ == "__main__":
    mcp.run()
"""
    }
}

def load_data():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
        return raw if isinstance(raw, list) else raw.get("items", [])

def main():
    parser = argparse.ArgumentParser(description="lazyradar 실전 기술 도입 및 연동 레시피 엔진")
    parser.add_argument("tool", type=str, nargs="?", default=None, help="적용할 도구명 또는 키워드 (예: donut, kiwi, mineru, fastmcp, pororo 등)")
    parser.add_argument("--save", action="store_true", help="연동 템플릿 코드 파일을 recipes/ 디렉토리에 자동 생성")
    parser.add_argument("--list", action="store_true", help="즉시 적용 가능한 레시피 템플릿 목록 출력")

    args = parser.parse_args()

    if args.list:
        print("\n🛠️ [즉시 실무 적용 가능한 고정밀 연동 레시피]")
        for k, v in RECIPE_TEMPLATES.items():
            print(f"  • {k:<12} : {v['description']}")
        print("\n사용법: python scripts/adopt.py <tool_name> [--save]\n")
        return

    if not args.tool:
        parser.print_help()
        return

    tool_q = args.tool.lower().strip()
    data = load_data()

    # Find matching project in dataset
    matched_item = None
    for it in data:
        if tool_q in it.get("name", "").lower() or tool_q in it.get("github", "").lower():
            matched_item = it
            break

    print("\n" + "=" * 80)
    print(f"🛰️  [lazyradar Technology Adoption Report: {tool_q.upper()}]")
    print("=" * 80)

    if matched_item:
        print(f"• 프로젝트명 : {matched_item.get('name')} ({matched_item.get('author')})")
        print(f"• 국가/권역  : {matched_item.get('country', matched_item.get('region'))}")
        print(f"• 저장소     : {matched_item.get('github')}")
        print(f"• 실시간 메트릭: ⭐ {matched_item.get('stars', 0):,} stars | 🍴 {matched_item.get('forks', 0):,} forks | {matched_item.get('status')}")
        print(f"• 핵심 설명  : {matched_item.get('summary')}")
        print(f"• 실무 활용처: {matched_item.get('use_case')}")
    else:
        print(f"⚠️  데이터셋에서 정확한 일치 항목을 찾지 못했으나 레시피 데이터베이스를 검색합니다.")

    # Match with recipe templates
    template_key = None
    for k in RECIPE_TEMPLATES:
        if k in tool_q or tool_q in k:
            template_key = k
            break

    if template_key:
        recipe = RECIPE_TEMPLATES[template_key]
        print("\n" + "-" * 80)
        print("📦 1. 패키지 설치 명령어 (Installation):")
        print(f"   $ {recipe['install']}")
        print("\n💻 2. 내 프로젝트 즉시 임포트용 실전 연동 코드 (Code Recipe):")
        print("-" * 80)
        print(recipe["code"])
        print("-" * 80)

        if args.save:
            os.makedirs(RECIPES_DIR, exist_ok=True)
            target_py = os.path.join(RECIPES_DIR, f"recipe_{template_key}.py")
            target_req = os.path.join(RECIPES_DIR, f"requirements_{template_key}.txt")
            with open(target_py, "w", encoding="utf-8") as f:
                f.write(recipe["code"])
            with open(target_req, "w", encoding="utf-8") as f:
                f.write(recipe["install"].replace("pip install ", "").replace(" ", "\n") + "\n")
            print(f"✅ 연동 코드 저장 완료: {target_py}")
            print(f"✅ 의존성 파일 저장 완료: {target_req}")
    else:
        print("\n" + "-" * 80)
        print("💡 일반 저장소 도입 가이드:")
        gh_url = matched_item.get("github") if matched_item else f"https://github.com/{tool_q}"
        print(f"1. 로컬 클론: git clone {gh_url}")
        print(f"2. 저장소 공식 README 분석 후 requirements.txt 확인")
        print(f"3. 프로젝트 연동: import 또는 subprocess CLI 래퍼 작성 권장")
        print("-" * 80)

    print()

if __name__ == "__main__":
    main()
