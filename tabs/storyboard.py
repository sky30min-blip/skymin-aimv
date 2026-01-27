"""
tabs/storyboard.py - 서사 중심 스토리보드 엔진 v3.1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎬 핵심 혁신: 가사의 텍스트가 아닌 '영혼'을 이미지로 번역
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

v3.1 업데이트 (NEW!):
🔗 **가사-장면 매핑** - 각 장면의 근거가 되는 가사 원문 표시

v3.0 주요 업그레이드:
1. 📜 서사 중심 모드 - 가사 흐름에 따라 12~25개 최적 장면 수 자동 결정
2. 🎭 입체적 맥락 해석 - 추상적 표현을 영화적 연출로 변환
3. 💎 시각적 직유 규칙 - 모든 개념을 물리적 행동/소품/빛으로 치환
4. ⚡ Action-Oriented - 정지 화면이 아닌 동사 중심 역동성

기존 완전판 기능 100% 유지:
- Visual Anchor AI 추천 (기본값 빈 칸)
- 실시간 수정 UI
- Match Cut 엔진
- 11가지 프리미엄 스타일
"""

import streamlit as st
from utils import get_gpt_response
import re
import json


# ============================================================================
# PART 1: 스타일 가이드 및 설정 데이터
# ============================================================================

STYLE_GUIDE = {
    "고퀄리티 일본 애니메이션": {
        "keywords": "Modern high-end Japanese anime style, cinematic production value, sharp character lines, highly detailed background, atmospheric lighting effects, masterpiece anime still, professional color grading",
        "description": "Production I.G, WIT Studio 같은 고예산 애니메이션의 한 장면",
        "preview": "🎬",
        "image": "https://cdn.midjourney.com/20533ac1-924a-4e01-966c-785eb60957b8/0_1.png"
    },
    "프리미엄 한국 웹툰": {
        "keywords": "Premium Korean webtoon style, sharp digital linework, vibrant gradient lighting, manhwa aesthetic, detailed background, modern webtoon masterpiece",
        "description": "나 혼자만 레벨업 같은 세련된 최신 웹툰 스타일",
        "preview": "📱",
        "image": "https://cdn.midjourney.com/ab3a0859-19ec-4eb9-8554-f04a9113db56/0_2.png"
    },
    "클래식 흑백 만화": {
        "keywords": "Classic Korean Manhwa style, detailed ink drawing, high contrast black and white with gray tones, traditional comic book hatching, 2D hand-drawn aesthetic",
        "description": "정통 흑백 만화 스타일",
        "preview": "📖",
        "image": "https://cdn.midjourney.com/007e0390-fcba-4175-a7db-758aeae4438b/0_1.png"
    },
    "교토 애니메이션 스타일": {
        "keywords": "Kyoto Animation style, delicate linework, soft lighting, emotional and serene, transparent colors, high-detail eyes, beautiful light reflections, premium slice-of-life anime aesthetic",
        "description": "바이올렛 에버가든 같은 극강의 섬세함",
        "preview": "🌸",
        "image": "https://cdn.midjourney.com/76d004b6-a235-409f-b0dc-41d3c58c8f13/0_1.png"
    },
    "수채화 판타지": {
        "keywords": "Dreamy watercolor illustration, soft pastels, fluid edges, emotional atmosphere, artistic brushstrokes, ethereal light, whimsical and poetic, high-end storybook aesthetic",
        "description": "몽환적인 수채화 느낌",
        "preview": "🎨",
        "image": "https://cdn.midjourney.com/89ff3672-f48b-4465-a214-935a8fd19633/0_1.png"
    },
    "90년대 사이버펑크": {
        "keywords": "1990s Japanese Cyberpunk anime style, grit and neon, high-tech noir, hand-drawn aesthetic, dramatic shadows, futuristic dystopian cityscape, cinematic lighting, detailed mechanical design",
        "description": "아키라, 공각기동대 같은 묵직한 미래 도시",
        "preview": "🌃",
        "image": "https://cdn.midjourney.com/4fb8a033-3db8-4e8a-8d08-f316471d69b8/0_3.png"
    },
    "럭셔리 시티팝": {
        "keywords": "Retro Japanese City Pop aesthetic, art style by Hiroshi Nagai, flat saturated colors, sharp shadows, 1980s luxury anime style, vaporwave sunset, clean minimalist lines",
        "description": "80년대 일본 시티팝 앨범 자켓",
        "preview": "🌆",
        "image": "https://cdn.midjourney.com/f9a94aba-fc63-4352-a787-c82ae17bbdee/0_0.png"
    },
    "신카이 마코토 감성": {
        "keywords": "Makoto Shinkai animation style, vibrant lighting, breathtaking sky and clouds, high-detail cityscapes, emotional atmosphere, hyper-detailed lens flare, luminous colors, cinematic background",
        "description": "너의 이름은 처럼 압도적인 배경",
        "preview": "☀️",
        "image": "https://cdn.midjourney.com/81db105a-9d37-401f-b056-3bf8e04f2daa/0_3.png"
    },
    "지브리 2.0": {
        "keywords": "Studio Ghibli art style by Hayao Miyazaki, lush painterly background, hand-drawn aesthetic, high-quality cel animation, soft natural sunlight, nostalgic atmosphere, detailed watercolor texture",
        "description": "미야자키 하야오의 원화 느낌",
        "preview": "🌿",
        "image": "https://cdn.midjourney.com/b8354c0a-dee9-4c5e-9013-00f3e8726dfa/0_2.png"
    },
    "90년대 한국 애니": {
        "keywords": "1990s Korean anime style, VHS aesthetic, chromatic aberration, bold outlines, neon purple and pink lighting, cinematic lofi vibe, retro cel-shaded",
        "description": "90년대 한국 애니메이션 향수",
        "preview": "📼",
        "image": "https://cdn.midjourney.com/d87c768f-65ab-4b5e-8f16-b3256a5627c9/0_1.png"
    },
    "90년대 레트로 일본 애니": {
        "keywords": "Retro 90s anime style, nostalgic, cel shading, vibrant colors, City Pop aesthetic, Lo-fi vibe, purple and blue neon lighting, dreamy atmosphere, vintage aesthetic",
        "description": "시티팝과 로파이의 만남",
        "preview": "🎵",
        "image": "https://cdn.midjourney.com/a83587b7-49e2-4830-b20b-1c7d2834d535/0_0.png"
    }
}

VIDEO_MOOD_GUIDE = {
    "역동적 Match Cut": {
        "en": "Dynamic match cuts with visual continuity",
        "description": "원테이크 영화처럼 시각적 연속성"
    },
    "부드러운 Fade": {
        "en": "Smooth fade transitions, gentle pacing",
        "description": "여운을 남기는 부드러운 전환"
    },
    "빠른 컷": {
        "en": "Fast-paced quick cuts, energetic editing",
        "description": "박진감 넘치는 빠른 편집"
    },
    "드라마틱 슬로우": {
        "en": "Dramatic slow-motion, emotional emphasis",
        "description": "감정을 극대화하는 슬로우 모션"
    }
}


# ============================================================================
# PART 2: 서사 중심 시스템 프롬프트 v3.0
# ============================================================================

STORY_SYSTEM_ROLE = """당신은 세계적인 뮤직비디오 감독이자 서사 해석 전문가입니다.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎬 당신의 임무: 가사의 '텍스트'가 아닌 '영혼'을 시각화
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 핵심 원칙: 입체적 맥락 해석 (Cinematic Interpretation)

가사를 **기계적으로 묘사하지 말고**, 그 뒤에 숨겨진 정서와 상황을 **영화적 연출**로 표현하세요.

### [감독의 연출 원칙] - 절대 규칙!

| 가사 (추상적 표현) | ❌ 피해야 할 기계적 묘사 | ✅ 구현해야 할 감독의 연출 (Mental Model) |
|---|---|---|
| "위대한 다섯 별" | 밤하늘에 별 5개 | 거대한 성당, 스테인드글라스를 통과한 빛이 5명의 성자(공자, 예수 등)의 긴 그림자를 주인공 발치까지 드리우는 장엄한 연출 |
| "성인들도 못 고친 스트레스" | 머리를 싸맨 주인공 | 넥타이를 거칠게 푼 주인공이 소주잔을 탁자에 세게 내리치는 순간, 액체가 조명을 받아 다이아몬드처럼 비산하는 쾌감의 클로즈업 |
| "세상이 아름답게 보이는 기적" | 꽃밭이나 무지개 | 취기가 오른 주인공 시점(POV), 지저분한 골목과 낡은 의자가 몽환적 보케 효과와 함께 금가루를 뿌린 듯 빛나는 환상적 연출 |
| "죽이고 싶던 부장님이 가엾은 양으로" | 부장님 머리에 양 뿔 | 찌든 표정의 부장님 얼굴이 소주잔 너머로 겹쳐 보일 때, 갑자기 보송보송한 어린양 얼굴로 시각적 모핑(Morphing)되는 위트 |
| "여기가 바로 무릉도원" | 구름 위 신선들 | 펄펄 끓는 안주 김이 화면을 가득 채웠다 걷히면, 현실의 포장마차가 신비로운 안개 자욱한 푸른 숲으로 변하며 주인공이 신선처럼 잔을 드는 변주 |
| "사랑의 힘" | 하트 모양, 커플 포옹 | 주인공이 떨어진 아이의 손을 잡아 일으켜주는 순간, 햇살이 두 손 사이를 비추며 빛 입자가 터지듯 확산되는 따뜻한 연출 |
| "인류애" | 지구본, 다양한 인종 | 지하철에서 노약자에게 자리를 양보하는 주인공의 뒷모습, 창밖으로 스쳐가는 도시 불빛이 반짝이는 별처럼 보이는 시적 연출 |

---

## [시각적 직유 규칙] - 금지어 목록!

### 🚫 절대 금지 단어 (Banned Abstract Words)
다음 단어들을 **절대 직접 사용하지 말 것**:
- 사랑, 구원, 인류애, 희망, 절망, 고독, 외로움, 기쁨, 슬픔
- 평화, 자유, 정의, 진실, 꿈, 운명, 영혼

### ✅ 치환 방법론 (Conversion Matrix)

**추상 개념 → 물리적 요소 3축 분해:**

1. **행동 (Action)**: 인물이 무엇을 하는가?
   - 예: "사랑" → "주인공이 떨어진 아이의 손을 잡아 일으켜주는 순간"

2. **소품 (Props)**: 어떤 물건이 상징하는가?
   - 예: "희망" → "깨진 화분 사이에서 싹튼 새싹에 물을 주는 손"

3. **빛의 각도 (Lighting Geometry)**: 빛이 어떻게 감정을 만드는가?
   - 예: "절망" → "창문 틈새로 들어오는 가느다란 빛줄기만이 주인공의 반쪽 얼굴을 비추는 극도로 어두운 공간"

---

## Action-Oriented 프롬프트 작성

### ❌ 나쁜 예 (정적, 설명적):
```
A man sitting on a bench, looking sad, dark background
```

### ✅ 좋은 예 (동적, 동사 중심):
```
{Visual Anchor} slumping down onto a rain-soaked bench, his trembling hands slowly releasing a crumpled letter, as streetlight cuts through the rain creating diagonal light shafts across his face
```

**핵심**: 모든 프롬프트는 **-ing 동사**를 포함하여 움직임과 과정을 표현할 것!

---

## 서사 흐름 판단 (Story Arc Recognition)

가사를 분석하여 **12~25개 사이**에서 최적의 장면 수를 결정하세요:

### 장면 수 결정 기준:
- **12-15개**: 미니멀리스트 서사 (반복 후렴, 짧은 가사)
- **16-20개**: 표준 서사 (일반적인 3분 곡)
- **21-25개**: 복합 서사 (스토리 전환 많음, 긴 곡)

### 서사 구조 인식:
1. **도입부 (Setup)**: 1-3 장면
2. **전개부 (Development)**: 전체의 40-50%
3. **절정 (Climax)**: 2-4 장면 (가장 극적)
4. **결말 (Resolution)**: 1-3 장면

---

## ⭐ 가사-장면 매핑 (v3.1 신규 기능)

**중요**: 각 장면은 반드시 **가사 원문에서 근거**를 찾아 `source_lyrics` 필드에 명시해야 합니다.

### 매핑 원칙:
1. **직접 인용**: 해당 장면을 만들게 된 가사 구절을 정확히 인용
2. **문맥 포함**: 앞뒤 1-2줄까지 포함하여 맥락 제공
3. **길이 제한**: 1-3줄 이내 (너무 길면 핵심만)

### 예시:
```
가사: "인류의 길을 밝힌 위대한 다섯 별이 있었으니\n공자, 석가, 예수, 소크라테스, 마호메트"
→ source_lyrics: "인류의 길을 밝힌 위대한 다섯 별이 있었으니\n공자, 석가, 예수, 소크라테스, 마호메트"
```

---

## 출력 형식 (JSON)

```json
{
  "total_scenes": 18,
  "reasoning": "이 가사는 술자리의 감정 변화를 3막 구조로 담고 있어 18개 장면이 최적입니다.",
  "scenes": [
    {
      "scene_number": 1,
      "source_lyrics": "회식 자리 가기 싫어\n오늘따라 왜 이렇게 힘든지",
      "korean_context": "회사 회식 직전, 주인공의 피곤한 모습",
      "english_prompt": "{Visual Anchor} loosening his tie while staring at the flickering neon sign of a street bar, his reflection distorted in the rain-puddle at his feet, golden hour backlighting creating a halo effect around his silhouette",
      "technical_notes": "Golden hour, shallow depth of field, neon glow"
    }
  ]
}
```

---

## 최종 체크리스트

프롬프트 생성 전 확인:
- [ ] **source_lyrics**: 각 장면의 근거가 되는 가사 원문을 추출했는가?
- [ ] 추상 개념을 물리적 요소로 100% 변환했는가?
- [ ] 모든 장면에 -ing 동사가 포함되어 있는가?
- [ ] 빛의 각도와 방향이 구체적으로 명시되어 있는가?
- [ ] 기계적 묘사를 피하고 영화적 연출을 했는가?
- [ ] Visual Anchor가 모든 장면에 자연스럽게 녹아있는가?

지금 바로 가사의 '영혼'을 번역하세요!"""


# ============================================================================
# PART 3: 기존 고정 장면 시스템 프롬프트 (20/40 모드용)
# ============================================================================

FIXED_SYSTEM_ROLE = """당신은 세계적인 뮤직비디오 감독입니다.

주어진 가사를 분석하여 시각적으로 완벽한 스토리보드를 생성하세요.

## 출력 형식

각 장면마다:
```
장면 N: [가사 원문]
한글 맥락: [한글 설명]
프롬프트: {Visual Anchor}, [구체적인 영어 프롬프트]
```

## 규칙
- **가사 원문**: 각 장면의 근거가 되는 가사 구절을 정확히 인용 (1-3줄)
- Visual Anchor를 모든 장면 프롬프트 맨 앞에 배치
- 구체적이고 시각적인 묘사
- 영화적 연출 요소 포함 (조명, 구도, 움직임)
"""

# ============================================================================
# PART 4: 헬퍼 함수들
# ============================================================================

def initialize_scene_overrides():
    """장면별 수동 수정 상태 초기화"""
    if "scene_overrides" not in st.session_state:
        st.session_state["scene_overrides"] = {}


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


def parse_story_mode_response(response: str) -> dict:
    """서사 중심 모드의 JSON 응답을 파싱합니다."""
    try:
        # JSON 코드 블록 제거
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
        
        data = json.loads(response)
        return data
    except Exception as e:
        print(f"JSON 파싱 오류: {str(e)}")
        return None


def parse_fixed_mode_response(response: str, num_scenes: int) -> list:
    """고정 장면 모드의 텍스트 응답을 파싱합니다."""
    scenes = []
    
    # 장면별로 분리
    scene_blocks = re.split(r'장면\s+\d+:', response)
    
    for idx, block in enumerate(scene_blocks[1:], 1):  # 첫 번째는 빈 문자열이므로 제외
        if not block.strip():
            continue
        
        source_lyrics = ""
        korean_context = ""
        english_prompt = ""
        
        # source_lyrics, 한글 맥락, 영어 프롬프트 분리
        lines = block.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('프롬프트:'):
                english_prompt = line.replace('프롬프트:', '').strip()
            elif line.startswith('한글 맥락:'):
                korean_context = line.replace('한글 맥락:', '').strip()
            elif line and not source_lyrics and not korean_context and not english_prompt:
                # 첫 번째 줄은 가사 원문으로 간주
                source_lyrics = line
        
        if english_prompt:
            scenes.append({
                "scene_number": idx,
                "source_lyrics": source_lyrics if source_lyrics else "가사 매핑 없음",
                "korean_context": korean_context.strip() if korean_context else "",
                "english_prompt": english_prompt,
                "technical_notes": ""
            })
    
    return scenes


def translate_korean_to_english(client, korean_text: str, visual_anchor: str, style_keywords: str) -> str:
    """한글 장면 설명을 영어 Midjourney 프롬프트로 변환합니다."""
    
    system_role = """당신은 한글 장면 설명을 Midjourney 프롬프트로 변환하는 전문가입니다.

## 규칙
1. Visual Anchor를 맨 앞에 배치
2. 구체적이고 시각적인 영어 표현 사용
3. 영화적 연출 요소 포함 (조명, 구도, 움직임)
4. -ing 동사로 역동성 부여

## 출력 형식
{Visual Anchor}, [영어 프롬프트]"""

    user_prompt = f"""다음 한글 장면 설명을 Midjourney 프롬프트로 변환하세요.

Visual Anchor: {visual_anchor}
스타일 키워드: {style_keywords}
한글 설명: {korean_text}

영어 프롬프트만 출력하세요 (설명 없이)."""

    try:
        result = get_gpt_response(client, system_role, user_prompt)
        return result.strip()
    except Exception as e:
        return f"{visual_anchor}, {korean_text}"

# ============================================================================
# PART 5: 메인 RENDER 함수
# ============================================================================

def render(client):
    """스토리보드 탭을 렌더링합니다."""
    
    # 장면 수정 상태 초기화
    initialize_scene_overrides()
    
    st.header("🎬 Step 3: 서사 중심 스토리보드 엔진 v3.1")
    st.markdown("""
    가사의 **텍스트가 아닌 '영혼'**을 시각화합니다.
    
    > 🎥 *"추상적 표현 → 영화적 연출 / 정지 화면 → 역동적 액션"*
    """)
    
    st.success("""
    ✨ **v3.1 업데이트 (NEW!):**
    🔗 **가사-장면 매핑** - 각 장면의 근거가 되는 가사 원문을 명확히 표시
    
    ✨ **v3.0 혁신적 업그레이드:**
    1. 📜 **서사 중심 모드** - 가사 흐름에 따라 12~25개 최적 장면 수 자동 결정
    2. 🎭 **입체적 맥락 해석** - "위대한 다섯 별" → 성당의 스테인드글라스 빛
    3. 💎 **시각적 직유 규칙** - 추상 개념을 물리적 행동/소품/빛으로 치환
    4. ⚡ **Action-Oriented** - 모든 프롬프트에 -ing 동사로 역동성 부여
    5. 🎨 **11가지 프리미엄 스타일** + **실시간 수정 UI** 유지
    """)
    
    st.divider()
    
    # ============ 가사 입력 ============
    st.subheader("📝 가사 입력")
    
    default_lyrics = st.session_state.get("lyrics", "")
    
    lyrics_input = st.text_area(
        "가사 전문 (한글 또는 영어)",
        value=default_lyrics,
        height=200,
        placeholder="가사를 입력하거나 Tab 1에서 생성한 가사가 자동으로 불러와집니다...",
        help="Tab 1에서 가사를 생성했다면 자동으로 채워집니다"
    )
    
    if not lyrics_input and default_lyrics:
        st.info("✅ Tab 1에서 생성한 가사가 감지되었습니다!")
    
    st.divider()
    
    # ============ 장면 생성 방식 선택 ============
    st.subheader("🎬 장면 생성 방식 선택")
    
    scene_mode = st.radio(
        "어떤 방식으로 스토리보드를 생성할까요?",
        options=[
            "📜 서사 중심 (가사 내용 따라 유연하게 12~25개)",
            "🎞️ 20개 장면 (각 장면 A/B컷)",
            "🎬 40개 독립 장면"
        ],
        help="서사 중심 모드는 AI가 가사를 분석하여 최적의 장면 수를 결정합니다"
    )
    
    # 선택된 모드 설명
    if "서사 중심" in scene_mode:
        st.info("""
        💡 **서사 중심 모드란?**
        
        가사의 이야기 구조를 AI가 분석하여:
        - **미니멀 서사** (반복 후렴) → 12-15개
        - **표준 서사** (일반 3분 곡) → 16-20개
        - **복합 서사** (긴 곡, 전환 많음) → 21-25개
        
        🎭 **핵심 차별점:**
        - "위대한 다섯 별" → 성당의 스테인드글라스 빛과 성자들의 그림자
        - "성인들도 못 고친 스트레스" → 소주잔을 내리치는 순간의 액체 비산 클로즈업
        - "세상이 아름답게 보이는 기적" → 취기 어린 시점(POV)의 몽환적 보케 효과
        """)
    elif "20개" in scene_mode:
        st.info("20개 장면, 각 장면마다 A컷/B컷 생성 → 총 40개 프롬프트")
    else:
        st.info("40개의 독립적인 장면으로 구성된 상세한 스토리보드")
    
    st.divider()
    

    # ============ 일관성 장치 (Character & Style URLs) ============
    st.subheader("🔗 일관성 장치 (Character & Style URLs)")
    
    # 🔍 디버깅 정보 (선택사항)
    with st.expander("🔍 디버깅: 세션 스테이트 확인"):
        url_keys = [k for k in st.session_state.keys() if 'url' in k.lower() or 'image' in k.lower() or 'character' in k.lower()]
        if url_keys:
            st.write("**세션에 저장된 URL/이미지 관련 키:**")
            for key in url_keys:
                value = st.session_state.get(key, "")
                if isinstance(value, str) and len(value) < 200:
                    st.write(f"- `{key}`: {value[:100]}")
        else:
            st.warning("URL 관련 세션 키가 없습니다!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🧑 캐릭터 참조 URL")
        
        # 세션에 캐릭터 URL이 없으면 초기화
        if "master_image_url" not in st.session_state:
            st.session_state["master_image_url"] = ""
        
        # 현재 세션 값 가져오기
        current_char_url = st.session_state.get("master_image_url", "")
        
        char_url = st.text_input(
            "캐릭터 이미지 URL (--cref)",
            value=current_char_url,
            placeholder="https://cdn.midjourney.com/...",
            help="Tab 2에서 생성한 캐릭터 이미지 URL"
        )
        
        # 사용자가 입력한 값이 세션과 다르면 업데이트
        if char_url != current_char_url:
            st.session_state["master_image_url"] = char_url
        
        if current_char_url:
            st.success("✅ Tab 2에서 저장한 URL이 불러와졌습니다!")
            st.caption(f"URL: {current_char_url[:50]}...")
    
    with col2:
        st.markdown("#### 🎨 스타일 참조 URL")
        
        # 세션에 스타일 URL이 없으면 초기화
        if "style_reference_url" not in st.session_state:
            st.session_state["style_reference_url"] = ""
        
        # 현재 세션 값 가져오기
        current_style_url = st.session_state.get("style_reference_url", "")
        
        style_url = st.text_input(
            "스타일(화풍) 이미지 URL (--sref)",
            value=current_style_url,
            placeholder="https://cdn.midjourney.com/...",
            help="모든 장면의 색감/질감을 고정할 참조 이미지 URL"
        )
        
        # 사용자가 입력한 값이 세션과 다르면 업데이트
        if style_url != current_style_url:
            st.session_state["style_reference_url"] = style_url
        
        if current_style_url:
            st.success("✅ 스타일 URL이 입력되었습니다.")
            st.caption("(--sw 1000 자동 적용)")
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
    
    # AI 추천 버튼
    col_input, col_suggest = st.columns([4, 1])
    
    with col_input:
        # 세션 스테이트에 visual_anchor가 없으면 초기화
        if "visual_anchor" not in st.session_state:
            st.session_state["visual_anchor"] = ""
        
        # 현재 세션 값 가져오기
        current_value = st.session_state.get("visual_anchor", "")
        
        # text_area 렌더링 (key 없이!)
        visual_anchor = st.text_area(
            "주인공 핵심 외형 (영어)",
            value=current_value,
            height=100,
            placeholder="예: Young woman with silver hair, wearing elegant dress, emerald pendant\n\n또는 '🤖 AI 추천' 버튼을 눌러 가사 기반 자동 생성",
            help="이 텍스트가 모든 장면에서 맥락에 맞게 적용됩니다"
        )
        
        # 사용자가 입력한 값이 세션과 다르면 업데이트
        if visual_anchor != current_value:
            st.session_state["visual_anchor"] = visual_anchor
    
    with col_suggest:
        st.markdown("#### 🤖")
        if st.button("AI 추천", use_container_width=True, help="가사를 분석하여 어울리는 주인공을 AI가 제안합니다", key="ai_suggest_anchor"):
            # 가사 확인
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
                            st.rerun()
                        else:
                            st.error("❌ AI 추천 생성에 실패했습니다. 다시 시도해주세요.")
                    except Exception as e:
                        st.error(f"❌ 오류 발생: {str(e)}")
    
    # visual_anchor 값 검증 (text_area에서 이미 세션에 저장됨)
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

    # ============ 스타일 선택 ============
    st.subheader("🎨 비주얼 스타일")
    
    # Tab 2에서 선택한 스타일 자동 불러오기
    default_style = st.session_state.get("character_style_kr", list(STYLE_GUIDE.keys())[0])
    
    if default_style and default_style in STYLE_GUIDE:
        st.info(f"✅ Tab 2에서 선택한 스타일: **{default_style}**")
    
    selected_style = st.selectbox(
        "프리미엄 스타일 선택",
        options=list(STYLE_GUIDE.keys()),
        index=list(STYLE_GUIDE.keys()).index(default_style) if default_style in STYLE_GUIDE else 0
    )
    
    # 선택된 스타일 미리보기
    style_info = STYLE_GUIDE[selected_style]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if style_info.get("image"):
            st.image(style_info["image"], use_container_width=True)
    
    with col2:
        st.markdown(f"### {style_info['preview']} {selected_style}")
        st.caption(style_info['description'])
        
        with st.expander("📋 스타일 키워드"):
            st.code(style_info['keywords'], language=None)
    
    # 전체 스타일 갤러리
    with st.expander("🎨 모든 스타일 갤러리"):
        cols = st.columns(3)
        for idx, (style_name, style_data) in enumerate(STYLE_GUIDE.items()):
            with cols[idx % 3]:
                if style_data.get("image"):
                    st.image(style_data["image"], use_container_width=True)
                st.markdown(f"**{style_data['preview']} {style_name}**")
                st.caption(style_data['description'])
    
    st.divider()
    
    # ============ 비디오 무드 ============
    st.subheader("🎬 영상 편집 스타일")
    
    selected_mood = st.selectbox(
        "편집 느낌",
        options=list(VIDEO_MOOD_GUIDE.keys())
    )
    
    mood_info = VIDEO_MOOD_GUIDE[selected_mood]
    st.caption(f"{mood_info['description']}")
    
    st.divider()
    
    # ============ 생성 버튼 ============
    generate_button_label = ""
    if "서사 중심" in scene_mode:
        generate_button_label = "🎬 서사 중심 스토리보드 생성 (AI가 최적 장면 수 결정)"
    elif "20개" in scene_mode:
        generate_button_label = "🎬 20개 장면 스토리보드 생성 (A/B컷 포함)"
    else:
        generate_button_label = "🎬 40개 장면 스토리보드 생성"
    
    if st.button(generate_button_label, type="primary", use_container_width=True):
        if not lyrics_input:
            st.error("가사를 입력해주세요.")
            return
        if not visual_anchor.strip():
            st.warning("⚠️ Visual Anchor가 비어있습니다. 캐릭터 일관성이 떨어질 수 있습니다.")
        if client is None:
            st.error("API 키가 설정되지 않았습니다.")
            return
        
        # 스타일 키워드
        style_keywords = style_info["keywords"]
        mood_keywords = mood_info["en"]
        
        # 서사 중심 모드 vs 고정 장면 모드
        if "서사 중심" in scene_mode:
            # ============ 서사 중심 모드 ============
            
            user_prompt = f"""다음 가사를 분석하여 서사 중심 스토리보드를 생성하세요.

## 가사
{lyrics_input}

## Visual Anchor
{visual_anchor if visual_anchor.strip() else "주인공 정보 없음 (장면마다 적절히 생성)"}

## 스타일
{style_keywords}

## 영상 편집 스타일
{mood_keywords}

## 지시사항
1. 가사의 서사 구조를 분석하여 **12~25개 사이**에서 최적의 장면 수를 결정하세요
2. [감독의 연출 원칙]을 엄격히 따라 추상적 표현을 영화적 연출로 변환하세요
3. 모든 장면에 -ing 동사를 포함하여 역동성을 부여하세요
4. JSON 형식으로 출력하세요

지금 바로 가사의 '영혼'을 번역하세요!"""

            with st.spinner("🎬 서사 중심 스토리보드를 생성하고 있습니다... (30초~1분 소요)"):
                try:
                    response = get_gpt_response(client, STORY_SYSTEM_ROLE, user_prompt)
                    
                    # JSON 파싱
                    data = parse_story_mode_response(response)
                    
                    if data and "scenes" in data:
                        st.session_state["storyboard_data"] = data
                        st.session_state["storyboard_mode"] = "서사 중심"
                        st.session_state["storyboard_style"] = selected_style
                        st.session_state["storyboard_style_keywords"] = style_keywords
                        st.session_state["storyboard_visual_anchor"] = visual_anchor
                        st.session_state["char_url"] = char_url
                        st.session_state["style_url"] = style_url
                        
                        st.success(f"🎉 서사 중심 스토리보드 생성 완료! (총 {data['total_scenes']}개 장면)")
                        st.info(f"**AI의 판단:** {data.get('reasoning', '')}")
                        st.rerun()
                    else:
                        st.error("JSON 파싱에 실패했습니다. 응답 형식을 확인해주세요.")
                        with st.expander("원본 응답 보기"):
                            st.code(response)
                
                except Exception as e:
                    st.error(f"오류 발생: {str(e)}")
                    return
        
        else:
            # ============ 고정 장면 모드 (20/40) ============
            
            num_scenes = 20 if "20개" in scene_mode else 40
            
            user_prompt = f"""다음 가사를 분석하여 {num_scenes}개 장면의 스토리보드를 생성하세요.

## 가사
{lyrics_input}

## Visual Anchor
{visual_anchor if visual_anchor.strip() else "주인공 정보 없음"}

## 스타일
{style_keywords}

## 영상 편집 스타일
{mood_keywords}

각 장면마다:
장면 N: [한글 맥락 설명]
프롬프트: {visual_anchor}, [구체적인 영어 프롬프트]

형식으로 {num_scenes}개를 모두 작성하세요."""

            with st.spinner(f"🎬 {num_scenes}개 장면 스토리보드를 생성하고 있습니다... (30초~1분 소요)"):
                try:
                    response = get_gpt_response(client, FIXED_SYSTEM_ROLE, user_prompt)
                    
                    # 텍스트 파싱
                    scenes = parse_fixed_mode_response(response, num_scenes)
                    
                    if scenes:
                        data = {
                            "total_scenes": len(scenes),
                            "reasoning": f"고정 {num_scenes}개 장면 모드",
                            "scenes": scenes
                        }
                        
                        st.session_state["storyboard_data"] = data
                        st.session_state["storyboard_mode"] = scene_mode
                        st.session_state["storyboard_style"] = selected_style
                        st.session_state["storyboard_style_keywords"] = style_keywords
                        st.session_state["storyboard_visual_anchor"] = visual_anchor
                        st.session_state["char_url"] = char_url
                        st.session_state["style_url"] = style_url
                        
                        st.success(f"🎉 스토리보드 생성 완료! (총 {len(scenes)}개 장면)")
                        st.rerun()
                    else:
                        st.error("장면 파싱에 실패했습니다.")
                        with st.expander("원본 응답 보기"):
                            st.code(response)
                
                except Exception as e:
                    st.error(f"오류 발생: {str(e)}")
                    return
    
    st.divider()

    # ============ 결과 표시 ============
    
    if "storyboard_data" in st.session_state and st.session_state["storyboard_data"]:
        data = st.session_state["storyboard_data"]
        scenes = data.get("scenes", [])
        
        if not scenes:
            st.warning("생성된 장면이 없습니다.")
            return
        
        st.header(f"📋 생성된 스토리보드 ({len(scenes)}개 장면)")
        
        # 메타 정보
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**🎨 스타일:** {st.session_state.get('storyboard_style', '-')}")
        with col2:
            st.markdown(f"**🎬 모드:** {st.session_state.get('storyboard_mode', '-')}")
        with col3:
            st.markdown(f"**⚓ Anchor:** {st.session_state.get('storyboard_visual_anchor', '없음')[:30]}...")
        
        if data.get("reasoning"):
            st.info(f"💡 **AI의 판단:** {data['reasoning']}")
        
        st.divider()
        
        # ============ 장면별 표시 + 실시간 수정 UI ============
        
        for scene in scenes:
            scene_num = scene["scene_number"]
            source_lyrics = scene.get("source_lyrics", "")
            korean_ctx = scene["korean_context"]
            english_prompt = scene["english_prompt"]
            tech_notes = scene.get("technical_notes", "")
            
            with st.expander(f"🎬 장면 {scene_num}: {korean_ctx[:50]}..."):
                
                # ⭐ 가사 원문 (v3.1 신규 - 맨 위에 표시)
                if source_lyrics and source_lyrics != "가사 매핑 없음":
                    st.markdown("**📖 기반 가사:**")
                    st.info(source_lyrics)
                    st.divider()
                
                # 한글 맥락
                st.markdown("**📝 한글 맥락:**")
                st.success(korean_ctx)
                
                # 영어 프롬프트
                st.markdown("**🔤 영어 프롬프트:**")
                st.code(english_prompt, language=None)
                
                # 기술 노트 (서사 중심 모드만)
                if tech_notes:
                    st.caption(f"🎥 **연출 노트:** {tech_notes}")
                
                st.divider()
                
                # ============ 실시간 수정 UI ============
                
                st.markdown("#### ✏️ 이 장면 수정하기")
                
                # 수정용 키 생성
                override_key = f"scene_{scene_num}_override"
                
                # 기존 수정사항 확인
                if override_key in st.session_state["scene_overrides"]:
                    current_override = st.session_state["scene_overrides"][override_key]
                else:
                    current_override = korean_ctx
                
                # 한글 수정 입력
                modified_korean = st.text_area(
                    "한글 장면 설명 수정",
                    value=current_override,
                    height=80,
                    key=f"modify_korean_{scene_num}",
                    help="이 장면을 어떻게 바꾸고 싶은지 한글로 작성하세요"
                )
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if st.button(f"🔄 장면 {scene_num} 영어로 변환", key=f"convert_{scene_num}"):
                        if client is None:
                            st.error("API 키가 설정되지 않았습니다.")
                        else:
                            with st.spinner("변환 중..."):
                                try:
                                    visual_anchor_val = st.session_state.get("storyboard_visual_anchor", "")
                                    style_kw = st.session_state.get("storyboard_style_keywords", "")
                                    
                                    new_english = translate_korean_to_english(
                                        client, 
                                        modified_korean, 
                                        visual_anchor_val, 
                                        style_kw
                                    )
                                    
                                    # 수정사항 저장
                                    st.session_state["scene_overrides"][override_key] = modified_korean
                                    
                                    # 장면 데이터 업데이트
                                    scene["korean_context"] = modified_korean
                                    scene["english_prompt"] = new_english
                                    
                                    st.success(f"✅ 장면 {scene_num} 업데이트 완료!")
                                    st.rerun()
                                
                                except Exception as e:
                                    st.error(f"변환 실패: {str(e)}")
                
                with col_b:
                    if st.button(f"↩️ 장면 {scene_num} 원래대로", key=f"reset_{scene_num}"):
                        # 수정사항 삭제
                        if override_key in st.session_state["scene_overrides"]:
                            del st.session_state["scene_overrides"][override_key]
                        st.success(f"장면 {scene_num}을 원래대로 되돌렸습니다!")
                        st.rerun()
        
        st.divider()
        
        # ============ 내보내기 탭 ============
        
        st.header("📤 내보내기")
        
        export_tabs = st.tabs(["📋 Midjourney 전용", "🎬 영상 편집용", "📦 전체"])
        
        # 준비: URL 파라미터
        cref_param = ""
        if st.session_state.get("char_url"):
            cref_param = f" --cref {st.session_state['char_url']}"
        
        sref_param = ""
        if st.session_state.get("style_url"):
            sref_param = f" --sref {st.session_state['style_url']} --sw 1000"
        
        with export_tabs[0]:
            st.markdown("### 📋 Midjourney 프롬프트 (복사해서 Discord에 붙여넣기)")
            
            midjourney_prompts = []
            for scene in scenes:
                prompt = f"/imagine prompt: {scene['english_prompt']}{cref_param}{sref_param} --ar 16:9 --v 6.1"
                midjourney_prompts.append(f"장면 {scene['scene_number']}: {scene['korean_context']}\n{prompt}\n")
            
            full_mj_text = "\n".join(midjourney_prompts)
            
            st.text_area(
                "전체 Midjourney 프롬프트",
                value=full_mj_text,
                height=400,
                help="Ctrl+A로 전체 선택 후 복사하세요"
            )
            
            st.download_button(
                "💾 Midjourney 프롬프트 다운로드",
                data=full_mj_text,
                file_name=f"midjourney_prompts_{len(scenes)}scenes.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with export_tabs[1]:
            st.markdown("### 🎬 영상 편집용 (한글 설명 + 영어 프롬프트)")
            
            editing_text = []
            for scene in scenes:
                editing_text.append(f"장면 {scene['scene_number']}")
                editing_text.append(f"한글: {scene['korean_context']}")
                editing_text.append(f"영어: {scene['english_prompt']}")
                if scene.get("technical_notes"):
                    editing_text.append(f"연출: {scene['technical_notes']}")
                editing_text.append("=" * 80)
                editing_text.append("")
            
            full_editing_text = "\n".join(editing_text)
            
            st.text_area(
                "편집용 스토리보드",
                value=full_editing_text,
                height=400
            )
            
            st.download_button(
                "💾 편집용 스토리보드 다운로드",
                data=full_editing_text,
                file_name=f"editing_storyboard_{len(scenes)}scenes.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with export_tabs[2]:
            st.markdown("### 📦 전체 데이터 (JSON)")
            
            full_export_data = {
                "metadata": {
                    "total_scenes": len(scenes),
                    "mode": st.session_state.get("storyboard_mode", ""),
                    "style": st.session_state.get("storyboard_style", ""),
                    "visual_anchor": st.session_state.get("storyboard_visual_anchor", ""),
                    "char_url": st.session_state.get("char_url", ""),
                    "style_url": st.session_state.get("style_url", ""),
                    "reasoning": data.get("reasoning", "")
                },
                "scenes": scenes
            }
            
            json_str = json.dumps(full_export_data, ensure_ascii=False, indent=2)
            
            st.text_area(
                "JSON 데이터",
                value=json_str,
                height=400
            )
            
            st.download_button(
                "💾 JSON 다운로드",
                data=json_str,
                file_name=f"storyboard_{len(scenes)}scenes.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.divider()
        
        # 초기화 버튼
        if st.button("🔄 새로운 스토리보드 생성", use_container_width=True):
            if "storyboard_data" in st.session_state:
                del st.session_state["storyboard_data"]
            st.session_state["scene_overrides"] = {}
            st.rerun()
    
    else:
        st.markdown("---")
        st.markdown("""
        ### 🚀 시작하기
        
        1. **가사 입력** - Tab 1에서 생성했다면 자동으로 불러와집니다
        2. **장면 생성 방식 선택**
           - 📜 **서사 중심**: AI가 가사를 분석하여 12~25개 최적 장면 수 결정
           - 🎞️ **20개 장면**: 각 장면마다 A/B컷
           - 🎬 **40개 장면**: 독립적인 상세 장면
        3. **Visual Anchor 설정** (선택) - AI 추천 또는 직접 입력
        4. **스타일 선택** - 11가지 프리미엄 스타일 중 선택
        5. **생성 버튼 클릭!**
        
        > 🎭 **서사 중심 모드의 차별점:**
        > 
        > - "위대한 다섯 별" → 성당의 스테인드글라스 빛과 성자들의 그림자
        > - "성인들도 못 고친 스트레스" → 소주잔을 내리치는 순간의 액체 비산
        > - "세상이 아름답게 보이는 기적" → 취기 어린 POV의 몽환적 보케 효과
        """)
