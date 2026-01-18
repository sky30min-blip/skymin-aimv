"""
tabs/character.py - 캐릭터 생성 탭 (Tab 2)
마스터 투샷 전략 적용 - 두 명 이상의 주인공도 지원
"""

import streamlit as st
from utils import get_gpt_response


# 화풍 리스트 정의
ART_STYLE_LIST = [
    "선택해주세요",
    "지브리 스타일 (Studio Ghibli)",
    "일본 애니메이션 (Japanese Anime)",
    "픽사/디즈니 3D (Pixar/Disney 3D)",
    "실사 (Photorealistic)",
    "사이버펑크 일러스트 (Cyberpunk Illustration)",
    "한국 웹툰 스타일 (Korean Webtoon)",
    "수채화 일러스트 (Watercolor)",
    "다크 판타지 (Dark Fantasy)",
    "레트로 90s 애니메이션 (Retro 90s Anime)",
    "직접 입력"
]


SYSTEM_ROLE = """당신은 Midjourney 프롬프트 전문가이자 뮤직비디오 비주얼 디렉터입니다.

## 당신의 핵심 임무
캐릭터 일관성 유지(--cref)를 위한 완벽한 **'마스터 레퍼런스 이미지(Master Reference Image)'**용 프롬프트를 작성합니다.

## 중요한 전략: 투샷(Two-shot) 마스터 이미지
뮤직비디오에 두 명 이상의 캐릭터가 등장한다면, 각각 따로 만드는 것보다 **두 캐릭터가 함께 있는 '가족사진' 스타일의 마스터 이미지**를 만드는 것이 훨씬 효과적입니다.
이 하나의 마스터 이미지 URL로 영상 전체에서 두 캐릭터의 일관성을 유지할 수 있습니다.

## 구도 결정 규칙 (매우 중요!)

### 두 명 이상의 대상이 묘사된 경우:
- **Two-shot composition** 또는 **Medium shot** 사용
- 두 대상이 **모두 화면에 명확하게** 보이는 구도
- 둘의 관계성이 느껴지는 자연스러운 포즈 (나란히 서기, 함께 앉기, 눈 맞춤 등)
- Full body 또는 3/4 shot으로 두 캐릭터 모두 잘 보이게

### 한 명만 묘사된 경우:
- **Portrait shot** 또는 **Medium close-up**
- 얼굴과 상반신이 명확하게 보이는 구도
- 캐릭터의 특징이 돋보이는 앵글

## 프롬프트 작성 규칙

1. **구도(Composition)**: 위 규칙에 따라 적절한 샷 타입 선택
2. **조명(Lighting)**: 캐릭터가 잘 보이는 소프트 라이팅, 얼굴에 그림자가 지지 않게
3. **배경(Background)**: 캐릭터가 돋보이도록 **심플하고 깔끔하게** (simple background, clean background, minimal background)
4. **표정/포즈**: 캐릭터의 성격이 드러나는 자연스러운 표정과 포즈
5. **디테일**: 의상, 액세서리, 특징적 요소를 구체적으로 묘사

## 출력 형식 (반드시 준수!)

/imagine prompt: [상세한 캐릭터 묘사], [구도/샷 타입], [아트 스타일], [조명], [배경], high quality, detailed --ar 16:9 --v 6.1

## 주의사항
- 프롬프트는 **영어**로 작성
- 설명은 **한국어**로 작성하여 사용자가 이해하기 쉽게
- --cref 파라미터는 작성하지 말 것 (사용자가 나중에 추가함)
- 반드시 --ar 16:9 --v 6.1로 끝낼 것"""


def render(client):
    """
    캐릭터 생성 탭을 렌더링합니다.
    
    Args:
        client: OpenAI 클라이언트 인스턴스
    """
    st.header("🎨 Step 2: 캐릭터 마스터 이미지 생성")
    st.markdown("""
    Midjourney로 **캐릭터 마스터 이미지**를 만들기 위한 프롬프트를 생성합니다.
    
    > 🎬 *"이 마스터 이미지 하나로 영상 전체의 캐릭터 일관성을 유지합니다"*
    """)
    
    # 핵심 팁 안내 박스
    st.info("""
    💡 **핵심 팁: 투샷(Two-shot) 마스터 이미지 전략**
    
    뮤직비디오에 **두 명(예: 소녀+강아지, 커플, 친구들)**이 계속 나온다면,
    여기서 **두 명이 함께 있는 '가족사진'**을 만드세요.
    
    그 **URL 하나**로 영상 전체에서 두 캐릭터의 일관성을 유지할 수 있습니다!
    """)
    
    st.divider()
    
    # 입력 영역
    st.subheader("🎭 캐릭터 정보 입력")
    
    # 주인공 주제
    main_subject = st.text_input(
        "🌟 주인공 주제",
        placeholder="예: 사이버펑크 소녀와 그녀의 로봇 강아지 (두 명일 경우 함께 적으세요)",
        help="한 명이든 두 명이든, 뮤직비디오의 주인공을 모두 적어주세요"
    )
    
    # 주제 예시 제공
    with st.expander("💡 주제 예시 보기"):
        st.markdown("""
        **1인 주인공:**
        - 은발의 마법사 소녀
        - 빈티지 카페의 바리스타 청년
        - 우주비행사 고양이
        
        **2인 주인공 (투샷):**
        - 사이버펑크 소녀와 그녀의 로봇 강아지
        - 어린 왕자와 여우
        - 할머니와 손녀
        - 록밴드의 보컬과 기타리스트
        - 형사와 그의 파트너 경찰견
        """)
    
    # 세부 특징
    details = st.text_area(
        "📝 세부 특징",
        placeholder="예: 소녀는 은발 단발에 LED 고글을 썼고, 검은 가죽 재킷을 입었다. 강아지는 크롬 메탈 재질에 파란 눈을 가졌고, 크기는 중형견 정도다. 둘이 나란히 서서 정면을 바라보고 있다.",
        height=150,
        help="캐릭터의 외모, 의상, 포즈, 관계성 등을 구체적으로 적어주세요"
    )
    
    # 세부 특징 가이드
    with st.expander("✍️ 세부 특징 작성 가이드"):
        st.markdown("""
        **꼭 포함하면 좋은 정보:**
        
        | 항목 | 예시 |
        |------|------|
        | 헤어 | 은발 단발, 파란 긴 머리, 갈색 곱슬머리 |
        | 눈 | 보라색 눈, 큰 눈동자, 날카로운 눈매 |
        | 의상 | 검은 가죽 재킷, 흰 원피스, 교복 |
        | 액세서리 | LED 고글, 별 모양 귀걸이, 목걸이 |
        | 표정/포즈 | 미소 짓는, 정면을 바라보는, 손 흔드는 |
        
        **두 캐릭터일 경우 추가:**
        - 둘의 위치 관계 (나란히, 마주보며, 한 명이 앞에)
        - 상호작용 (손잡고, 눈 맞추며, 기대어)
        - 크기 비교 (강아지는 중형견 크기)
        """)
    
    # 화풍 선택
    st.subheader("🖼️ 아트 스타일")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        art_style = st.selectbox(
            "화풍 선택",
            options=ART_STYLE_LIST,
            help="원하는 아트 스타일을 선택하세요"
        )
    
    with col2:
        # '직접 입력' 선택 시 추가 입력칸 표시
        custom_style = ""
        if art_style == "직접 입력":
            custom_style = st.text_input(
                "✍️ 화풍 직접 입력",
                placeholder="예: 뭉크 스타일 + 네온 컬러",
                help="원하는 화풍을 자유롭게 입력하세요"
            )
        else:
            # 선택된 스타일 미리보기
            style_descriptions = {
                "지브리 스타일 (Studio Ghibli)": "따뜻하고 섬세한 수채화 느낌, 자연과 조화로운 색감",
                "일본 애니메이션 (Japanese Anime)": "선명한 선, 큰 눈, 다양한 표정 연출에 적합",
                "픽사/디즈니 3D (Pixar/Disney 3D)": "귀엽고 생동감 있는 3D 렌더링 스타일",
                "실사 (Photorealistic)": "사진처럼 사실적인 묘사",
                "사이버펑크 일러스트 (Cyberpunk Illustration)": "네온 컬러, 미래적 분위기, SF 감성",
            }
            if art_style in style_descriptions:
                st.caption(f"ℹ️ {style_descriptions[art_style]}")
    
    # 추가 옵션
    with st.expander("⚙️ 추가 옵션"):
        col3, col4 = st.columns(2)
        
        with col3:
            mood_lighting = st.selectbox(
                "조명 분위기",
                options=[
                    "자동 (AI 추천)",
                    "밝고 화사한 (Bright)",
                    "따뜻한 골든아워 (Golden hour)",
                    "차가운 블루톤 (Cool blue)",
                    "드라마틱 명암 (Dramatic)",
                    "네온 조명 (Neon lights)",
                    "부드러운 스튜디오 (Soft studio)"
                ]
            )
        
        with col4:
            background_pref = st.selectbox(
                "배경 스타일",
                options=[
                    "심플 단색 (Simple solid)",
                    "그라데이션 (Gradient)",
                    "살짝 흐린 배경 (Soft blur)",
                    "미니멀 공간 (Minimal space)",
                    "추상적 패턴 (Abstract)"
                ]
            )
    
    st.divider()
    
    # 생성 버튼
    if st.button("🎨 마스터 이미지 프롬프트 생성", type="primary", use_container_width=True):
        # 유효성 검사
        if not main_subject:
            st.error("주인공 주제를 입력해주세요.")
            return
        
        if not details:
            st.error("세부 특징을 입력해주세요.")
            return
        
        if art_style == "선택해주세요":
            st.error("화풍을 선택해주세요.")
            return
        
        if art_style == "직접 입력" and not custom_style:
            st.error("화풍을 직접 입력해주세요.")
            return
        
        if client is None:
            st.error("API 키가 설정되지 않았습니다. secrets.toml 파일을 확인해주세요.")
            return
        
        # 최종 스타일 결정
        final_style = custom_style if art_style == "직접 입력" else art_style
        
        # 프롬프트 구성
        user_prompt = f"""다음 정보를 바탕으로 Midjourney 마스터 이미지 프롬프트를 작성해주세요.

## 캐릭터 정보
- 주인공: {main_subject}
- 세부 특징: {details}

## 스타일 정보
- 화풍: {final_style}
- 조명: {mood_lighting}
- 배경: {background_pref}

## 중요 지시사항
1. 위 정보를 분석하여 **한 명인지 두 명 이상인지** 파악하세요.
2. 두 명 이상이면 반드시 **Two-shot composition**으로, 둘 다 화면에 잘 보이게 구성하세요.
3. 한 명이면 **Portrait 또는 Medium shot**으로 집중하세요.
4. 배경은 심플하게 처리하여 캐릭터가 돋보이게 하세요.
5. --ar 16:9 --v 6.1 파라미터를 반드시 포함하세요.

프롬프트와 함께 한국어로 간단한 설명도 추가해주세요."""

        with st.spinner("🎨 마스터 이미지 프롬프트를 생성하고 있습니다..."):
            try:
                result = get_gpt_response(client, SYSTEM_ROLE, user_prompt)
                
                # 세션 스테이트에 저장
                st.session_state["character_prompt"] = result
                st.session_state["character_style"] = final_style
                st.session_state["character_subject"] = main_subject
                
                st.success("🎉 마스터 이미지 프롬프트가 생성되었습니다!")
                
            except Exception as e:
                st.error(str(e))
                return
    
    # 결과 표시
    st.divider()
    
    if "character_prompt" in st.session_state and st.session_state["character_prompt"]:
        st.subheader("🖼️ 생성된 Midjourney 프롬프트")
        
        # 메타 정보 표시
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            st.caption(f"🌟 주인공: {st.session_state.get('character_subject', '-')}")
        with col_meta2:
            st.caption(f"🎨 화풍: {st.session_state.get('character_style', '-')}")
        
        # 전체 결과 표시 (설명 포함)
        st.markdown(st.session_state["character_prompt"])
        
        # 프롬프트만 추출하여 코드 블록으로 표시
        st.subheader("📋 복사용 프롬프트")
        
        # /imagine prompt: 부분 추출
        full_result = st.session_state["character_prompt"]
        if "/imagine prompt:" in full_result:
            # /imagine prompt: 이후 부분 추출
            prompt_start = full_result.find("/imagine prompt:")
            prompt_text = full_result[prompt_start:].split("\n\n")[0].strip()
            st.code(prompt_text, language=None)
        else:
            st.code(full_result, language=None)
        
        # 다음 단계 안내
        st.warning("""
        📌 **다음 단계 (중요!):**
        
        1. 위 프롬프트를 **Midjourney Discord**에서 실행하세요
        2. 생성된 이미지 중 마음에 드는 것을 선택 **(Upscale: U1~U4)**
        3. Upscale된 이미지를 클릭 → **"Open in Browser"** → **URL 복사**
        4. 아래에 URL을 붙여넣고 저장하세요
        """)
        
        # 마스터 이미지 URL 입력
        st.divider()
        st.subheader("🔗 마스터 이미지 URL 등록")
        
        st.markdown("""
        Midjourney에서 생성한 마스터 이미지의 URL을 입력하세요.
        이 URL이 **Tab 3 (스토리보드)**에서 `--cref` 파라미터로 사용됩니다.
        """)
        
        master_url = st.text_input(
            "마스터 이미지 URL",
            placeholder="https://cdn.midjourney.com/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/0_0.png",
            value=st.session_state.get("master_image_url", ""),
            help="Midjourney에서 Upscale 후 'Open in Browser'로 얻은 URL"
        )
        
        col_url1, col_url2 = st.columns(2)
        
        with col_url1:
            if st.button("💾 URL 저장", type="primary", use_container_width=True):
                if master_url:
                    if "midjourney" in master_url.lower() or "cdn.discordapp" in master_url.lower() or master_url.startswith("http"):
                        st.session_state["master_image_url"] = master_url
                        st.success("✅ 마스터 이미지 URL이 저장되었습니다!")
                        st.info("👉 이제 **Tab 3 (스토리보드)**로 이동하세요!")
                    else:
                        st.warning("유효한 이미지 URL인지 확인해주세요.")
                else:
                    st.error("URL을 입력해주세요.")
        
        with col_url2:
            if st.session_state.get("master_image_url"):
                if st.button("🗑️ URL 초기화", use_container_width=True):
                    st.session_state["master_image_url"] = ""
                    st.rerun()
        
        # 저장된 URL 표시
        if st.session_state.get("master_image_url"):
            st.success(f"✅ 저장된 URL: `{st.session_state['master_image_url'][:50]}...`")
    
    # 아직 프롬프트가 없을 때 가이드 표시
    else:
        st.markdown("---")
        st.markdown("""
        ### 🚀 시작하기
        
        1. **주인공 주제**에 캐릭터를 입력하세요 (한 명 또는 두 명)
        2. **세부 특징**에 외모, 의상, 포즈 등을 자세히 적어주세요
        3. **화풍**을 선택하고 생성 버튼을 클릭하세요
        
        > 💡 두 캐릭터가 함께 나오는 뮤직비디오라면, 꼭 둘을 함께 적어주세요!
        """)