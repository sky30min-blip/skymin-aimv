"""
utils.py - OpenAI API 유틸리티 모듈
secrets.toml을 통한 API 키 관리
"""

import streamlit as st
from openai import OpenAI


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