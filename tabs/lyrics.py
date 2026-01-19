"""
tabs/lyrics.py - Suno/Udio 최적화 가사 생성 탭 (Tab 1)
제목 + 구조적 태그 + 보컬/연출 지시어 + 수정 기능 포함
"""

import streamlit as st
from utils import get_gpt_response
from tabs.lyrics_config import GENRE_LIST, VIBE_LIST, SYSTEM_ROLE


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
## 보컬 구조 지시사항 (남성 솔로)
- 모든 파트에 [Verse], [Chorus], [Bridge] 태그 필수
- 보컬 타입 명시: [Male Vocal], [Male Voice]
- 감정 변화를 연출 지시어로 표현:
  * 약한 감정: (Soft voice), (Whispering), (Gentle singing)
  * 보통 감정: (Clear vocal), (Steady voice)
  * 강한 감정: (Powerful belting), (Emotional cry), (High note)
- Sound FX 활용: (Guitar riff), (Drum hit), (Bass drop), (Clock ticking)

**출력 예시:**
[Intro - Male]
(Soft acoustic guitar)
가사 내용...

[Verse 1 - Male]
(Clear vocal, steady beat)
가사 내용...
(Building emotion)
가사 내용...
""",
        
        "솔로 (여성)": """
## 보컬 구조 지시사항 (여성 솔로)
- 모든 파트에 [Verse], [Chorus], [Bridge] 태그 필수
- 보컬 타입 명시: [Female Vocal], [Female Voice]
- 감정 변화를 연출 지시어로 표현:
  * 부드러운: (Soft voice), (Whispering), (Breathy vocal)
  * 강렬한: (Powerful voice), (Soaring high note), (Belting)
  * 감성적: (Emotional vocal), (Trembling voice), (Crying tone)
- Sound FX 활용: (Piano melody), (String swell), (Soft rain), (Wind chimes)

**출력 예시:**
[Intro - Female]
(Soft piano intro)
가사 내용...

[Verse 1 - Female]
(Breathy vocal, intimate)
가사 내용...
(Building to chorus)
가사 내용...
""",
        
        "혼성 듀엣 (남/녀)": """
## 보컬 구조 지시사항 (혼성 듀엣) ⭐ 매우 중요!
- **화자 명시 필수**: [Verse 1 - Male], [Verse 2 - Female], [Chorus - Harmony]
- 각 파트마다 누가 부르는지 태그로 명확히 구분
- 하모니 파트는 [Harmony], [Duet], [Both] 태그 사용
- 대화하듯 주고받는 구조 권장

**Few-Shot 예시 (반드시 이 형식 따를 것!):**

[Intro - Both]
(Atmospheric synth)
(Male) 첫 번째 라인
(Female) 두 번째 라인

[Verse 1 - Male]
(Clear male vocal)
남성 파트 가사...
남성 파트 가사...

[Verse 2 - Female]
(Soft female vocal)
여성 파트 가사...
여성 파트 가사...

[Pre-Chorus - Both]
(Building harmony)
(Male) 남성 라인
(Female) 여성 라인

[Chorus - Harmony]
(Powerful duet, full harmony)
함께 부르는 후렴구...
함께 부르는 후렴구...

[Bridge - Male & Female Alternating]
(Male) 남성 라인
(Female) 여성 응답
(Male) 남성 라인
(Female) 여성 응답
(Both) 함께 마무리
""",
        
        "합창/콰이어": """
## 보컬 구조 지시사항 (합창/콰이어)
- [Choir], [Chorus Group], [Ensemble] 태그 사용
- 파트별 성부 구분: [Soprano], [Alto], [Tenor], [Bass]
- 웅장한 분위기 연출 지시어:
  * (Full choir), (Layered voices), (Harmony build-up)
  * (Orchestral backing), (Epic crescendo)
- 클래식/성가 느낌 강조

**출력 예시:**
[Intro - Choir]
(Soft choir humming, a cappella)
Ooh... Aah...

[Verse 1 - Lead + Choir]
(Lead vocal with choir backing)
가사 내용...
(Choir: Harmony response)
""",
        
        "AI/로봇 보컬": """
## 보컬 구조 지시사항 (AI/로봇 보컬)
- [Robotic Voice], [Vocoder], [Auto-tuned], [Synthetic Vocal] 태그 사용
- 기계적 효과 지시어:
  * (Vocoder effect), (Glitchy vocal), (Digital distortion)
  * (Auto-tune heavy), (Robotic tone), (Synthesized voice)
- 사이버펑크/전자음악 분위기
- Sound FX: (Beep), (Static noise), (Digital glitch), (Circuit sound)

**출력 예시:**
[Intro - Robotic]
(Heavy vocoder, glitchy)
가사 내용...
(Digital distortion)
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
    
    st.header("🎵 Step 1: Suno/Udio 최적화 가사 생성기")
    st.markdown("""
    **AI 음악 생성 툴에 최적화된 가사**를 만듭니다.
    
    > 🎼 *"구조적 태그 + 보컬 지시어 + Sound FX = 완벽한 AI 음악"*
    """)
    
    st.info("""
    ✨ **Suno/Udio 최적화 기능:**
    - 🎤 **보컬 타입별 맞춤 구조** (솔로, 듀엣, 합창 등)
    - 🏷️ **구조적 태그 자동 삽입** ([Intro], [Verse], [Chorus])
    - 🎭 **연출 지시어 포함** ((Whisper), (Build up), (Guitar solo))
    - 🔊 **Sound FX 추가** ((Clock ticking), (Rain falling))
    - 🛠️ **가사 깎기 기능** (외부에서 수정한 가사 포맷팅)
    """)
    
    st.divider()
    
    # ============ 기본 정보 섹션 ============
    st.subheader("📝 기본 정보")
    
    topic = st.text_area(
        "🎯 노래 주제 / 스토리",
        placeholder="예: 새벽 3시 편의점에서 마주친 전 여자친구\n\n긴 내용도 OK (소설 줄거리, 일기 등)",
        height=150,
        help="한 줄이든 장문이든 OK! AI가 핵심을 추출하여 가사로 만듭니다."
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
        
        # ============ Generation Mode Prompt ============
        user_prompt = f"""다음 조건에 맞는 **Suno/Udio 최적화 가사**를 작성해주세요.

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

## ⚠️ Suno/Udio 최적화 필수 요구사항 ⚠️

1. **구조적 태그 필수**:
   - [Intro], [Verse 1], [Pre-Chorus], [Chorus], [Verse 2], [Bridge], [Outro]
   - 보컬 타입에 따라 화자 명시 (예: [Verse 1 - Male])

2. **연출 지시어 필수**:
   - 가사 줄 사이에 괄호로 음악적 연출 삽입
   - 예: (Piano intro), (Build up), (Vocal emphasis), (Fade out)

3. **Sound FX 활용**:
   - 분위기에 맞는 효과음 지시어 추가
   - 예: (Clock ticking), (Rain falling), (Gunshot), (Thunder)

4. **Mureka & Suno 스타일 태그 생성**:
   - Mureka V7.6 Pro: 악기, 장르, 보컬, BPM, 분위기
   - Suno AI: 영어 태그 10개 내외

## 출력 형식 (Suno/Udio 최적화)

[제목]
(주제와 장르에 어울리는 제목)

[가사]
[Intro]
(연출 지시어)
가사 내용...

[Verse 1]
(연출 지시어)
가사 내용...
(감정 변화 지시어)
가사 내용...

[Pre-Chorus]
(Build up)
가사 내용...

[Chorus]
(Full power, hook line)
가사 내용...

... (계속)

---
💡 **Mureka V7.6 Pro 스타일 태그:**
`[악기], [장르], [보컬], [BPM], [분위기]`

---
💡 **Suno AI 추천 스타일 태그:**
`[영어 태그들]`

지금 바로 Suno/Udio에서 최상의 결과를 낼 수 있는 가사를 작성해주세요!"""

        with st.spinner(f"🎼 '{final_genre}' / '{vocal_type}' 가사 생성 중..."):
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
                
                st.success("🎉 Suno/Udio 최적화 가사가 완성되었습니다!")
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
        
        # Suno 태그 추출
        if "Suno AI" in lyrics_content or "스타일 태그" in lyrics_content:
            tag_markers = ["💡 **Suno", "💡 Suno", "---\n💡", "Suno AI 추천"]
            for marker in tag_markers:
                if marker in lyrics_content:
                    split_index = lyrics_content.find(marker)
                    if mureka_tags is None:
                        main_lyrics = lyrics_content[:split_index].strip()
                    suno_tags = lyrics_content[split_index:].strip()
                    break
        
        # 가사 표시
        st.text_area("가사 내용", value=main_lyrics, height=400, label_visibility="collapsed")
        
        char_count = len(main_lyrics.replace(" ", "").replace("\n", ""))
        st.caption(f"📊 총 {char_count}자 (공백 제외)")
        
        # Mureka 태그 표시
        if st.session_state.get("mureka_style_tag"):
            st.divider()
            st.success("🎵 **Mureka V7.6 Pro 전용 스타일 태그**")
            
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
        
        # Suno 태그 표시
        if suno_tags:
            st.divider()
            st.markdown(suno_tags)
        
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
                    
                    # ============ Revision Mode Prompt ============
                    if is_full_lyrics:
                        # 포맷팅 모드: 내용 유지, 태그만 추가
                        refinement_prompt = f"""다음은 사용자가 작성한 완성된 가사입니다. 내용을 절대 변경하지 말고, **Suno/Udio 최적화 태그만 추가**해주세요.

## 사용자 가사
{revision_input}

## 보컬 타입
{current_vocal_type}

{vocal_instruction}

## 작업 지시사항 (매우 중요!)
1. **가사 내용은 절대 변경하지 마세요** - 원문 그대로 유지!
2. 각 파트 앞에 구조 태그 추가: [Intro], [Verse], [Chorus] 등
3. 적절한 위치에 연출 지시어 삽입: (Piano intro), (Build up) 등
4. 보컬 타입에 맞는 화자 태그 추가 (듀엣인 경우 [Male]/[Female])
5. Mureka 스타일 태그와 Suno 스타일 태그 생성

## 출력 형식
[제목]
(기존 제목 또는 적절한 제목)

[가사]
(구조 태그와 연출 지시어가 추가된 가사)

---
💡 **Mureka V7.6 Pro 스타일 태그:**
`...`

---
💡 **Suno AI 추천 스타일 태그:**
`...`
"""
                    else:
                        # 재작성 모드: 요청사항 반영하여 재작성
                        refinement_prompt = f"""다음은 기존 가사와 사용자의 수정 요청입니다. 요청사항을 반영하여 가사를 **재작성**해주세요.

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
3. 구조 태그와 연출 지시어 포함
4. Mureka & Suno 스타일 태그 생성

## 출력 형식
[제목]
(수정된 제목)

[가사]
(수정사항이 반영된 가사)

---
💡 **Mureka V7.6 Pro 스타일 태그:**
`...`

---
💡 **Suno AI 추천 스타일 태그:**
`...`
"""
                    
                    with st.spinner("🛠️ 가사를 수정하고 있습니다..."):
                        try:
                            revised_response = get_gpt_response(client, SYSTEM_ROLE, refinement_prompt)
                            
                            # 수정된 가사 파싱
                            revised_title, revised_lyrics, revised_mureka = parse_title_and_lyrics(revised_response)
                            
                            # 세션 스테이트 업데이트
                            if revised_title:
                                st.session_state["song_title"] = revised_title
                            st.session_state["lyrics"] = revised_response
                            st.session_state["mureka_style_tag"] = revised_mureka
                            
                            st.success("✅ 가사가 수정되었습니다!")
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
        ### 🚀 시작하기
        
        1. **주제 입력** - 짧은 한 줄이든 긴 이야기든 OK!
        2. **장르 & 보컬 타입 선택** - 듀엣을 선택하면 화자가 자동으로 구분됩니다
        3. **Vibe 선택** - 정석, 반전, 역설, 광기 중 선택
        4. **생성 버튼 클릭** - Suno/Udio 최적화 가사 완성!
        
        > 💡 구조 태그 + 연출 지시어 + Sound FX가 자동으로 포함됩니다!
        """)
