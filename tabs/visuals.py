"""
tabs/visuals.py - 이미지 생성 탭 (Tab 4)
스타일 프리셋 + AI 자동 추천 + 영상 편집 레시피
"""

import streamlit as st
from utils import get_gpt_response


# ============ 통합 스타일 가이드 (10종+) ============

STYLE_GUIDE = {
    "AI 자동 추천": {
        "image_prompt": "",
        "video_keywords": "",
        "effects": "",
        "transitions": "",
        "description": "가사의 장르와 키워드를 분석하여 AI가 최적의 스타일을 선택합니다",
        "preview": "🤖"
    },
    
    "르네상스 유화 (Renaissance Oil)": {
        "image_prompt": "In the style of a Renaissance oil painting, dramatic chiaroscuro, high detail, religious masterpiece aesthetic, classical composition, golden age painting techniques, museum quality",
        "video_keywords": "Golden hour, candle light, slow motion, museum atmosphere, classical architecture, Renaissance painting, baroque interior, dramatic shadows",
        "effects": "Film grain, warm glow, soft focus, vignette, sepia tone, vintage film overlay",
        "transitions": "Cross dissolve, fade to black, slow zoom, cinematic wipe",
        "description": "고전적이고 웅장한 분위기, 극적인 명암 대비",
        "preview": "🖼️",
        "editing_tips": [
            "🎬 **템포**: 느리고 웅장하게 (60-80 BPM에 맞춤)",
            "✂️ **컷 타이밍**: 4박자마다 장면 전환 (바로크 음악의 리듬)",
            "🎨 **색보정**: 따뜻한 톤 (Orange 30%, Teal -20%)",
            "💡 **조명**: Golden hour 영상 위주, 촛불 클로즈업"
        ]
    },
    
    "80년대 디스코 팝아트 (80s Disco Pop-Art)": {
        "image_prompt": "Vibrant 80s disco pop art style, neon colors, halftone patterns, funky and energetic, retro groovy aesthetic, bold geometric shapes, Andy Warhol inspired",
        "video_keywords": "Dancing lights, disco ball, city neon, retro party, 80s fashion, roller skating, arcade games, VHS aesthetic, dance floor",
        "effects": "Glitch effect, RGB split, strobe lights, chromatic aberration, VHS distortion, neon glow, halftone dots",
        "transitions": "Glitch transition, whip pan, beat-synced cuts, kaleidoscope effect",
        "description": "화려한 네온 컬러, 에너지 넘치는 레트로 감성",
        "preview": "🕺",
        "editing_tips": [
            "🎬 **템포**: 빠르고 경쾌하게 (110-130 BPM)",
            "✂️ **컷 타이밍**: 비트마다 빠른 컷 (0.5초 간격)",
            "🎨 **색보정**: 네온 강조 (Saturation +40%, Contrast +20%)",
            "💡 **필수 요소**: 디스코 볼 반짝임, RGB 글리치"
        ]
    },
    
    "한국 민화 모던 (Modern Korean Minhwa)": {
        "image_prompt": "Modernized Korean Minhwa style, traditional ink and wash brushwork, witty and colorful traditional depiction, Korean folk art aesthetic, symbolic animals and flowers, vibrant but harmonious colors",
        "video_keywords": "Traditional Korean village, paper texture, nature scenes, joyful feast, hanbok, traditional market, Korean nature, folk dance, paper art animation",
        "effects": "Ink splash transition, paper overlay, watercolor bleeding, traditional pattern overlay, brush stroke animation",
        "transitions": "Ink wash wipe, paper tear transition, folding screen effect",
        "description": "전통과 현대가 조화된 한국적 감성",
        "preview": "🎨",
        "editing_tips": [
            "🎬 **템포**: 경쾌하고 리드미컬 (90-110 BPM)",
            "✂️ **컷 타이밍**: 전통 장단에 맞춰 (3박, 4박 혼합)",
            "🎨 **색보정**: 오방색 강조 (빨강, 파랑, 노랑, 검정, 흰색)",
            "💡 **특수효과**: 종이 질감 오버레이, 먹물 번짐"
        ]
    },
    
    "지브리 애니메이션 (Studio Ghibli)": {
        "image_prompt": "Studio Ghibli animation style, hand-drawn cel animation, lush landscapes, soft watercolor textures, nostalgic atmosphere, Hayao Miyazaki aesthetic, dreamy and whimsical",
        "video_keywords": "Nature scenes, countryside, clouds moving, peaceful village, train journey, sky view, green fields, gentle breeze, sunset horizon",
        "effects": "Watercolor wash, soft bloom, film grain (subtle), hand-drawn overlay, dreamy atmosphere",
        "transitions": "Cloud transition, gentle fade, parallax scrolling, sky wipe",
        "description": "따뜻하고 섬세한 손그림 애니메이션",
        "preview": "🌿",
        "editing_tips": [
            "🎬 **템포**: 잔잔하고 서정적 (70-90 BPM)",
            "✂️ **컷 타이밍**: 여유있게 (2-4초 지속)",
            "🎨 **색보정**: 파스텔톤 (Saturation -10%, 따뜻한 필터)",
            "💡 **필수 요소**: 구름 타임랩스, 자연 풍경"
        ]
    },
    
    "사이버펑크 2077 (Cyberpunk Noir)": {
        "image_prompt": "Cyberpunk 2077 style, high-tech noir aesthetic, neon-soaked streets, cinematic lighting, futuristic and gritty digital art, dystopian cityscape, holographic effects",
        "video_keywords": "Neon city night, rain on street, hologram display, futuristic interface, cyberpunk street, digital glitch, robot movement, flying cars",
        "effects": "Neon glow, digital glitch, holographic overlay, chromatic aberration, rain effect, lens flare, data stream",
        "transitions": "Digital glitch, matrix transition, hologram flicker, cybernetic wipe",
        "description": "네온과 어둠이 공존하는 미래 도시",
        "preview": "🌃",
        "editing_tips": [
            "🎬 **템포**: 강렬하고 날카롭게 (100-140 BPM)",
            "✂️ **컷 타이밍**: 비트에 정확히 맞춤, 갑작스런 컷",
            "🎨 **색보정**: 사이언 + 마젠타 (Teal +30%, Magenta +20%)",
            "💡 **필수 요소**: 네온 반사, 비 오는 밤거리"
        ]
    },
    
    "언리얼 엔진 5 렌더 (UE5 Photorealistic)": {
        "image_prompt": "Unreal Engine 5 render, hyper-realistic 3D visualization, volumetric lighting, photorealistic textures, ray-traced reflections, movie-like cinematic quality, AAA game graphics",
        "video_keywords": "Cinematic camera movement, dramatic lighting, slow motion action, epic landscape, photorealistic human, detailed textures, volumetric fog",
        "effects": "Lens flare, depth of field, motion blur, volumetric lighting, god rays, chromatic aberration",
        "transitions": "Camera pan, dramatic zoom, fade with light leak, cinematic wipe",
        "description": "초사실적인 3D 렌더링, 영화 같은 품질",
        "preview": "💎",
        "editing_tips": [
            "🎬 **템포**: 영화적으로 다이나믹 (80-120 BPM)",
            "✂️ **컷 타이밍**: 액션 신에 맞춤, 슬로우 모션 활용",
            "🎨 **색보정**: 시네마틱 LUT (영화 같은 색감)",
            "💡 **필수 요소**: Lens flare, 부드러운 피사체 심도"
        ]
    },
    
    "픽사 3D 애니메이션 (Pixar 3D)": {
        "image_prompt": "Pixar Disney 3D animation style, expressive character design, vibrant colors, soft ambient lighting, family-friendly aesthetic, rounded shapes, heartwarming atmosphere",
        "video_keywords": "Cartoon character, playful animation, bright colors, bouncing movement, happy expressions, colorful environment, fun activities",
        "effects": "Cartoon motion blur, exaggerated movement, bounce effect, sparkle overlay, bright highlights",
        "transitions": "Bounce transition, pop-in effect, playful wipe, cartoon zoom",
        "description": "귀엽고 생동감 넘치는 3D 애니메이션",
        "preview": "🎬",
        "editing_tips": [
            "🎬 **템포**: 경쾌하고 활기차게 (100-130 BPM)",
            "✂️ **컷 타이밍**: 탄력있게, 동작에 맞춰 컷",
            "🎨 **색보정**: 채도 높게 (Saturation +30%, Vibrance +20%)",
            "💡 **필수 요소**: 과장된 움직임, 표정 클로즈업"
        ]
    },
    
    "반 고흐 인상파 (Van Gogh Impressionism)": {
        "image_prompt": "In the style of Vincent van Gogh, post-impressionist brushwork, swirling brushstrokes, vibrant impasto texture, emotional color palette, Starry Night aesthetic",
        "video_keywords": "Starry night sky, swirling clouds, countryside, sunflower field, wheat field, cafe scene, artist studio, moonlight",
        "effects": "Oil painting effect, brushstroke overlay, impasto texture, color vibration, painterly filter",
        "transitions": "Brush stroke wipe, paint splash transition, swirling transition",
        "description": "소용돌이치는 붓터치, 감성적 색채",
        "preview": "🌌",
        "editing_tips": [
            "🎬 **템포**: 감정적이고 표현적 (60-90 BPM)",
            "✂️ **컷 타이밍**: 감정선에 따라 자연스럽게",
            "🎨 **색보정**: 강렬한 원색 (파랑, 노랑 강조)",
            "💡 **필수 요소**: 붓터치 효과, 소용돌이 패턴"
        ]
    },
    
    "미니멀 라인 아트 (Minimal Line Art)": {
        "image_prompt": "Minimalist line art illustration, single continuous line drawing, simple elegant composition, negative space emphasis, modern clean aesthetic, vector art style",
        "video_keywords": "Simple shapes, geometric patterns, clean lines, white background, minimalist design, abstract forms, elegant movement",
        "effects": "Line drawing animation, minimalist transition, clean fade, geometric overlay",
        "transitions": "Line wipe, geometric reveal, minimal fade, shape morphing",
        "description": "깔끔하고 세련된 라인 드로잉",
        "preview": "✏️",
        "editing_tips": [
            "🎬 **템포**: 모던하고 세련되게 (90-120 BPM)",
            "✂️ **컷 타이밍**: 정확하고 깔끔한 컷",
            "🎨 **색보정**: 단색 또는 2-3색 제한",
            "💡 **필수 요소**: 선 그리기 애니메이션, 여백 활용"
        ]
    },
    
    "다크 판타지 (Dark Fantasy)": {
        "image_prompt": "Dark fantasy illustration, gothic aesthetic, dramatic shadows, mysterious atmosphere, ethereal lighting, medieval dark ages inspiration, moody and atmospheric",
        "video_keywords": "Dark castle, foggy forest, moonlight, ravens, gothic architecture, mysterious ritual, shadow movement, torch light",
        "effects": "Dark vignette, fog overlay, light rays, shadow enhancement, desaturation, eerie glow",
        "transitions": "Shadow wipe, fade to black, smoke transition, mysterious reveal",
        "description": "어둡고 신비로운 판타지 세계관",
        "preview": "🌑",
        "editing_tips": [
            "🎬 **템포**: 느리고 불안하게 (60-80 BPM)",
            "✂️ **컷 타이밍**: 긴장감 유지, 갑작스런 컷 활용",
            "🎨 **색보정**: 저채도, 어두운 톤 (Shadows -30%)",
            "💡 **필수 요소**: 안개 효과, 불빛 플리커"
        ]
    },
    
    "레트로 게임 픽셀아트 (Retro Pixel Art)": {
        "image_prompt": "16-bit pixel art style, retro video game aesthetic, limited color palette, crisp pixel-perfect rendering, nostalgic 90s gaming vibe, isometric or side-view",
        "video_keywords": "Retro game screen, pixel animation, 8-bit graphics, arcade games, game console, retro TV, pixel art characters",
        "effects": "Pixelate effect, CRT scanlines, screen glitch, retro color palette, bit crush",
        "transitions": "Pixel dissolve, screen transition, game over effect, loading screen",
        "description": "향수를 자극하는 레트로 픽셀 그래픽",
        "preview": "🎮",
        "editing_tips": [
            "🎬 **템포**: 리드미컬하고 중독적 (100-140 BPM)",
            "✂️ **컷 타이밍**: 8비트 음악 리듬에 맞춤",
            "🎨 **색보정**: 제한된 팔레트 (8-16색)",
            "💡 **필수 요소**: CRT 스캔라인, 픽셀 애니메이션"
        ]
    }
}


# ============ AI 자동 추천 매핑 (확장) ============

STYLE_AUTO_SELECT = {
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

# 키워드 기반 추천 (가사 분석용)
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
    """
    가사, 장르, Vibe를 분석하여 최적의 스타일을 추천합니다.
    
    Args:
        lyrics: 가사 텍스트
        genre: 장르
        vibe: 분위기
        
    Returns:
        추천 스타일 이름
    """
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


SYSTEM_ROLE = """당신은 AI 이미지 생성 프롬프트 전문가이며, **2단계 조립 공식(Two-Step Assembly Formula)**을 완벽히 구사합니다.

## 당신의 핵심 임무
사용자가 제공한 가사/주제를 분석하여 Midjourney/DALL-E/Stable Diffusion에서 최상의 결과를 내는 프롬프트를 **2단계 조립 공식**에 따라 작성합니다.

## ⭐ 2단계 조립 공식 (Two-Step Assembly Formula) ⭐

### Step 1: Subject Generation (장면 묘사 생성)
가사 내용을 분석하여 **구체적인 핵심 장면**을 영어로 1-2문장 생성합니다.

**필수 포함 요소:**
1. **주체(Subject)**: 인물, 사물, 배경의 구체적 묘사
2. **행위/상태(Action/State)**: 무엇을 하고 있는지, 어떤 상태인지
3. **분위기(Atmosphere)**: 감정, 시간대, 날씨 등

**예시:**
- 가사: "새벽 카페에서 혼자 커피를 마시며 옛 연인을 그리워한다"
- Step 1 결과: `"A lonely young woman sitting by a rain-streaked window in a dimly lit cafe at midnight, warm amber lighting from vintage lamps, steam rising from a coffee cup, melancholic atmosphere"`

### Step 2: Style Integration (스타일 키워드 결합)
Step 1의 장면 묘사 뒤에 **선택된 스타일 키워드**를 자연스럽게 결합합니다.

**공식:**
```
[Step 1 장면 묘사] + ", in the style of" + [Style Keywords] + [품질 태그]
```

**최종 프롬프트 예시:**
```
A lonely young woman sitting by a rain-streaked window in a dimly lit cafe at midnight, warm amber lighting from vintage lamps, steam rising from a coffee cup, melancholic atmosphere, in the style of a Renaissance oil painting, dramatic chiaroscuro, high detail, museum quality, 8K resolution, masterpiece
```

## 장면 묘사 작성 규칙 (Step 1 상세)

### 1. 구체적 시각 정보만 사용
- ❌ 나쁜 예: "슬픈 장면", "아름다운 순간"
- ✅ 좋은 예: "A person with tear-stained cheeks, hands covering face, slouched posture"

### 2. 감각적 디테일 포함
- 조명: "golden hour sunlight", "neon glow", "candlelight flickering"
- 색감: "warm orange tones", "cool blue atmosphere", "vibrant neon colors"
- 질감: "rain-streaked glass", "worn leather jacket", "soft fabric flowing"

### 3. 구도와 앵글 명시
- "close-up portrait", "wide angle view", "bird's eye view", "low angle shot"
- "cinematic composition", "centered framing", "rule of thirds"

### 4. 가사의 핵심 감정 시각화
- 가사: "디지털 코드 속에 갇힌 영혼"
- 시각화: "A human silhouette trapped inside glowing digital code matrix, surrounded by floating binary numbers, holographic prison bars made of data streams"

## 품질 태그 (Quality Tags)
Step 2 마지막에 추가:
- 해상도: "4K", "8K", "high resolution"
- 품질: "highly detailed", "masterpiece", "professional quality"
- 렌더링: "octane render", "unreal engine" (필요시)

## 출력 형식 (반드시 준수!)

**[장면 분석]**
(가사/주제에서 포착한 핵심 장면 설명 - 한국어 1-2문장)

**[Step 1: 장면 묘사]**
(영어 장면 묘사만)

**[Step 2: 최종 프롬프트]**
(장면 묘사 + 스타일 키워드 + 품질 태그)

**[한글 설명]**
(최종 이미지 컨셉 설명 2-3문장)

## 예시 출력

**[장면 분석]**
새벽 카페에서 창밖을 바라보며 옛 연인을 그리워하는 여성의 고독한 순간

**[Step 1: 장면 묘사]**
A lonely young woman sitting by a rain-streaked window in a dimly lit cafe at midnight, warm amber lighting from vintage lamps, steam rising from a coffee cup, looking out at empty streets

**[Step 2: 최종 프롬프트]**
A lonely young woman sitting by a rain-streaked window in a dimly lit cafe at midnight, warm amber lighting from vintage lamps, steam rising from a coffee cup, looking out at empty streets, in the style of a Renaissance oil painting, dramatic chiaroscuro, high detail, religious masterpiece aesthetic, classical composition, museum quality, 8K resolution, masterpiece

**[한글 설명]**
새벽 카페의 고독한 여성을 르네상스 유화 기법으로 표현합니다. 극적인 명암 대비가 내면의 슬픔을 부각시키며, 고전적 구도가 보편적 감정을 담아냅니다."""


def parse_image_prompt(response: str) -> dict:
    """GPT 응답에서 장면 분석, Step 1, Step 2, 설명을 추출합니다."""
    result = {
        'scene_analysis': '',
        'step1_scene': '',
        'step2_final': '',
        'description': ''
    }
    
    # 장면 분석 추출
    if '[장면 분석]' in response or '**[장면 분석]**' in response:
        start = response.find('[장면 분석]')
        if start == -1:
            start = response.find('**[장면 분석]**')
        end = response.find('[Step 1', start)
        if end == -1:
            end = response.find('**[Step 1', start)
        if end != -1:
            section = response[start:end]
            lines = section.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('[') and not line.startswith('**'):
                    result['scene_analysis'] += line.strip() + ' '
            result['scene_analysis'] = result['scene_analysis'].strip()
    
    # Step 1 장면 묘사 추출
    if '[Step 1' in response or '**[Step 1' in response:
        start = response.find('[Step 1')
        if start == -1:
            start = response.find('**[Step 1')
        end = response.find('[Step 2', start)
        if end == -1:
            end = response.find('**[Step 2', start)
        if end != -1:
            section = response[start:end]
            lines = section.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('[') and not line.startswith('**'):
                    result['step1_scene'] += line.strip() + ' '
            result['step1_scene'] = result['step1_scene'].strip()
    
    # Step 2 최종 프롬프트 추출
    if '[Step 2' in response or '**[Step 2' in response:
        start = response.find('[Step 2')
        if start == -1:
            start = response.find('**[Step 2')
        end = response.find('[한글 설명]', start)
        if end == -1:
            end = response.find('**[한글 설명]**', start)
        if end == -1:
            end = response.find('[설명]', start)
        if end != -1:
            section = response[start:end]
            lines = section.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('[') and not line.startswith('**'):
                    result['step2_final'] += line.strip() + ' '
            result['step2_final'] = result['step2_final'].strip()
    
    # 한글 설명 추출
    desc_markers = ['[한글 설명]', '**[한글 설명]**', '[설명]', '**[설명]**']
    for marker in desc_markers:
        if marker in response:
            start = response.find(marker)
            section = response[start:]
            lines = section.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('[') and not line.startswith('**'):
                    result['description'] += line.strip() + ' '
            result['description'] = result['description'].strip()
            break
    
    return result


def render(client):
    """이미지 생성 탭을 렌더링합니다."""
    
    st.header("🎨 Step 4: AI 이미지 생성 + 영상 편집 가이드")
    st.markdown("""
    가사 주제를 바탕으로 **독특한 스타일의 이미지 프롬프트**와 **유튜브 편집 레시피**를 생성합니다.
    
    > 🎯 *"AI 자동 추천 + 10가지 스타일 + 편집 가이드"*
    """)
    
    st.info("""
    ✨ **이 탭에서 제공하는 것:**
    1. 🎨 **이미지 생성 프롬프트** - Midjourney/DALL-E용
    2. 🎬 **영상 편집 레시피** - 스톡 영상 키워드, 전환효과, 특수효과
    3. 📋 **편집 가이드** - 템포, 컷 타이밍, 색보정 팁
    """)
    
    st.divider()
    
    # ============ 주제 입력 ============
    st.subheader("🖼️ 이미지 주제")
    
    # Tab 1에서 가사 주제 자동 불러오기
    default_topic = st.session_state.get("lyrics_topic", "")
    default_lyrics = st.session_state.get("lyrics", "")
    
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
    st.subheader("🎨 비주얼 스타일")
    
    # 현재 장르/Vibe/가사 가져오기
    current_genre = st.session_state.get("lyrics_genre", "")
    current_vibe = st.session_state.get("lyrics_vibe", "")
    
    # AI 자동 추천 스타일
    auto_recommended = None
    if current_genre or current_vibe or default_lyrics:
        auto_recommended = analyze_lyrics_for_style(default_lyrics, current_genre, current_vibe)
        st.success(f"🤖 **AI 추천 스타일:** {auto_recommended}")
        
        if current_genre:
            st.caption(f"📊 분석: 장르({current_genre}), Vibe({current_vibe})")
        
        # 추천 이유 표시
        if default_lyrics:
            found_keywords = [kw for kw in KEYWORD_STYLE_MAP.keys() if kw in default_lyrics.lower()]
            if found_keywords:
                st.caption(f"🔍 가사 키워드 발견: {', '.join(found_keywords[:3])}")
    
    # 스타일 선택
    style_options = list(STYLE_GUIDE.keys())
    
    selected_style = st.selectbox(
        "이미지 스타일 선택",
        options=style_options,
        help="'AI 자동 추천'을 선택하면 가사 분석 결과에 맞는 스타일이 자동으로 적용됩니다"
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
    
    # 스타일 미리보기 (전체)
    with st.expander("🎨 모든 스타일 미리보기"):
        for style_name, style_data in STYLE_GUIDE.items():
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
    if st.button("🎨 이미지 프롬프트 + 편집 가이드 생성", type="primary", use_container_width=True):
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
        
        # 스타일 데이터 가져오기
        style_data = STYLE_GUIDE[final_style]
        style_keywords = style_data["image_prompt"]
        
        # 고급 옵션 반영
        additional_keywords = []
        if composition != "자동":
            additional_keywords.append(composition.lower())
        if lighting != "자동":
            additional_keywords.append(lighting.lower())
        
        additional_text = ", ".join(additional_keywords) if additional_keywords else ""
        
        # 사용자 프롬프트 구성
        user_prompt = f"""다음 주제와 스타일을 결합하여 **2단계 조립 공식**에 따라 최상의 이미지 프롬프트를 작성해주세요.

## 주제/가사 내용
{image_topic}

## 선택된 스타일
{final_style}

## 스타일 키워드 (Step 2에서 사용)
{style_keywords}

## 추가 요청사항
{additional_text if additional_text else "없음"}

## ⭐ 작성 절차 (반드시 준수) ⭐

### Step 1: Subject Generation (장면 묘사)
위 주제/가사를 분석하여 구체적인 장면을 영어로 1-2문장 생성하세요.
- 필수: 주체(인물/사물), 행위/상태, 분위기
- 구체적 시각 정보만 사용 (추상적 표현 금지)
- 조명, 색감, 구도 포함

### Step 2: Style Integration (스타일 결합)
Step 1의 장면 묘사 뒤에 제공된 스타일 키워드를 결합하세요.
- 공식: [Step 1] + ", in the style of" + [스타일 키워드] + [품질 태그]

## 출력 형식 (정확히 준수!)

**[장면 분석]**
(한국어 1-2문장)

**[Step 1: 장면 묘사]**
(영어 장면 묘사만)

**[Step 2: 최종 프롬프트]**
(Step 1 + 스타일 키워드 + 품질 태그)

**[한글 설명]**
(최종 컨셉 설명 2-3문장)

지금 바로 위 형식으로 프롬프트를 작성해주세요!"""

        with st.spinner("🎨 AI가 이미지 프롬프트와 편집 가이드를 생성하고 있습니다..."):
            try:
                response = get_gpt_response(client, SYSTEM_ROLE, user_prompt)
                
                # 파싱
                parsed = parse_image_prompt(response)
                
                # 세션 스테이트에 저장
                st.session_state["image_prompt"] = parsed
                st.session_state["image_style"] = final_style
                st.session_state["image_topic"] = image_topic
                st.session_state["image_raw"] = response
                
                st.success("🎉 이미지 프롬프트와 편집 가이드가 생성되었습니다!")
                st.rerun()
                
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
                return
    
    # ============ 결과 표시 ============
    st.divider()
    
    if "image_prompt" in st.session_state and st.session_state["image_prompt"]:
        parsed = st.session_state["image_prompt"]
        final_style = st.session_state.get("image_style", "")
        style_data = STYLE_GUIDE.get(final_style, {})
        
        # 메타 정보
        st.caption(f"🎨 스타일: **{final_style}**")
        
        st.divider()
        
        # ============ 2단계 조립 과정 시각화 ============
        st.subheader("🔧 2단계 프롬프트 조립 과정")
        
        # 장면 분석
        if parsed.get('scene_analysis'):
            st.markdown("### 📋 장면 분석")
            st.info(parsed['scene_analysis'])
        
        # Step 1: 장면 묘사
        if parsed.get('step1_scene'):
            st.markdown("### 🎬 Step 1: 장면 묘사 (Subject Generation)")
            st.code(parsed['step1_scene'], language=None)
            st.caption("💡 가사/주제를 구체적인 시각 정보로 변환")
        
        # Step 2: 최종 프롬프트
        if parsed.get('step2_final'):
            st.markdown("### ✨ Step 2: 최종 프롬프트 (Style Integration)")
            st.code(parsed['step2_final'], language=None)
            st.caption("💡 Step 1 + 스타일 키워드 + 품질 태그")
        
        # 한글 설명
        if parsed.get('description'):
            st.divider()
            st.success(f"📖 **컨셉:** {parsed['description']}")
        
        st.divider()
        
        # ============ 최종 프롬프트 (복사용) ============
        st.subheader("📋 최종 이미지 프롬프트 (복사용)")
        
        final_prompt = parsed.get('step2_final', '')
        if final_prompt:
            st.code(final_prompt, language=None)
            st.caption("👆 위 프롬프트를 Midjourney/DALL-E/Stable Diffusion에 붙여넣으세요!")
        else:
            st.warning("프롬프트 생성에 실패했습니다. 다시 시도해주세요.")
        
        st.divider()
        
        # ============ 영상 편집 레시피 ============
        st.subheader("🎬 유튜브 영상 편집 가이드")
        
        if style_data:
            # 탭으로 구성
            tab1, tab2, tab3, tab4 = st.tabs([
                "📹 스톡 영상 키워드",
                "✨ 특수 효과",
                "🔄 화면 전환",
                "🎯 편집 팁"
            ])
            
            with tab1:
                st.markdown("### 📹 추천 스톡 영상 검색 키워드")
                st.markdown("**무료 스톡 영상 사이트에서 검색하세요:**")
                st.success("🔍 Pexels, Pixabay, Videvo, Mixkit")
                
                if style_data.get("video_keywords"):
                    keywords_list = [kw.strip() for kw in style_data["video_keywords"].split(',')]
                    
                    st.markdown("**추천 키워드:**")
                    for i, keyword in enumerate(keywords_list, 1):
                        st.markdown(f"{i}. `{keyword}`")
                    
                    # 전체 복사
                    st.divider()
                    st.code(style_data["video_keywords"], language=None)
                    st.caption("👆 위 키워드들을 복사해서 스톡 영상 사이트에서 검색하세요")
            
            with tab2:
                st.markdown("### ✨ 추천 특수 효과 (Effects)")
                
                if style_data.get("effects"):
                    effects_list = [fx.strip() for fx in style_data["effects"].split(',')]
                    
                    st.markdown("**프리미어/다빈치 리졸브에서 적용:**")
                    for i, effect in enumerate(effects_list, 1):
                        st.markdown(f"{i}. 🎨 **{effect}**")
                    
                    st.divider()
                    st.info("""
                    💡 **효과 적용 팁:**
                    - 과하지 않게, 음악과 어울리게
                    - 클라이맥스에서 효과 강화
                    - 일관된 스타일 유지
                    """)
            
            with tab3:
                st.markdown("### 🔄 추천 화면 전환 (Transitions)")
                
                if style_data.get("transitions"):
                    transitions_list = [tr.strip() for tr in style_data["transitions"].split(',')]
                    
                    st.markdown("**추천 전환 효과:**")
                    for i, transition in enumerate(transitions_list, 1):
                        st.markdown(f"{i}. ➡️ **{transition}**")
                    
                    st.divider()
                    st.warning("""
                    ⚠️ **전환 사용 주의:**
                    - 비트에 맞춰 전환
                    - 한 영상에 2-3가지만 사용
                    - 남발하지 말 것
                    """)
            
            with tab4:
                st.markdown("### 🎯 편집 실전 팁")
                
                if style_data.get("editing_tips"):
                    for tip in style_data["editing_tips"]:
                        st.markdown(tip)
                    
                    st.divider()
                    st.success("""
                    ✅ **편집 체크리스트:**
                    - [ ] 템포에 맞는 컷 편집
                    - [ ] 색보정 일관성 유지
                    - [ ] 클라이맥스 강조
                    - [ ] 전환 효과 적절히 사용
                    - [ ] 스타일 통일성 유지
                    """)
                else:
                    st.info("이 스타일에 대한 편집 팁이 준비 중입니다.")
        
        st.divider()
        
        # ============ 통합 레시피 (복사용) ============
        st.subheader("📋 통합 편집 레시피 (복사용)")
        
        scene_title = parsed.get('scene_analysis', '이미지 프롬프트')[:50]
        
        recipe_text = f"""# {scene_title} - 편집 레시피

## 🎨 스타일
{final_style}

## 🎬 최종 이미지 프롬프트
{parsed.get('step2_final', '-')}

## 📹 스톡 영상 검색 키워드
{style_data.get('video_keywords', '-')}

## ✨ 특수 효과
{style_data.get('effects', '-')}

## 🔄 화면 전환
{style_data.get('transitions', '-')}

## 🎯 편집 팁
"""
        
        if style_data.get("editing_tips"):
            for tip in style_data["editing_tips"]:
                recipe_text += f"{tip}\n"
        
        st.text_area(
            "전체 레시피",
            value=recipe_text,
            height=400,
            label_visibility="collapsed"
        )
        
        # 다운로드 버튼
        col1, col2 = st.columns(2)
        
        final_prompt = parsed.get('step2_final', '')
        scene_analysis = parsed.get('scene_analysis', '')
        
        with col1:
            st.download_button(
                label="📥 최종 프롬프트 다운로드",
                data=final_prompt,
                file_name=f"image_prompt_{final_style.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            st.download_button(
                label="📥 편집 레시피 다운로드",
                data=recipe_text,
                file_name=f"editing_recipe_{final_style.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        # 사용 안내
        st.divider()
        st.success("""
        🎉 **이미지 프롬프트 + 편집 가이드 완성!**
        
        **다음 단계:**
        1. 📸 **이미지 생성**: 프롬프트를 Midjourney/DALL-E에서 실행
        2. 🎬 **스톡 영상 다운로드**: 추천 키워드로 무료 영상 검색
        3. ✂️ **영상 편집**: 편집 레시피에 따라 프리미어/다빈치에서 편집
        4. 🎵 **음악 합성**: Suno/Udio에서 생성한 음악 추가
        5. 🚀 **유튜브 업로드**: 완성된 뮤직비디오 공유!
        
        💡 **무료 스톡 영상 사이트:**
        - Pexels: https://www.pexels.com/videos/
        - Pixabay: https://pixabay.com/videos/
        - Videvo: https://www.videvo.net/
        - Mixkit: https://mixkit.co/free-stock-video/
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
           - AI 자동 추천: 가사 분석 후 최적 스타일 자동 선택
           - 직접 선택: 10가지 독특한 스타일 중 선택
        
        3. **생성 버튼** 클릭
        
        4. **이미지 프롬프트 + 영상 편집 레시피** 받기!
        
        > 💡 이미지 생성부터 영상 편집까지, 모든 가이드를 한 번에!
        """)
