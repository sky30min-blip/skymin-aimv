"""
main.py - AI 뮤직비디오 제작 올인원 툴
메인 실행 파일
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
from utils import get_openai_client
from tabs import lyrics, character, storyboard


def init_session_state():
    """세션 스테이트 초기화"""
    defaults = {
        "lyrics": "",
        "lyrics_topic": "",
        "lyrics_mood": "",
        "character_prompt": "",
        "character_style": "",
        "master_image_url": "",
        "storyboard_raw": "",
        "storyboard_url": "",
        "storyboard_style": "",
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
        
        st.divider()
        
        # 사용 안내
        st.subheader("📖 사용 방법")
        st.markdown("""
        1. **Tab 1**: 노래 주제로 가사 생성
        2. **Tab 2**: 캐릭터 프롬프트 생성 → Midjourney에서 실행
        3. **Tab 3**: 가사 + 마스터 이미지 URL로 10개 장면 프롬프트 생성
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
    st.markdown("""
    가사 생성부터 캐릭터 일관성이 적용된 Midjourney 프롬프트까지, 
    뮤직비디오 제작에 필요한 모든 것을 한 곳에서!
    """)
    
    st.divider()
    
    # 탭 생성
    tab1, tab2, tab3 = st.tabs([
        "🎵 Step 1: 가사 생성",
        "🎨 Step 2: 캐릭터 생성",
        "🎬 Step 3: 스토리보드"
    ])
    
    # 각 탭 렌더링
    with tab1:
        lyrics.render(client)
    
    with tab2:
        character.render(client)
    
    with tab3:
        storyboard.render(client)


if __name__ == "__main__":
    main()