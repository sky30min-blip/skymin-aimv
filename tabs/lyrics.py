"""
tabs/lyrics.py - 가사 생성 탭 (Tab 1) - 모바일 최적화 버전
제목 + 가사 동시 생성 기능 포함
"""

import streamlit as st
from utils import get_gpt_response
from tabs.lyrics_config import GENRE_LIST, VIBE_LIST, SYSTEM_ROLE


def parse_title_and_lyrics(response: str) -> tuple[str, str]:
    """
    GPT 응답에서 제목과 가사를 분리합니다.
    
    Args:
        response: GPT 응답 텍스트
        
    Returns:
        tuple: (제목, 가사)
    """
    title = ""
    lyrics = response
    
    # 제목 추출 시도
    title_markers = ["[제목]", "[Title]", "제목:", "Title:", "**제목:**", "**제목**:"]
    
    for marker in title_markers:
        if marker in response:
            parts = response.split(marker, 1)
            if len(parts) > 1:
                # 제목 부분 추출 (첫 줄만)
                title_part = parts[1].strip()
                title_lines = title_part.split("\n")
                title = title_lines[0].strip().strip("*").strip('"').strip("'").strip()
                
                # 나머지는 가사
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
    
    return title, lyrics


def render(client):
    """가사 생성 탭을 렌더링합니다."""
    
    st.header("🎵 Step 1: AI 리릭 마스터")
    st.markdown("""
    **모든 음악 장르**의 가사를 완벽하게 생성합니다.
    
    > 🎼 *"트로트부터 데스메탈까지, 동요부터 오페라까지 — 모든 장르를 소화합니다"*
    """)
    
    st.info("""
    ✨ **AI 리릭 마스터의 특징:**
    - 🎵 **노래 제목** 자동 생성
    - 🌍 **전 세계 모든 장르** 지원 (퓨전 장르도 OK!)
    - 🎭 **반전 매력** 옵션 (슬픈데 신나게, B급인데 진지하게)
    - 🎹 **Suno AI 스타일 태그** 자동 생성
    """)
    
    st.divider()
    
    # ============ 기본 정보 섹션 (모바일 최적화) ============
    st.subheader("📝 기본 정보")
    
    topic = st.text_input(
        "🎯 노래 주제 / 스토리",
        placeholder="예: 새벽 3시 편의점에서 마주친 전 여자친구",
        help="무엇이든 가능합니다. 구체적일수록 좋아요!"
    )
    
    with st.expander("💡 주제 아이디어 (클릭해서 열기)"):
        st.markdown("""
        **진지한 주제:**
        - 10년 만에 고향에 돌아온 날
        - 암 투병 중인 어머니에게 보내는 편지
        - 졸업식 날, 말하지 못한 고백
        
        **B급/재미있는 주제:**
        - 월요일 아침 출근길의 고통
        - 치킨은 왜 이렇게 맛있는가
        - 내 방 귀퉁이 먼지와의 대화
        
        **판타지/특이한 주제:**
        - AI가 인간에게 보내는 러브레터
        - 멸망한 지구에서 마지막 로봇의 독백
        """)
    
    genre = st.selectbox(
        "🎸 장르 선택",
        options=GENRE_LIST,
        help="원하는 장르가 없으면 '직접 입력'을 선택하세요"
    )
    
    custom_genre = ""
    if genre == "직접 입력 (Custom)":
        custom_genre = st.text_input(
            "✍️ 장르 직접 입력",
            placeholder="예: 1990년대 LA 갱스터 랩, 판소리 퓨전 록",
            help="어떤 장르든, 퓨전이든 마음대로 입력하세요!"
        )
        
        with st.expander("🔥 퓨전 장르 아이디어"):
            st.markdown("""
            - **사이버펑크 국악**: 가야금 + 신스웨이브
            - **트로트 메탈**: 꺾기 창법 + 헤비 리프
            - **불경 EDM**: 염불 + 베이스 드롭
            """)
    
    st.divider()
    
    # ============ 분위기/반전 매력 섹션 ============
    st.subheader("🎭 분위기 & 반전 매력 (Vibe)")
    
    vibe_options = [v[0] for v in VIBE_LIST]
    selected_vibe_name = st.radio(
        "가사의 톤을 선택하세요",
        options=vibe_options,
        help="같은 주제도 Vibe에 따라 완전히 다른 가사가 됩니다"
    )
    
    selected_vibe = next((v for v in VIBE_LIST if v[0] == selected_vibe_name), VIBE_LIST[0])
    vibe_key = selected_vibe[1]
    
    vibe_colors = {"standard": "🟢", "satire": "🟡", "paradox": "🔵", "madness": "🔴"}
    st.caption(f"{vibe_colors.get(vibe_key, '⚪')} {selected_vibe[2]}")
    
    st.divider()
    
    # ============ 추가 옵션 섹션 (모바일 최적화) ============
    st.subheader("⚙️ 추가 옵션")
    
    language = st.selectbox("🌐 가사 언어", ["한국어", "영어", "한영 혼합", "일본어", "한일 혼합"])
    
    era = st.selectbox("📅 시대적 분위기", 
        ["현대 (2020s)", "2010년대", "2000년대", "1990년대", "1980년대", "미래적", "시대 무관"])
    
    intensity = st.select_slider("🔥 감정 강도", 
        ["차분하게", "적당히", "격렬하게", "폭발적으로"], value="적당히")
    
    keywords = st.text_input(
        "🔑 포함할 키워드 (선택사항)",
        placeholder="예: 벚꽃, 새벽, 소주, 첫사랑, 비 오는 날",
        help="가사에 꼭 들어갔으면 하는 단어들을 쉼표로 구분해 입력하세요"
    )
    
    st.divider()
    
    # ============ 생성 버튼 ============
    if st.button("🎤 제목 + 가사 생성하기", type="primary", use_container_width=True):
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
        
        # 제목 생성을 포함한 프롬프트
        user_prompt = f"""다음 조건에 맞는 **노래 제목**과 **가사**를 작성해주세요.

## 기본 정보
- **주제/스토리**: {topic}
- **장르**: {final_genre}
- **분위기(Vibe)**: {selected_vibe_name}
- **언어**: {language}
- **시대적 분위기**: {era}
- **감정 강도**: {intensity}
{f'- **포함 키워드**: {keywords}' if keywords else ''}

## 출력 형식 (반드시 준수!)

[제목]
(주제와 장르에 어울리는 매력적인 제목 한 줄)

[가사]
(1500~2000자 분량의 가사)

---
💡 **Suno AI 추천 스타일 태그:**
`[영어 태그들]`

## 특별 지시
1. **제목**은 주제를 함축하면서도 기억에 남는 것으로!
2. 장르 '{final_genre}'의 특성을 100% 살려주세요.
3. Vibe가 '{selected_vibe_name}'이므로, 이 톤에 맞게 작성해주세요.

지금 바로 제목과 가사를 작성해주세요!"""

        with st.spinner(f"🎼 '{final_genre}' 장르의 제목과 가사를 작곡 중..."):
            try:
                response = get_gpt_response(client, SYSTEM_ROLE, user_prompt)
                
                # 제목과 가사 분리
                title, lyrics = parse_title_and_lyrics(response)
                
                # 제목이 추출되지 않았으면 기본값
                if not title:
                    title = f"{topic} ({final_genre})"
                
                # 세션 스테이트에 저장
                st.session_state["song_title"] = title
                st.session_state["lyrics"] = response  # 전체 응답 저장
                st.session_state["lyrics_topic"] = topic
                st.session_state["lyrics_genre"] = final_genre
                st.session_state["lyrics_vibe"] = selected_vibe_name
                
                st.success("🎉 제목과 가사가 완성되었습니다!")
                
            except Exception as e:
                st.error(str(e))
                return
    
    # ============ 결과 표시 ============
    st.divider()
    
    if "lyrics" in st.session_state and st.session_state["lyrics"]:
        # 제목 표시
        if st.session_state.get("song_title"):
            st.header(f"🎵 {st.session_state['song_title']}")
        
        st.subheader("📜 생성된 가사")
        
        st.markdown(f"**🎯 주제:** {st.session_state.get('lyrics_topic', '-')}")
        st.markdown(f"**🎸 장르:** {st.session_state.get('lyrics_genre', '-')}")
        st.markdown(f"**🎭 Vibe:** {st.session_state.get('lyrics_vibe', '-')}")
        
        st.divider()
        
        lyrics_content = st.session_state["lyrics"]
        
        # Suno 태그 분리
        if "Suno AI" in lyrics_content or "스타일 태그" in lyrics_content:
            tag_markers = ["💡 **Suno", "💡 Suno", "---\n💡", "Suno AI 추천"]
            split_index = -1
            for marker in tag_markers:
                if marker in lyrics_content:
                    split_index = lyrics_content.find(marker)
                    break
            
            if split_index > 0:
                main_lyrics = lyrics_content[:split_index].strip()
                suno_tags = lyrics_content[split_index:].strip()
            else:
                main_lyrics = lyrics_content
                suno_tags = None
        else:
            main_lyrics = lyrics_content
            suno_tags = None
        
        st.text_area("가사 내용", value=main_lyrics, height=400, label_visibility="collapsed")
        
        char_count = len(main_lyrics.replace(" ", "").replace("\n", ""))
        st.caption(f"📊 총 {char_count}자 (공백 제외)")
        
        if suno_tags:
            st.divider()
            st.markdown(suno_tags)
        
        st.info("💡 가사가 마음에 드시면 **Tab 2 (캐릭터 생성)**로 이동하세요!")
        
        # 제목 수정 옵션
        with st.expander("✏️ 제목 수정하기"):
            new_title = st.text_input("새 제목", value=st.session_state.get("song_title", ""))
            if st.button("💾 제목 저장"):
                st.session_state["song_title"] = new_title
                st.success("제목이 저장되었습니다!")
                st.rerun()
        
        with st.expander("✏️ 가사 직접 수정하기"):
            edited_lyrics = st.text_area("가사 수정", st.session_state["lyrics"], height=400, key="lyrics_editor")
            
            if st.button("💾 수정 저장", use_container_width=True):
                st.session_state["lyrics"] = edited_lyrics
                st.success("저장되었습니다!")
                st.rerun()
            if st.button("🗑️ 초기화", use_container_width=True):
                st.session_state["lyrics"] = ""
                st.session_state["song_title"] = ""
                st.rerun()
    
    else:
        st.markdown("---")
        st.markdown("""
        ### 🚀 시작하기
        
        1. **주제**를 입력하세요 (진지해도, B급이어도 OK!)
        2. **장르**를 선택하세요 (없으면 직접 입력)
        3. **Vibe**를 선택하세요 (반전 매력을 원하면 Satire나 Paradox!)
        4. **생성 버튼**을 클릭하면 **제목과 가사**가 함께 만들어집니다!
        """)
