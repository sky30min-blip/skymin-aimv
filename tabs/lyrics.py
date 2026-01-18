"""
tabs/lyrics.py - 가사 생성 탭 (Tab 1)
전 장르 마스터 & 반전 매력 통합 버전
AI 리릭 마스터: 모든 음악 장르를 완벽 소화
"""

import streamlit as st
from utils import get_gpt_response
from tabs.lyrics_config import GENRE_LIST, VIBE_LIST, SYSTEM_ROLE


def render(client):
    """가사 생성 탭을 렌더링합니다."""
    
    st.header("🎵 Step 1: AI 리릭 마스터")
    st.markdown("""
    **모든 음악 장르**의 가사를 완벽하게 생성합니다.
    
    > 🎼 *"트로트부터 데스메탈까지, 동요부터 오페라까지 — 모든 장르를 소화합니다"*
    """)
    
    # 핵심 기능 안내
    st.info("""
    ✨ **AI 리릭 마스터의 특징:**
    - 🌍 **전 세계 모든 장르** 지원 (퓨전 장르도 OK!)
    - 🎭 **반전 매력** 옵션 (슬픈데 신나게, B급인데 진지하게)
    - 🎹 **Suno AI 스타일 태그** 자동 생성
    """)
    
    st.divider()
    
    # ============ 기본 정보 섹션 ============
    st.subheader("📝 기본 정보")
    
    col1, col2 = st.columns(2)
    
    with col1:
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
            - 냉장고 속 유통기한 지난 우유의 슬픔
            
            **판타지/특이한 주제:**
            - AI가 인간에게 보내는 러브레터
            - 멸망한 지구에서 마지막 로봇의 독백
            - 조선시대로 타임슬립한 아이돌
            """)
    
    with col2:
        genre = st.selectbox(
            "🎸 장르 선택",
            options=GENRE_LIST,
            help="원하는 장르가 없으면 '직접 입력'을 선택하세요"
        )
        
        custom_genre = ""
        if genre == "직접 입력 (Custom)":
            custom_genre = st.text_input(
                "✍️ 장르 직접 입력",
                placeholder="예: 1990년대 LA 갱스터 랩, 판소리 퓨전 록, 중세 그레고리안 성가",
                help="어떤 장르든, 퓨전이든 마음대로 입력하세요!"
            )
            
            with st.expander("🔥 퓨전 장르 아이디어"):
                st.markdown("""
                - **사이버펑크 국악**: 가야금 + 신스웨이브
                - **트로트 메탈**: 꺾기 창법 + 헤비 리프
                - **불경 EDM**: 염불 + 베이스 드롭
                - **조선 힙합**: 사또 디스 + 808 비트
                - **동요 데스메탈**: 곰 세 마리 + 그로울링
                """)
    
    # ============ 분위기/반전 매력 섹션 ============
    st.subheader("🎭 분위기 & 반전 매력 (Vibe)")
    
    vibe_options = [v[0] for v in VIBE_LIST]
    selected_vibe_name = st.radio(
        "가사의 톤을 선택하세요",
        options=vibe_options,
        horizontal=True,
        help="같은 주제도 Vibe에 따라 완전히 다른 가사가 됩니다"
    )
    
    selected_vibe = next((v for v in VIBE_LIST if v[0] == selected_vibe_name), VIBE_LIST[0])
    vibe_key = selected_vibe[1]
    
    vibe_colors = {"standard": "🟢", "satire": "🟡", "paradox": "🔵", "madness": "🔴"}
    st.caption(f"{vibe_colors.get(vibe_key, '⚪')} {selected_vibe[2]}")
    
    # ============ 추가 옵션 섹션 ============
    st.subheader("⚙️ 추가 옵션")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        language = st.selectbox("🌐 가사 언어", ["한국어", "영어", "한영 혼합", "일본어", "한일 혼합"])
    
    with col4:
        era = st.selectbox("📅 시대적 분위기", 
            ["현대 (2020s)", "2010년대", "2000년대", "1990년대", "1980년대", "1970년대 이전", "미래적", "시대 무관"])
    
    with col5:
        intensity = st.select_slider("🔥 감정 강도", 
            ["차분하게", "적당히", "격렬하게", "폭발적으로"], value="적당히")
    
    keywords = st.text_input(
        "🔑 포함할 키워드 (선택사항)",
        placeholder="예: 벚꽃, 새벽, 소주, 첫사랑, 비 오는 날",
        help="가사에 꼭 들어갔으면 하는 단어들을 쉼표로 구분해 입력하세요"
    )
    
    st.divider()
    
    # ============ 생성 버튼 ============
    if st.button("🎤 가사 생성하기", type="primary", use_container_width=True):
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
            st.error("API 키가 설정되지 않았습니다. secrets.toml 파일을 확인해주세요.")
            return
        
        final_genre = custom_genre if genre == "직접 입력 (Custom)" else genre
        
        user_prompt = f"""다음 조건에 맞는 노래 가사를 작성해주세요.

## 기본 정보
- **주제/스토리**: {topic}
- **장르**: {final_genre}
- **분위기(Vibe)**: {selected_vibe_name}
- **언어**: {language}
- **시대적 분위기**: {era}
- **감정 강도**: {intensity}
{f'- **포함 키워드**: {keywords}' if keywords else ''}

## 특별 지시
1. 장르 '{final_genre}'의 특성을 100% 살려주세요. 그 장르를 대표하는 아티스트가 쓴 것처럼!
2. Vibe가 '{selected_vibe_name}'이므로, 이 톤에 맞게 작성해주세요.
3. 감정 강도가 '{intensity}'이니 이에 맞는 표현 수위를 사용하세요.
4. 1500~2000자 분량으로 작성하세요.
5. 마지막에 반드시 **Suno AI 추천 스타일 태그**를 포함하세요!

지금 바로 이 장르의 마스터가 되어 가사를 작성해주세요!"""

        with st.spinner(f"🎼 '{final_genre}' 장르의 가사를 작곡 중... (약 30초~1분)"):
            try:
                lyrics = get_gpt_response(client, SYSTEM_ROLE, user_prompt)
                st.session_state["lyrics"] = lyrics
                st.session_state["lyrics_topic"] = topic
                st.session_state["lyrics_genre"] = final_genre
                st.session_state["lyrics_vibe"] = selected_vibe_name
                st.success("🎉 가사가 완성되었습니다!")
            except Exception as e:
                st.error(str(e))
                return
    
    # ============ 결과 표시 ============
    st.divider()
    
    if "lyrics" in st.session_state and st.session_state["lyrics"]:
        st.subheader("📜 생성된 가사")
        
        col_meta1, col_meta2, col_meta3 = st.columns(3)
        col_meta1.markdown(f"**🎯 주제:** {st.session_state.get('lyrics_topic', '-')}")
        col_meta2.markdown(f"**🎸 장르:** {st.session_state.get('lyrics_genre', '-')}")
        col_meta3.markdown(f"**🎭 Vibe:** {st.session_state.get('lyrics_vibe', '-')}")
        
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
        
        st.text_area("가사 내용", value=main_lyrics, height=500, label_visibility="collapsed")
        
        char_count = len(main_lyrics.replace(" ", "").replace("\n", ""))
        st.caption(f"📊 총 {char_count}자 (공백 제외)")
        
        if suno_tags:
            st.divider()
            st.markdown(suno_tags)
        
        st.info("💡 가사가 마음에 드시면 **Tab 2 (캐릭터 생성)**로 이동하세요!")
        
        with st.expander("✏️ 가사 직접 수정하기"):
            edited_lyrics = st.text_area("가사 수정", st.session_state["lyrics"], height=500, key="lyrics_editor")
            
            col_btn1, col_btn2 = st.columns(2)
            if col_btn1.button("💾 수정 내용 저장", use_container_width=True):
                st.session_state["lyrics"] = edited_lyrics
                st.success("저장되었습니다!")
                st.rerun()
            if col_btn2.button("🗑️ 가사 초기화", use_container_width=True):
                st.session_state["lyrics"] = ""
                st.rerun()
    
    else:
        st.markdown("---")
        st.markdown("""
        ### 🚀 시작하기
        
        1. **주제**를 입력하세요 (진지해도, B급이어도 OK!)
        2. **장르**를 선택하세요 (없으면 직접 입력)
        3. **Vibe**를 선택하세요 (반전 매력을 원하면 Satire나 Paradox!)
        4. **생성 버튼**을 클릭하면 끝!
        
        > 💡 **팁:** "치킨"을 주제로 "이별 발라드"를 선택하고 "Satire" Vibe를 적용하면? 
        > → 치킨과의 이별을 눈물나게 노래하는 명곡이 탄생합니다! 🍗😢
        """)