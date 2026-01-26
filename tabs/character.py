"""
tabs/character.py - 캐릭터 생성 탭 (Tab 2) - Tab 3 스타일 완전 동기화
가사 기반 자동 추천 + 11종 프리미엄 스타일 + 이미지 미리보기 + 마스터 투샷 전략
"""

import streamlit as st
from utils import get_gpt_response
import re


# ============ Tab 3와 동기화된 프리미엄 스타일 가이드 (11종) ============

STYLE_GUIDE = {
    "AI 자동 추천": {
        "image_keywords": "",
        "description": "가사의 장르와 분위기를 분석하여 AI가 최적의 스타일을 선택합니다",
        "preview": "🤖",
        "preview_image": ""
    },
    
    "고퀄리티 일본 애니메이션 (Cinematic Japanese Anime)": {
        "image_keywords": "Modern high-end Japanese anime style, cinematic production value, sharp character lines, highly detailed background, atmospheric lighting effects, masterpiece anime still, professional color grading",
        "description": "Production I.G, WIT Studio 같은 고예산 애니메이션의 한 장면. 선명한 선과 완벽한 배경",
        "preview": "🎬",
        "preview_image": "https://cdn.midjourney.com/20533ac1-924a-4e01-966c-785eb60957b8/0_1.png"
    },
    
    "프리미엄 한국 웹툰 (Premium Korean Webtoon)": {
        "image_keywords": "Premium Korean webtoon style, sharp digital linework, vibrant gradient lighting, manhwa aesthetic, detailed background, modern webtoon masterpiece",
        "description": "나 혼자만 레벨업, 어느 날 공주가 되어버렸다 같은 세련된 최신 웹툰 스타일",
        "preview": "📱",
        "preview_image": "https://cdn.midjourney.com/ab3a0859-19ec-4eb9-8554-f04a9113db56/0_2.png"
    },
    
    "클래식 흑백 만화 (Classic Korean Manhwa)": {
        "image_keywords": "Classic Korean Manhwa style, detailed ink drawing, high contrast black and white with gray tones, traditional comic book hatching, 2D hand-drawn aesthetic",
        "description": "정통 흑백 만화 스타일. 세밀한 펜터치와 강렬한 명암 대비",
        "preview": "📖",
        "preview_image": "https://cdn.midjourney.com/007e0390-fcba-4175-a7db-758aeae4438b/0_1.png"
    },
    
    "교토 애니메이션 스타일 (Kyoto Animation)": {
        "image_keywords": "Kyoto Animation style, delicate linework, soft lighting, emotional and serene, transparent colors, high-detail eyes, beautiful light reflections, premium slice-of-life anime aesthetic",
        "description": "바이올렛 에버가든 같은 극강의 섬세함. 투명한 색채와 부드러운 감성",
        "preview": "🌸",
        "preview_image": "https://cdn.midjourney.com/76d004b6-a235-409f-b0dc-41d3c58c8f13/0_1.png"
    },
    
    "수채화 판타지 (Ethereal Watercolor)": {
        "image_keywords": "Dreamy watercolor illustration, soft pastels, fluid edges, emotional atmosphere, artistic brushstrokes, ethereal light, whimsical and poetic, high-end storybook aesthetic",
        "description": "몽환적인 수채화 느낌. 경계가 번지는 서정적 분위기, 발라드에 최적",
        "preview": "🎨",
        "preview_image": "https://cdn.midjourney.com/89ff3672-f48b-4465-a214-935a8fd19633/0_1.png"
    },
    
    "90년대 사이버펑크 (Classic Cyberpunk)": {
        "image_keywords": "1990s Japanese Cyberpunk anime style, grit and neon, high-tech noir, hand-drawn aesthetic, dramatic shadows, futuristic dystopian cityscape, cinematic lighting, detailed mechanical design",
        "description": "아키라, 공각기동대 같은 묵직하고 거친 느낌의 미래 도시",
        "preview": "🌃",
        "preview_image": "https://cdn.midjourney.com/4fb8a033-3db8-4e8a-8d08-f316471d69b8/0_3.png"
    },
    
    "럭셔리 시티팝 (80s City Pop)": {
        "image_keywords": "Retro Japanese City Pop aesthetic, art style by Hiroshi Nagai, flat saturated colors, sharp shadows, 1980s luxury anime style, vaporwave sunset, clean minimalist lines",
        "description": "80년대 일본 시티팝 앨범 자켓. 강렬한 원색과 미니멀한 선의 세련미",
        "preview": "🌆",
        "preview_image": "https://cdn.midjourney.com/f9a94aba-fc63-4352-a787-c82ae17bbdee/0_0.png"
    },
    
    "신카이 마코토 감성 (Makoto Shinkai)": {
        "image_keywords": "Makoto Shinkai animation style, vibrant lighting, breathtaking sky and clouds, high-detail cityscapes, emotional atmosphere, hyper-detailed lens flare, luminous colors, cinematic background",
        "description": "너의 이름은 처럼 빛의 산란과 구름, 압도적인 배경 퀄리티",
        "preview": "☀️",
        "preview_image": "https://cdn.midjourney.com/81db105a-9d37-401f-b056-3bf8e04f2daa/0_3.png"
    },
    
    "지브리 2.0 (Miyazaki Masterpiece)": {
        "image_keywords": "Studio Ghibli art style by Hayao Miyazaki, lush painterly background, hand-drawn aesthetic, high-quality cel animation, soft natural sunlight, nostalgic atmosphere, detailed watercolor texture",
        "description": "거장 미야자키 하야오의 원화 느낌. 수채화 배경과 따뜻한 햇살",
        "preview": "🌿",
        "preview_image": "https://cdn.midjourney.com/b8354c0a-dee9-4c5e-9013-00f3e8726dfa/0_2.png"
    },
    
    "90년대 한국 애니 (90s Korean Anime)": {
        "image_keywords": "1990s Korean anime style, VHS aesthetic, chromatic aberration, bold outlines, neon purple and pink lighting, cinematic lofi vibe, retro cel-shaded",
        "description": "90년대 한국 애니메이션 향수. VHS 질감과 전통 요소의 조화",
        "preview": "📼",
        "preview_image": "https://cdn.midjourney.com/d87c768f-65ab-4b5e-8f16-b3256a5627c9/0_1.png"
    },
    
    "90년대 레트로 일본 애니 (90s Retro Anime)": {
        "image_keywords": "Retro 90s anime style, nostalgic, cel shading, vibrant colors, City Pop aesthetic, Lo-fi vibe, purple and blue neon lighting, dreamy atmosphere, vintage aesthetic",
        "description": "향수를 자극하는 90년대 일본 애니 감성. 시티팝과 로파이의 만남",
        "preview": "🎵",
        "preview_image": "https://cdn.midjourney.com/a83587b7-49e2-4830-b20b-1c7d2834d535/0_0.png"
    }
}

# 스타일 옵션 리스트
STYLE_OPTIONS = list(STYLE_GUIDE.keys())


# ============ 추가 옵션 매핑 ============

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


# ============ 가사 분석 함수 (정규표현식 파싱) ============

def analyze_lyrics_for_character(client, lyrics: str) -> dict:
    """
    가사를 분석하여 캐릭터 주제와 세부 특징을 추출합니다.
    
    Args:
        client: OpenAI 클라이언트
        lyrics: 분석할 가사 텍스트
        
    Returns:
        dict: {"subject": str, "details": str} 형태의 딕셔너리
    """
    
    if not lyrics or not lyrics.strip():
        return {"subject": "", "details": ""}
    
    analysis_system_role = """당신은 가사를 분석하여 뮤직비디오의 주인공 캐릭터를 추출하는 전문가입니다.

## 당신의 임무
가사를 읽고 다음 정보를 추출하세요:
1. **주인공(Subject)**: 가사 속 화자나 등장인물의 핵심 정체성
2. **세부 특징(Details)**: 외모, 의상, 포즈, 분위기, 관계성 등

## 추출 규칙
- 가사에 직접 언급되지 않아도, 문맥상 추론 가능한 정보 포함
- 구체적이고 시각적인 묘사 우선
- 한 명 또는 두 명 이상일 경우 모두 명시
- 분위기와 장르를 반영한 캐릭터 설정

## ⚠️ 출력 형식 (절대 준수!) ⚠️
반드시 아래 형식으로만 출력하고, 서론이나 추가 설명은 절대 넣지 마세요!

Subject: (한 줄 요약)
Details: (구체적 묘사, 3-5문장)

예시:
Subject: 사이버펑크 소녀와 그녀의 로봇 강아지
Details: 소녀는 은발 단발에 LED 고글을 쓰고 있으며, 검은 가죽 재킷을 입었다. 네온 불빛이 반사되는 도시를 배경으로 로봇 강아지와 함께 서 있다. 강아지는 금속 재질이며 파란 LED 눈을 가지고 있다. 둘의 관계는 친밀하고 서로를 신뢰하는 모습이다."""

    analysis_prompt = f"""다음 가사를 분석하여 뮤직비디오에 등장할 주인공 캐릭터를 추출해주세요.

## 가사
{lyrics}

## 지시사항
- 가사의 분위기와 내용을 고려하여 시각적으로 매력적인 캐릭터 설정
- 한 명인지 두 명 이상인지 판단하여 명시
- 구체적이고 이미지가 떠오르는 묘사

⚠️ 중요: 서론 없이 바로 "Subject:"로 시작하세요!"""

    try:
        response = get_gpt_response(client, analysis_system_role, analysis_prompt)
        
        # 정규표현식으로 안전하게 파싱
        subject = ""
        details = ""
        
        subject_match = re.search(r'Subject:\s*(.+?)(?=Details:|$)', response, re.DOTALL | re.IGNORECASE)
        if subject_match:
            subject = subject_match.group(1).strip()
        
        details_match = re.search(r'Details:\s*(.+)', response, re.DOTALL | re.IGNORECASE)
        if details_match:
            details = details_match.group(1).strip()
        
        return {
            "subject": subject if subject else "",
            "details": details if details else ""
        }
        
    except Exception as e:
        print(f"가사 분석 오류: {str(e)}")
        return {"subject": "", "details": ""}


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
    
    # ============ 가사 기반 자동 추천 ============
    st.subheader("🎭 캐릭터 정보 입력")
    
    has_lyrics = "lyrics" in st.session_state and st.session_state["lyrics"]
    
    if has_lyrics:
        st.success("✅ Tab 1에서 생성한 가사가 감지되었습니다!")
        
        if st.button("✨ 가사로 캐릭터 자동 추천받기", use_container_width=True, type="primary"):
            if client is None:
                st.error("API 키가 설정되지 않았습니다.")
            else:
                with st.spinner("🤖 가사를 분석하여 캐릭터를 추천하고 있습니다..."):
                    lyrics_content = st.session_state["lyrics"]
                    analysis_result = analyze_lyrics_for_character(client, lyrics_content)
                    
                    if analysis_result["subject"] or analysis_result["details"]:
                        st.session_state["char_subject_input"] = analysis_result["subject"]
                        st.session_state["char_details_input"] = analysis_result["details"]
                        
                        st.success("✅ 가사 분석 완료! 아래 입력창이 자동으로 채워졌습니다.")
                        st.info("💡 마음에 들지 않으면 직접 수정하세요!")
                        st.rerun()
                    else:
                        st.warning("가사에서 캐릭터 정보를 추출하지 못했습니다. 직접 입력해주세요.")
        
        st.caption("💡 자동 추천 후에도 아래에서 자유롭게 수정할 수 있습니다.")
        st.divider()
    else:
        st.info("💡 Tab 1에서 가사를 먼저 생성하면, 여기서 캐릭터를 자동으로 추천받을 수 있습니다.")
        st.divider()
    
    # ============ 캐릭터 정보 입력 ============
    
    main_subject = st.text_input(
        "🌟 주인공 주제",
        placeholder="예: 사이버펑크 소녀와 그녀의 로봇 강아지",
        help="한 명이든 두 명이든, 뮤직비디오의 주인공을 모두 적어주세요",
        key="char_subject_input"
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
        help="캐릭터의 외모, 의상, 포즈, 관계성 등을 구체적으로 적어주세요",
        key="char_details_input"
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
    
    # ============ 프리미엄 스타일 선택 (이미지 미리보기) ============
    st.subheader("🎨 비주얼 스타일")
    
    selected_style = st.selectbox(
        "프리미엄 스타일 선택 (Tab 3와 동기화)",
        options=STYLE_OPTIONS,
        help="Tab 3 스토리보드와 동일한 11종 프리미엄 스타일"
    )
    
    # 선택된 스타일 정보 + 이미지 미리보기
    if selected_style != "AI 자동 추천":
        style_info = STYLE_GUIDE[selected_style]
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            # 이미지 미리보기
            if style_info.get("preview_image"):
                st.image(
                    style_info["preview_image"], 
                    caption=f"{style_info['preview']} {selected_style}",
                    use_container_width=True
                )
            else:
                st.markdown(f"### {style_info['preview']}")
                st.markdown(f"**{selected_style}**")
        
        with col2:
            st.markdown(f"### {selected_style}")
            st.caption(style_info['description'])
            
            with st.expander("📋 스타일 키워드 보기"):
                st.code(style_info['image_keywords'], language=None)
    
    # 전체 스타일 갤러리
    with st.expander("🎨 모든 스타일 미리보기 갤러리"):
        cols = st.columns(3)
        col_idx = 0
        
        for style_name, style_data in STYLE_GUIDE.items():
            if style_name == "AI 자동 추천":
                continue
            
            with cols[col_idx % 3]:
                if style_data.get("preview_image"):
                    st.image(style_data["preview_image"], use_container_width=True)
                st.markdown(f"**{style_data['preview']} {style_name}**")
                st.caption(style_data['description'])
                st.divider()
            
            col_idx += 1
    
    st.divider()
    
    # ============ 추가 옵션 ============
    with st.expander("⚙️ 추가 옵션 (조명 & 배경)"):
        lighting_kr = st.selectbox(
            "조명 분위기",
            options=LIGHTING_OPTIONS
        )
        st.caption(f"🔤 `{LIGHTING_MAP[lighting_kr]}`")
        
        background_kr = st.selectbox(
            "배경 스타일",
            options=BACKGROUND_OPTIONS
        )
        st.caption(f"🔤 `{BACKGROUND_MAP[background_kr]}`")
    
    st.divider()
    
    # ============ 생성 버튼 ============
    if st.button("🎨 마스터 이미지 프롬프트 생성", type="primary", use_container_width=True):
        if not main_subject:
            st.error("주인공 주제를 입력해주세요.")
            return
        if not details:
            st.error("세부 특징을 입력해주세요.")
            return
        if selected_style == "AI 자동 추천":
            st.warning("구체적인 스타일을 선택해주세요. (AI 자동 추천은 Tab 3에서 사용됩니다)")
            return
        if client is None:
            st.error("API 키가 설정되지 않았습니다.")
            return
        
        # 스타일 데이터 가져오기
        style_data = STYLE_GUIDE[selected_style]
        style_keywords = style_data["image_keywords"]
        lighting_en = LIGHTING_MAP[lighting_kr]
        background_en = BACKGROUND_MAP[background_kr]
        
        user_prompt = f"""다음 정보를 바탕으로 Midjourney 마스터 이미지 프롬프트를 작성해주세요.

## 캐릭터 정보
- 주인공: {main_subject}
- 세부 특징: {details}

## 스타일 정보
- 화풍: {style_keywords}
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
                
                # ⭐ 중요: Tab 3 연동을 위한 데이터 저장
                st.session_state["character_prompt"] = result
                st.session_state["character_style"] = style_keywords  # 영어 키워드
                st.session_state["character_style_kr"] = selected_style  # ⭐ 한글 스타일명 (Tab 3 연동용)
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
        st.caption(f"🎨 화풍: {st.session_state.get('character_style_kr', '-')}")
        
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
        
        # --cw 안내
        with st.expander("💡 --cw (Character Weight) 파라미터 안내"):
            st.markdown("""
            **--cw** 파라미터는 캐릭터 참조의 강도를 조절합니다:
            
            - `--cw 100` (기본값): **얼굴 + 헤어 + 의상** 모두 참조
              - 추천: 캐릭터의 의상까지 고정하고 싶을 때
            
            - `--cw 0`: **얼굴만** 참조, 의상은 자유롭게
              - 추천: 장면마다 다른 의상을 입히고 싶을 때
            
            💡 **팁:** Tab 3에서 프롬프트 생성 후, 필요에 따라 `--cw 0` 또는 `--cw 100`을 수동으로 추가할 수 있습니다.
            """)
        
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
                    st.rerun()
                else:
                    st.warning("유효한 URL인지 확인해주세요.")
            else:
                st.error("URL을 입력해주세요.")
        
        # 이미지 미리보기
        if st.session_state.get("master_image_url"):
            st.divider()
            st.subheader("🖼️ 등록된 마스터 이미지")
            
            try:
                st.image(
                    st.session_state["master_image_url"], 
                    caption="✅ 등록된 마스터 캐릭터 이미지", 
                    use_container_width=True
                )
                st.success(f"✅ 저장된 URL: `{st.session_state['master_image_url'][:50]}...`")
            except Exception as e:
                st.error(f"이미지를 불러올 수 없습니다. URL을 확인해주세요: {str(e)}")
            
            # URL 초기화
            if st.button("🗑️ URL 초기화", use_container_width=True):
                st.session_state["master_image_url"] = ""
                st.rerun()
    
    else:
        st.markdown("---")
        st.markdown("""
        ### 🚀 시작하기
        
        1. **주인공 주제**에 캐릭터를 입력하세요
           - 💡 Tab 1에서 가사를 생성했다면 '가사로 캐릭터 자동 추천받기' 버튼 클릭!
        2. **세부 특징**에 외모, 의상, 포즈 등을 자세히 적어주세요
        3. **프리미엄 스타일**을 선택하고 생성 버튼을 클릭하세요
        4. 생성된 프롬프트로 Midjourney에서 이미지를 만드세요
        5. URL을 저장하고 **Tab 3 (스토리보드)**로 이동하세요!
        """)
