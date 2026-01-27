"""
storyboard_utils.py - 스토리보드 유틸리티 함수
파서 + 번역기 + AI 추천 로직
"""

import streamlit as st
from utils import get_gpt_response


# ============ 장면 파싱 함수들 ============

def parse_scenes_20_ab(gpt_response: str) -> list:
    """20+A/B 방식 GPT 응답 파싱"""
    scenes = []
    raw_scenes = gpt_response.split("|||")
    
    for scene_idx, raw_scene in enumerate(raw_scenes, 1):
        raw_scene = raw_scene.strip()
        if not raw_scene:
            continue
        
        # A/B 컷으로 분리
        if "@AB@" in raw_scene:
            parts = raw_scene.split("@AB@")
            korean_desc = parts[0].strip() if parts else "장면 설명"
            
            # A컷, B컷 파싱
            for cut_idx, cut_part in enumerate(parts[1:], 1):
                cut_type = "A" if cut_idx == 1 else "B"
                
                image_prompt = ""
                motion_prompt = ""
                
                if "###" in cut_part:
                    cut_parts = cut_part.split("###")
                    cut_desc = cut_parts[0].strip() if cut_parts else ""
                    remaining = cut_parts[1].strip() if len(cut_parts) > 1 else ""
                else:
                    remaining = cut_part
                    cut_desc = "와이드샷" if cut_type == "A" else "클로즈업"
                
                if "@@@" in remaining:
                    motion_parts = remaining.split("@@@")
                    image_prompt = motion_parts[0].strip()
                    motion_prompt = motion_parts[1].strip() if len(motion_parts) > 1 else ""
                else:
                    image_prompt = remaining
                    motion_prompt = ""
                
                if not motion_prompt:
                    motion_prompt = "Slow cinematic movement" if cut_type == "A" else "Intimate close-up focus"
                
                scenes.append({
                    "scene_number": scene_idx,
                    "cut_type": cut_type,
                    "korean_desc": f"{korean_desc} [{cut_type}컷: {cut_desc}]",
                    "image_prompt": image_prompt,
                    "motion_prompt": motion_prompt
                })
        else:
            # @AB@ 없으면 일반 파싱
            korean_desc = "장면 설명"
            image_prompt = ""
            motion_prompt = ""
            
            if "###" in raw_scene:
                parts = raw_scene.split("###")
                korean_desc = parts[0].strip()
                remaining = parts[1].strip() if len(parts) > 1 else ""
            else:
                remaining = raw_scene
            
            if "@@@" in remaining:
                parts = remaining.split("@@@")
                image_prompt = parts[0].strip()
                motion_prompt = parts[1].strip() if len(parts) > 1 else ""
            else:
                image_prompt = remaining
            
            if not motion_prompt:
                motion_prompt = "Cinematic camera movement"
            
            scenes.append({
                "scene_number": scene_idx,
                "cut_type": "Single",
                "korean_desc": korean_desc,
                "image_prompt": image_prompt,
                "motion_prompt": motion_prompt
            })
    
    return scenes


def parse_scenes_40_independent(gpt_response: str) -> list:
    """40개 독립 장면 방식 GPT 응답 파싱"""
    scenes = []
    raw_scenes = gpt_response.split("|||")
    
    for scene_idx, raw_scene in enumerate(raw_scenes, 1):
        raw_scene = raw_scene.strip()
        if not raw_scene:
            continue
        
        korean_desc = ""
        image_prompt = ""
        motion_prompt = ""
        
        if "###" in raw_scene:
            parts = raw_scene.split("###")
            korean_desc = parts[0].strip()
            remaining = parts[1].strip() if len(parts) > 1 else ""
        else:
            remaining = raw_scene
            korean_desc = f"장면 {scene_idx}"
        
        if "@@@" in remaining:
            parts = remaining.split("@@@")
            image_prompt = parts[0].strip()
            motion_prompt = parts[1].strip() if len(parts) > 1 else ""
        else:
            image_prompt = remaining
            motion_prompt = ""
        
        if not motion_prompt:
            motion_prompt = "Cinematic slow motion, atmospheric lighting"
        
        scenes.append({
            "scene_number": scene_idx,
            "cut_type": "Independent",
            "korean_desc": korean_desc,
            "image_prompt": image_prompt,
            "motion_prompt": motion_prompt
        })
    
    return scenes


# ============ 장면 수정 상태 관리 ============

def initialize_scene_overrides():
    """장면 수정 상태 초기화"""
    if "scene_overrides" not in st.session_state:
        st.session_state["scene_overrides"] = {}


def get_scene_override(scene_key: str) -> str:
    """특정 장면의 사용자 수정 내용 가져오기"""
    return st.session_state.get("scene_overrides", {}).get(scene_key, "")


def set_scene_override(scene_key: str, override_text: str):
    """특정 장면의 사용자 수정 내용 저장"""
    if "scene_overrides" not in st.session_state:
        st.session_state["scene_overrides"] = {}
    
    if override_text.strip():
        st.session_state["scene_overrides"][scene_key] = override_text.strip()
    elif scene_key in st.session_state["scene_overrides"]:
        del st.session_state["scene_overrides"][scene_key]


# ============ 한영 번역 함수들 ============

def translate_korean_to_prompt(client, korean_text: str, visual_anchor: str) -> str:
    """한글 설명을 영어 Midjourney 프롬프트로 변환합니다."""
    
    system_prompt = """당신은 한글 장면 설명을 고품질 영어 Midjourney 프롬프트로 변환하는 전문가입니다.

## 변환 규칙:

1. **Visual Literalism (시각적 직유)**
   - 추상적 표현을 구체적 물리적 실체로 변환
   - 예: "희망" → "golden sunlight breaking through clouds"
   - 예: "슬픔" → "tears streaming down cheeks, downcast eyes"

2. **필수 포함 요소:**
   - Subject (주체): 구체적 외형, 자세, 표정
   - Environment (환경): 장소, 시간, 날씨
   - Lighting (조명): 빛의 원천과 방향
   - Composition (구도): 카메라 각도

3. **금지 사항:**
   - 추상적 단어: "representing", "symbolizing", "concept of"
   - 스타일 키워드 포함 금지 (시스템이 자동 추가)

4. **문장 구조:**
   - 구체적 명사로 시작
   - 물리적 묘사만 사용
   - 영어로만 출력

## 출력 형식:
영어 프롬프트만 출력하고, 추가 설명이나 주석은 절대 포함하지 마세요."""

    user_prompt = f"""다음 한글 장면 설명을 영어 Midjourney 프롬프트로 변환해주세요.

## Visual Anchor (반드시 프롬프트 앞에 포함)
{visual_anchor}

## 한글 장면 설명
{korean_text}

## 변환 예시:
한글: "여자가 비 오는 거리에서 슬프게 서있다"
영어: "{visual_anchor}, standing in heavy rain on dark city street, tears mixing with raindrops on cheeks, hands hanging loosely at sides, wet pavement reflecting neon lights"

지금 바로 위 한글 설명을 영어 프롬프트로 변환해주세요. 영어 프롬프트만 출력하세요."""

    try:
        result = get_gpt_response(client, system_prompt, user_prompt)
        return result.strip()
    except Exception as e:
        return f"변환 실패: {str(e)}"


def translate_english_to_korean(client, english_text: str) -> str:
    """영어 프롬프트를 한글 장면 설명으로 번역합니다."""
    
    system_prompt = """당신은 영어 Midjourney 프롬프트를 자연스러운 한글 장면 설명으로 번역하는 전문가입니다.

## 변환 규칙:

1. **기술적인 프롬프트 용어를 자연스러운 한글 문장으로**
   - "full body shot" → "전신이 보이는"
   - "close-up" → "클로즈업으로"
   - "dramatic lighting" → "극적인 조명 아래"

2. **Visual Anchor 부분은 간단히**
   - "Young woman with silver hair..." → "주인공이" 또는 캐릭터 특징 간단히

3. **카메라/기술 용어는 생략하고 장면의 핵심만**
   - "bokeh background", "4k", "cinematic" 같은 기술 용어 제외
   - 장면의 내용과 분위기에 집중

4. **2-3문장의 자연스러운 한글 설명**
   - 읽기 쉽고 이해하기 쉬운 문장
   - 시각적으로 상상 가능한 묘사

## 출력 형식:
한글 설명만 출력하고, 추가 설명이나 주석은 절대 포함하지 마세요."""

    user_prompt = f"""다음 영어 Midjourney 프롬프트를 자연스러운 한글 장면 설명으로 번역해주세요.

영어 프롬프트:
{english_text}

한글 설명만 출력하세요. 기술 용어는 제외하고 장면의 핵심만 2-3문장으로 설명하세요."""

    try:
        result = get_gpt_response(client, system_prompt, user_prompt)
        return result.strip()
    except Exception as e:
        return f"번역 실패: {str(e)}"


# ============ ⭐ AI 기반 Visual Anchor 추천 (신규) ============

def suggest_visual_anchor(client, lyrics: str, genre: str = "", vibe: str = "") -> str:
    """가사를 분석하여 어울리는 주인공 외형을 AI가 제안합니다."""
    
    system_prompt = """당신은 가사를 분석하여 뮤직비디오의 주인공 외형을 제안하는 전문가입니다.

## 임무
가사의 시대적 배경, 문화적 맥락, 감정 톤을 분석하여 **이 노래에 가장 어울리는 주인공의 구체적 외형**을 제안하세요.

## 원칙
1. **맥락 존중**: 가사가 고대 중국이면 한복/한푸, 인도면 사리, 중세 유럽이면 갑옷 등
2. **시대 정합성**: 현대곡이 아닌 이상 가죽 재킷 같은 현대 의상은 절대 제안하지 말 것
3. **유연성**: 성별/연령은 가사의 화자에 맞출 것 (반드시 젊은 여성일 필요 없음)
4. **구체성**: 헤어스타일, 의상, 액세서리, 표정까지 상세히

## 출력 형식
**반드시 영어로만 출력**하고, 100단어 이내로 간결하게.

예시:
- 발라드 + 현대: "Young woman with flowing black hair, wearing elegant white dress, delicate silver necklace, melancholic expression"
- 트로트 + 전통: "Middle-aged man wearing traditional Korean hanbok, dignified posture, warm smile, carrying wooden cane"
- 힙합 + 도시: "Young man with dreadlocks, oversized streetwear hoodie, gold chains, confident stance"
- 역사물: "Ancient Chinese scholar in silk robes, long beard, holding bamboo scroll, wise contemplative expression"

**중요**: 주인공이 꼭 노래의 화자일 필요는 없습니다. 때로는 관찰자나 배경 인물로 존재할 수도 있습니다."""

    user_prompt = f"""다음 가사를 분석하여 어울리는 주인공 외형을 제안해주세요.

## 가사
{lyrics[:1000]}

## 장르
{genre if genre else '미지정'}

## 분위기
{vibe if vibe else '미지정'}

지금 바로 영어로 주인공 외형을 제안하세요 (100단어 이내)."""

    try:
        result = get_gpt_response(client, system_prompt, user_prompt)
        return result.strip()
    except Exception as e:
        return ""
