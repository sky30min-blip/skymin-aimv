"""
utils.py - OpenAI API 유틸리티 모듈 + 프로젝트 저장/불러오기
secrets.toml을 통한 API 키 관리
"""

import streamlit as st
from openai import OpenAI
import json
from datetime import datetime


# ============ 프로젝트 저장/불러오기에 사용할 키 목록 ============
PROJECT_KEYS = [
    "song_title",
    "lyrics",
    "lyrics_topic",
    "lyrics_genre",
    "lyrics_vibe",
    "lyrics_mood",
    "lyrics_language",
    "lyrics_era",
    "lyrics_intensity",
    "character_prompt",
    "character_style",
    "character_style_kr",
    "character_subject",
    "master_image_url",
    "storyboard_raw",
    "storyboard_url",
    "storyboard_style",
    "storyboard_style_kr",
    "storyboard_video_mood",
    "storyboard_video_mood_kr",
    "final_prompts"
]


def get_openai_client() -> OpenAI | None:
    """
    secrets.toml에서 API 키를 읽어 OpenAI 클라이언트를 생성합니다.
    
    Returns:
        OpenAI 클라이언트 인스턴스 또는 None (키가 없는 경우)
    """
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        
        if not api_key:
            st.error("🔑 secrets.toml 파일을 확인해주세요. OPENAI_API_KEY가 비어있습니다.")
            return None
        
        client = OpenAI(api_key=api_key)
        return client
    
    except KeyError:
        st.error("""
        🔑 **secrets.toml 파일을 확인해주세요.**
        
        `.streamlit/secrets.toml` 파일에 다음 내용을 추가하세요:
        ```
        OPENAI_API_KEY = "sk-your-api-key-here"
        ```
        """)
        return None
    
    except Exception as e:
        st.error(f"🔑 secrets.toml 파일을 확인해주세요. 오류: {str(e)}")
        return None


def get_gpt_response(client: OpenAI, system_role: str, user_prompt: str) -> str:
    """
    GPT 모델에 요청을 보내고 응답을 받습니다.
    
    Args:
        client: OpenAI 클라이언트 인스턴스
        system_role: 시스템 역할 메시지
        user_prompt: 사용자 프롬프트
        
    Returns:
        GPT 응답 텍스트
        
    Raises:
        Exception: API 호출 실패 시 에러 메시지 반환
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=4000
        )
        return response.choices[0].message.content
    
    except Exception as e:
        error_message = f"API 호출 중 오류가 발생했습니다: {str(e)}"
        raise Exception(error_message)


# ============ 프로젝트 저장/불러오기 함수 ============

def export_project_to_json() -> tuple[str, str]:
    """
    현재 세션 스테이트를 JSON 문자열로 변환합니다.
    
    Returns:
        tuple: (JSON 문자열, 파일명)
    """
    project_data = {
        "version": "1.0",
        "created_at": datetime.now().isoformat(),
        "data": {}
    }
    
    for key in PROJECT_KEYS:
        if key in st.session_state:
            project_data["data"][key] = st.session_state[key]
    
    # 파일명 생성 (날짜 + 제목 기반)
    title = st.session_state.get("song_title", "untitled")
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()[:20]
    if not safe_title:
        safe_title = "untitled"
    
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"musicvideo_project_{safe_title}_{date_str}.json"
    
    json_str = json.dumps(project_data, ensure_ascii=False, indent=2)
    
    return json_str, filename


def import_project_from_json(json_str: str) -> bool:
    """
    JSON 문자열에서 프로젝트 데이터를 로드하여 세션 스테이트에 저장합니다.
    
    Args:
        json_str: JSON 문자열
        
    Returns:
        bool: 성공 여부
    """
    try:
        project_data = json.loads(json_str)
        
        # 버전 확인
        if "data" not in project_data:
            return False
        
        # 데이터 복원
        for key, value in project_data["data"].items():
            if key in PROJECT_KEYS:
                st.session_state[key] = value
        
        return True
    
    except json.JSONDecodeError:
        return False
    except Exception:
        return False


def get_project_info_from_json(json_str: str) -> dict | None:
    """
    JSON 문자열에서 프로젝트 정보만 추출합니다.
    
    Args:
        json_str: JSON 문자열
        
    Returns:
        dict: 프로젝트 정보 또는 None
    """
    try:
        project_data = json.loads(json_str)
        return {
            "version": project_data.get("version", "unknown"),
            "created_at": project_data.get("created_at", "unknown"),
            "title": project_data.get("data", {}).get("song_title", "제목 없음"),
            "has_lyrics": bool(project_data.get("data", {}).get("lyrics")),
            "has_character": bool(project_data.get("data", {}).get("character_prompt")),
            "has_storyboard": bool(project_data.get("data", {}).get("final_prompts"))
        }
    except:
        return None