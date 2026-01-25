"""
tabs/visuals.py - 이미지 생성 탭 (Tab 4)
스타일 프리셋 시스템 + AI 자동 추천
"""

import streamlit as st
from utils import get_gpt_response


# ============ 스타일 라이브러리 (15종) ============

STYLE_PRESETS = {
    "AI 자동 추천": {
        "keywords": "",
        "description": "가사의 장르와 분위기를 분석하여 AI가 최적의 스타일을 선택합니다",
        "preview": "🤖"
    },
    
    "르네상스 유화 (Renaissance Oil)": {
        "keywords": "In the style of a Renaissance oil painting, dramatic chiaroscuro, high detail, religious masterpiece aesthetic, classical composition, golden age painting techniques, museum quality",
        "description": "고전적이고 웅장한 분위기, 극적인 명암 대비",
        "preview": "🖼️"
    },
    
    "80년대 디스코 팝아트 (80s Disco Pop-Art)": {
        "keywords": "Vibrant 80s disco pop art style, neon colors, halftone patterns, funky and energetic, retro groovy aesthetic, bold geometric shapes, Andy Warhol inspired",
        "description": "화려한 네온 컬러, 에너지 넘치는 레트로 감성",
        "preview": "🕺"
    },
    
    "한국 민화 모던 (Modern Korean Minhwa)": {
        "keywords": "Modernized Korean Minhwa style, traditional ink and wash brushwork, witty and colorful traditional depiction, Korean folk art aesthetic, symbolic animals and flowers, vibrant but harmonious colors",
        "description": "전통과 현대가 조화된 한국적 감성",
        "preview": "🎨"
    },
    
    "지브리 애니메이션 (Studio Ghibli)": {
        "keywords": "Studio Ghibli animation style, hand-drawn cel animation, lush landscapes, soft watercolor textures, nostalgic atmosphere, Hayao Miyazaki aesthetic, dreamy and whimsical",
        "description": "따뜻하고 섬세한 손그림 애니메이션",
        "preview": "🌿"
    },
    
    "사이버펑크 2077 (Cyberpunk Noir)": {
        "keywords": "Cyberpunk 2077 style, high-tech noir aesthetic, neon-soaked streets, cinematic lighting, futuristic and gritty digital art, dystopian cityscape, holographic effects",
        "description": "네온과 어둠이 공존하는 미래 도시",
        "preview": "🌃"
    },
    
    "언리얼 엔진 5 렌더 (UE5 Photorealistic)": {
        "keywords": "Unreal Engine 5 render, hyper-realistic 3D visualization, volumetric lighting, photorealistic textures, ray-traced reflections, movie-like cinematic quality, AAA game graphics",
        "description": "초사실적인 3D 렌더링, 영화 같은 품질",
        "preview": "💎"
    },
    
    "픽사 3D 애니메이션 (Pixar 3D)": {
        "keywords": "Pixar Disney 3D animation style, expressive character design, vibrant colors, soft ambient lighting, family-friendly aesthetic, rounded shapes, heartwarming atmosphere",
        "description": "귀엽고 생동감 넘치는 3D 애니메이션",
        "preview": "🎬"
    },
    
    "반 고흐 인상파 (Van Gogh Impressionism)": {
        "keywords": "In the style of Vincent van Gogh, post-impressionist brushwork, swirling brushstrokes, vibrant impasto texture, emotional color palette, Starry Night aesthetic",
        "description": "소용돌이치는 붓터치, 감성적 색채",
        "preview": "🌌"
    },
    
    "미니멀 라인 아트 (Minimal Line Art)": {
        "keywords": "Minimalist line art illustration, single continuous line drawing, simple elegant composition, negative space emphasis, modern clean aesthetic, vector art style",
        "description": "깔끔하고 세련된 라인 드로잉",
        "preview": "✏️"
    },
    
    "일본 우키요에 (Japanese Ukiyo-e)": {
        "keywords": "Japanese Ukiyo-e woodblock print style, bold outlines, flat color blocks, traditional Edo period aesthetic, Hokusai and Hiroshige inspired, elegant composition",
        "description": "전통 일본 목판화 스타일",
        "preview": "🗾"
    },
    
    "다크 판타지 (Dark Fantasy)": {
        "keywords": "Dark fantasy illustration, gothic aesthetic, dramatic shadows, mysterious atmosphere, ethereal lighting, medieval dark ages inspiration, moody and atmospheric",
        "description": "어둡고 신비로운 판타지 세계관",
        "preview": "🌑"
    },
    
    "레트로 게임 픽셀아트 (Retro Pixel Art)": {
        "keywords": "16-bit pixel art style, retro video game aesthetic, limited color palette, crisp pixel-perfect rendering, nostalgic 90s gaming vibe, isometric or side-view",
        "description": "향수를 자극하는 레트로 픽셀 그래픽",
        "preview": "🎮"
    },
    
    "아르누보 포스터 (Art Nouveau Poster)": {
        "keywords": "Art Nouveau poster style, flowing organic lines, ornamental floral motifs, elegant typography integration, Alphonse Mucha inspired, vintage advertising aesthetic",
        "description": "우아한 곡선과 장식적 요소",
        "preview": "🎭"
    },
    
    "수채화 드로잉 (Watercolor Sketch)": {
        "keywords": "Delicate watercolor illustration, soft edges, transparent washes, hand-painted texture, loose brushwork, artistic and dreamy atmosphere, paper texture visible",
        "description": "부드럽고 몽환적인 수채화",
        "preview": "🖌️"
    },
    
    "스팀펑크 빅토리안 (Steampunk Victorian)": {
        "keywords": "Steampunk Victorian style, brass and copper machinery, intricate gears and clockwork, industrial revolution aesthetic, retro-futuristic inventions, sepia-toned atmosphere",
        "description": "증기기관과 빅토리아 시대의 만남",
        "preview": "⚙️"
    }
}


# ============ AI 자동 추천 매핑 규칙 ============

AUTO_STYLE_MAPPING = {
    # 장르 기반
    "발라드": "수채화 드로잉 (Watercolor Sketch)",
    "시티팝": "80년대 디스코 팝아트 (80s Disco Pop-Art)",
    "힙합/랩": "사이버펑크 2077 (Cyberpunk Noir)",
    "록/메탈": "다크 판타지 (Dark Fantasy)",
    "재즈": "반 고흐 인상파 (Van Gogh Impressionism)",
    "트로트": "한국 민화 모던 (Modern Korean Minhwa)",
    "EDM/일렉트로닉": "사이버펑크 2077 (Cyberpunk Noir)",
    "동요/키즈": "픽사 3D 애니메이션 (Pixar 3D)",
    "클래식 크로스오버": "르네상스 유화 (Renaissance Oil)",
    "Lo-fi/Chill": "지브리 애니메이션 (Studio Ghibli)",
    
    # Vibe 기반
    "광기/호러": "다크 판타지 (Dark Fantasy)",
    "슬픈데 신나게": "80년대 디스코 팝아트 (80s Disco Pop-Art)",
    "웃기지만 진지하게": "레트로 게임 픽셀아트 (Retro Pixel Art)",
}


def get_auto_recommended_style(genre: str, vibe: str) -> str:
    """
    장르와 Vibe를 분석하여 최적의 스타일을 자동 추천합니다.
    
    Args:
        genre: 가사 장르
        vibe: 가사 Vibe
        
    Returns:
        추천 스타일 이름
    """
    # Vibe 우선 (더 구체적이므로)
    if vibe in AUTO_STYLE_MAPPING:
        return AUTO_STYLE_MAPPING[vibe]
    
    # 장르 기반
    if genre in AUTO_STYLE_MAPPING:
        return AUTO_STYLE_MAPPING[genre]
    
    # 기본값
    return "지브리 애니메이션 (Studio Ghibli)"


SYSTEM_ROLE = """당신은 AI 이미지 생성 프롬프트 전문가입니다.

## 당신의 임무
사용자가 제공한 주제와 선택한 이미지 스타일을 결합하여 Midjourney/DALL-E/Stable Diffusion에서 최상의 결과를 내는 프롬프트를 작성합니다.

## 프롬프트 작성 규칙

1. **구조**: `[주제 묘사] + [스타일 키워드] + [품질 태그]`

2. **주제 묘사**:
   - 구체적인 시각적 요소 (인물, 배경, 사물)
   - 구도와 앵글 (close-up, wide shot, bird's eye view)
   - 조명과 분위기 (dramatic lighting, soft glow)
   - 색감 (vibrant, muted, monochrome)

3. **스타일 키워드 적용**:
   - 제공된 스타일 키워드를 자연스럽게 통합
   - 스타일에 맞는 추가 형용사 보강

4. **품질 태그**:
   - 해상도: 4K, 8K, high resolution
   - 품질: highly detailed, masterpiece, professional
   - 기술: octane render, unreal engine (필요시)

## 출력 형식

**[이미지 제목]**
(주제를 함축하는 매력적인 제목)

**[프롬프트]**
(최종 영어 프롬프트 - 한 문단)

**[설명]**
(한국어로 이미지 컨셉 설명 2-3문장)

## 예시

**[이미지 제목]**
Midnight Coffee Solitude

**[프롬프트]**
A lonely young woman sitting by a rain-streaked window in a dimly lit cafe at midnight, warm amber lighting from vintage lamps, steam rising from a coffee cup, melancholic atmosphere, in the style of a Renaissance oil painting, dramatic chiaroscuro, high detail, museum quality, 8K resolution, masterpiece

**[설명]**
새벽 카페에서 창밖을 바라보는 여성의 고독한 순간을 르네상스 유화 기법으로 표현했습니다. 극적인 명암 대비가 인물의 감정을 더욱 부각시킵니다."""


def parse_image_prompt(response: str) -> dict:
    """
    GPT 응답에서 제목, 프롬프트, 설명을 추출합니다.
    
    Returns:
        dict: {
            'title': str,
            'prompt': str,
            'description': str
        }
    """
    result = {
        'title': '',
        'prompt': '',
        'description': ''
    }
    
    # 제목 추출
    if '[이미지 제목]' in response or '**[이미지 제목]**' in response:
        title_start = response.find('[이미지 제목]')
        if title_start == -1:
            title_start = response.find('**[이미지 제목]**')
        title_end = response.find('\n', title_start)
        if title_end != -1:
            title_line = response[title_start:title_end]
            result['title'] = title_line.split(']')[-1].strip().replace('*', '')
    
    # 프롬프트 추출
    if '[프롬프트]' in response or '**[프롬프트]**' in response:
        prompt_start = response.find('[프롬프트]')
        if prompt_start == -1:
            prompt_start = response.find('**[프롬프트]**')
        prompt_end = response.find('[설명]', prompt_start)
        if prompt_end == -1:
            prompt_end = response.find('**[설명]**', prompt_start)
        if prompt_end != -1:
            prompt_section = response[prompt_start:prompt_end]
            lines = prompt_section.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('[') and not line.startswith('**'):
                    result['prompt'] += line.strip() + ' '
            result['prompt'] = result['prompt'].strip()
    
    # 설명 추출
    if '[설명]' in response or '**[설명]**' in response:
        desc_start = response.find('[설명]')
        if desc_start == -1:
            desc_start = response.find('**[설명]**')
        desc_section = response[desc_start:]
        lines = desc_section.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('[') and not line.startswith('**'):
                result['description'] += line.strip() + ' '
        result['description'] = result['description'].strip()
    
    return result


def render(client):
    """이미지 생성 탭을 렌더링합니다."""
    
    st.header("🎨 Step 4: AI 이미지 생성")
    st.markdown("""
    가사 주제를 바탕으로 **독특한 스타일의 이미지 프롬프트**를 생성합니다.
    
    > 🎯 *"15가지 아트 스타일 중 선택 또는 AI 자동 추천"*
    """)
    
    st.info("""
    ✨ **이렇게 사용하세요:**
    1. 주제 입력 (Tab 1에서 생성한 가사 주제 활용 가능)
    2. 스타일 선택 (AI 자동 추천 또는 직접 선택)
    3. 프롬프트 생성
    4. Midjourney/DALL-E/Stable Diffusion에서 실행!
    """)
    
    st.divider()
    
    # ============ 주제 입력 ============
    st.subheader("🖼️ 이미지 주제")
    
    # Tab 1에서 가사 주제 자동 불러오기
    default_topic = st.session_state.get("lyrics_topic", "")
    
    image_topic = st.text_area(
        "어떤 이미지를 만들고 싶으신가요?",
        value=default_topic,
        placeholder="예시:\n- 새벽 카페에서 혼자 커피를 마시는 여성\n- 네온 불빛이 가득한 미래 도시의 밤거리\n- 벚꽃이 흩날리는 봄날의 한강 공원",
        height=120,
        help="구체적으로 묘사할수록 좋은 결과가 나옵니다"
    )
    
    if default_topic:
        st.caption("💡 Tab 1에서 생성한 가사 주제가 자동으로 불러와졌습니다.")
    
    st.divider()
    
    # ============ 스타일 선택 ============
    st.subheader("🎨 이미지 스타일")
    
    # 현재 장르/Vibe 가져오기
    current_genre = st.session_state.get("lyrics_genre", "")
    current_vibe = st.session_state.get("lyrics_vibe", "")
    
    # AI 자동 추천 스타일
    auto_recommended = None
    if current_genre or current_vibe:
        auto_recommended = get_auto_recommended_style(current_genre, current_vibe)
        st.success(f"🤖 **AI 추천 스타일:** {auto_recommended}")
        st.caption(f"현재 장르({current_genre})와 Vibe({current_vibe})를 분석한 결과입니다.")
    
    # 스타일 선택
    style_options = list(STYLE_PRESETS.keys())
    
    selected_style = st.selectbox(
        "이미지 스타일 선택",
        options=style_options,
        help="'AI 자동 추천'을 선택하면 장르에 맞는 스타일이 자동으로 적용됩니다"
    )
    
    # 선택된 스타일 정보 표시
    if selected_style != "AI 자동 추천":
        style_info = STYLE_PRESETS[selected_style]
        
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"### {style_info['preview']}")
        with col2:
            st.markdown(f"**{selected_style}**")
            st.caption(style_info['description'])
    
    # 스타일 미리보기 (전체)
    with st.expander("🎨 모든 스타일 미리보기"):
        for style_name, style_data in STYLE_PRESETS.items():
            if style_name == "AI 자동 추천":
                continue
            st.markdown(f"{style_data['preview']} **{style_name}**")
            st.caption(style_data['description'])
            st.divider()
    
    st.divider()
    
    # ============ 추가 옵션 ============
    with st.expander("⚙️ 고급 옵션"):
        col1, col2 = st.columns(2)
        
        with col1:
            composition = st.selectbox(
                "구도",
                ["자동", "Close-up", "Medium shot", "Wide shot", "Bird's eye view", "Low angle"]
            )
        
        with col2:
            lighting = st.selectbox(
                "조명",
                ["자동", "Dramatic lighting", "Soft glow", "Golden hour", "Neon lights", "Natural sunlight"]
            )
    
    st.divider()
    
    # ============ 생성 버튼 ============
    if st.button("🎨 이미지 프롬프트 생성", type="primary", use_container_width=True):
        if not image_topic.strip():
            st.error("이미지 주제를 입력해주세요.")
            return
        if client is None:
            st.error("API 키가 설정되지 않았습니다.")
            return
        
        # 최종 스타일 결정
        if selected_style == "AI 자동 추천":
            if auto_recommended:
                final_style = auto_recommended
            else:
                final_style = "지브리 애니메이션 (Studio Ghibli)"
            st.info(f"🤖 AI가 선택한 스타일: **{final_style}**")
        else:
            final_style = selected_style
        
        # 스타일 키워드 가져오기
        style_keywords = STYLE_PRESETS[final_style]["keywords"]
        
        # 고급 옵션 반영
        additional_keywords = []
        if composition != "자동":
            additional_keywords.append(composition.lower())
        if lighting != "자동":
            additional_keywords.append(lighting.lower())
        
        additional_text = ", ".join(additional_keywords) if additional_keywords else ""
        
        # 사용자 프롬프트 구성
        user_prompt = f"""다음 주제와 스타일을 결합하여 최상의 이미지 프롬프트를 작성해주세요.

## 이미지 주제
{image_topic}

## 선택된 스타일
{final_style}

## 스타일 키워드
{style_keywords}

## 추가 요청사항
{additional_text if additional_text else "없음"}

위 정보를 바탕으로 Midjourney/DALL-E/Stable Diffusion에서 최상의 결과를 낼 수 있는 프롬프트를 작성해주세요."""

        with st.spinner("🎨 AI가 이미지 프롬프트를 생성하고 있습니다..."):
            try:
                response = get_gpt_response(client, SYSTEM_ROLE, user_prompt)
                
                # 파싱
                parsed = parse_image_prompt(response)
                
                # 세션 스테이트에 저장
                st.session_state["image_prompt"] = parsed
                st.session_state["image_style"] = final_style
                st.session_state["image_topic"] = image_topic
                st.session_state["image_raw"] = response
                
                st.success("🎉 이미지 프롬프트가 생성되었습니다!")
                st.rerun()
                
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
                return
    
    # ============ 결과 표시 ============
    st.divider()
    
    if "image_prompt" in st.session_state and st.session_state["image_prompt"]:
        parsed = st.session_state["image_prompt"]
        final_style = st.session_state.get("image_style", "")
        
        # 제목
        if parsed['title']:
            st.header(f"🖼️ {parsed['title']}")
        
        # 메타 정보
        st.caption(f"🎨 스타일: **{final_style}**")
        
        st.divider()
        
        # 프롬프트 (복사 쉽게)
        st.subheader("📋 Midjourney/DALL-E 프롬프트")
        st.code(parsed['prompt'], language=None)
        st.caption("👆 위 프롬프트를 복사해서 AI 이미지 생성 툴에 붙여넣으세요!")
        
        # 설명
        if parsed['description']:
            st.divider()
            st.subheader("💡 이미지 컨셉 설명")
            st.info(parsed['description'])
        
        # 다운로드 버튼
        st.divider()
        st.download_button(
            label="📥 프롬프트 다운로드",
            data=parsed['prompt'],
            file_name=f"{parsed['title'].replace(' ', '_')}_prompt.txt",
            mime="text/plain",
            use_container_width=True
        )
        
        # 사용 안내
        st.divider()
        st.success("""
        🎉 **프롬프트 생성 완료!**
        
        **다음 단계:**
        1. 위 프롬프트를 **복사**
        2. **Midjourney Discord** 또는 **DALL-E**에서 실행
        3. 생성된 이미지를 뮤직비디오에 활용!
        
        💡 **팁:** Midjourney에서는 `--ar 16:9` 파라미터를 추가하면 와이드 화면으로 생성됩니다!
        """)
        
        # 원본 응답 (디버깅용)
        with st.expander("🔍 원본 AI 응답 확인 (디버깅용)"):
            st.text(st.session_state.get("image_raw", ""))
    
    else:
        st.markdown("---")
        st.markdown("""
        ### 🚀 시작하기
        
        1. **이미지 주제**를 입력하세요
           - Tab 1에서 가사를 만들었다면 자동으로 불러와집니다
        
        2. **스타일 선택**
           - AI 자동 추천: 장르에 맞는 스타일 자동 선택
           - 직접 선택: 15가지 독특한 스타일 중 선택
        
        3. **생성 버튼** 클릭
        
        4. **프롬프트 복사** → 이미지 생성 툴에서 실행!
        
        > 💡 르네상스 유화부터 사이버펑크까지, 다양한 스타일을 시도해보세요!
        """)
