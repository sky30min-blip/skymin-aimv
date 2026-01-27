"""
storyboard_config.py - 스토리보드 설정 파일
스타일 가이드 데이터 + AI 시스템 프롬프트
"""

# ============ 스타일 가이드 (11종 + AI 자동 추천) ============

STYLE_GUIDE = {
    "AI 자동 추천": {
        "image_keywords": "",
        "video_keywords": "",
        "effects": "",
        "transitions": "",
        "description": "가사의 장르와 분위기를 분석하여 AI가 최적의 스타일을 선택합니다",
        "preview": "🤖",
        "preview_image": ""
    },
    
    "고퀄리티 일본 애니메이션 (Cinematic Japanese Anime)": {
        "image_keywords": "Modern high-end Japanese anime style, cinematic production value, sharp character lines, highly detailed background, atmospheric lighting effects, masterpiece anime still, high frame rate aesthetic, professional color grading, trending on Pixiv",
        "video_keywords": "Cinematic anime camera movement, dramatic lighting, detailed animation",
        "effects": "Anime motion blur, speed lines, dramatic lighting, lens flare",
        "transitions": "Anime cut, dramatic zoom, fast cuts on beat",
        "description": "Production I.G, WIT Studio 같은 고예산 애니메이션의 한 장면. 선명한 선과 완벽한 배경",
        "preview": "🎬",
        "preview_image": "https://cdn.midjourney.com/20533ac1-924a-4e01-966c-785eb60957b8/0_1.png"
    },
    
    "프리미엄 한국 웹툰 (Premium Korean Webtoon)": {
        "image_keywords": "Premium Korean webtoon style, sharp digital linework, vibrant gradient lighting, manhwa aesthetic, detailed background, modern webtoon masterpiece",
        "video_keywords": "Webtoon panel transition, dramatic lighting changes, emotional closeups",
        "effects": "Gradient overlay, glow effects, dramatic shadows, digital painting texture",
        "transitions": "Panel swipe, fade with glow, dramatic reveal",
        "description": "나 혼자만 레벨업, 어느 날 공주가 되어버렸다 같은 세련된 최신 웹툰 스타일",
        "preview": "📱",
        "preview_image": "https://cdn.midjourney.com/ab3a0859-19ec-4eb9-8554-f04a9113db56/0_2.png"
    },
    
    "클래식 흑백 만화 (Classic Korean Manhwa)": {
        "image_keywords": "Classic Korean Manhwa style, detailed ink drawing, high contrast black and white with gray tones, traditional comic book hatching, 2D hand-drawn aesthetic",
        "video_keywords": "High contrast black and white, dramatic ink effects, classic comic aesthetic",
        "effects": "Film grain, high contrast, ink splatter, halftone texture",
        "transitions": "Comic panel wipe, ink splash transition, page turn effect",
        "description": "정통 흑백 만화 스타일. 세밀한 펜터치와 강렬한 명암 대비",
        "preview": "📖",
        "preview_image": "https://cdn.midjourney.com/007e0390-fcba-4175-a7db-758aeae4438b/0_1.png"
    },
    
    "교토 애니메이션 스타일 (Kyoto Animation)": {
        "image_keywords": "Kyoto Animation style, delicate linework, soft lighting, emotional and serene, transparent colors, high-detail eyes, beautiful light reflections, premium slice-of-life anime aesthetic, hyper-detailed objects",
        "video_keywords": "Soft natural light, gentle camera movement, detailed everyday objects, emotional atmosphere",
        "effects": "Soft bloom, light rays, subtle lens flare, watercolor wash, delicate particles",
        "transitions": "Gentle fade, light transition, soft dissolve, peaceful cuts",
        "description": "바이올렛 에버가든 같은 극강의 섬세함. 투명한 색채와 부드러운 감성",
        "preview": "🌸",
        "preview_image": "https://cdn.midjourney.com/76d004b6-a235-409f-b0dc-41d3c58c8f13/0_1.png"
    },
    
    "수채화 판타지 (Ethereal Watercolor)": {
        "image_keywords": "Dreamy watercolor illustration, soft pastels, fluid edges, emotional atmosphere, artistic brushstrokes, ethereal light, whimsical and poetic, high-end storybook aesthetic, fluid ink wash",
        "video_keywords": "Watercolor bleeding, soft transitions, dreamy atmosphere, floating particles",
        "effects": "Watercolor wash, color bleeding, soft edges, pastel overlay, dreamy glow",
        "transitions": "Watercolor dissolve, color bleed transition, ink wash fade",
        "description": "몽환적인 수채화 느낌. 경계가 번지는 서정적 분위기, 발라드에 최적",
        "preview": "🎨",
        "preview_image": "https://cdn.midjourney.com/89ff3672-f48b-4465-a214-935a8fd19633/0_1.png"
    },
    
    "90년대 사이버펑크 (Classic Cyberpunk)": {
        "image_keywords": "1990s Japanese Cyberpunk anime style, grit and neon, high-tech noir, hand-drawn aesthetic, dramatic shadows, futuristic dystopian cityscape, cinematic lighting, detailed mechanical design, retro sci-fi masterpiece",
        "video_keywords": "Neon-lit streets, rain on cyberpunk city, holographic displays, futuristic vehicles",
        "effects": "Neon glow, chromatic aberration, digital glitch, rain effects, holographic overlay",
        "transitions": "Glitch transition, neon fade, digital wipe, cyberpunk cut",
        "description": "아키라, 공각기동대 같은 묵직하고 거친 느낌의 미래 도시",
        "preview": "🌃",
        "preview_image": "https://cdn.midjourney.com/4fb8a033-3db8-4e8a-8d08-f316471d69b8/0_3.png"
    },
    
    "럭셔리 시티팝 (80s City Pop)": {
        "image_keywords": "Retro Japanese City Pop aesthetic, art style by Hiroshi Nagai and Eizin Suzuki, flat saturated colors, sharp shadows, 1980s luxury anime style, vaporwave sunset, clean minimalist lines, high-end retro illustration",
        "video_keywords": "80s city sunset, luxury car driving, beach scenes, retro Tokyo night",
        "effects": "Vaporwave color grading, sharp shadows, flat color blocks, retro glow",
        "transitions": "Hard cut, color block wipe, retro fade, minimalist transition",
        "description": "80년대 일본 시티팝 앨범 자켓. 강렬한 원색과 미니멀한 선의 세련미",
        "preview": "🌆",
        "preview_image": "https://cdn.midjourney.com/f9a94aba-fc63-4352-a787-c82ae17bbdee/0_0.png"
    },
    
    "신카이 마코토 감성 (Makoto Shinkai)": {
        "image_keywords": "Makoto Shinkai animation style, vibrant lighting, breathtaking sky and clouds, high-detail cityscapes, emotional atmosphere, hyper-detailed lens flare, luminous colors, cinematic background, 4k anime masterpiece",
        "video_keywords": "Dramatic sky timelapses, city lights at dusk, luminous clouds, emotional atmosphere",
        "effects": "God rays, intense lens flare, volumetric lighting, atmospheric glow, light particles",
        "transitions": "Light transition, dramatic sky fade, luminous dissolve, emotional cuts",
        "description": "너의 이름은 처럼 빛의 산란과 구름, 압도적인 배경 퀄리티",
        "preview": "☀️",
        "preview_image": "https://cdn.midjourney.com/81db105a-9d37-401f-b056-3bf8e04f2daa/0_3.png"
    },
    
    "지브리 2.0 (Miyazaki Masterpiece)": {
        "image_keywords": "Studio Ghibli art style by Hayao Miyazaki, lush painterly background, hand-drawn aesthetic, high-quality cel animation, soft natural sunlight, nostalgic atmosphere, cinematic Makoto Shinkai lighting, detailed watercolor texture, high-end anime still",
        "video_keywords": "Lush nature scenes, countryside landscapes, gentle wind, peaceful villages, natural beauty",
        "effects": "Watercolor texture, soft natural light, film grain subtle, painterly overlay, nostalgic glow",
        "transitions": "Cloud transition, gentle fade, nature wipe, peaceful dissolve",
        "description": "거장 미야자키 하야오의 원화 느낌. 수채화 배경과 따뜻한 햇살",
        "preview": "🌿",
        "preview_image": "https://cdn.midjourney.com/b8354c0a-dee9-4c5e-9013-00f3e8726dfa/0_2.png"
    },
    
    "90년대 한국 애니 (90s Korean Anime)": {
        "image_keywords": "1990s Korean anime style, VHS aesthetic, chromatic aberration, bold outlines, traditional Korean gat hat, neon purple and pink lighting, cinematic lofi vibe, retro cel-shaded",
        "video_keywords": "Retro Korean cityscape, VHS aesthetic, traditional meets modern, nostalgic atmosphere",
        "effects": "VHS grain, chromatic aberration, scan lines, color bleeding, retro glow",
        "transitions": "VHS glitch, scan line wipe, retro fade, nostalgic dissolve",
        "description": "90년대 한국 애니메이션 향수. VHS 질감과 전통 요소의 조화",
        "preview": "📼",
        "preview_image": "https://cdn.midjourney.com/d87c768f-65ab-4b5e-8f16-b3256a5627c9/0_1.png"
    },
    
    "90년대 레트로 일본 애니 (90s Retro Anime)": {
        "image_keywords": "Retro 90s anime style, nostalgic, cel shading, vibrant colors, City Pop aesthetic, Lo-fi vibe, purple and blue neon lighting, dreamy atmosphere, vintage aesthetic, VHS grain effect",
        "video_keywords": "Retro city night, neon signs, cassette tapes, CRT TV, vintage cars, 90s nostalgia",
        "effects": "VHS grain, scan lines, color bleeding, lo-fi aesthetic, retro glow",
        "transitions": "VHS glitch, scan line wipe, retro fade, nostalgic cut",
        "description": "향수를 자극하는 90년대 일본 애니 감성. 시티팝과 로파이의 만남",
        "preview": "🎵",
        "preview_image": "https://cdn.midjourney.com/a83587b7-49e2-4830-b20b-1c7d2834d535/0_0.png"
    },
    
    "귀여운 치비 스타일 (Cute Chibi SD)": {
        "image_keywords": "Cute Chibi style, SD Super Deformed character, 2-3 head tall proportions, big sparkling expressive eyes, tiny body, 2D vector art, clean lineart, vibrant pastel colors, kawaii aesthetic, trendy Korean illustration, high quality, detailed, round face, simplified features",
        "video_keywords": "Cute character motion, bouncy animation, expressive facial changes, simple background, kawaii movements",
        "effects": "Sparkle effects, floating heart icons, bright bloom, cartoonish motion lines, star twinkle, bubble pop",
        "transitions": "Pop transition, bouncy slide, circle wipe, heart burst transition",
        "description": "2~3등신의 극강의 귀여움. 웅장한 가사와 대비될 때 폭발적인 병맛 시너지를 냄",
        "preview": "🧸",
        "preview_image": "https://cdn.midjourney.com/8c4e9c72-14f0-4b15-8e5e-5c2f8e3b4d9a/0_1.png"
    }
}


# ============ AI 자동 추천 매핑 ============

STYLE_AUTO_SELECT = {
    # 장르 기반
    "발라드": "수채화 판타지 (Ethereal Watercolor)",
    "시티팝": "럭셔리 시티팝 (80s City Pop)",
    "힙합/랩": "90년대 사이버펑크 (Classic Cyberpunk)",
    "록/메탈": "90년대 사이버펑크 (Classic Cyberpunk)",
    "재즈": "럭셔리 시티팝 (80s City Pop)",
    "트로트": "90년대 한국 애니 (90s Korean Anime)",
    "EDM/일렉트로닉": "90년대 사이버펑크 (Classic Cyberpunk)",
    "동요/키즈": "지브리 2.0 (Miyazaki Masterpiece)",
    "클래식 크로스오버": "교토 애니메이션 스타일 (Kyoto Animation)",
    "Lo-fi/Chill": "90년대 레트로 일본 애니 (90s Retro Anime)",
    
    # Vibe 기반
    "광기/호러": "클래식 흑백 만화 (Classic Korean Manhwa)",
    "슬픈데 신나게": "럭셔리 시티팝 (80s City Pop)",
    "웃기지만 진지하게": "프리미엄 한국 웹툰 (Premium Korean Webtoon)",
}

KEYWORD_STYLE_MAP = {
    "디지털": "90년대 사이버펑크 (Classic Cyberpunk)",
    "코드": "90년대 사이버펑크 (Classic Cyberpunk)",
    "네온": "90년대 사이버펑크 (Classic Cyberpunk)",
    "미래": "90년대 사이버펑크 (Classic Cyberpunk)",
    "애니": "고퀄리티 일본 애니메이션 (Cinematic Japanese Anime)",
    "웹툰": "프리미엄 한국 웹툰 (Premium Korean Webtoon)",
    "만화": "클래식 흑백 만화 (Classic Korean Manhwa)",
    "하늘": "신카이 마코토 감성 (Makoto Shinkai)",
    "구름": "신카이 마코토 감성 (Makoto Shinkai)",
    "자연": "지브리 2.0 (Miyazaki Masterpiece)",
    "시티": "럭셔리 시티팝 (80s City Pop)",
    "레트로": "90년대 레트로 일본 애니 (90s Retro Anime)",
    "귀여운": "귀여운 치비 스타일 (Cute Chibi SD)",
    "치비": "귀여운 치비 스타일 (Cute Chibi SD)",
    "카와이": "귀여운 치비 스타일 (Cute Chibi SD)",
    "병맛": "귀여운 치비 스타일 (Cute Chibi SD)",
}


# ============ 영상 분위기 매핑 ============

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


# ============ 시스템 프롬프트: 20+A/B 버전 ============

SYSTEM_ROLE_20_AB = """당신은 세계적인 뮤직비디오 연출가이자 **대서사시 연계 엔진(Long-form Narrative Engine)** 전문가입니다.

## 당신의 핵심 임무
3~4분 길이의 노래를 완벽히 채울 수 있도록 가사를 분석하여 **20개의 메인 장면**을 구성하고, 각 메인 장면마다 **A컷(와이드샷)과 B컷(클로즈업/디테일샷) 2가지 앵글**을 생성합니다. 총 40개 컷으로 편집 자유도를 극대화합니다.

## ⭐ 1. 20+A/B 구조 (총 40컷) ⭐

### 20개 메인 장면 구성:
- Scene 1-3: 도입부 (Intro)
- Scene 4-7: 전개 1 (Verse 1)
- Scene 8-11: 고조 1 (Chorus 1)
- Scene 12-14: 전환부 (Verse 2)
- Scene 15-16: 브릿지 (Bridge)
- Scene 17-19: 클라이맥스 (Final Chorus)
- Scene 20: 마무리 (Outro)

### A/B 컷 설계:
- **A컷**: 와이드샷 (전신, 환경 포함, 구도 확립)
- **B컷**: 클로즈업/디테일샷 (얼굴, 손, 눈, 감정 강조)

## ⭐ 2. Visual Anchor (전역 앵커) ⭐

**모든 40개 컷에서 반드시 유지:**
1. **주인공 외형:** 의상, 헤어스타일, 신체 특징
2. **핵심 상징물:** 액세서리, 특정 색상 등

## ⭐ 3. Match Cut (장면 계승) ⭐

**n번 메인 장면의 마지막 요소 = n+1번 메인 장면의 시작 요소**

## ⭐ 4. 시각적 직유 (Visual Literalism) ⭐

**Midjourney는 은유를 이해하지 못합니다. 추상적 표현을 100% 물리적 실체로 변환하세요.**

**변환 규칙:**
1. **추상 비유 → 물리적 실체**
   - ❌ "별이 내려온다" → ✅ "Five robed beings descending on beams of starlight"
   - ❌ "희망의 빛" → ✅ "Golden sunbeams breaking through dark clouds"

2. **금지 단어:** "Representing", "Symbolizing", "Concept of", "Metaphor for"

## ⭐ 5. 출력 형식 ⭐

### 구분자:
- 메인 장면 구분: `|||`
- A/B 컷 구분: `@AB@`
- 한글/이미지/모션 구분: `###`, `@@@`

### 출력 예시:

```
빗속에서 슬픈 표정의 소녀 [시작] @AB@ 와이드샷 전신 ### {Visual Anchor}, standing in heavy rain under streetlight, full body visible, wet streets reflecting neon lights @@@ Slow zoom in from wide shot @AB@ 얼굴 클로즈업 ### {Visual Anchor}, close-up of face with rain drops on cheeks, emerald pendant visible in frame @@@ Gentle push-in to extreme close-up |||
```

## 절대 규칙:
1. **정확히 20개 메인 장면**
2. **각 메인 장면마다 A/B 2컷** (총 40컷)
3. 구분자 정확히 사용: `|||`, `@AB@`, `###`, `@@@`
4. **Visual Anchor 100% 유지**
5. **이미지 묘사에 스타일 키워드 포함 금지** (시스템이 자동 추가)

**기억하세요: 20개 메인 장면 × 2컷(A/B) = 총 40컷의 편집 자유도!**"""


# ============ 시스템 프롬프트: 40개 독립 장면 버전 ============

SYSTEM_ROLE_40_INDEPENDENT = """당신은 세계적인 뮤직비디오 연출가이자 **대서사시 연계 엔진(Long-form Narrative Engine)** 전문가입니다.

## 당신의 핵심 임무
3~4분 길이의 노래를 완벽히 채울 수 있도록 가사를 분석하여 **40개의 독립적인 영화적 장면(Scene)**을 구성합니다.

## ⭐ 1. 40개 독립 장면 구성 ⭐

**서사적 배분:**
- Scene 1-5: 도입부 (Intro)
- Scene 6-12: 전개 1 (Verse 1)
- Scene 13-20: 고조 1 (Chorus 1)
- Scene 21-27: 전환부 (Verse 2)
- Scene 28-32: 브릿지 (Bridge)
- Scene 33-37: 클라이맥스 (Final Chorus)
- Scene 38-40: 마무리 (Outro)

## ⭐ 2. Visual Anchor (전역 앵커) ⭐

**모든 40개 장면에서 반드시 유지:**
```
{Visual Anchor} - 모든 장면 첫 부분에 포함
```

## ⭐ 3. Match Cut (장면 계승) ⭐

**n번 장면의 마지막 요소 = n+1번 장면의 시작 요소**

## ⭐ 4. 시각적 직유 (Visual Literalism) ⭐

**추상 비유를 물리적 실체로 100% 변환**

## ⭐ 5. 출력 형식 ⭐

### 구분자:
- 장면 구분: `|||`
- 한글/이미지/모션: `###`, `@@@`

### 출력 예시:

```
빗속에서 슬픈 표정의 소녀 [시작] ### {Visual Anchor}, standing in heavy rain under flickering streetlight, tear-stained cheeks @@@ Slow zoom in ||| 하늘을 올려다보는 모습 [이전: 고개 숙임 → 현재: 하늘 응시] ### {Visual Anchor}, tilts head upward gazing at stormy clouds @@@ Camera pans upward |||
```

## 절대 규칙:
1. **정확히 40개 독립 장면**
2. 구분자: `|||`, `###`, `@@@`
3. **Visual Anchor 100% 유지**
4. **Match Cut 연결점 명시**

**기억하세요: 40개 장면이 하나의 원테이크 영화처럼 흐릅니다!**"""


# ============ 스타일 분석 함수 ============

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
    return "지브리 2.0 (Miyazaki Masterpiece)"
