"""
tabs/storyboard.py - 스토리보드 생성 탭 (완전판 All-in-One)
원본 3개 파일의 모든 기능 포함
"""

import streamlit as st
from utils import get_gpt_response


# ============================================================================
# CONFIG 데이터 (storyboard_config.py 내용)
# ============================================================================


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


# ============================================================================
# UTILS 함수들 (storyboard_utils.py 내용)
# ============================================================================


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


# ============================================================================
# 메인 RENDER 함수 (tabs/storyboard.py 내용)
# ============================================================================

def render(client):
    """스토리보드 탭을 렌더링합니다."""
    
    # 장면 수정 상태 초기화
    initialize_scene_overrides()
    
    st.header("🎬 Step 3: 대서사시 스토리보드 생성")
    st.markdown("""
    가사를 분석하여 **초고품질 이미지 프롬프트**를 생성합니다.
    
    > 🎥 *"대서사시 연계 엔진 + 시각적 연속성 + 실시간 수정 + AI 추천"*
    """)
    
    st.success("""
    ✨ **v2.1 완전 업그레이드:**
    1. 🎨 **11가지 프리미엄 스타일** - 실제 이미지 미리보기
    2. 🎬 **장면 방식 선택** - 20개+A/B컷 or 40개 독립 장면
    3. 🔗 **시각적 연속성** - Match Cut 원테이크 영화
    4. ⚓ **Visual Anchor** - AI 자동 추천 또는 직접 입력
    5. 🎨 **--cref + --sref** - 이중 URL 고정
    6. ✏️ **실시간 수동 수정** - 각 장면 직접 편집
    """)
    
    st.divider()
    
    # ============ 장면 생성 방식 선택 ============
    st.subheader("🎬 장면 생성 방식 선택")
    
    scene_mode = st.radio(
        "원하는 방식을 선택하세요",
        options=[
            "20개 메인 장면 + A/B 앵글 (총 40컷)",
            "40개 독립 장면"
        ],
        help="""
        • 20+A/B: 편집 자유도 최대 (같은 장면을 와이드/클로즈업 2가지로)
        • 40개: 서사 풍부함 최대 (모두 다른 장면)
        """,
        horizontal=True
    )
    
    if scene_mode == "20개 메인 장면 + A/B 앵글 (총 40컷)":
        st.info("""
        📐 **20+A/B 구조:**
        - 20개 메인 장면
        - 각 장면마다 A컷(와이드샷) + B컷(클로즈업) = 총 40컷
        - 편집 시 A만, B만, 또는 A→B 순서로 자유롭게 조합 가능
        """)
        selected_mode = "20_AB"
    else:
        st.info("""
        🎞️ **40개 독립 장면:**
        - 모두 완전히 다른 장면
        - 서사가 풍부하게 전개
        - 3~4분 영상을 완벽히 채움
        """)
        selected_mode = "40_INDEPENDENT"
    
    st.divider()
    
    # ============ 가사 입력 ============
    st.subheader("📝 가사 입력")
    default_lyrics = st.session_state.get("lyrics", "")
    
    lyrics_input = st.text_area(
        "뮤직비디오에 사용할 가사",
        value=default_lyrics,
        height=250,
        placeholder="[Verse 1]\n여기에 가사를 입력하세요...",
        help="가사를 기반으로 장면이 생성됩니다"
    )
    
    if default_lyrics:
        st.caption("💡 Tab 1에서 생성한 가사가 자동으로 불러와졌습니다.")
    
    st.divider()
    
    # ============ 일관성 장치 (Character & Style URLs) ============
    st.subheader("🔗 일관성 장치 (Character & Style URLs)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🧑 캐릭터 참조 URL")
        default_char_url = st.session_state.get("master_image_url", "")
        
        char_url = st.text_input(
            "캐릭터 이미지 URL (--cref)",
            value=default_char_url,
            placeholder="https://cdn.midjourney.com/...",
            help="Tab 2에서 생성한 캐릭터 이미지 URL",
            key="char_url_input"
        )
        
        if default_char_url:
            st.caption("💡 Tab 2에서 저장한 URL이 불러와졌습니다.")
    
    with col2:
        st.markdown("#### 🎨 스타일 참조 URL")
        default_style_url = st.session_state.get("style_reference_url", "")
        
        style_url = st.text_input(
            "스타일(화풍) 이미지 URL (--sref)",
            value=default_style_url,
            placeholder="https://cdn.midjourney.com/...",
            help="모든 장면의 색감/질감을 고정할 참조 이미지 URL",
            key="style_url_input"
        )
        
        if style_url:
            st.caption("✅ 스타일 URL이 입력되었습니다. (--sw 1000 자동 적용)")
        else:
            st.info("💡 스타일 URL을 입력하면 모든 장면의 화풍이 완벽히 통일됩니다.")
    
    st.divider()
    
    # ============ ⭐ Visual Anchor 설정 (AI 추천 기능 포함) ============
    st.subheader("⚓ Visual Anchor (전역 앵커)")
    st.markdown("""
    **모든 장면에 공통으로 적용될 주인공의 외형**을 정의하세요.
    이것이 시각적 일관성의 핵심입니다!
    """)
    
    # ⭐ Tab 2에서 만든 캐릭터 자동 불러오기 (개선 버전)
    tab2_character_loaded = False
    
    # 방법 1: character_prompt에서 영어 부분 추출 시도
    if "character_prompt" in st.session_state and st.session_state["character_prompt"]:
        prompt_text = st.session_state["character_prompt"]
        # /imagine prompt: 이후의 내용 추출
        if "/imagine prompt:" in prompt_text:
            import re
            # /imagine prompt: 다음부터 --ar 전까지 추출
            match = re.search(r'/imagine prompt:\s*(.+?)(?:\s*--|\n|$)', prompt_text)
            if match:
                extracted = match.group(1).strip()
                # 스타일 키워드 제거 (in the style of~ 부분)
                if "in the style of" in extracted.lower():
                    extracted = extracted.split(",")[0].strip()
                
                if extracted and len(extracted) > 10:  # 최소 길이 확인
                    if "visual_anchor" not in st.session_state or not st.session_state.get("visual_anchor"):
                        st.session_state["visual_anchor"] = extracted
                        tab2_character_loaded = True
    
    # 방법 2: character_subject 사용 (한글일 수 있음)
    if not tab2_character_loaded and "character_subject" in st.session_state and st.session_state["character_subject"]:
        subject = st.session_state["character_subject"]
        if "visual_anchor" not in st.session_state or not st.session_state.get("visual_anchor"):
            # 한글이면 경고 표시
            if any('\uac00' <= char <= '\ud7a3' for char in subject):
                st.warning(f"⚠️ Tab 2 캐릭터: '{subject}' (한글입니다. 영어로 번역하거나 AI 추천을 사용하세요)")
            else:
                st.session_state["visual_anchor"] = subject
                tab2_character_loaded = True
    
    if tab2_character_loaded:
        st.success("✅ Tab 2에서 생성한 캐릭터가 자동으로 불러와졌습니다!")
    
    # ⭐ 하드코딩 제거 - 빈 문자열로 변경
    default_anchor = st.session_state.get("visual_anchor", "")
    
    # AI 추천 버튼
    col_input, col_suggest = st.columns([4, 1])
    
    with col_input:
        # 세션 스테이트에 visual_anchor가 없으면 초기화
        if "visual_anchor" not in st.session_state:
            st.session_state["visual_anchor"] = ""
        
        visual_anchor = st.text_area(
            "주인공 핵심 외형 (영어)",
            value=st.session_state["visual_anchor"],  # value를 세션에서 직접 가져오기
            height=100,
            placeholder="예: Young woman with silver hair, wearing elegant dress, emerald pendant\n\n또는 '🤖 AI 추천' 버튼을 눌러 가사 기반 자동 생성",
            help="이 텍스트가 모든 장면에서 맥락에 맞게 적용됩니다",
            key="visual_anchor_input"
        )
        
        # 사용자가 직접 입력한 경우 세션에 저장
        if visual_anchor != st.session_state.get("visual_anchor", ""):
            st.session_state["visual_anchor"] = visual_anchor
    
    with col_suggest:
        st.markdown("#### 🤖")
        if st.button("AI 추천", use_container_width=True, help="가사를 분석하여 어울리는 주인공을 AI가 제안합니다", key="ai_suggest_anchor"):
            # 가사 확인 - lyrics_input이 아니라 세션에서 가져오기
            available_lyrics = lyrics_input.strip() if lyrics_input.strip() else st.session_state.get("lyrics", "")
            
            if not available_lyrics:
                st.error("❌ 먼저 Tab 1-B에서 가사를 생성해주세요!")
            elif client is None:
                st.error("❌ API 키가 설정되지 않았습니다.")
            else:
                with st.spinner("🤖 가사를 분석하여 주인공을 추천하고 있습니다..."):
                    current_genre = st.session_state.get("lyrics_genre", "")
                    current_vibe = st.session_state.get("lyrics_vibe", "")
                    
                    try:
                        suggested = suggest_visual_anchor(client, available_lyrics, current_genre, current_vibe)
                        
                        if suggested and suggested.strip():
                            # 세션 스테이트에 저장
                            st.session_state["visual_anchor"] = suggested.strip()
                            st.success(f"✅ AI 추천 완료!")
                            st.info(f"**추천 결과:**\n\n{suggested.strip()}")
                            st.warning("⚠️ 위 내용이 입력칸에 표시되려면 **페이지를 새로고침**하거나 **다른 탭을 클릭 후 다시 돌아오세요**!")
                            # rerun으로 즉시 반영
                            st.rerun()
                        else:
                            st.error("❌ AI 추천 생성에 실패했습니다. 다시 시도해주세요.")
                    except Exception as e:
                        st.error(f"❌ 오류 발생: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())
                    else:
                        st.error("추천 생성에 실패했습니다. 직접 입력해주세요.")
    
    st.session_state["visual_anchor"] = visual_anchor
    
    if not visual_anchor.strip():
        st.warning("""
        ⚠️ **Visual Anchor가 비어있습니다!**
        
        다음 중 하나를 선택하세요:
        1. 🤖 **'AI 추천' 버튼** 클릭 - 가사 기반 자동 생성
        2. ✍️ **직접 입력** - 원하는 주인공 외형 작성
        
        비워두면 AI가 장면마다 임의로 캐릭터를 생성하여 일관성이 떨어질 수 있습니다.
        """)
    else:
        st.info(f"""
        💡 **Visual Anchor 작성 팁:**
        - ✅ 헤어스타일과 색상 명시
        - ✅ 핵심 액세서리 (펜던트, 반지 등)
        - ✅ 기본 외형 특징
        - ⚠️ 의상은 최소한으로 (장면 맥락에 맞게 자동 변형됨)
        """)
    
    st.divider()
    
    # ============ 스타일 선택 (이미지 미리보기 포함) ============
    st.subheader("🎨 비주얼 스타일 선택")
    
    # AI 자동 추천
    current_genre = st.session_state.get("lyrics_genre", "")
    current_vibe = st.session_state.get("lyrics_vibe", "")
    
    auto_recommended = None
    if current_genre or current_vibe or lyrics_input:
        auto_recommended = analyze_lyrics_for_style(lyrics_input, current_genre, current_vibe)
        st.success(f"🤖 **AI 추천 스타일:** {auto_recommended}")
        
        if current_genre:
            st.caption(f"📊 분석 근거: 장르({current_genre}), Vibe({current_vibe})")
    
    # 스타일 선택
    style_options = list(STYLE_GUIDE.keys())
    
    # Tab 2에서 선택한 스타일을 기본값으로 설정
    default_style = "AI 자동 추천"
    if "character_style_kr" in st.session_state and st.session_state["character_style_kr"]:
        char_style = st.session_state["character_style_kr"]
        if char_style in style_options:
            default_style = char_style
            st.info(f"💡 Tab 2에서 선택하신 **{char_style}** 스타일이 자동 선택되었습니다!")
    
    # 기본값의 인덱스 찾기
    try:
        default_index = style_options.index(default_style)
    except ValueError:
        default_index = 0
    
    selected_style = st.selectbox(
        "이미지 스타일 선택",
        options=style_options,
        index=default_index,
        help="각 스타일의 미리보기 이미지를 확인하세요"
    )
    
    # 선택된 스타일 정보 + 이미지 표시
    if selected_style != "AI 자동 추천":
        style_info = STYLE_GUIDE[selected_style]
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            # 미리보기 이미지 표시
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
            
            with st.expander("📋 스타일 상세 정보"):
                st.markdown("**이미지 키워드:**")
                st.code(style_info['image_keywords'], language=None)
                
                st.markdown("**영상 키워드:**")
                st.text(style_info['video_keywords'])
                
                st.markdown("**특수 효과:**")
                st.text(style_info['effects'])
                
                st.markdown("**화면 전환:**")
                st.text(style_info['transitions'])
    
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
    
    # ============ 영상 분위기 ============
    st.subheader("🎥 영상 분위기")
    
    video_mood_kr = st.selectbox(
        "전체 영상 톤",
        options=VIDEO_MOOD_OPTIONS
    )
    
    st.caption(f"🔤 영어값: `{VIDEO_MOOD_MAP[video_mood_kr]}`")
    
    st.divider()
    
    # ============ 생성 버튼 ============
    generate_button_text = "🎬 20개+A/B (총 40컷) 생성" if selected_mode == "20_AB" else "🎬 40개 독립 장면 생성"
    
    if st.button(generate_button_text, type="primary", use_container_width=True):
        if not lyrics_input.strip():
            st.error("가사를 입력해주세요.")
            return
        if client is None:
            st.error("API 키가 설정되지 않았습니다.")
            return
        if not visual_anchor.strip():
            st.error("Visual Anchor (주인공 외형)를 입력하거나 'AI 추천' 버튼을 눌러주세요.")
            return
        
        # 최종 스타일 결정
        if selected_style == "AI 자동 추천":
            if auto_recommended:
                final_style = auto_recommended
            else:
                final_style = "지브리 2.0 (Miyazaki Masterpiece)"
            st.info(f"🤖 AI가 선택한 스타일: **{final_style}**")
        else:
            final_style = selected_style
        
        # 스타일 데이터 가져오기
        style_data = STYLE_GUIDE[final_style]
        style_keywords = style_data["image_keywords"]
        video_mood_en = VIDEO_MOOD_MAP[video_mood_kr]
        
        # 선택된 모드에 따라 시스템 프롬프트 선택
        if selected_mode == "20_AB":
            system_role = SYSTEM_ROLE_20_AB
            mode_description = "20개 메인 장면 + 각 A/B 앵글 (총 40컷)"
        else:
            system_role = SYSTEM_ROLE_40_INDEPENDENT
            mode_description = "40개 독립 장면"
        
        # 사용자 프롬프트 구성
        user_prompt = f"""다음 가사를 분석하여 뮤직비디오용 프롬프트를 생성해주세요.

## 생성 방식
{mode_description}

## 가사
{lyrics_input}

## Visual Anchor (모든 장면 공통)
{visual_anchor}

## 영상 분위기
{video_mood_en}

## 스타일 키워드 (시스템이 자동 추가)
{style_keywords}

## ⭐ 핵심 규칙 ⭐

1. **Visual Anchor 100% 유지**
   - 모든 장면의 첫 부분에 다음을 반드시 포함: "{visual_anchor}"

2. **Match Cut (장면 계승)**
   - n번 장면의 마지막 요소가 n+1번의 시작 요소
   - 한글 설명 끝에 연결점 표시: [이전: X → 현재: Y]

3. **시각적 직유 (Visual Literalism)**
   - 추상 비유를 물리적 실체로 100% 변환
   - 금지 단어: "Representing", "Symbolizing", "Concept of"

4. **이미지 묘사에 스타일 키워드 포함 금지**
   - 시스템이 자동으로 추가합니다

지금 바로 위 규칙을 엄격히 준수하여 생성해주세요!"""

        spinner_text = "🎬 AI가 장면을 분석하고 있습니다... (약 2-3분)" if selected_mode == "20_AB" else "🎬 AI가 40개 장면을 분석하고 있습니다... (약 2-3분)"
        
        with st.spinner(spinner_text):
            try:
                result = get_gpt_response(client, system_role, user_prompt)
                
                # 세션 스테이트에 저장
                st.session_state["storyboard_raw"] = result
                st.session_state["storyboard_mode"] = selected_mode
                st.session_state["storyboard_char_url"] = char_url
                st.session_state["storyboard_style_url"] = style_url
                st.session_state["storyboard_style"] = final_style
                st.session_state["storyboard_video_mood"] = video_mood_en
                st.session_state["storyboard_video_mood_kr"] = video_mood_kr
                st.session_state["storyboard_visual_anchor"] = visual_anchor
                
                # 스타일 URL 저장
                if style_url:
                    st.session_state["style_reference_url"] = style_url
                
                success_message = "🎉 20개+A/B (총 40컷)이 생성되었습니다!" if selected_mode == "20_AB" else "🎉 40개 독립 장면이 생성되었습니다!"
                st.success(success_message)
                st.rerun()
                
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
                return
    
    # ============ 결과 표시 ============
    st.divider()
    
    if "storyboard_raw" in st.session_state and st.session_state["storyboard_raw"]:
        stored_mode = st.session_state.get("storyboard_mode", "40_INDEPENDENT")
        
        st.subheader(f"🎬 생성된 장면")
        
        # 저장된 값 불러오기
        char_url = st.session_state.get("storyboard_char_url", "")
        style_url = st.session_state.get("storyboard_style_url", "")
        final_style = st.session_state.get("storyboard_style", "")
        visual_anchor = st.session_state.get("storyboard_visual_anchor", "")
        style_data = STYLE_GUIDE.get(final_style, {})
        style_keywords = style_data.get("image_keywords", "")
        
        # 적용 설정 안내
        mode_desc = "20개 메인 + A/B 앵글 (총 40컷)" if stored_mode == "20_AB" else "40개 독립 장면"
        
        st.info(f"""
        📌 **적용된 설정:**
        - 🎬 생성 방식: **{mode_desc}**
        - ⚓ Visual Anchor: **{visual_anchor[:50]}{'...' if len(visual_anchor) > 50 else ''}**
        - 🎨 스타일: **{final_style}**
        - 🎥 분위기: **{st.session_state.get('storyboard_video_mood_kr', '-')}**
        - 🧑 캐릭터 참조 (--cref): {'✅ 적용' if char_url else '❌ 미적용'}
        - 🎨 스타일 참조 (--sref): {'✅ 적용 (--sw 1000)' if style_url else '❌ 미적용'}
        - 📐 화면 비율: `--ar 16:9`
        """)
        
        # 모드에 따라 파싱
        if stored_mode == "20_AB":
            scenes = parse_scenes_20_ab(st.session_state["storyboard_raw"])
        else:
            scenes = parse_scenes_40_independent(st.session_state["storyboard_raw"])
        
        if len(scenes) == 0:
            st.error("장면 파싱에 실패했습니다. 다시 생성해주세요.")
            return
        
        st.caption(f"✅ {len(scenes)}개 컷이 생성되었습니다.")
        
        st.divider()
        
        # ============ 실시간 수동 수정 시스템 ============
        st.subheader("✏️ 장면별 실시간 수정")
        st.markdown("""
        각 장면 하단의 편집창에서 **직접 수정**할 수 있습니다.
        """)
        
        st.divider()
        
        # ============ 최종 프롬프트 조립 ============
        final_prompts = []
        
        for i, scene in enumerate(scenes, 1):
            # 장면 키 생성 (수정 내용 저장용)
            if stored_mode == "20_AB":
                scene_key = f"{scene['scene_number']}-{scene['cut_type']}"
                scene_title = f"Scene {scene['scene_number']:02d}-{scene['cut_type']}컷"
            else:
                scene_key = f"{scene['scene_number']}"
                scene_title = f"Scene {scene['scene_number']:02d}"
            
            # 가독성을 위한 컨테이너 스타일
            with st.container():
                st.markdown(f"""
                <div style="
                    border: 3px solid #1f77b4;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 15px 0;
                    background-color: #f0f2f6;
                ">
                """, unsafe_allow_html=True)
                
                with st.expander(f"🎬 {scene_title}", expanded=(i <= 3)):
                    
                    # 영어 프롬프트를 한글로 자동 번역
                    original_english = scene.get('image_prompt', '')
                    
                    # 세션에 번역본이 없으면 자동 번역
                    translation_key = f"korean_translation_{scene_key}"
                    if translation_key not in st.session_state:
                        with st.spinner(f"🤖 {scene_title} 한글 번역 중..."):
                            korean_translation = translate_english_to_korean(client, original_english)
                            st.session_state[translation_key] = korean_translation
                    else:
                        korean_translation = st.session_state[translation_key]
                    
                    # ============ 한글 설명 수정 및 영어 변환 ============
                    st.markdown("### 📖 장면 설명 (한글)")
                    
                    # 한글 설명 입력칸
                    korean_input_key = f"korean_desc_{scene_key}"
                    
                    korean_desc_input = st.text_area(
                        "장면을 한글로 설명하세요",
                        value=korean_translation,
                        height=100,
                        key=korean_input_key,
                        placeholder="예: 여자가 비 오는 거리에서 우산을 쓰고 슬픈 표정으로 서 있다",
                        help="한글로 수정한 후 '영어 프롬프트로 변환' 버튼을 누르세요"
                    )
                    
                    # 영어 변환 버튼
                    col_translate, col_clear = st.columns([3, 1])
                    
                    with col_translate:
                        if st.button(f"🔄 영어 프롬프트로 변환", key=f"translate_{scene_key}", use_container_width=True):
                            if not korean_desc_input.strip():
                                st.error("한글 설명을 입력해주세요.")
                            else:
                                with st.spinner("🤖 GPT가 영어 프롬프트로 변환 중..."):
                                    visual_anchor = st.session_state.get("storyboard_visual_anchor", "")
                                    translated = translate_korean_to_prompt(client, korean_desc_input, visual_anchor)
                                    
                                    if translated and not translated.startswith("변환 실패"):
                                        # 변환된 영어를 override로 저장
                                        set_scene_override(scene_key, translated)
                                        st.success("✅ 영어 프롬프트로 변환 완료!")
                                        st.rerun()
                                    else:
                                        st.error(f"변환 실패: {translated}")
                    
                    with col_clear:
                        if st.button(f"🗑️ 초기화", key=f"clear_korean_{scene_key}", use_container_width=True):
                            # 한글 번역과 override 모두 초기화
                            if translation_key in st.session_state:
                                del st.session_state[translation_key]
                            set_scene_override(scene_key, "")
                            st.info("한글 설명이 초기화되었습니다.")
                            st.rerun()
                    
                    st.divider()
                    
                    # 사용자 수정 확인
                    override = get_scene_override(scene_key)
                    
                    if override:
                        # 사용자가 수정한 경우
                        st.warning("✏️ **사용자 수정 버전이 적용되었습니다.**")
                        
                        st.markdown("**🎬 수정된 장면 묘사**")
                        st.code(override, language=None)
                        
                        step2_prompt = f"{override}, {style_keywords}"
                        actual_image_prompt = override
                        
                    else:
                        # AI 원본 사용
                        st.markdown("**🎬 Step 1: 장면 묘사**")
                        st.code(scene['image_prompt'], language=None)
                        
                        step2_prompt = f"{scene['image_prompt']}, {style_keywords}"
                        actual_image_prompt = scene['image_prompt']
                    
                    # Step 2 표시
                    st.markdown("**✨ Step 2: 최종 Midjourney 프롬프트**")
                    
                    # URL 파라미터 결합
                    url_params = ""
                    if char_url:
                        url_params += f" --cref {char_url}"
                    if style_url:
                        url_params += f" --sref {style_url} --sw 1000"
                    
                    midjourney_prompt = f"/imagine prompt: {step2_prompt}{url_params} --ar 16:9"
                    
                    st.code(midjourney_prompt, language=None)
                    
                    # Motion 프롬프트
                    st.markdown("**🎥 Motion 프롬프트 (Kling/Runway)**")
                    st.success(f"🎬 {scene['motion_prompt']}")
                    
                    st.divider()
                    
                    # ============ 영어 프롬프트 직접 수정 (고급) ============
                    st.markdown("### ✏️ 영어 프롬프트 직접 수정 (고급)")
                    st.caption("💡 위에서 '영어 프롬프트로 변환'을 사용했다면, 여기서 추가 미세 조정이 가능합니다.")
                    
                    current_override = get_scene_override(scene_key)
                    
                    user_edit = st.text_area(
                        f"{scene_title} 영어 프롬프트 직접 수정",
                        value=current_override,
                        height=100,
                        placeholder=f"예: {scene['image_prompt'][:100]}...",
                        key=f"override_{scene_key}",
                        help="영어 프롬프트를 직접 수정할 수 있습니다. 비우면 AI 원본 사용."
                    )
                    
                    col_save, col_reset = st.columns(2)
                    
                    with col_save:
                        if st.button(f"💾 {scene_title} 수정 저장", key=f"save_{scene_key}", use_container_width=True):
                            set_scene_override(scene_key, user_edit)
                            st.success(f"{scene_title} 수정이 저장되었습니다!")
                            st.rerun()
                    
                    with col_reset:
                        if st.button(f"🔄 {scene_title} 원본 복구", key=f"reset_{scene_key}", use_container_width=True):
                            set_scene_override(scene_key, "")
                            if translation_key in st.session_state:
                                del st.session_state[translation_key]
                            st.info(f"{scene_title}를 AI 원본으로 복구했습니다.")
                            st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # 프롬프트 저장
                final_prompts.append({
                    "scene_key": scene_key,
                    "scene_title": scene_title,
                    "korean_desc": korean_translation,
                    "step1_scene": actual_image_prompt,
                    "step2_final": step2_prompt,
                    "midjourney": midjourney_prompt,
                    "motion": scene['motion_prompt'],
                    "is_user_override": bool(override)
                })
        
        # 세션에 최종 프롬프트 저장
        st.session_state["final_prompts"] = final_prompts
        
        st.divider()
        
        # ============ 수정 통계 ============
        user_modified_count = sum(1 for p in final_prompts if p.get("is_user_override"))
        
        if user_modified_count > 0:
            st.success(f"""
            ✏️ **사용자 수정 통계:**
            - 총 {len(scenes)}개 컷 중 **{user_modified_count}개 컷**이 수정되었습니다.
            - 나머지 {len(scenes) - user_modified_count}개는 AI 원본이 사용됩니다.
            """)
        
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
4. Match Cut으로 장면 연결
5. 음악과 싱크 맞추기
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
                f"# {p['scene_title']}: {p['korean_desc']}\n{p['midjourney']}"
                for p in final_prompts
            ])
            st.text_area("MJ 프롬프트", value=all_mj, height=400, label_visibility="collapsed")
        
        with tab_motion:
            st.markdown("**Kling/Runway에서 사용:**")
            all_motion = "\n\n".join([
                f"# {p['scene_title']}: {p['korean_desc']}\n{p['motion']}"
                for p in final_prompts
            ])
            st.text_area("Motion", value=all_motion, height=400, label_visibility="collapsed")
        
        with tab_all:
            st.markdown("**전체 데이터:**")
            all_data = "\n\n".join([
                f"{'='*60}\n🎬 {p['scene_title']} {'[USER MODIFIED]' if p.get('is_user_override') else '[AI GENERATED]'}\n{'='*60}\n\n"
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
        st.success(f"""
        🎉 **모든 장면이 완성되었습니다!**
        
        **생성 정보:**
        - 🎬 방식: **{mode_desc}**
        - ⚓ Visual Anchor: 모든 장면 일관성 유지
        - 🔗 Match Cut: 장면 간 연결점 명시
        - ✏️ 사용자 수정: {user_modified_count}/{len(scenes)} 컷
        - 🧑 --cref: {'✅' if char_url else '❌'}
        - 🎨 --sref: {'✅' if style_url else '❌'}
        
        **다음 단계:**
        1. 📸 **Midjourney 프롬프트** 복사 → Discord에서 이미지 생성
        2. 📹 **스톡 영상** 다운로드 (추천 키워드 사용)
        3. 🎬 **Kling/Runway**에 이미지 업로드 + Motion 프롬프트 적용
        4. ✂️ **영상 편집** (Match Cut으로 끊김없이 연결)
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
        
        1. **장면 생성 방식 선택** (20+A/B or 40개)
        2. **가사 입력** (Tab 1에서 자동 불러오기)
        3. **Visual Anchor 설정**
           - 🤖 **'AI 추천' 버튼** 클릭 (가사 기반 자동 생성)
           - ✍️ **직접 입력** (원하는 주인공 외형)
        4. **URL 입력** (캐릭터 참조 + 스타일 참조)
        5. **스타일 선택** (이미지 미리보기 확인)
        6. **생성 버튼 클릭**
        7. **필요시 각 장면 수동 수정**
        
        > 💡 대서사시 연계 엔진으로 3~4분 영상을 완벽히 채웁니다!
        """)
