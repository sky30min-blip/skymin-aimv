"""
tabs/theme_expander.py - 주제 확장기 탭 (Tab 1-A)
모바일 최적화 + 원클릭 복사 기능
"""

import streamlit as st
from utils import get_gpt_response


SYSTEM_ROLE = """당신은 세계적인 작사가이자 스토리텔러입니다.

## 당신의 임무
사용자가 제공한 짧은 주제를 분석하여 **3가지 버전**으로 확장하고, 최적의 설정을 추천합니다.

## 3가지 버전 작성 규칙

### 1. 미니멀 버전 (Minimal)
- 사용자의 원래 주제를 **정리만** 함
- 핵심 메시지 유지
- 간결하게 (50자 내외)

### 2. 스탠다드 버전 (Standard)
- 구체적인 **추억/장소 1-2개** 추가
- 감정을 더 명확하게
- 중간 길이 (100-150자)

### 3. 디럭스 버전 (Deluxe)
- 시간, 장소, 구체적 에피소드 모두 포함
- 영화 같은 스토리텔링
- 풍부한 디테일 (200-300자)

## 추천 설정 규칙

사용자의 주제를 분석하여:
- **장르**: 감정과 어울리는 장르 (예: 발라드, R&B, 힙합)
- **보컬**: 주제에 맞는 보컬 타입 (솔로 남성/여성, 듀엣 등)
- **Vibe**: 분위기 (정석대로, 슬픈데 신나게, 웃기지만 진지하게, 광기/호러)
- **키워드**: 가사에 포함하면 좋을 단어 3-5개

## 출력 형식 (반드시 준수!)

[미니멀]
(정리된 주제)

[스탠다드]
(디테일 추가된 주제)

[디럭스]
(최대한 구체적인 주제)

[추천설정]
장르: (추천 장르)
보컬: (추천 보컬 타입)
Vibe: (추천 Vibe)
키워드: (쉼표로 구분된 키워드)

## 추천 예시

**사용자 입력:** "7년 연인 헤어짐, 추억 많아서 못 잊을 것 같음"

[미니멀]
7년을 함께한 연인과 헤어졌다. 너무 많은 추억 때문에 잊을 수 있을까?

[스탠다드]
7년을 함께한 연인과 헤어졌다. 매일 밤 통화하던 습관, 주말마다 걷던 한강... 이 모든 추억을 지우고 너를 잊을 수 있겠냐?

[디럭스]
우리는 7년을 함께했다. 스물셋, 서로의 첫사랑으로 시작해서 서른이 되어서야 헤어졌다. 매일 밤 11시, 잠들기 전 통화가 습관이었고, 주말이면 한강을 걸으며 미래를 그렸다. 사소한 다툼도, 달콤한 화해도 수백 번. 이제 다른 길을 가야 한다고 했지만, 7년의 기억을 지우고 너를 처음 보는 사람처럼 대할 수 있겠냐?

[추천설정]
장르: 발라드
보컬: 혼성 듀엣 (남/녀) - 서로의 시선을 대화로 표현
Vibe: 정석대로
키워드: 7년, 추억, 한강, 통화, 미련, 후회"""


def parse_expansion(response: str) -> dict:
    """
    GPT 응답을 파싱하여 3가지 버전과 추천사항을 추출합니다.
    
    Returns:
        dict: {
            'minimal': str,
            'standard': str,
            'deluxe': str,
            'genre': str,
            'vocal': str,
            'vibe': str,
            'keywords': str
        }
    """
    result = {
        'minimal': '',
        'standard': '',
        'deluxe': '',
        'genre': '',
        'vocal': '',
        'vibe': '',
        'keywords': ''
    }
    
    # 미니멀 추출
    if '[미니멀]' in response:
        parts = response.split('[미니멀]')[1].split('[스탠다드]')
        result['minimal'] = parts[0].strip()
    
    # 스탠다드 추출
    if '[스탠다드]' in response:
        parts = response.split('[스탠다드]')[1].split('[디럭스]')
        result['standard'] = parts[0].strip()
    
    # 디럭스 추출
    if '[디럭스]' in response:
        parts = response.split('[디럭스]')[1].split('[추천설정]')
        result['deluxe'] = parts[0].strip()
    
    # 추천설정 추출
    if '[추천설정]' in response:
        settings = response.split('[추천설정]')[1].strip()
        
        for line in settings.split('\n'):
            if '장르:' in line:
                result['genre'] = line.split('장르:')[1].strip()
            elif '보컬:' in line:
                result['vocal'] = line.split('보컬:')[1].strip()
            elif 'Vibe:' in line or '분위기:' in line:
                result['vibe'] = line.split(':')[1].strip()
            elif '키워드:' in line:
                result['keywords'] = line.split('키워드:')[1].strip()
    
    return result


def render(client):
    """주제 확장기 탭을 렌더링합니다."""
    
    st.header("💡 Step 1-A: AI 주제 확장기")
    st.markdown("""
    짧은 아이디어만 입력하세요. AI가 **3가지 버전**으로 확장해드립니다!
    
    > 🎯 *"간단한 메모 → 영화 같은 스토리로"*
    """)
    
    st.info("""
    ✨ **이렇게 사용하세요:**
    1. 떠오른 주제를 **짧게** 입력
    2. "AI 확장" 버튼 클릭
    3. 3가지 버전 중 하나 선택
    4. 복사해서 **Step 1-B (가사 생성)**로!
    """)
    
    st.divider()
    
    # ============ 짧은 주제 입력 ============
    st.subheader("📝 주제 입력")
    
    short_theme = st.text_area(
        "떠오른 주제를 짧게 적어주세요",
        placeholder="예시:\n- 7년 연인 헤어짐, 추억 많아서 못 잊을 듯\n- 월요일 출근길이 전쟁터 같음\n- 어머니 마지막 편지 읽는 순간\n- AI가 인간에게 보내는 러브레터",
        height=150,
        help="한 줄이든, 몇 단어든 상관없습니다!"
    )
    
    with st.expander("💡 주제 입력 팁"):
        st.markdown("""
        **좋은 예시:**
        - ✅ "10년 만에 고향 돌아왔는데 다 변해 있음"
        - ✅ "치킨 먹을 때가 제일 행복함"
        - ✅ "암호화폐로 전재산 날림"
        - ✅ "새벽 3시 편의점 알바생의 독백"
        
        **나쁜 예시:**
        - ❌ "사랑 노래" (너무 추상적)
        - ❌ "좋은 가사" (구체성 없음)
        """)
    
    st.divider()
    
    # ============ AI 확장 버튼 ============
    if st.button("✨ AI가 3가지 버전으로 확장하기", type="primary", use_container_width=True):
        if not short_theme.strip():
            st.error("주제를 입력해주세요.")
            return
        if client is None:
            st.error("API 키가 설정되지 않았습니다.")
            return
        
        user_prompt = f"""다음 주제를 분석하여 3가지 버전(미니멀, 스탠다드, 디럭스)으로 확장하고 최적의 설정을 추천해주세요.

## 사용자 주제
{short_theme}

위 형식에 맞춰 정확히 출력해주세요."""

        with st.spinner("🤖 AI가 주제를 분석하고 있습니다..."):
            try:
                response = get_gpt_response(client, SYSTEM_ROLE, user_prompt)
                
                # 파싱
                parsed = parse_expansion(response)
                
                # 세션 스테이트에 저장
                st.session_state["theme_expansion"] = parsed
                st.session_state["theme_raw"] = response
                
                st.success("🎉 3가지 버전이 완성되었습니다!")
                st.rerun()
                
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
                return
    
    # ============ 결과 표시 ============
    st.divider()
    
    if "theme_expansion" in st.session_state and st.session_state["theme_expansion"]:
        parsed = st.session_state["theme_expansion"]
        
        st.subheader("🎯 AI가 확장한 3가지 버전")
        st.caption("원하는 버전을 복사해서 **Step 1-B (가사 생성)**에 붙여넣으세요!")
        
        # ============ 모바일 최적화: 세로 배치 ============
        
        # 버전 1: 미니멀
        with st.container():
            st.markdown("### 🥉 미니멀 (간결)")
            st.info(parsed['minimal'])
            
            # 복사 버튼 (코드 블록으로)
            st.code(parsed['minimal'], language=None)
            st.caption("👆 위 텍스트를 길게 눌러 복사하세요 (모바일)")
            
            st.divider()
        
        # 버전 2: 스탠다드
        with st.container():
            st.markdown("### 🥈 스탠다드 (적당한 디테일) ⭐ 추천")
            st.success(parsed['standard'])
            
            # 복사 버튼
            st.code(parsed['standard'], language=None)
            st.caption("👆 위 텍스트를 길게 눌러 복사하세요 (모바일)")
            
            st.divider()
        
        # 버전 3: 디럭스
        with st.container():
            st.markdown("### 🥇 디럭스 (최대 구체화)")
            st.warning(parsed['deluxe'])
            
            # 복사 버튼
            st.code(parsed['deluxe'], language=None)
            st.caption("👆 위 텍스트를 길게 눌러 복사하세요 (모바일)")
            
            st.divider()
        
        # ============ 추천 설정 표시 ============
        st.subheader("🎯 AI 추천 설정")
        st.markdown("""
        아래 설정을 **Step 1-B (가사 생성)**에서 사용하면 더 좋은 결과를 얻을 수 있습니다!
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if parsed['genre']:
                st.metric("🎸 추천 장르", parsed['genre'])
            if parsed['vocal']:
                st.metric("🎤 추천 보컬", parsed['vocal'])
        
        with col2:
            if parsed['vibe']:
                st.metric("🎭 추천 Vibe", parsed['vibe'])
            if parsed['keywords']:
                st.metric("🔑 추천 키워드", parsed['keywords'])
        
        # 추천 설정 복사 (전체)
        st.divider()
        st.markdown("**📋 추천 설정 전체 복사:**")
        settings_text = f"""장르: {parsed['genre']}
보컬: {parsed['vocal']}
Vibe: {parsed['vibe']}
키워드: {parsed['keywords']}"""
        st.code(settings_text, language=None)
        
        st.divider()
        
        # ============ 다음 단계 안내 ============
        st.success("""
        🎉 **주제 확장 완료!**
        
        **다음 단계:**
        1. 위에서 원하는 버전을 **복사** (길게 눌러서)
        2. **Step 1-B (가사 생성)** 탭으로 이동
        3. "주제" 입력칸에 **붙여넣기**
        4. 추천 설정 적용
        5. 가사 생성! 🎵
        """)
        
        # 초기화 버튼
        if st.button("🔄 새로운 주제로 다시 시작", use_container_width=True):
            del st.session_state["theme_expansion"]
            del st.session_state["theme_raw"]
            st.rerun()
        
        # 원본 응답 확인 (디버깅용)
        with st.expander("🔍 원본 AI 응답 확인 (디버깅용)"):
            st.text(st.session_state.get("theme_raw", ""))
    
    else:
        st.markdown("---")
        st.markdown("""
        ### 🚀 시작하기
        
        1. **위에 주제를 짧게** 입력하세요
           - 한 줄이든, 몇 단어든 OK!
           - "7년 연인 헤어짐" 같은 짧은 메모도 좋습니다
        
        2. **"AI 확장" 버튼** 클릭
        
        3. **3가지 버전** 중 마음에 드는 것 선택
        
        4. **복사해서 Step 1-B로** 이동!
        
        > 💡 완전 초보자도 쉽게 멋진 가사를 만들 수 있습니다!
        """)
