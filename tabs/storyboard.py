"""
tabs/storyboard.py - 스토리보드 생성 탭 (Tab 3) - 완전 업그레이드
STYLE_GUIDE + AI 자동 추천 + 2단계 조립 공식 + 영상 편집 레시피
"""

import streamlit as st
from utils import get_gpt_response


# ============ 통합 스타일 가이드 (10종+) ============

STYLE_GUIDE = {
    "AI 자동 추천": {
        "image_keywords": "",
        "video_keywords": "",
        "effects": "",
        "transitions": "",
        "description": "가사의 장르와 분위기를 분석하여 AI가 최적의 스타일을 선택합니다",
        "preview": "🤖"
    },
    
    "르네상스 유화 (Renaissance Oil)": {
        "image_keywords": "Renaissance oil painting style, dramatic chiaroscuro, high detail, religious masterpiece aesthetic, classical composition, golden age painting techniques",
        "video_keywords": "Golden hour, candle light, slow motion, museum atmosphere",
        "effects": "Film grain, warm glow, soft focus, vignette",
        "transitions": "Cross dissolve, fade to black, slow zoom",
        "description": "고전적이고 웅장한 분위기, 극적인 명암 대비",
        "preview": "🖼️"
    },
    
    "80년대 디스코 팝아트 (80s Disco Pop-Art)": {
        "image_keywords": "Vibrant 80s disco pop art style, neon colors, halftone patterns, funky and energetic, retro groovy aesthetic, bold geometric shapes",
        "video_keywords": "Dancing lights, disco ball, city neon, retro party",
        "effects": "Glitch effect, RGB split, strobe lights, chromatic aberration",
        "transitions": "Glitch transition, whip pan, beat-synced cuts",
        "description": "화려한 네온 컬러, 에너지 넘치는 레트로 감성",
        "preview": "🕺"
    },
    
    "한국 민화 모던 (Modern Korean Minhwa)": {
        "image_keywords": "Modernized Korean Minhwa style, traditional ink and wash brushwork, witty and colorful traditional depiction, Korean folk art aesthetic, vibrant harmonious colors",
        "video_keywords": "Traditional Korean village, paper texture, nature, joyful feast",
        "effects": "Ink splash transition, paper overlay, watercolor bleeding",
        "transitions": "Ink wash wipe, paper tear transition",
        "description": "전통과 현대가 조화된 한국적 감성",
        "preview": "🎨"
    },
    
    "지브리 애니메이션 (Studio Ghibli)": {
        "image_keywords": "Studio Ghibli animation style, hand-drawn cel animation, lush landscapes, soft watercolor textures, nostalgic atmosphere, dreamy and whimsical",
        "video_keywords": "Nature scenes, countryside, clouds moving, peaceful village",
        "effects": "Watercolor wash, soft bloom, film grain subtle, dreamy atmosphere",
        "transitions": "Cloud transition, gentle fade, parallax scrolling",
        "description": "따뜻하고 섬세한 손그림 애니메이션",
        "preview": "🌿"
    },
    
    "사이버펑크 2077 (Cyberpunk Noir)": {
        "image_keywords": "Cyberpunk 2077 style, high-tech noir aesthetic, neon-soaked streets, cinematic lighting, futuristic and gritty digital art, dystopian cityscape",
        "video_keywords": "Neon city night, rain on street, hologram display, futuristic interface",
        "effects": "Neon glow, digital glitch, holographic overlay, chromatic aberration",
        "transitions": "Digital glitch, matrix transition, hologram flicker",
        "description": "네온과 어둠이 공존하는 미래 도시",
        "preview": "🌃"
    },
    
    "언리얼 엔진 5 렌더 (UE5 Photorealistic)": {
        "image_keywords": "Unreal Engine 5 render, hyper-realistic 3D visualization, volumetric lighting, photorealistic textures, ray-traced reflections, movie-like cinematic quality",
        "video_keywords": "Cinematic camera movement, dramatic lighting, slow motion action",
        "effects": "Lens flare, depth of field, motion blur, volumetric lighting",
        "transitions": "Camera pan, dramatic zoom, fade with light leak",
        "description": "초사실적인 3D 렌더링, 영화 같은 품질",
        "preview": "💎"
    },
    
    "픽사 3D 애니메이션 (Pixar 3D)": {
        "image_keywords": "Pixar Disney 3D animation style, expressive character design, vibrant colors, soft ambient lighting, family-friendly aesthetic, rounded shapes",
        "video_keywords": "Cartoon character, playful animation, bright colors, bouncing movement",
        "effects": "Cartoon motion blur, exaggerated movement, bounce effect",
        "transitions": "Bounce transition, pop-in effect, playful wipe",
        "description": "귀엽고 생동감 넘치는 3D 애니메이션",
        "preview": "🎬"
    },
    
    "반 고흐 인상파 (Van Gogh Impressionism)": {
        "image_keywords": "Vincent van Gogh style, post-impressionist brushwork, swirling brushstrokes, vibrant impasto texture, emotional color palette, Starry Night aesthetic",
        "video_keywords": "Starry night sky, swirling clouds, countryside, sunflower field",
        "effects": "Oil painting effect, brushstroke overlay, impasto texture",
        "transitions": "Brush stroke wipe, paint splash transition",
        "description": "소용돌이치는 붓터치, 감성적 색채",
        "preview": "🌌"
    },
    
    "일본 우키요에 (Japanese Ukiyo-e)": {
        "image_keywords": "Japanese Ukiyo-e woodblock print style, bold outlines, flat color blocks, traditional Edo period aesthetic, elegant composition",
        "video_keywords": "Japanese landscape, waves, Mount Fuji, traditional architecture",
        "effects": "Woodblock texture, flat colors, bold outlines",
        "transitions": "Sliding panel transition, wave wipe",
        "description": "전통 일본 목판화 스타일",
        "preview": "🗾"
    },
    
    "다크 판타지 (Dark Fantasy)": {
        "image_keywords": "Dark fantasy illustration, gothic aesthetic, dramatic shadows, mysterious atmosphere, ethereal lighting, medieval dark ages inspiration",
        "video_keywords": "Dark castle, foggy forest, moonlight, ravens, gothic architecture",
        "effects": "Dark vignette, fog overlay, light rays, shadow enhancement",
        "transitions": "Shadow wipe, fade to black, smoke transition",
        "description": "어둡고 신비로운 판타지 세계관",
        "preview": "🌑"
    },
    
    "90년대 레트로 애니 (90s Retro Anime)": {
        "image_keywords": "Retro 90s anime style, nostalgic, cel shading, vibrant colors, City Pop aesthetic, Lo-fi vibe, purple and blue neon lighting, dreamy atmosphere, vintage",
        "video_keywords": "Retro city night, neon signs, cassette tapes, CRT TV, vintage cars",
        "effects": "VHS grain, scan lines, color bleeding, lo-fi aesthetic",
        "transitions": "VHS glitch, scan line wipe, retro fade",
        "description": "향수를 자극하는 90년대 애니 감성",
        "preview": "📼"
    }
}


# ============ AI 자동 추천 매핑 ============

STYLE_AUTO_SELECT = {
    # 장르 기반
    "발라드": "반 고흐 인상파 (Van Gogh Impressionism)",
    "시티팝": "90년대 레트로 애니 (90s Retro Anime)",
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
    "웃기지만 진지하게": "90년대 레트로 애니 (90s Retro Anime)",
}

# 키워드 기반 추천
KEYWORD_STYLE_MAP = {
    "디지털": "사이버펑크 2077 (Cyberpunk Noir)",
    "코드": "사이버펑크 2077 (Cyberpunk Noir)",
    "네온": "사이버펑크 2077 (Cyberpunk Noir)",
    "취한": "한국 민화 모던 (Modern Korean Minhwa)",
    "포장마차": "한국 민화 모던 (Modern Korean Minhwa)",
    "아멘": "르네상스 유화 (Renaissance Oil)",
    "교회": "르네상스 유화 (Renaissance Oil)",
    "하늘": "지브리 애니메이션 (Studio Ghibli)",
    "구름": "지브리 애니메이션 (Studio Ghibli)",
    "어둠": "다크 판타지 (Dark Fantasy)",
    "밤": "다크 판타지 (Dark Fantasy)",
    "춤": "80년대 디스코 팝아트 (80s Disco Pop-Art)",
    "디스코": "80년대 디스코 팝아트 (80s Disco Pop-Art)",
}


def analyze_lyrics_for_style(lyrics: str, genre: str, vibe: str) -> str:
    """가사, 장르, Vibe를 분석하여 최적의 스타일을 추천합니다."""
    # 1순위: Vibe 기반
    if vibe in STYLE_AUTO_SELECT:
        return STYLE_AUTO_SELECT[vibe]
    
    # 2순위: 가사 키워드 분석
    if lyrics:
        lyrics_lower = lyrics.lower()
        for keyword, style in KEYWORD_STYLE_MAP.items():
            if keyword in lyrics_lower:
                return style
    
    # 3순위: 장르 기반
    if genre in STYLE_AUTO_SELECT:
        return STYLE_AUTO_SELECT[genre]
    
    # 기본값
    return "지브리 애니메이션 (Studio Ghibli)"


VIDEO_MOOD_MAP = {
    "시네마틱 감성 (영화 같은)": "Cinematic and emotional",
    "몽환적/꿈같은": "Dreamy and ethereal",
    "역동적/에너지 넘치는": "Energetic and dynamic",
    "멜랑콜리/잔잔한": "Melancholic and slow",
    "미스터리/어두운": "Mysterious and dark",
    "밝고 희망찬": "Bright and hopeful",
    "향수/따뜻한": "Nostalgic and warm"
}

VIDEO_MOOD_OPTIONS = list(VIDEO_MOOD_MAP.keys())


SYSTEM_ROLE = """당신은 세계적인 뮤직비디오 연출가이자 **2단계 조립 공식(Two-Step Assembly Formula)** 전문가입니다.

## 당신의 핵심 임무
가사의 기승전결을 분석하여 20개의 영화적 장면(Scene)을 구성하고, 각 장면마다 **2단계 조립 공식**을 적용하여 최상의 Midjourney 프롬프트를 생성합니다.

## ⭐ 2단계 조립 공식 (Two-Step Assembly Formula) ⭐

### Step 1: Subject Generation (장면 묘사)
가사 내용을 분석하여 **구체적인 핵심 장면**을 영어로 생성합니다.

**필수 포함 요소:**
1. **Subject (주체)**: 캐릭터 외형, 옷차림, 자세, 표정
2. **Environment (환경)**: 장소, 날씨, 시간대, 구체적 디테일
3. **Lighting & Color**: 조명 방향, 색온도, 분위기
4. **Composition**: 카메라 각도, 구도

**예시:**
```
A melancholic girl in white dress standing under flickering streetlight, 
tear-stained cheeks glistening, hands loosely hanging, wet streets reflecting 
neon signs in purple and blue, rain creating ripples in puddles
```

### Step 2: Style Integration (스타일 결합)
**Step 1의 장면 묘사는 그대로 유지**하고, 뒤에 스타일 키워드만 추가합니다.

**공식:**
```
[Step 1 장면 묘사] + ", " + [Style Keywords]
```

**⚠️ 중요: Step 1을 절대 수정하지 마세요! 뒤에 추가만 하세요!**

## 출력 형식 (매우 중요!)

### 구분자 규칙:
- **장면과 장면 사이**: `|||` (파이프 3개)
- **한글 설명과 이미지 묘사 사이**: `###` (샵 3개)
- **이미지 묘사와 모션 묘사 사이**: `@@@` (골뱅이 3개)

### 출력 예시:
```
빗속에서 슬픈 표정으로 서 있는 소녀 ### A melancholic girl in white dress standing under flickering streetlight, tear-stained cheeks glistening, hands loosely hanging, wet streets reflecting neon signs in purple and blue, rain creating ripples in puddles @@@ Slow zoom in from medium shot to close-up, rain falling diagonally across frame ||| 하늘을 올려다보며 희망을 품는 모습 ### She tilts head upward gazing at dark stormy clouds, hopeful expression with slight smile, single ray of golden sunlight breaking through clouds @@@ Camera pans upward smoothly following her gaze |||
```

## 이미지 묘사 작성 규칙 (Step 1)

### 필수 포함:
1. **구체적 시각 정보만** (추상적 표현 금지)
   - ❌ "슬픈 소녀" → ✅ "Girl with tear-stained cheeks, slouched posture"
   
2. **감각적 디테일**
   - 조명: "golden hour sunlight", "neon glow", "candlelight"
   - 색감: "warm orange tones", "cool blue atmosphere"
   - 질감: "rain-streaked glass", "worn leather jacket"

3. **구도와 앵글**
   - "close-up portrait", "wide angle view", "bird's eye view"

4. **가사 연출 지시어 반영**
   - `(Piano intro)` → "grand piano with keys visible, spotlight on piano"
   - `(Build up)` → "dynamic composition, dramatic lighting, tension"

### ⚠️ 주의사항:
- 영어로 작성 (Midjourney 최적화)
- **스타일 키워드는 절대 포함하지 마세요!** (시스템이 Step 2에서 자동 추가)

## 모션 묘사 작성 규칙

1. 카메라 움직임: zoom in/out, pan, tilt, dolly
2. 피사체 동작: walking, turning, reaching out
3. 환경 효과: rain falling, wind blowing
4. 영어로 작성 (Kling/Runway 최적화)

## 20개 장면 구성:
- Scene 1-3: 도입부 (Intro)
- Scene 4-7: 전개 1 (Verse 1)
- Scene 8-11: 고조 1 (Chorus 1)
- Scene 12-14: 전개 2 (Verse 2/Bridge)
- Scene 15-18: 클라이맥스 (Chorus 2/Final)
- Scene 19-20: 마무리 (Outro)

## 절대 규칙
1. 정확히 20개의 장면 생성
2. 각 장면은 `|||`로 구분
3. 한글설명, 이미지, 모션은 각각 `###`, `@@@`로 구분
4. **이미지 묘사에 스타일 키워드 포함 금지** (시스템이 자동 추가)
5. 구체적 시각 정보만 사용 (추상적 표현 금지)"""


def parse_scenes(gpt_response: str) -> list:
    """GPT 응답을 파싱하여 장면 리스트를 반환합니다."""
    scenes = []
    raw_scenes = gpt_response.split("|||")
    
    for raw_scene in raw_scenes:
        raw_scene = raw_scene.strip()
        if not raw_scene:
            continue
        
        korean_desc = ""
        image_prompt = ""
        motion_prompt = ""
        
        # 한글 설명과 나머지 분리
        if "###" in raw_scene:
            parts = raw_scene.split("###")
            korean_desc = parts[0].strip()
            remaining = parts[1].strip() if len(parts) > 1 else ""
        else:
            remaining = raw_scene
            korean_desc = "장면 설명"
        
        # 이미지와 모션 분리
        if "@@@" in remaining:
            parts = remaining.split("@@@")
            image_prompt = parts[0].strip()
            motion_prompt = parts[1].strip() if len(parts) > 1 else ""
        else:
            image_prompt = remaining
            motion_prompt = ""
        
        if not motion_prompt:
            motion_prompt = "Cinematic slow motion, gentle camera movement, atmospheric lighting"
        
        scenes.append({
            "korean_desc": korean_desc,
            "image_prompt": image_prompt,
            "motion_prompt": motion_prompt
        })
    
    return scenes


def render(client):
    """스토리보드 탭을 렌더링합니다."""
    
    st.header("🎬 Step 3: 스토리보드 & 이미지 프롬프트 생성")
    st.markdown("""
    가사를 분석하여 **20개 장면**의 초고품질 이미지 프롬프트를 생성합니다.
    
    > 🎥 *"2단계 조립 공식 + AI 스타일 추천 + 영상 편집 레시피"*
    """)
    
    st.success("""
    ✨ **NEW 업그레이드:**
    1. 🤖 **AI 자동 추천** - 가사 분석으로 최적 스타일 선택
    2. 🎨 **10가지+ 독특한 스타일** - 르네상스부터 사이버펑크까지
    3. 🔧 **2단계 조립 공식** - 장면 묘사 + 스타일 결합
    4. 🎬 **영상 편집 레시피** - 스톡 영상, 효과, 전환 가이드
    """)
    
    st.divider()
    
    # ============ 가사 입력 ============
    st.subheader("📝 가사 입력")
    default_lyrics = st.session_state.get("lyrics", "")
    
    lyrics_input = st.text_area(
        "뮤직비디오에 사용할 가사",
        value=default_lyrics,
        height=250,
        placeholder="[Verse 1]\n여기에 가사를 입력하세요...",
        help="가사를 기반으로 20개의 장면이 생성됩니다"
    )
    
    if default_lyrics:
        st.caption("💡 Tab 1에서 생성한 가사가 자동으로 불러와졌습니다.")
    
    st.divider()
    
    # ============ 마스터 이미지 URL ============
    st.subheader("🔗 마스터 이미지 URL (선택)")
    default_url = st.session_state.get("master_image_url", "")
    
    master_url = st.text_input(
        "캐릭터 참조용 이미지 URL",
        value=default_url,
        placeholder="https://cdn.midjourney.com/...",
        help="Tab 2에서 생성한 캐릭터 이미지 URL (선택사항)"
    )
    
    if default_url:
        st.caption("💡 Tab 2에서 저장한 URL이 불러와졌습니다.")
    else:
        st.info("💡 URL이 없어도 괜찮습니다! 스타일만으로도 일관성 있는 이미지가 생성됩니다.")
    
    st.divider()
    
    # ============ 스타일 선택 ============
    st.subheader("🎨 비주얼 스타일")
    
    # 현재 장르/Vibe 가져오기
    current_genre = st.session_state.get("lyrics_genre", "")
    current_vibe = st.session_state.get("lyrics_vibe", "")
    
    # AI 자동 추천 스타일
    auto_recommended = None
    if current_genre or current_vibe or lyrics_input:
        auto_recommended = analyze_lyrics_for_style(lyrics_input, current_genre, current_vibe)
        st.success(f"🤖 **AI 추천 스타일:** {auto_recommended}")
        
        if current_genre:
            st.caption(f"📊 분석 근거: 장르({current_genre}), Vibe({current_vibe})")
        
        # 키워드 발견 표시
        if lyrics_input:
            found_keywords = [kw for kw in KEYWORD_STYLE_MAP.keys() if kw in lyrics_input.lower()]
            if found_keywords:
                st.caption(f"🔍 가사 키워드 발견: {', '.join(found_keywords[:3])}")
    
    # 스타일 선택
    style_options = list(STYLE_GUIDE.keys())
    
    selected_style = st.selectbox(
        "이미지 스타일 선택",
        options=style_options,
        help="'AI 자동 추천'을 선택하면 가사 분석 결과가 자동 적용됩니다"
    )
    
    # 선택된 스타일 정보 표시
    if selected_style != "AI 자동 추천":
        style_info = STYLE_GUIDE[selected_style]
        
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"### {style_info['preview']}")
        with col2:
            st.markdown(f"**{selected_style}**")
            st.caption(style_info['description'])
    
    # 스타일 미리보기
    with st.expander("🎨 모든 스타일 미리보기"):
        for style_name, style_data in STYLE_GUIDE.items():
            if style_name == "AI 자동 추천":
                continue
            st.markdown(f"{style_data['preview']} **{style_name}**")
            st.caption(style_data['description'])
            st.divider()
    
    st.divider()
    
    # ============ 영상 분위기 ============
    st.subheader("🎥 영상 분위기")
    
    video_mood_kr = st.selectbox(
        "전체 영상 톤",
        options=VIDEO_MOOD_OPTIONS
    )
    
    st.caption(f"🔤 영어값: `{VIDEO_MOOD_MAP[video_mood_kr]}`")
    
    st.divider()
    
    # ============ 생성 버튼 ============
    if st.button("🎬 20개 장면 이미지 프롬프트 생성", type="primary", use_container_width=True):
        if not lyrics_input.strip():
            st.error("가사를 입력해주세요.")
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
        
        # 스타일 데이터 가져오기
        style_data = STYLE_GUIDE[final_style]
        style_keywords = style_data["image_keywords"]
        video_mood_en = VIDEO_MOOD_MAP[video_mood_kr]
        
        # 사용자 프롬프트 구성
        user_prompt = f"""다음 가사를 분석하여 뮤직비디오용 20개 장면의 이미지 프롬프트를 **2단계 조립 공식**에 따라 작성해주세요.

## 가사
{lyrics_input}

## 영상 분위기
{video_mood_en}

## ⭐ 중요 지시사항 ⭐

**각 장면마다 2단계 조립 공식을 적용하세요:**

### Step 1: Subject Generation
- 가사 내용을 구체적 시각 정보로 변환
- 주체, 환경, 조명, 구도 모두 포함
- **스타일 키워드는 절대 포함하지 마세요!**

### Step 2: Style Integration (시스템이 자동 처리)
- 시스템이 각 장면 뒤에 다음 스타일을 자동 추가합니다:
- Style Keywords: {style_keywords}

## 출력 형식 (정확히 준수!)

각 장면:
```
한글 설명 (20-30자) ### 영어 장면 묘사 (Step 1만, 스타일 제외) @@@ 영어 모션 묘사
```

장면 구분자: `|||`

## 예시:
```
빗속에서 슬픈 표정으로 서 있는 소녀 ### A melancholic girl in white dress standing under flickering streetlight, tear-stained cheeks glistening, wet streets reflecting neon signs @@@ Slow zoom in, rain falling ||| 하늘을 올려다보며 희망을 품는 모습 ### She tilts head upward gazing at dark clouds, hopeful expression, sunlight breaking through @@@ Camera pans upward |||
```

⚠️ 주의:
- 이미지 묘사에 스타일 키워드 포함 금지!
- 구체적 시각 정보만 사용
- 정확히 20개 장면 생성

지금 바로 20개 장면을 위 형식으로 생성해주세요!"""

        with st.spinner("🎬 AI가 20개 장면을 분석하고 있습니다... (약 1-2분)"):
            try:
                result = get_gpt_response(client, SYSTEM_ROLE, user_prompt)
                
                # 세션 스테이트에 저장
                st.session_state["storyboard_raw"] = result
                st.session_state["storyboard_url"] = master_url
                st.session_state["storyboard_style"] = final_style
                st.session_state["storyboard_video_mood"] = video_mood_en
                st.session_state["storyboard_video_mood_kr"] = video_mood_kr
                
                st.success("🎉 20개 장면 이미지 프롬프트가 생성되었습니다!")
                st.rerun()
                
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
                return
    
    # ============ 결과 표시 ============
    st.divider()
    
    if "storyboard_raw" in st.session_state and st.session_state["storyboard_raw"]:
        st.subheader("🎬 생성된 20개 장면")
        
        # 저장된 값 불러오기
        master_url = st.session_state.get("storyboard_url", "")
        final_style = st.session_state.get("storyboard_style", "")
        style_data = STYLE_GUIDE.get(final_style, {})
        style_keywords = style_data.get("image_keywords", "")
        
        # 적용 설정 안내
        st.info(f"""
        📌 **적용된 설정:**
        - 🎨 스타일: **{final_style}**
        - 🎬 분위기: **{st.session_state.get('storyboard_video_mood_kr', '-')}**
        - 🔗 캐릭터 참조: {'있음 (--cref 적용)' if master_url else '없음'}
        - 📐 화면 비율: `--ar 16:9`
        """)
        
        # GPT 결과 파싱
        scenes = parse_scenes(st.session_state["storyboard_raw"])
        
        if len(scenes) == 0:
            st.error("장면 파싱에 실패했습니다. 다시 생성해주세요.")
            return
        
        st.caption(f"✅ {len(scenes)}개 장면이 생성되었습니다.")
        
        st.divider()
        
        # ============ 최종 프롬프트 조립 (2단계 공식 적용) ============
        st.subheader("🔧 2단계 조립 공식 적용 결과")
        st.markdown("""
        각 장면의 이미지 프롬프트는 **2단계 조립 공식**으로 생성되었습니다:
        - **Step 1**: 가사 → 구체적 장면 묘사
        - **Step 2**: Step 1 + 스타일 키워드
        """)
        
        final_prompts = []
        
        for i, scene in enumerate(scenes[:20], 1):
            with st.expander(f"🎬 Scene {i}", expanded=(i <= 3)):
                
                # 한글 설명
                if scene.get('korean_desc'):
                    st.info(f"📖 **장면 설명:** {scene['korean_desc']}")
                
                # Step 1: 장면 묘사
                st.markdown("**🎬 Step 1: 장면 묘사 (Subject Generation)**")
                st.code(scene['image_prompt'], language=None)
                
                # Step 2: 최종 프롬프트 (스타일 결합)
                st.markdown("**✨ Step 2: 최종 Midjourney 프롬프트 (Style Integration)**")
                
                # 2단계 조립: Step 1 + 스타일 키워드
                step2_prompt = f"{scene['image_prompt']}, {style_keywords}"
                
                # --cref 추가 (URL 있을 때만)
                if master_url:
                    midjourney_prompt = f"/imagine prompt: {step2_prompt} --cref {master_url} --ar 16:9"
                else:
                    midjourney_prompt = f"/imagine prompt: {step2_prompt} --ar 16:9"
                
                st.code(midjourney_prompt, language=None)
                
                # Motion 프롬프트
                st.markdown("**🎥 Motion 프롬프트 (Kling/Runway)**")
                st.success(f"🎬 {scene['motion_prompt']}")
                
                final_prompts.append({
                    "scene": i,
                    "korean_desc": scene.get('korean_desc', ''),
                    "step1_scene": scene['image_prompt'],
                    "step2_final": step2_prompt,
                    "midjourney": midjourney_prompt,
                    "motion": scene['motion_prompt']
                })
        
        # 세션에 최종 프롬프트 저장
        st.session_state["final_prompts"] = final_prompts
        
        st.divider()
        
        # ============ 영상 편집 레시피 ============
        st.subheader("🎬 영상 편집 레시피")
        
        if style_data:
            tab1, tab2, tab3 = st.tabs([
                "📹 스톡 영상 키워드",
                "✨ 특수 효과 & 전환",
                "📋 통합 레시피"
            ])
            
            with tab1:
                st.markdown("### 📹 추천 스톡 영상 검색 키워드")
                st.success("🔍 **무료 스톡 영상 사이트:** Pexels, Pixabay, Videvo, Mixkit")
                
                if style_data.get("video_keywords"):
                    keywords = style_data["video_keywords"]
                    st.code(keywords, language=None)
                    st.caption("👆 위 키워드로 스톡 영상을 검색하세요")
            
            with tab2:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### ✨ 특수 효과")
                    if style_data.get("effects"):
                        st.info(style_data["effects"])
                
                with col2:
                    st.markdown("### 🔄 화면 전환")
                    if style_data.get("transitions"):
                        st.warning(style_data["transitions"])
            
            with tab3:
                st.markdown("### 📋 완전한 편집 가이드")
                
                recipe = f"""# {final_style} - 편집 레시피

## 🎨 스타일
{final_style}

## 📹 스톡 영상 키워드
{style_data.get('video_keywords', '-')}

## ✨ 특수 효과
{style_data.get('effects', '-')}

## 🔄 화면 전환
{style_data.get('transitions', '-')}

## 🎯 사용 방법
1. 위 키워드로 무료 스톡 영상 다운로드
2. 프리미어/다빈치 리졸브에서 편집
3. 추천 효과와 전환 적용
4. 음악과 싱크 맞추기
"""
                st.text_area("전체 레시피", value=recipe, height=300)
        
        st.divider()
        
        # ============ 전체 프롬프트 복사 섹션 ============
        st.subheader("📋 전체 프롬프트 (복사용)")
        
        tab_mj, tab_motion, tab_all = st.tabs([
            "🖼️ Midjourney 전체",
            "🎥 Motion 전체",
            "📄 통합 전체"
        ])
        
        with tab_mj:
            st.markdown("**Midjourney Discord에 순서대로 붙여넣기:**")
            all_mj = "\n\n".join([
                f"# Scene {p['scene']}: {p['korean_desc']}\n{p['midjourney']}"
                for p in final_prompts
            ])
            st.text_area("MJ 프롬프트", value=all_mj, height=400, label_visibility="collapsed")
        
        with tab_motion:
            st.markdown("**Kling/Runway에서 사용:**")
            all_motion = "\n\n".join([
                f"# Scene {p['scene']}: {p['korean_desc']}\n{p['motion']}"
                for p in final_prompts
            ])
            st.text_area("Motion", value=all_motion, height=400, label_visibility="collapsed")
        
        with tab_all:
            st.markdown("**전체 데이터:**")
            all_data = "\n\n".join([
                f"{'='*50}\n🎬 SCENE {p['scene']}\n{'='*50}\n\n"
                f"[한글 설명]\n{p['korean_desc']}\n\n"
                f"[Step 1: 장면 묘사]\n{p['step1_scene']}\n\n"
                f"[Step 2: 최종 프롬프트]\n{p['step2_final']}\n\n"
                f"[Midjourney]\n{p['midjourney']}\n\n"
                f"[Motion]\n{p['motion']}"
                for p in final_prompts
            ])
            st.text_area("통합", value=all_data, height=400, label_visibility="collapsed")
        
        # 완료 안내
        st.divider()
        st.success("""
        🎉 **모든 프롬프트가 생성되었습니다!**
        
        **다음 단계:**
        1. 📸 **Midjourney 프롬프트** 복사 → Discord에서 20개 이미지 생성
        2. 📹 **스톡 영상** 다운로드 (추천 키워드 사용)
        3. 🎬 **Kling/Runway**에 이미지 업로드 + Motion 프롬프트 적용
        4. ✂️ **영상 편집** (편집 레시피 참고)
        5. 🎵 **음악 합성** (Suno/Udio 가사)
        6. 🚀 **유튜브 업로드**
        
        💡 **무료 스톡 영상:**
        - Pexels: https://www.pexels.com/videos/
        - Pixabay: https://pixabay.com/videos/
        - Videvo: https://www.videvo.net/
        """)
    
    else:
        st.markdown("---")
        st.markdown("""
        ### 🚀 시작하기
        
        1. **가사 입력** (Tab 1에서 자동 불러오기)
        2. **스타일 선택** (AI 자동 추천 또는 직접 선택)
        3. **생성 버튼 클릭**
        4. **20개 초고품질 이미지 프롬프트 받기!**
        
        > 💡 2단계 조립 공식으로 장면 묘사 + 스타일이 완벽하게 결합됩니다!
        """)
