"""
tabs/character.py - 캐릭터 생성 탭 (Tab 2) - 모바일 최적화 버전
한글 UI 매핑 + 마스터 투샷 전략
"""

import streamlit as st
from utils import get_gpt_response


# ============ 한글-영어 매핑 딕셔너리 ============

ART_STYLE_MAP = {
    "선택해주세요": "",
    "지브리 스타일 (따뜻하고 섬세한)": "Studio Ghibli style, warm colors, soft lighting, hand-painted aesthetic",
    "일본 애니메이션 (선명하고 역동적)": "Japanese anime style, vibrant colors, dynamic, cel-shaded, expressive",
    "픽사/디즈니 3D (귀엽고 생동감)": "Pixar Disney 3D animation style, expressive, detailed, vibrant",
    "실사 영화 (사실적이고 시네마틱)": "Photorealistic, cinematic lighting, high detail, movie still",
    "사이버펑크 (네온, 미래적)": "Cyberpunk illustration, neon lights, futuristic, high contrast, sci-fi",
    "한국 웹툰 (깔끔하고 감성적)": "Korean webtoon style, clean lines, emotional, soft shading, manhwa",
    "수채화 (부드럽고 몽환적)": "Watercolor illustration, soft edges, dreamy atmosphere, artistic",
    "다크 판타지 (어둡고 신비로운)": "Dark fantasy style, dramatic lighting, mysterious, gothic",
    "90년대 레트로 애니 (복고풍 감성)": "Retro 90s anime style, nostalgic, cel shading, vibrant colors",
    "직접 입력": "custom"
}

LIGHTING_MAP = {
    "자동 (AI 추천)": "natural lighting, well-lit",
    "밝고 화사한": "bright soft lighting, cheerful atmosphere",
    "따뜻한 골든아워": "golden hour lighting, warm tones, sunset glow",
    "차가운 블루톤": "cool blue lighting, cold atmosphere, moonlight",
    "드라마틱 명암": "dramatic lighting, high contrast, chiaroscuro",
    "네온 조명": "neon lights, cyberpunk glow, colorful lighting",
    "부드러운 스튜디오": "soft studio lighting, even illumination, professional"
}

BACKGROUND_MAP = {
    "심플 단색": "simple solid color background, clean",
    "그라데이션": "gradient background, smooth color transition",
    "살짝 흐린 배경": "soft blurred background, bokeh effect",
    "미니멀 공간": "minimal space, simple environment",
    "추상적 패턴": "abstract pattern background, artistic"
}

# 한글 옵션 리스트 (UI 표시용)
ART_STYLE_OPTIONS = list(ART_STYLE_MAP.keys())
LIGHTING_OPTIONS = list(LIGHTING_MAP.keys())
BACKGROUND_OPTIONS = list(BACKGROUND_MAP.keys())


SYSTEM_ROLE = """당신은 Midjourney 프롬프트 전문가이자 뮤직비디오 비주얼 디렉터입니다.

## 당신의 핵심 임무
캐릭터 일관성 유지(--cref)를 위한 완벽한 **'마스터 레퍼런스 이미지'**용 프롬프트를 작성합니다.

## 중요한 전략: 투샷(Two-shot) 마스터 이미지
뮤직비디오에 두 명 이상의 캐릭터가 등장한다면, **두 캐릭터가 함께 있는 마스터 이미지**를 만드는 것이 효과적입니다.

## 구도 결정 규칙

### 두 명 이상의 대상:
- **Two-shot composition** 사용
- 두 대상이 모두 화면에 명확하게 보이는 구도
- 관계성이 느껴지는 자연스러운 포즈

### 한 명만 묘사:
- **Portrait shot** 또는 **Medium close-up**
- 얼굴과 상반신이 명확하게 보이는 구도

## 프롬프트 작성 규칙
1. 배경은 **심플하고 깔끔하게**
2. 캐릭터의 특징이 돋보이도록
3. 조명은 캐릭터가 잘 보이도록

## 출력 형식 (반드시 준수!)

/imagine prompt: [캐릭터 묘사], [구도], [아트 스타일], [조명], [배경], high quality, detailed --ar 16:9 --v 6.1

## 주의사항
- 프롬프트는 **영어**로 작성
- 설명은 **한국어**로 작성
- --cref 파라미터는 작성하지 말 것
- 반드시 --ar 16:9 --v 6.1로 끝낼 것"""


def render(client):
    """캐릭터 생성 탭을 렌더링합니다."""
    
    st.header("🎨 Step 2: 캐릭터 마스터 이미지 생성")
    st.markdown("""
    Midjourney로 **캐릭터 마스터 이미지**를 만들기 위한 프롬프트를 생성합니다.
    
    > 🎬 *"이 마스터 이미지 하나로 영상 전체의 캐릭터 일관성을 유지합니다"*
    """)
    
    st.info("""
    💡 **핵심 팁: 투샷(Two-shot) 마스터 이미지 전략**
    
    뮤직비디오에 **두 명(예: 소녀+강아지, 커플)**이 계속 나온다면,
    여기서 **두 명이 함께 있는 '가족사진'**을 만드세요!
    """)
    
    st.divider()
    
    # ============ 캐릭터 정보 입력 (모바일 최적화) ============
    st.subheader("🎭 캐릭터 정보 입력")
    
    main_subject = st.text_input(
        "🌟 주인공 주제",
        placeholder="예: 사이버펑크 소녀와 그녀의 로봇 강아지",
        help="한 명이든 두 명이든, 뮤직비디오의 주인공을 모두 적어주세요"
    )
    
    with st.expander("💡 주제 예시 보기"):
        st.markdown("""
        **1인 주인공:** 은발의 마법사 소녀 / 빈티지 카페의 바리스타 청년
        
        **2인 주인공 (투샷):** 사이버펑크 소녀와 로봇 강아지 / 어린 왕자와 여우
        """)
    
    details = st.text_area(
        "📝 세부 특징",
        placeholder="예: 소녀는 은발 단발에 LED 고글을 썼고, 검은 가죽 재킷을 입었다...",
        height=120,
        help="캐릭터의 외모, 의상, 포즈, 관계성 등을 구체적으로 적어주세요"
    )
    
    with st.expander("✍️ 세부 특징 작성 가이드"):
        st.markdown("""
        **꼭 포함하면 좋은 정보:**
        - 헤어: 은발 단발, 파란 긴 머리
        - 눈: 보라색 눈, 큰 눈동자
        - 의상: 검은 가죽 재킷, 흰 원피스
        - 액세서리: LED 고글, 별 모양 귀걸이
        - 표정/포즈: 미소 짓는, 정면을 바라보는
        """)
    
    st.divider()
    
    # ============ 아트 스타일 (한글 매핑) ============
    st.subheader("🖼️ 아트 스타일")
    
    art_style_kr = st.selectbox(
        "화풍 선택",
        options=ART_STYLE_OPTIONS,
        help="원하는 아트 스타일을 선택하세요"
    )
    
    custom_style = ""
    if art_style_kr == "직접 입력":
        custom_style = st.text_input(
            "✍️ 화풍 직접 입력 (영어 권장)",
            placeholder="예: Moebius comic style, detailed linework",
            help="Midjourney에서 사용할 영어 스타일을 입력하세요"
        )
    else:
        # 선택된 스타일의 영어값 미리보기
        if art_style_kr != "선택해주세요":
            st.caption(f"🔤 **영어값:** `{ART_STYLE_MAP[art_style_kr][:40]}...`")
    
    # ============ 추가 옵션 (한글 매핑) ============
    with st.expander("⚙️ 추가 옵션"):
        lighting_kr = st.selectbox(
            "조명 분위기",
            options=LIGHTING_OPTIONS
        )
        st.caption(f"🔤 `{LIGHTING_MAP[lighting_kr][:30]}...`")
        
        background_kr = st.selectbox(
            "배경 스타일",
            options=BACKGROUND_OPTIONS
        )
        st.caption(f"🔤 `{BACKGROUND_MAP[background_kr][:30]}...`")
    
    st.divider()
    
    # ============ 생성 버튼 ============
    if st.button("🎨 마스터 이미지 프롬프트 생성", type="primary", use_container_width=True):
        if not main_subject:
            st.error("주인공 주제를 입력해주세요.")
            return
        if not details:
            st.error("세부 특징을 입력해주세요.")
            return
        if art_style_kr == "선택해주세요":
            st.error("화풍을 선택해주세요.")
            return
        if art_style_kr == "직접 입력" and not custom_style:
            st.error("화풍을 직접 입력해주세요.")
            return
        if client is None:
            st.error("API 키가 설정되지 않았습니다.")
            return
        
        # ============ 영어값 변환 (핵심!) ============
        if art_style_kr == "직접 입력":
            art_style_en = custom_style
            art_style_display = custom_style
        else:
            art_style_en = ART_STYLE_MAP[art_style_kr]
            art_style_display = art_style_kr
        
        lighting_en = LIGHTING_MAP[lighting_kr]
        background_en = BACKGROUND_MAP[background_kr]
        
        user_prompt = f"""다음 정보를 바탕으로 Midjourney 마스터 이미지 프롬프트를 작성해주세요.

## 캐릭터 정보
- 주인공: {main_subject}
- 세부 특징: {details}

## 스타일 정보
- 화풍: {art_style_en}
- 조명: {lighting_en}
- 배경: {background_en}

## 중요 지시사항
1. 위 정보를 분석하여 **한 명인지 두 명 이상인지** 파악하세요.
2. 두 명 이상이면 **Two-shot composition**으로 구성하세요.
3. 배경은 심플하게 처리하여 캐릭터가 돋보이게 하세요.
4. --ar 16:9 --v 6.1 파라미터를 반드시 포함하세요.

프롬프트와 함께 한국어로 간단한 설명도 추가해주세요."""

        with st.spinner("🎨 마스터 이미지 프롬프트를 생성하고 있습니다..."):
            try:
                result = get_gpt_response(client, SYSTEM_ROLE, user_prompt)
                
                # 세션 스테이트에 저장 (한글값과 영어값 모두!)
                st.session_state["character_prompt"] = result
                st.session_state["character_style"] = art_style_en  # 영어값 (스토리보드에서 사용)
                st.session_state["character_style_kr"] = art_style_display  # 한글값 (UI 표시용)
                st.session_state["character_subject"] = main_subject
                
                st.success("🎉 마스터 이미지 프롬프트가 생성되었습니다!")
                
            except Exception as e:
                st.error(str(e))
                return
    
    # ============ 결과 표시 ============
    st.divider()
    
    if "character_prompt" in st.session_state and st.session_state["character_prompt"]:
        st.subheader("🖼️ 생성된 Midjourney 프롬프트")
        
        st.caption(f"🌟 주인공: {st.session_state.get('character_subject', '-')}")
        st.caption(f"🎨 화풍: {st.session_state.get('character_style_kr', st.session_state.get('character_style', '-'))}")
        
        st.markdown(st.session_state["character_prompt"])
        
        # 프롬프트만 추출
        st.subheader("📋 복사용 프롬프트")
        
        full_result = st.session_state["character_prompt"]
        if "/imagine prompt:" in full_result:
            prompt_start = full_result.find("/imagine prompt:")
            prompt_text = full_result[prompt_start:].split("\n\n")[0].strip()
            st.code(prompt_text, language=None)
        else:
            st.code(full_result, language=None)
        
        st.warning("""
        📌 **다음 단계:**
        1. 위 프롬프트를 **Midjourney Discord**에서 실행
        2. Upscale된 이미지 클릭 → **"Open in Browser"** → **URL 복사**
        3. 아래에 URL을 붙여넣고 저장
        """)
        
        # ============ 마스터 이미지 URL 입력 ============
        st.divider()
        st.subheader("🔗 마스터 이미지 URL 등록")
        
        st.markdown("이 URL이 **Tab 3 (스토리보드)**에서 `--cref` 파라미터로 사용됩니다.")
        
        master_url = st.text_input(
            "마스터 이미지 URL",
            placeholder="https://cdn.midjourney.com/...",
            value=st.session_state.get("master_image_url", ""),
            help="Midjourney에서 Upscale 후 'Open in Browser'로 얻은 URL"
        )
        
        if st.button("💾 URL 저장", type="primary", use_container_width=True):
            if master_url:
                if master_url.startswith("http"):
                    st.session_state["master_image_url"] = master_url
                    st.success("✅ 마스터 이미지 URL이 저장되었습니다!")
                    st.info("👉 이제 **Tab 3 (스토리보드)**로 이동하세요!")
                else:
                    st.warning("유효한 URL인지 확인해주세요.")
            else:
                st.error("URL을 입력해주세요.")
        
        if st.session_state.get("master_image_url"):
            if st.button("🗑️ URL 초기화", use_container_width=True):
                st.session_state["master_image_url"] = ""
                st.rerun()
        
        if st.session_state.get("master_image_url"):
            st.success(f"✅ 저장된 URL: `{st.session_state['master_image_url'][:50]}...`")
    
    else:
        st.markdown("---")
        st.markdown("""
        ### 🚀 시작하기
        
        1. **주인공 주제**에 캐릭터를 입력하세요
        2. **세부 특징**에 외모, 의상, 포즈 등을 자세히 적어주세요
        3. **화풍**을 선택하고 생성 버튼을 클릭하세요
        """)
