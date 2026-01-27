"""
tabs/lyrics.py - Suno/Udio 최적화 가사 생성 탭 (Tab 1)
제목 + 구조적 태그 + 보컬/연출 지시어 + 수정 기능 포함 + 멀티 페르소나 모드 트리거
Clean & Epic 철학 완전 통합 버전
"""

import streamlit as st
from utils import get_gpt_response
from .lyrics_config import GENRE_LIST, VIBE_LIST, SYSTEM_ROLE


# ============ Helper Functions ============

def get_vocal_instruction(vocal_type: str) -> str:
    """
    보컬 타입에 따른 구조 강제 지시문을 반환합니다.
    
    Args:
        vocal_type: 선택된 보컬 타입
        
    Returns:
        보컬 타입별 상세 지시문
    """
    instructions = {
        "솔로 (남성)": """
## 보컬 구조 지시사항 (남성 솔로 - Clean & Epic)
- 모든 파트에 [Verse], [Chorus], [Bridge] 태그 필수
- 보컬 타입 명시: [Male Vocal], [Male Voice]
- 감정 변화를 연출 지시어로 표현 (명료성 우선):
  * 약한 감정: (Soft voice), (Gentle singing), (Intimate delivery)
  * 보통 감정: (Clear vocal), (Steady voice), (Articulate tone)
  * 강한 감정: (Powerful belting), (Emotional cry), (Soaring high note)
- ⚠️ 금지: (Gritty), (Shouting), (Aggressive), (Screaming)
- Sound FX 활용: (Guitar riff), (Drum hit), (Deep bass pulse), (Clock ticking)

**출력 예시:**
[Intro - Male]
(Soft acoustic guitar, atmospheric)
가사 내용...

[Verse 1 - Male]
(Clear vocal, steady beat, articulate delivery)
가사 내용...
(Building emotion, maintaining clarity)
가사 내용...
""",
        
        "솔로 (여성)": """
## 보컬 구조 지시사항 (여성 솔로 - Clean & Epic)
- 모든 파트에 [Verse], [Chorus], [Bridge] 태그 필수
- 보컬 타입 명시: [Female Vocal], [Female Voice]
- 감정 변화를 연출 지시어로 표현 (명료성 우선):
  * 부드러운: (Soft voice), (Breathy vocal), (Gentle delivery)
  * 강렬한: (Powerful voice), (Soaring high note), (Clear belting)
  * 감성적: (Emotional vocal), (Well-enunciated), (Expressive tone)
- ⚠️ 금지: (Harsh), (Screaming), (Distorted)
- Sound FX 활용: (Piano melody), (Cinematic strings), (Soft rain), (Wind chimes)

**출력 예시:**
[Intro - Female]
(Soft piano intro, cinematic atmosphere)
가사 내용...

[Verse 1 - Female]
(Breathy vocal, intimate, clear enunciation)
가사 내용...
(Building to chorus, maintaining vocal clarity)
가사 내용...
""",
        
        "혼성 듀엣 (남/녀)": """
## 보컬 구조 지시사항 (혼성 듀엣) ⭐ 매우 중요!

### ⚠️ 핵심 원칙: 블록 단위 배분 (Block Assignment)
**DO NOT alternate lines frequently!** 
리스너의 몰입을 위해 **섹션 전체를 한 명에게 배정**하세요.

### 몰입감 중심 구조 (Immersive Structure)

**1. 블록 단위 파트 배분:**
- ❌ 나쁜 예: 한 소절씩 남녀가 번갈아 부르기 (음색이 튐, 몰입 방해)
- ✅ 좋은 예: [Verse 1] 전체는 남성, [Verse 2] 전체는 여성

**2. 빌드업 구조 (Emotional Buildup):**
- **[Intro]:** 한 명 또는 악기만 (분위기 조성)
- **[Verse 1 - Male or Female]:** 한 명이 **최소 4~8행 이상** 전담하여 서사 시작
- **[Verse 2 - Opposite Gender]:** 다른 한 명이 **최소 4~8행 이상** 전담하여 감정 확장
- **[Pre-Chorus - Call & Response]:** 여기서 처음으로 짧게 대화하듯 교차 (긴장감 조성)
- **[Chorus - Together/Harmony]:** 두 보컬 화음 위주, 음색 섞이게 구성
- **[Bridge - Emotional Peak]:** 감정 폭발, Together 또는 Solo 섹션

**3. Clean & Epic 보컬 지시어:**
- 남성: (Clear male vocal), (Articulate baritone), (Smooth delivery)
- 여성: (Clear female vocal), (Crisp soprano), (Well-enunciated)
- ⚠️ 금지: (Gritty), (Aggressive), (Harsh), (Screaming)

**4. 교차 허용 시점:**
- Pre-Chorus에서만 짧게 대화
- Bridge에서 클라이맥스 연출
- Outro에서 여운

### 구조적 예시 (Few-Shot) - 반드시 이 형식 따를 것!

```
[Intro - Instrumental or Solo]
(Cinematic strings, atmospheric)
(Optional: 한 명이 짧게 시작)

[Verse 1 - Male]
(Clear male vocal, steady rhythm, articulate)
남성이 4~8행 이상 부르며 이야기 시작
음색에 적응할 시간을 충분히 주세요
청자가 이 보컬에 몰입하도록
파트를 쪼개지 마세요

[Verse 2 - Female]
(Soft female vocal, emotional depth, clear enunciation)
여성이 4~8행 이상 부르며 이야기 전개
남성 파트와는 다른 관점 제시
역시 충분한 분량으로
섹션 전체를 전담합니다

[Pre-Chorus - Call & Response]
(Building tension, clean crisp delivery)
(Male) 짧은 질문 또는 제시
(Female) 짧은 응답
(Male) 다시 한 번
(Female) 마지막 응답
(Together) 함께 브릿지로

[Chorus - Together/Harmony]
(Full power, dual harmony, layered vocals, clear delivery)
함께 부르는 후렴구
화음 위주로 구성
두 음색이 자연스럽게 섞임
여기서는 개별 태그 대신 Together 사용

[Bridge - Emotional Peak]
(Male leading or Female leading, powerful yet clear)
필요시 한 명이 브릿지 전담
또는 감정 폭발을 위한 교차

[Chorus - Together/Harmony]
(Powerful duet, final climax, maintaining clarity)
마지막 후렴구
두 보컬 최대 시너지

[Outro - Together or Fade]
(Soft fade out, gentle ending)
함께 마무리 또는 한 명이 여운
```

### 절대 규칙 (Absolute Rules)
1. **Do not alternate lines frequently within a single section**
2. **Assign full sections (4-8+ lines) to each gender for better immersion**
3. **Allow mixing only in Pre-Chorus, Chorus, Bridge, and Outro**
4. **Verse sections must be dominated by one vocalist**
5. **Give listeners time to adapt to each vocal tone**
6. **Always use clear, articulate vocal descriptions (Clean & Epic)**
""",
        
        "합창/콰이어": """
## 보컬 구조 지시사항 (합창/콰이어 - Clean & Epic)
- [Choir], [Chorus Group], [Ensemble] 태그 사용
- 파트별 성부 구분: [Soprano], [Alto], [Tenor], [Bass]
- 웅장한 분위기 연출 지시어 (Clean & Epic):
  * (Full choir with clear harmony), (Layered voices, well-blended)
  * (Cinematic orchestral backing), (Epic crescendo with clarity)
- ⚠️ 종교적 색채 제거: Pipe Organ, Church Choir 대신 Cinematic Strings, Epic Brass 사용

**출력 예시:**
[Intro - Choir]
(Soft choir humming, a cappella, clear harmony)
Ooh... Aah...

[Verse 1 - Lead + Choir]
(Lead vocal with choir backing, cinematic atmosphere)
가사 내용...
(Choir: Clear harmony response)
""",
        
        "AI/로봇 보컬": """
## 보컬 구조 지시사항 (AI/로봇 보컬 - Clean & Epic)
- [Robotic Voice], [Vocoder], [Auto-tuned], [Synthetic Vocal] 태그 사용
- 기계적 효과 지시어 (명료성 유지):
  * (Vocoder effect with clear pitch), (Clean digital vocal)
  * (Auto-tune heavy but articulate), (Synthesized voice, crisp)
- 사이버펑크/전자음악 분위기
- Sound FX: (Beep), (Static noise), (Digital glitch), (Circuit sound)

**출력 예시:**
[Intro - Robotic]
(Heavy vocoder, clean digital processing)
가사 내용...
(Digital distortion, maintaining clarity)
""",
    }
    
    return instructions.get(vocal_type, instructions["솔로 (남성)"])


def parse_title_and_lyrics(response: str) -> tuple[str, str, str]:
    """
    GPT 응답에서 제목, 가사, Mureka 스타일 태그를 분리합니다.
    
    Args:
        response: GPT 응답 텍스트
        
    Returns:
        tuple: (제목, 가사, Mureka 스타일 태그)
    """
    title = ""
    lyrics = response
    mureka_tag = ""
    
    # Mureka 태그 추출
    mureka_markers = ["💡 **Mureka V7.6 Pro 스타일 태그:**", "💡 Mureka V7.6 Pro", "Mureka V7.6 Pro 스타일 태그:"]
    for marker in mureka_markers:
        if marker in response:
            parts = response.split(marker)
            if len(parts) > 1:
                mureka_section = parts[1]
                # Suno 태그나 다른 섹션 전까지
                end_markers = ["💡 **Suno", "💡 Suno", "---\n💡"]
                mureka_end = len(mureka_section)
                for end_marker in end_markers:
                    if end_marker in mureka_section:
                        mureka_end = mureka_section.find(end_marker)
                        break
                
                mureka_tag = mureka_section[:mureka_end].strip()
                mureka_tag = mureka_tag.strip('`').strip()
                break
    
    # 제목 추출
    title_markers = ["[제목]", "[Title]", "제목:", "Title:", "**제목:**", "**제목**:"]
    for marker in title_markers:
        if marker in response:
            parts = response.split(marker, 1)
            if len(parts) > 1:
                title_part = parts[1].strip()
                title_lines = title_part.split("\n")
                title = title_lines[0].strip().strip("*").strip('"').strip("'").strip()
                
                if len(title_lines) > 1:
                    lyrics = "\n".join(title_lines[1:]).strip()
                else:
                    lyrics = parts[0].strip()
                break
    
    # 제목이 없으면 첫 줄을 제목으로 시도
    if not title and response.strip():
        lines = response.strip().split("\n")
        if lines[0].startswith("#") or lines[0].startswith("**"):
            title = lines[0].strip("#").strip("*").strip()
            lyrics = "\n".join(lines[1:]).strip()
    
    return title, lyrics, mureka_tag


# ============ Main Render Function ============

def render(client):
    """가사 생성 탭을 렌더링합니다."""
    
    st.header("🎵 Step 1: Suno/Udio 최적화 가사 생성기 (Clean & Epic)")
    st.markdown("""
    **AI 음악 생성 툴에 최적화된 가사**를 만듭니다.
    
    > 🎼 *"구조적 태그 + Clean 보컬 + Epic 사운드 = 완벽한 AI 음악"*
    """)
    
    st.info("""
    ✨ **Suno/Udio 최적화 기능 (Clean & Epic):**
    - 🎤 **보컬 타입별 맞춤 구조** (솔로, 듀엣, 합창 등)
    - 🏷️ **구조적 태그 자동 삽입** ([Intro], [Verse], [Chorus])
    - 🎭 **명료한 연출 지시어** ((Clear vocal), (Cinematic strings))
    - 🔊 **세련된 Sound FX** ((Deep bass pulse), (Epic brass hits))
    - 🛠️ **가사 깎기 기능** (외부에서 수정한 가사 포맷팅)
    - 🎬 **Clean & Epic 철학** (웅장하되 명료하게, 종교적 색채 제거)
    """)
    
    st.divider()
    
    # ============ 기본 정보 섹션 ============
    st.subheader("📝 기본 정보")
    
    # ⭐ Tab 1-A에서 넘어온 주제 자동 입력
    default_topic = ""
    if "expanded_theme_for_lyrics" in st.session_state:
        default_topic = st.session_state["expanded_theme_for_lyrics"]
        st.success("✅ Tab 1-A에서 선택한 주제가 자동으로 입력되었습니다!")
        
        # 추천사항도 표시
        if any(key in st.session_state for key in ["recommended_genre", "recommended_vocal", "recommended_vibe", "recommended_keywords"]):
            st.info(f"""
            💡 **AI 추천 설정:**
            - 장르: {st.session_state.get('recommended_genre', '-')}
            - 보컬: {st.session_state.get('recommended_vocal', '-')}
            - Vibe: {st.session_state.get('recommended_vibe', '-')}
            - 키워드: {st.session_state.get('recommended_keywords', '-')}
            """)
    
    topic = st.text_area(
        "🎯 노래 주제 / 스토리 / 긴 이야기",
        value=default_topic,
        placeholder="예: 새벽 3시 편의점에서 마주친 전 여자친구\n\n긴 내용도 OK (소설 줄거리, 일기 등)",
        height=150,
        help="한 줄이든 장문이든 OK! AI가 핵심을 추출하여 가사로 만듭니다. Tab 1-A에서 주제를 확장할 수도 있습니다!"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        genre = st.selectbox(
            "🎸 장르",
            options=GENRE_LIST,
            help="원하는 장르가 없으면 '직접 입력' 선택"
        )
    
    with col2:
        # ⭐ NEW: 보컬 타입 선택
        vocal_type = st.selectbox(
            "🎤 보컬 타입",
            options=[
                "솔로 (남성)",
                "솔로 (여성)",
                "혼성 듀엣 (남/녀)",
                "합창/콰이어",
                "AI/로봇 보컬"
            ],
            help="보컬 타입에 따라 구조가 달라집니다"
        )
    
    custom_genre = ""
    if genre == "직접 입력 (Custom)":
        custom_genre = st.text_input(
            "✍️ 장르 직접 입력",
            placeholder="예: 1990년대 LA 갱스터 랩, 판소리 퓨전 록"
        )
    
    st.divider()
    
    # ============ 분위기 섹션 ============
    st.subheader("🎭 분위기 & 스타일")
    
    col1, col2 = st.columns(2)
    
    with col1:
        vibe_options = [v[0] for v in VIBE_LIST]
        selected_vibe_name = st.selectbox(
            "Vibe (반전 매력)",
            options=vibe_options
        )
        selected_vibe = next((v for v in VIBE_LIST if v[0] == selected_vibe_name), VIBE_LIST[0])
    
    with col2:
        language = st.selectbox(
            "🌐 가사 언어",
            ["한국어", "영어", "한영 혼합", "일본어", "한일 혼합"]
        )
    
    with st.expander("⚙️ 추가 옵션"):
        era = st.selectbox(
            "📅 시대적 분위기",
            ["현대 (2020s)", "2010년대", "2000년대", "1990년대", "1980년대", "미래적", "시대 무관"]
        )
        
        intensity = st.select_slider(
            "🔥 감정 강도",
            ["차분하게", "적당히", "격렬하게", "폭발적으로"],
            value="적당히"
        )
        
        keywords = st.text_input(
            "🔑 포함할 키워드 (선택)",
            placeholder="예: 벚꽃, 새벽, 소주, 첫사랑"
        )
    
    st.divider()
    
    # ============ 생성 버튼 ============
    if st.button("🎤 Suno/Udio 최적화 가사 생성", type="primary", use_container_width=True):
        if not topic:
            st.error("노래 주제를 입력해주세요.")
            return
        if genre == "선택해주세요":
            st.error("장르를 선택해주세요.")
            return
        if genre == "직접 입력 (Custom)" and not custom_genre:
            st.error("장르를 직접 입력해주세요.")
            return
        if client is None:
            st.error("API 키가 설정되지 않았습니다.")
            return
        
        final_genre = custom_genre if genre == "직접 입력 (Custom)" else genre
        
        # 보컬 타입별 지시문 가져오기
        vocal_instruction = get_vocal_instruction(vocal_type)
        
        # ============ ⭐ Vibe 기반 모드 트리거 (Clean & Epic 버전) ⭐ ============
        mode_trigger = ""
        mode_examples = ""
        
        if selected_vibe_name in ["웃기지만 진지하게 (Satire)", "슬픈데 신나게 (Paradox)"]:
            mode_trigger = """
## ⚠️ 🌟 [모드 2: 공감과 반전의 엔터테이닝 모드] 강력 발동! (Clean & Epic 버전) ⚠️

**당신의 임무: 시청자가 "와, 이거 내 얘기네!"라며 무릎을 탁 치게 만들기**

### 핵심 원칙 (Clean & Epic):
1. **사소한 것을 영화적으로 장엄하게** - 치킨, 배달, 배터리, 재난문자 → 시네마틱하게
2. **스케일의 부조화** - 핸드폰 1% → 영화 OST급 비극 / 배달 음식 → 영웅의 귀환
3. **극단적 대비** - 밝은 멜로디 + 현실 고통 가사
4. **100% 진지하게** - 억지 유머 금지! 진지할수록 더 웃김!

### ⚠️ Clean & Epic 필수 규칙:
- **보컬**: `Clear rap flow`, `Articulate delivery`, `Crisp vocal` - 명료성 최우선
- **악기**: `Cinematic Strings`, `Epic Brass Hits`, `Deep Sub-bass` - 영화적 웅장함
- **절대 금지**: `Pipe Organ`, `Church Choir`, `Gritty vocal`, `Shouting`

### 연출 지시어 (Clean & Epic 버전):
- [Intro - Cinematic Strings & Deep Sub-bass] 또는 [Intro - Bright Acoustic Guitar]
- [Chorus - Epic Brass Hits with Clear Vocal] 또는 [Chorus - Modern Trap Beat]
- 구체적 디테일: "부산 앞바다 파고", "1% 배터리 경고", "양념 반 후라이드 반"

### 'Aha!' 대표 예시: 500km의 사이렌
- ✅ 웅장하지만 명료한 랩 (Clear rap, not gritty)
- ✅ 시네마틱 악기 (Cinematic Strings, not Pipe Organ)
- ✅ 영화적 웅장함 (Epic Brass, Deep Sub-bass)
- ✅ 사소한 것(재난문자)을 장엄하게, 하지만 세련되게

**절대 규칙: 웅장하되 명료하게! 영화 OST처럼, 성가대처럼 쓰지 마세요!**
"""
            mode_examples = """

## 🎬 엔터테이닝 모드 출력 예시 (Clean & Epic 표준)

**대표 예시: 500km의 사이렌: 03:00 AM**
```
[제목]
500km의 사이렌: 03:00 AM

[Intro - Cinematic Strings & Deep Sub-bass]
(Epic film score atmosphere, modern production)
(Clock ticking sound effect at 3 AM)

[Verse 1 - Clear Male Rap, Articulate Mid-range]
(Clean delivery, crisp enunciation)
새벽 세 시, 서울 빌딩 숲 속
내 방 한 칸의 평화가 깨지는 순간
(Deep bass pulse)
핸드폰 화면 속 경고음이 울리네
부산 앞바다 파고 3미터라는데

[Pre-Chorus - Building Tension]
(Trap hi-hats enter, clean crisp rhythm)
재난문자여, 재난문자여
왜 너는 지역 구분을 못 하는가

[Chorus - Epic Brass Hits with Clear Vocal]
(Full cinematic power, articulate delivery)
500킬로미터를 건너
나의 새벽 3시를 침략하는
이 부조리한 시스템이여
```

**포인트:**
- ✅ Clear rap flow (가사 또박또박 들림)
- ✅ Cinematic Strings & Epic Brass (종교적 색채 없이 영화적)
- ✅ Deep Sub-bass (현대적 웅장함)
- ✅ 사소한 재난문자 → 영화급 서사

**추가 예시: 배달의 기적 (Clean & Epic 버전)**
```
[Intro - Cinematic Orchestral Build-up]
(Epic film score strings, anticipation)

그가 오신다
60분을 기다린 끝에
(Timpani rolls, modern production)

[Verse 1 - Clear Baritone Vocal, Articulate]
(Smooth delivery, well-enunciated)
저 멀리서 들려오는
오토바이 배기음 소리가
영화 속 영웅의 테마곡처럼 귀를 울리네

[Chorus - Epic Brass & Modern Beat]
(Cinematic crescendo, clear vocal delivery)
오오~ 양념 반 후라이드 반의 구원이여!
```
"""
        
        else:
            mode_trigger = """
## ⚠️ [모드 1: 진솔한 서사 모드] 사용 (Clean & Epic 적용) ⚠️

**당신의 임무: 깊은 울림을 주는 진정성 있는 가사 작성**

### 핵심 원칙:
1. **일상의 세밀한 감정선** - 작은 순간들의 의미 포착
2. **문학적이고 시적인 표현** - 은유와 상징 활용
3. **억지 유머 없이** - 진솔하고 가슴 시린 고백
4. **점층적 고조** - 감정이 자연스럽게 쌓여가도록

### ⚠️ Clean & Epic 필수 규칙:
- **보컬**: `Clear emotional vocal`, `Smooth delivery`, `Well-enunciated`
- **악기**: 장르 특성 살리되, 명료성 유지
- **웅장함 필요 시**: `Cinematic Strings`, `Orchestral arrangement` (종교적 색채 제거)

### 연출 지시어:
- [Intro - Soft piano intro, atmospheric]
- [Chorus - Full band, emotional peak, clear vocal]
- 계절과 자연의 비유 (벚꽃, 눈, 비)
- 섬세한 감정 묘사

**절대 규칙: 진부한 클리셰를 피하고, 참신하면서도 공감 가능한 표현을 사용하세요.**
"""
            mode_examples = ""
        
        # ============ Generation Mode Prompt ============
        user_prompt = f"""{mode_trigger}

## 기본 정보
- **주제/스토리**: {topic}
- **장르**: {final_genre}
- **보컬 타입**: {vocal_type}
- **분위기(Vibe)**: {selected_vibe_name}
- **언어**: {language}
- **시대적 분위기**: {era}
- **감정 강도**: {intensity}
{f'- **포함 키워드**: {keywords}' if keywords else ''}

{vocal_instruction}

## ⚠️ Suno/Udio 최적화 필수 요구사항 (Clean & Epic) ⚠️

1. **구조적 태그 필수**:
   - [Intro], [Verse 1], [Pre-Chorus], [Chorus], [Verse 2], [Bridge], [Outro]
   - 보컬 타입에 따라 화자 명시 (예: [Verse 1 - Male])

2. **듀엣 곡 몰입감 규칙** (혼성 듀엣 선택 시):
   - ⚠️ **블록 단위 배분**: 한 소절씩 교차 금지! 섹션 전체를 한 명에게 배정
   - ✅ [Verse 1] 전체 = 한 명, [Verse 2] 전체 = 다른 한 명
   - ✅ 교차는 Pre-Chorus, Bridge에서만 허용
   - ✅ Chorus는 Together/Harmony 위주
   - **Do not alternate lines frequently within sections!**

3. **연출 지시어 필수 (Clean & Epic)**:
   - 가사 줄 사이에 괄호로 음악적 연출 삽입
   - 예: (Cinematic strings intro), (Clear vocal), (Epic brass hits), (Fade out)
   - **보컬**: Clear, Crisp, Articulate, Smooth 등 명료성 강조
   - **악기**: Cinematic Strings, Epic Brass, Deep Sub-bass 등 영화적 웅장함

4. **Sound FX 활용**:
   - 분위기에 맞는 효과음 지시어 추가
   - 예: (Clock ticking), (Rain falling), (Thunder), (Deep bass pulse)

5. **Mureka & Suno 스타일 태그 생성 (Clean & Epic)**:
   - Mureka V7.6 Pro: 악기, 장르, 보컬(Clear/Crisp 명시), BPM, 분위기
   - Suno AI: 5단계 문장형 프롬프트
     * Performance 단계: 명료성 강조 (clear, articulate, crisp, avoiding gritty/aggressive)
     * Production 단계: 품질 키워드 필수 (high-definition, spacious, polished, clear lyric delivery)

{mode_examples}

## 출력 형식 (Suno/Udio 최적화 - Clean & Epic)

[제목]
(주제와 장르에 어울리는 제목)

[가사]
[Intro]
(Clean & Epic 연출 지시어)
가사 내용...

[Verse 1]
(Clear vocal, articulate delivery)
가사 내용...
(감정 변화 지시어)
가사 내용...

[Pre-Chorus]
(Build up, clean rhythm)
가사 내용...

[Chorus]
(Epic power, clear hook line)
가사 내용...

... (계속)

---
💡 **Mureka V7.6 Pro 스타일 태그 (Clean & Epic):**
`[시네마틱 악기], [장르], [Clear/Crisp 보컬], [BPM], [분위기]`
예: `Cinematic Strings, Deep Sub-bass, Epic Brass Hits, Modern Hip-Hop, Clear Articulate Male Vocal, 85BPM, Epic yet Clean, Film Score Vibe`

---
💡 **Suno 최적화 프롬프트 (5단계 문장형 - Clean & Epic):**
(5단계 공식에 따라 하나의 영어 문단으로 작성)
A [Gender] vocalist sings over a [Genre] piece with [cinematic/modern] elements. It features a [Tempo] and an [epic yet clean Mood], set in a [Key]. The [Cinematic Instrument] plays [Sharp/Clean Style], while the [Deep Bass] provides a [clean foundation]. The vocals are delivered in a [clear/articulate Range] with [smooth technique], avoiding any [gritty/aggressive] qualities. The production is [high-definition/spacious], featuring [clear mixing] with emphasis on [clear lyric delivery], and follows a [Structure].

지금 바로 Clean & Epic 원칙에 따라 Suno/Udio에서 최상의 결과를 낼 수 있는 가사를 작성해주세요!"""

        with st.spinner(f"🎼 '{final_genre}' / '{vocal_type}' 가사 생성 중... (Clean & Epic 적용)"):
            try:
                response = get_gpt_response(client, SYSTEM_ROLE, user_prompt)
                
                # 제목, 가사, Mureka 태그 분리
                title, lyrics, mureka_tag = parse_title_and_lyrics(response)
                
                if not title:
                    title = f"{topic[:20]}... ({final_genre})"
                
                # 세션 스테이트에 저장
                st.session_state["song_title"] = title
                st.session_state["lyrics"] = response
                st.session_state["mureka_style_tag"] = mureka_tag
                st.session_state["lyrics_topic"] = topic
                st.session_state["lyrics_genre"] = final_genre
                st.session_state["lyrics_vibe"] = selected_vibe_name
                st.session_state["lyrics_vocal_type"] = vocal_type  # 보컬 타입 저장
                
                st.success("🎉 Clean & Epic 가사가 완성되었습니다!")
                st.rerun()
                
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
                return
    
    # ============ 결과 표시 ============
    st.divider()
    
    if "lyrics" in st.session_state and st.session_state["lyrics"]:
        # 제목 표시
        if st.session_state.get("song_title"):
            st.header(f"🎵 {st.session_state['song_title']}")
        
        st.subheader("📜 생성된 가사")
        
        # 메타 정보
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**🎸 장르:** {st.session_state.get('lyrics_genre', '-')}")
        with col2:
            st.markdown(f"**🎤 보컬:** {st.session_state.get('lyrics_vocal_type', '-')}")
        with col3:
            st.markdown(f"**🎭 Vibe:** {st.session_state.get('lyrics_vibe', '-')}")
        
        st.divider()
        
        lyrics_content = st.session_state["lyrics"]
        
        # 태그 분리
        mureka_tags = None
        suno_tags = None
        main_lyrics = lyrics_content
        
        # Mureka 태그 추출
        if "Mureka V7.6 Pro" in lyrics_content or "Mureka" in lyrics_content:
            mureka_markers = ["💡 **Mureka", "💡 Mureka", "Mureka V7.6 Pro"]
            for marker in mureka_markers:
                if marker in lyrics_content:
                    mureka_start = lyrics_content.find(marker)
                    mureka_end = lyrics_content.find("💡 **Suno", mureka_start)
                    if mureka_end == -1:
                        mureka_end = lyrics_content.find("💡 Suno", mureka_start)
                    if mureka_end == -1:
                        mureka_end = len(lyrics_content)
                    
                    mureka_tags = lyrics_content[mureka_start:mureka_end].strip()
                    main_lyrics = lyrics_content[:mureka_start].strip()
                    lyrics_content = lyrics_content[mureka_end:]
                    break
        
        # Suno 5단계 프롬프트 추출
        if "Suno 최적화 프롬프트" in lyrics_content or "Suno AI" in lyrics_content or "스타일 태그" in lyrics_content:
            tag_markers = ["💡 **Suno", "💡 Suno", "---\n💡", "Suno AI", "Suno 최적화"]
            for marker in tag_markers:
                if marker in lyrics_content:
                    split_index = lyrics_content.find(marker)
                    if mureka_tags is None:
                        main_lyrics = lyrics_content[:split_index].strip()
                    suno_tags = lyrics_content[split_index:].strip()
                    break
        
        # 가사 표시
        st.markdown("**📜 가사 전문**")
        st.code(main_lyrics, language=None)
        st.caption("👆 위 가사를 길게 눌러 복사하세요 (모바일)")
        
        char_count = len(main_lyrics.replace(" ", "").replace("\n", ""))
        st.caption(f"📊 총 {char_count}자 (공백 제외)")
        
        # Mureka 태그 표시
        if st.session_state.get("mureka_style_tag"):
            st.divider()
            st.success("🎵 **Mureka V7.6 Pro 전용 스타일 태그 (Clean & Epic)**")
            
            mureka_tag_display = st.session_state["mureka_style_tag"]
            st.code(mureka_tag_display, language=None)
            
            st.caption("💡 위 태그를 Mureka V7.6 Pro의 'Style Prompt'에 복사하세요!")
            
            # 다운로드 버튼
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📋 Mureka 태그",
                    data=mureka_tag_display,
                    file_name=f"{st.session_state.get('song_title', 'song')}_mureka.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with col2:
                st.download_button(
                    label="📝 가사 전문",
                    data=main_lyrics,
                    file_name=f"{st.session_state.get('song_title', 'song')}_lyrics.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        # Suno 프롬프트 표시
        if suno_tags:
            st.divider()
            st.info("🎵 **Suno 최적화 프롬프트 (Copy & Paste - Clean & Epic)**")
            
            # Suno 프롬프트 추출 (마크다운 제거)
            suno_prompt_text = suno_tags.replace("💡 **Suno 최적화 프롬프트 (Copy & Paste):**", "").replace("💡 Suno", "").strip()
            # 첫 문단만 추출 (실제 프롬프트 부분)
            if "\n\n" in suno_prompt_text:
                suno_prompt_text = suno_prompt_text.split("\n\n")[0]
            
            st.code(suno_prompt_text, language=None)
            st.caption("👆 위 문단을 Suno AI의 프롬프트 입력란에 붙여넣으세요!")
        
        st.divider()
        
        # ============ ⭐ NEW: 장르/스타일만 변경하기 ============
        with st.expander("🎨 장르/스타일만 변경하기"):
            st.markdown("""
            **💡 가사는 그대로 두고 장르와 스타일 태그만 바꿉니다.**
            
            예: 발라드로 만든 가사를 시티팝 스타일로 변경
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                new_genre = st.selectbox(
                    "변경할 장르",
                    GENRE_LIST,
                    index=0,
                    key="style_change_genre"
                )
            
            with col2:
                new_vibe = st.selectbox(
                    "Vibe",
                    [v[0] for v in VIBE_LIST],
                    key="style_change_vibe"
                )
            
            if st.button("🎨 스타일 태그 다시 생성", use_container_width=True, key="regenerate_style"):
                if new_genre == "선택해주세요":
                    st.error("장르를 선택해주세요.")
                elif client is None:
                    st.error("API 키가 설정되지 않았습니다.")
                else:
                    # 현재 보컬 타입 가져오기
                    current_vocal_type = st.session_state.get("lyrics_vocal_type", "솔로 (남성)")
                    
                    # 장르 변경 프롬프트 (Clean & Epic)
                    style_change_prompt = f"""다음 가사의 장르를 **{new_genre}**로 변경하고, Vibe는 **{new_vibe}**로 설정해주세요.

## 기존 가사 (내용은 절대 변경하지 말 것!)
{main_lyrics}

## 요구사항 (Clean & Epic 원칙 적용)
1. **가사 내용과 구조는 100% 유지**

2. **Clean & Epic 원칙에 따른 Mureka V7.6 Pro 스타일 태그 생성**:
   - {new_genre}에 어울리는 악기 조합 (시네마틱 악기 우선)
   - 보컬: Clear, Crisp, Articulate 등 명료성 강조
   - 적절한 BPM
   - 장르 특성에 맞는 분위기 키워드
   - ⚠️ 금지: Pipe Organ, Church Choir, Gritty, Aggressive

3. **Clean & Epic 원칙에 따른 Suno 5단계 프롬프트 생성**:
   - Identity: {new_genre} 장르로 명시
   - Mood: {new_vibe}에 맞는 분위기 (epic yet clean)
   - Instruments: {new_genre}의 특징적인 악기 연주 방식 (Cinematic Strings, Epic Brass 등)
   - Performance: {new_genre}에 어울리는 보컬 스타일 (clear, articulate, avoiding gritty/aggressive 명시)
   - Production: 품질 키워드 필수 (high-definition, spacious, polished, clear lyric delivery)

## 출력 형식
가사는 절대 출력하지 말고, 아래 두 가지만 출력하세요:

---
💡 **Mureka V7.6 Pro 스타일 태그 (Clean & Epic):**
`[시네마틱 악기], [장르], [Clear 보컬], [BPM], [분위기]`

---
💡 **Suno 최적화 프롬프트 (5단계 문장형 - Clean & Epic):**
(5단계 공식에 따라 하나의 영어 문단으로 작성, Performance와 Production 단계에 명료성 키워드 필수)

지금 바로 위 형식으로 Clean & Epic 스타일 태그만 생성해주세요!"""

                    with st.spinner(f"🎨 {new_genre} 스타일 태그 생성 중... (Clean & Epic)"):
                        try:
                            style_response = get_gpt_response(client, SYSTEM_ROLE, style_change_prompt)
                            
                            # Mureka 태그 추출
                            new_mureka_tag = ""
                            if "Mureka" in style_response or "💡" in style_response:
                                mureka_start = style_response.find("💡")
                                mureka_end = style_response.find("---", mureka_start + 1)
                                if mureka_end == -1:
                                    mureka_end = style_response.find("💡", mureka_start + 1)
                                if mureka_end != -1:
                                    mureka_section = style_response[mureka_start:mureka_end]
                                    # 백틱 안의 내용 추출
                                    if "`" in mureka_section:
                                        new_mureka_tag = mureka_section.split("`")[1].strip()
                            
                            # 세션 스테이트 업데이트
                            if new_mureka_tag:
                                st.session_state["mureka_style_tag"] = new_mureka_tag
                            st.session_state["lyrics_genre"] = new_genre
                            st.session_state["lyrics_vibe"] = new_vibe
                            
                            st.success(f"🎉 {new_genre} 스타일로 변경되었습니다! (Clean & Epic 적용)")
                            
                            # 결과 표시
                            st.markdown("**🎵 새로운 Mureka 태그 (Clean & Epic):**")
                            st.code(new_mureka_tag, language=None)
                            
                            st.markdown("**🎵 새로운 Suno 프롬프트 (Clean & Epic):**")
                            # Suno 프롬프트 추출
                            suno_start = style_response.find("Suno")
                            if suno_start != -1:
                                suno_section = style_response[suno_start:]
                                # 첫 문단 추출
                                lines = suno_section.split("\n")
                                suno_prompt = ""
                                for line in lines:
                                    if line.strip() and not line.startswith("💡") and not line.startswith("#"):
                                        suno_prompt += line.strip() + " "
                                if suno_prompt:
                                    st.code(suno_prompt.strip(), language=None)
                            
                            st.info("💡 페이지를 새로고침하면 위에 반영된 태그가 보입니다!")
                            
                            # 새로고침 버튼
                            if st.button("🔄 페이지 새로고침", use_container_width=True):
                                st.rerun()
                            
                        except Exception as e:
                            st.error(f"오류 발생: {str(e)}")
        
        st.divider()
        
        # ============ ⭐ NEW: 가사 깎기 (Revision) 섹션 ============
        with st.expander("🛠️ 가사 깎기 & 태그 정리"):
            st.markdown("""
            **💡 이 기능은 다음과 같은 경우에 사용하세요:**
            - Gemini나 다른 AI와 상의한 가사를 Suno/Udio 포맷으로 변환
            - 외부에서 작성한 가사에 구조 태그만 추가
            - 기존 가사를 조금 수정하고 싶을 때
            """)
            
            revision_input = st.text_area(
                "수정 지시사항 또는 완성된 가사 붙여넣기",
                placeholder="예시 1: '더 슬프게 만들어주세요'\n예시 2: (완성된 가사 전문을 붙여넣기)",
                height=200,
                help="짧은 요청이면 재작성, 긴 가사면 포맷팅만 수행합니다"
            )
            
            if st.button("✨ 수정사항 반영하여 다시 쓰기", use_container_width=True):
                if not revision_input.strip():
                    st.error("수정 지시사항 또는 가사를 입력해주세요.")
                else:
                    # 입력 길이로 모드 판단
                    is_full_lyrics = len(revision_input.strip()) > 200
                    
                    # 보컬 타입 가져오기
                    current_vocal_type = st.session_state.get("lyrics_vocal_type", "솔로 (남성)")
                    vocal_instruction = get_vocal_instruction(current_vocal_type)
                    
                    # ============ Revision Mode Prompt (Clean & Epic) ============
                    if is_full_lyrics:
                        # 포맷팅 모드: 내용 유지, 태그만 추가
                        refinement_prompt = f"""다음은 사용자가 작성한 완성된 가사입니다. 내용을 절대 변경하지 말고, **Suno/Udio 최적화 태그만 추가**해주세요. (Clean & Epic 원칙 적용)

## 사용자 가사
{revision_input}

## 보컬 타입
{current_vocal_type}

{vocal_instruction}

## 작업 지시사항 (매우 중요!)
1. **가사 내용은 절대 변경하지 마세요** - 원문 그대로 유지!
2. 각 파트 앞에 구조 태그 추가: [Intro], [Verse], [Chorus] 등
3. 적절한 위치에 연출 지시어 삽입: (Cinematic strings intro), (Clear vocal), (Epic brass hits)
4. 보컬 타입에 맞는 화자 태그 추가
5. **듀엣인 경우**: 블록 단위로 [Male]/[Female] 배정, 잦은 교차 금지!
6. **Clean & Epic 원칙** 적용:
   - 보컬: Clear, Crisp, Articulate 등
   - 악기: Cinematic Strings, Epic Brass, Deep Sub-bass 등
   - 금지: Pipe Organ, Church Choir, Gritty, Aggressive
7. Mureka 스타일 태그와 Suno 스타일 태그 생성 (Clean & Epic 버전)

## 출력 형식
[제목]
(기존 제목 또는 적절한 제목)

[가사]
(구조 태그와 Clean & Epic 연출 지시어가 추가된 가사)

---
💡 **Mureka V7.6 Pro 스타일 태그 (Clean & Epic):**
`...`

---
💡 **Suno 최적화 프롬프트 (5단계 문장형 - Clean & Epic):**
(5단계 공식에 따라 하나의 영어 문단으로 작성, 명료성 키워드 필수)
"""
                    else:
                        # 재작성 모드: 요청사항 반영하여 재작성
                        refinement_prompt = f"""다음은 기존 가사와 사용자의 수정 요청입니다. 요청사항을 반영하여 가사를 **재작성**해주세요. (Clean & Epic 원칙 적용)

## 기존 가사
{main_lyrics}

## 사용자 수정 요청
{revision_input}

## 보컬 타입
{current_vocal_type}

{vocal_instruction}

## 작업 지시사항
1. 사용자의 수정 요청을 최대한 반영
2. 기존 가사의 핵심 메시지는 유지하되 표현 개선
3. 구조 태그와 연출 지시어 포함 (Clean & Epic)
4. Mureka & Suno 스타일 태그 생성 (Clean & Epic 버전)

## 출력 형식
[제목]
(수정된 제목)

[가사]
(수정사항이 반영된 가사 with Clean & Epic 연출)

---
💡 **Mureka V7.6 Pro 스타일 태그 (Clean & Epic):**
`...`

---
💡 **Suno 최적화 프롬프트 (5단계 문장형 - Clean & Epic):**
(5단계 공식에 따라 하나의 영어 문단으로 작성, 명료성 키워드 필수)
"""
                    
                    with st.spinner("🛠️ 가사를 수정하고 있습니다... (Clean & Epic 적용)"):
                        try:
                            revised_response = get_gpt_response(client, SYSTEM_ROLE, refinement_prompt)
                            
                            # 수정된 가사 파싱
                            revised_title, revised_lyrics, revised_mureka = parse_title_and_lyrics(revised_response)
                            
                            # 세션 스테이트 업데이트
                            if revised_title:
                                st.session_state["song_title"] = revised_title
                            st.session_state["lyrics"] = revised_response
                            st.session_state["mureka_style_tag"] = revised_mureka
                            
                            st.success("✅ Clean & Epic 가사가 수정되었습니다!")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"수정 중 오류 발생: {str(e)}")
        
        st.info("💡 가사가 마음에 드시면 **Tab 2 (캐릭터 생성)**로 이동하세요!")
        
        # 제목 수정
        with st.expander("✏️ 제목 수정"):
            new_title = st.text_input("새 제목", value=st.session_state.get("song_title", ""))
            if st.button("💾 제목 저장"):
                st.session_state["song_title"] = new_title
                st.success("제목이 저장되었습니다!")
                st.rerun()
        
        # 가사 직접 수정
        with st.expander("✏️ 가사 직접 수정"):
            edited_lyrics = st.text_area(
                "가사 수정",
                st.session_state["lyrics"],
                height=400,
                key="lyrics_editor"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 수정 저장", use_container_width=True):
                    st.session_state["lyrics"] = edited_lyrics
                    st.success("저장되었습니다!")
                    st.rerun()
            with col2:
                if st.button("🗑️ 초기화", use_container_width=True):
                    for key in ["lyrics", "song_title", "mureka_style_tag"]:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
    
    else:
        st.markdown("---")
        st.markdown("""
        ### 🚀 시작하기 (Clean & Epic)
        
        1. **주제 입력** - 짧은 한 줄이든 긴 이야기든 OK!
        2. **장르 & 보컬 타입 선택** - 듀엣을 선택하면 화자가 자동으로 구분됩니다
        3. **Vibe 선택** - 정석, 반전, 역설, 광기 중 선택
        4. **생성 버튼 클릭** - Clean & Epic 가사 완성!
        
        > 🎬 **Clean & Epic 철학**: 웅장하되 명료하게, 영화 OST처럼 세련되게!
        > 
        > - ✅ Clear, Crisp, Articulate 보컬
        > - ✅ Cinematic Strings, Epic Brass, Deep Sub-bass
        > - ❌ Pipe Organ, Church Choir, Gritty, Shouting
        """)
