"""
main.py - AI 뮤직비디오 제작 올인원 툴
메인 실행 파일 + 프로젝트 저장/불러오기
API 키는 .streamlit/secrets.toml에서 관리
"""

import streamlit as st

# 페이지 설정 (반드시 첫 번째로 호출)
st.set_page_config(
    page_title="AI 뮤직비디오 제작 툴",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 모듈 임포트
from utils import (
    get_openai_client, 
    export_project_to_json, 
    import_project_from_json, 
    get_project_info_from_json
)
from tabs import theme_expander, lyrics, character, storyboard


def init_session_state():
    """세션 스테이트 초기화"""
    defaults = {
        # 가사 관련
        "song_title": "",
        "lyrics": "",
        "lyrics_topic": "",
        "lyrics_genre": "",
        "lyrics_vibe": "",
        "lyrics_mood": "",
        # 캐릭터 관련
        "character_prompt": "",
        "character_style": "",
        "character_style_kr": "",
        "character_subject": "",
        "master_image_url": "",
        # 스토리보드 관련
        "storyboard_raw": "",
        "storyboard_url": "",
        "storyboard_style": "",
        "storyboard_style_kr": "",
        "storyboard_video_mood": "",
        "storyboard_video_mood_kr": "",
        "final_prompts": []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_sidebar(client):
    """사이드바 렌더링"""
    with st.sidebar:
        st.title("⚙️ 설정")
        
        st.divider()
        
        # API 연결 상태 표시
        st.subheader("🔑 API 연결 상태")
        
        if client is not None:
            st.success("✅ OpenAI API 연결됨")
        else:
            st.error("❌ API 키 설정 필요")
            st.caption("`.streamlit/secrets.toml` 파일을 확인하세요")
        
        st.divider()
        
        # ============ 프로젝트 관리 섹션 ============
        st.subheader("📂 프로젝트 관리")
        
        # 저장 버튼
        if st.button("💾 프로젝트 저장", use_container_width=True):
            json_str, filename = export_project_to_json()
            st.download_button(
                label="📥 JSON 다운로드",
                data=json_str,
                file_name=filename,
                mime="application/json",
                use_container_width=True
            )
        
        # 불러오기
        uploaded_file = st.file_uploader(
            "📤 프로젝트 불러오기",
            type=["json"],
            help="저장된 JSON 파일을 선택하세요",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            json_str = uploaded_file.read().decode("utf-8")
            
            # 프로젝트 정보 미리보기
            info = get_project_info_from_json(json_str)
            if info:
                st.caption(f"📄 **{info['title']}**")
                st.caption(f"생성: {info['created_at'][:10]}")
                
                status_icons = []
                if info['has_lyrics']:
                    status_icons.append("🎵")
                if info['has_character']:
                    status_icons.append("🎨")
                if info['has_storyboard']:
                    status_icons.append("🎬")
                st.caption(f"포함: {' '.join(status_icons) if status_icons else '없음'}")
                
                if st.button("✅ 이 프로젝트 불러오기", type="primary", use_container_width=True):
                    if import_project_from_json(json_str):
                        st.success("프로젝트를 불러왔습니다!")
                        st.rerun()
                    else:
                        st.error("파일 형식이 올바르지 않습니다.")
            else:
                st.error("올바른 프로젝트 파일이 아닙니다.")
        
        st.divider()
        
        # 진행 상황 표시
        st.subheader("📊 진행 상황")
        
        progress_items = [
            ("가사 생성", bool(st.session_state.get("lyrics"))),
            ("캐릭터 프롬프트", bool(st.session_state.get("character_prompt"))),
            ("마스터 이미지 URL", bool(st.session_state.get("master_image_url"))),
            ("스토리보드 완성", bool(st.session_state.get("final_prompts")))
        ]
        
        for item, completed in progress_items:
            if completed:
                st.markdown(f"✅ {item}")
            else:
                st.markdown(f"⬜ {item}")
        
        # 현재 곡 제목 표시
        if st.session_state.get("song_title"):
            st.divider()
            st.markdown(f"🎵 **현재 곡:** {st.session_state['song_title']}")
        
        st.divider()
        
        # 사용 안내
        st.subheader("📖 사용 방법")
        st.markdown("""
        1. **Tab 1-A**: 주제 확장 (선택)
        2. **Tab 1-B**: 가사 생성
        3. **Tab 2**: 캐릭터 프롬프트
        4. **Tab 3**: 스토리보드 (올인원!) 🎬
           - 20개 장면 이미지 프롬프트
           - AI 스타일 자동 추천
           - 영상 편집 레시피
        """)
        
        st.divider()
        
        # 초기화 버튼
        if st.button("🔄 모든 데이터 초기화", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.divider()
        
        # 푸터
        st.caption("Made with ❤️ using Streamlit & OpenAI")


def main():
    """메인 함수"""
    # 세션 스테이트 초기화
    init_session_state()
    
    # OpenAI 클라이언트 생성 (secrets.toml에서 API 키 로드)
    client = get_openai_client()
    
    # 사이드바 렌더링
    render_sidebar(client)
    
    # 메인 헤더
    st.title("🎬 AI 뮤직비디오 제작 올인원 툴")
    
    # 현재 곡 제목 표시
    if st.session_state.get("song_title"):
        st.markdown(f"### 🎵 *{st.session_state['song_title']}*")
    
    st.markdown("""
    가사 생성부터 캐릭터 일관성이 적용된 Midjourney 프롬프트까지, 
    뮤직비디오 제작에 필요한 모든 것을 한 곳에서!
    """)
    
    st.divider()
    
    # 탭 생성 (4개)
    tab1a, tab1b, tab2, tab3 = st.tabs([
        "💡 Step 1-A: 주제 확장",
        "🎵 Step 1-B: 가사 생성",
        "🎨 Step 2: 캐릭터 생성",
        "🎬 Step 3: 스토리보드"
    ])
    
    # 각 탭 렌더링
    with tab1a:
        theme_expander.render(client)
    
    with tab1b:
        lyrics.render(client)
    
    with tab2:
        character.render(client)
    
    with tab3:
        storyboard.render(client)
    
    # ============ 하단 네비게이션 ============
    st.divider()
    st.markdown("### 🔄 탭 전환하기")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.info("""
        **탭을 전환하려면:**
        1. 오른쪽 버튼을 눌러 페이지 상단으로 이동
        2. 원하는 탭을 클릭하세요
        """)
    
    with col2:
        # JavaScript로 상단 스크롤
        scroll_to_top = st.button("⬆️ 상단으로 이동", use_container_width=True, type="primary")
        
        if scroll_to_top:
            st.markdown(
                """
                <script>
                window.scrollTo({top: 0, behavior: 'smooth'});
                </script>
                """,
                unsafe_allow_html=True
            )
    
    st.divider()
    
    # 단계별 안내
    st.markdown("### 📋 각 단계 요약")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        **💡 Step 1-A**
        
        주제 확장 (선택)
        - 짧은 주제 입력
        - AI가 3가지 버전 생성
        """)
    
    with col2:
        st.markdown("""
        **🎵 Step 1-B**
        
        가사 생성
        - 장르, Vibe 선택
        - Suno/Udio 최적화
        - Mureka 태그
        """)
    
    with col3:
        st.markdown("""
        **🎨 Step 2**
        
        캐릭터 생성
        - 마스터 이미지 프롬프트
        - URL 저장
        """)
    
    with col4:
        st.markdown("""
        **🎬 Step 3**
        
        스토리보드
        - 20개 장면 프롬프트
        - AI 스타일 추천
        - 편집 레시피
        """)


if __name__ == "__main__":
    main()
