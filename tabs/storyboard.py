"""
tabs/storyboard.py - 스토리보드 생성 탭 (Tab 3) - 메인 UI
"""

import streamlit as st
from utils import get_gpt_response

# ⭐ 모듈 import
from storyboard_config import (
    STYLE_GUIDE,
    VIDEO_MOOD_MAP,
    VIDEO_MOOD_OPTIONS,
    SYSTEM_ROLE_20_AB,
    SYSTEM_ROLE_40_INDEPENDENT,
    analyze_lyrics_for_style
)
from storyboard_utils import (
    parse_scenes_20_ab,
    parse_scenes_40_independent,
    initialize_scene_overrides,
    get_scene_override,
    set_scene_override,
    translate_korean_to_prompt,
    translate_english_to_korean,
    suggest_visual_anchor
)


def render(client):
    """스토리보드 탭을 렌더링합니다."""
    
    # 장면 수정 상태 초기화
    initialize_scene_overrides()
    
    st.header("🎬 Step 3: 대서사시 스토리보드 생성")
    st.markdown("""
    가사를 분석하여 **초고품질 이미지 프롬프트**를 생성합니다.
    
    > 🎥 *"대서사시 연계 엔진 + 시각적 연속성 + 실시간 수정 + AI 추천"*
    """)
    
    st.success("""
    ✨ **v2.1 완전 업그레이드:**
    1. 🎨 **11가지 프리미엄 스타일** - 실제 이미지 미리보기
    2. 🎬 **장면 방식 선택** - 20개+A/B컷 or 40개 독립 장면
    3. 🔗 **시각적 연속성** - Match Cut 원테이크 영화
    4. ⚓ **Visual Anchor** - AI 자동 추천 또는 직접 입력
    5. 🎨 **--cref + --sref** - 이중 URL 고정
    6. ✏️ **실시간 수동 수정** - 각 장면 직접 편집
    """)
    
    st.divider()
    
    # ============ 장면 생성 방식 선택 ============
    st.subheader("🎬 장면 생성 방식 선택")
    
    scene_mode = st.radio(
        "원하는 방식을 선택하세요",
        options=[
            "20개 메인 장면 + A/B 앵글 (총 40컷)",
            "40개 독립 장면"
        ],
        help="""
        • 20+A/B: 편집 자유도 최대 (같은 장면을 와이드/클로즈업 2가지로)
        • 40개: 서사 풍부함 최대 (모두 다른 장면)
        """,
        horizontal=True
    )
    
    if scene_mode == "20개 메인 장면 + A/B 앵글 (총 40컷)":
        st.info("""
        📐 **20+A/B 구조:**
        - 20개 메인 장면
        - 각 장면마다 A컷(와이드샷) + B컷(클로즈업) = 총 40컷
        - 편집 시 A만, B만, 또는 A→B 순서로 자유롭게 조합 가능
        """)
        selected_mode = "20_AB"
    else:
        st.info("""
        🎞️ **40개 독립 장면:**
        - 모두 완전히 다른 장면
        - 서사가 풍부하게 전개
        - 3~4분 영상을 완벽히 채움
        """)
        selected_mode = "40_INDEPENDENT"
    
    st.divider()
    
    # ============ 가사 입력 ============
    st.subheader("📝 가사 입력")
    default_lyrics = st.session_state.get("lyrics", "")
    
    lyrics_input = st.text_area(
        "뮤직비디오에 사용할 가사",
        value=default_lyrics,
        height=250,
        placeholder="[Verse 1]\n여기에 가사를 입력하세요...",
        help="가사를 기반으로 장면이 생성됩니다"
    )
    
    if default_lyrics:
        st.caption("💡 Tab 1에서 생성한 가사가 자동으로 불러와졌습니다.")
    
    st.divider()
    
    # ============ 일관성 장치 (Character & Style URLs) ============
    st.subheader("🔗 일관성 장치 (Character & Style URLs)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🧑 캐릭터 참조 URL")
        default_char_url = st.session_state.get("master_image_url", "")
        
        char_url = st.text_input(
            "캐릭터 이미지 URL (--cref)",
            value=default_char_url,
            placeholder="https://cdn.midjourney.com/...",
            help="Tab 2에서 생성한 캐릭터 이미지 URL",
            key="char_url_input"
        )
        
        if default_char_url:
            st.caption("💡 Tab 2에서 저장한 URL이 불러와졌습니다.")
    
    with col2:
        st.markdown("#### 🎨 스타일 참조 URL")
        default_style_url = st.session_state.get("style_reference_url", "")
        
        style_url = st.text_input(
            "스타일(화풍) 이미지 URL (--sref)",
            value=default_style_url,
            placeholder="https://cdn.midjourney.com/...",
            help="모든 장면의 색감/질감을 고정할 참조 이미지 URL",
            key="style_url_input"
        )
        
        if style_url:
            st.caption("✅ 스타일 URL이 입력되었습니다. (--sw 1000 자동 적용)")
        else:
            st.info("💡 스타일 URL을 입력하면 모든 장면의 화풍이 완벽히 통일됩니다.")
    
    st.divider()
    
    # ============ ⭐ Visual Anchor 설정 (AI 추천 기능 포함) ============
    st.subheader("⚓ Visual Anchor (전역 앵커)")
    st.markdown("""
    **모든 장면에 공통으로 적용될 주인공의 외형**을 정의하세요.
    이것이 시각적 일관성의 핵심입니다!
    """)
    
    # ⭐ 하드코딩 제거 - 빈 문자열로 변경
    default_anchor = st.session_state.get("visual_anchor", "")
    
    # AI 추천 버튼
    col_input, col_suggest = st.columns([4, 1])
    
    with col_input:
        visual_anchor = st.text_area(
            "주인공 핵심 외형 (영어)",
            value=default_anchor,
            height=100,
            placeholder="예: Young woman with silver hair, wearing elegant dress, emerald pendant\n\n또는 '🤖 AI 추천' 버튼을 눌러 가사 기반 자동 생성",
            help="이 텍스트가 모든 장면에서 맥락에 맞게 적용됩니다",
            key="visual_anchor_input"
        )
    
    with col_suggest:
        st.markdown("#### 🤖")
        if st.button("AI 추천", use_container_width=True, help="가사를 분석하여 어울리는 주인공을 AI가 제안합니다"):
            if not lyrics_input.strip():
                st.error("먼저 가사를 입력해주세요.")
            elif client is None:
                st.error("API 키가 설정되지 않았습니다.")
            else:
                with st.spinner("🤖 가사를 분석하여 주인공을 추천하고 있습니다..."):
                    current_genre = st.session_state.get("lyrics_genre", "")
                    current_vibe = st.session_state.get("lyrics_vibe", "")
                    
                    suggested = suggest_visual_anchor(client, lyrics_input, current_genre, current_vibe)
                    
                    if suggested:
                        st.session_state["visual_anchor"] = suggested
                        st.success("✅ AI 추천 완료! 아래 입력창에 반영되었습니다.")
                        st.rerun()
                    else:
                        st.error("추천 생성에 실패했습니다. 직접 입력해주세요.")
    
    st.session_state["visual_anchor"] = visual_anchor
    
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
    
    # ============ 스타일 선택 (이미지 미리보기 포함) ============
    st.subheader("🎨 비주얼 스타일 선택")
    
    # AI 자동 추천
    current_genre = st.session_state.get("lyrics_genre", "")
    current_vibe = st.session_state.get("lyrics_vibe", "")
    
    auto_recommended = None
    if current_genre or current_vibe or lyrics_input:
        auto_recommended = analyze_lyrics_for_style(lyrics_input, current_genre, current_vibe)
        st.success(f"🤖 **AI 추천 스타일:** {auto_recommended}")
        
        if current_genre:
            st.caption(f"📊 분석 근거: 장르({current_genre}), Vibe({current_vibe})")
    
    # 스타일 선택
    style_options = list(STYLE_GUIDE.keys())
    
    # Tab 2에서 선택한 스타일을 기본값으로 설정
    default_style = "AI 자동 추천"
    if "character_style_kr" in st.session_state and st.session_state["character_style_kr"]:
        char_style = st.session_state["character_style_kr"]
        if char_style in style_options:
            default_style = char_style
            st.info(f"💡 Tab 2에서 선택하신 **{char_style}** 스타일이 자동 선택되었습니다!")
    
    # 기본값의 인덱스 찾기
    try:
        default_index = style_options.index(default_style)
    except ValueError:
        default_index = 0
    
    selected_style = st.selectbox(
        "이미지 스타일 선택",
        options=style_options,
        index=default_index,
        help="각 스타일의 미리보기 이미지를 확인하세요"
    )
    
    # 선택된 스타일 정보 + 이미지 표시
    if selected_style != "AI 자동 추천":
        style_info = STYLE_GUIDE[selected_style]
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            # 미리보기 이미지 표시
            if style_info.get("preview_image"):
                st.image(
                    style_info["preview_image"], 
                    caption=f"{style_info['preview']} {selected_style}",
                    use_container_width=True
                )
            else:
                st.markdown(f"### {style_info['preview']}")
                st.markdown(f"**{selected_style}**")
        
        with col2:
            st.markdown(f"### {selected_style}")
            st.caption(style_info['description'])
            
            with st.expander("📋 스타일 상세 정보"):
                st.markdown("**이미지 키워드:**")
                st.code(style_info['image_keywords'], language=None)
                
                st.markdown("**영상 키워드:**")
                st.text(style_info['video_keywords'])
                
                st.markdown("**특수 효과:**")
                st.text(style_info['effects'])
                
                st.markdown("**화면 전환:**")
                st.text(style_info['transitions'])
    
    # 전체 스타일 갤러리
    with st.expander("🎨 모든 스타일 미리보기 갤러리"):
        cols = st.columns(3)
        col_idx = 0
        
        for style_name, style_data in STYLE_GUIDE.items():
            if style_name == "AI 자동 추천":
                continue
            
            with cols[col_idx % 3]:
                if style_data.get("preview_image"):
                    st.image(style_data["preview_image"], use_container_width=True)
                st.markdown(f"**{style_data['preview']} {style_name}**")
                st.caption(style_data['description'])
                st.divider()
            
            col_idx += 1
    
    st.divider()
    
    # ============ 영상 분위기 ============
    st.subheader("🎥 영상 분위기")
    
    video_mood_kr = st.selectbox(
        "전체 영상 톤",
        options=VIDEO_MOOD_OPTIONS
    )
    
    st.caption(f"🔤 영어값: `{VIDEO_MOOD_MAP[video_mood_kr]}`")
    
    st.divider()
    
    # ============ 생성 버튼 ============
    generate_button_text = "🎬 20개+A/B (총 40컷) 생성" if selected_mode == "20_AB" else "🎬 40개 독립 장면 생성"
    
    if st.button(generate_button_text, type="primary", use_container_width=True):
        if not lyrics_input.strip():
            st.error("가사를 입력해주세요.")
            return
        if client is None:
            st.error("API 키가 설정되지 않았습니다.")
            return
        if not visual_anchor.strip():
            st.error("Visual Anchor (주인공 외형)를 입력하거나 'AI 추천' 버튼을 눌러주세요.")
            return
        
        # 최종 스타일 결정
        if selected_style == "AI 자동 추천":
            if auto_recommended:
                final_style = auto_recommended
            else:
                final_style = "지브리 2.0 (Miyazaki Masterpiece)"
            st.info(f"🤖 AI가 선택한 스타일: **{final_style}**")
        else:
            final_style = selected_style
        
        # 스타일 데이터 가져오기
        style_data = STYLE_GUIDE[final_style]
        style_keywords = style_data["image_keywords"]
        video_mood_en = VIDEO_MOOD_MAP[video_mood_kr]
        
        # 선택된 모드에 따라 시스템 프롬프트 선택
        if selected_mode == "20_AB":
            system_role = SYSTEM_ROLE_20_AB
            mode_description = "20개 메인 장면 + 각 A/B 앵글 (총 40컷)"
        else:
            system_role = SYSTEM_ROLE_40_INDEPENDENT
            mode_description = "40개 독립 장면"
        
        # 사용자 프롬프트 구성
        user_prompt = f"""다음 가사를 분석하여 뮤직비디오용 프롬프트를 생성해주세요.

## 생성 방식
{mode_description}

## 가사
{lyrics_input}

## Visual Anchor (모든 장면 공통)
{visual_anchor}

## 영상 분위기
{video_mood_en}

## 스타일 키워드 (시스템이 자동 추가)
{style_keywords}

## ⭐ 핵심 규칙 ⭐

1. **Visual Anchor 100% 유지**
   - 모든 장면의 첫 부분에 다음을 반드시 포함: "{visual_anchor}"

2. **Match Cut (장면 계승)**
   - n번 장면의 마지막 요소가 n+1번의 시작 요소
   - 한글 설명 끝에 연결점 표시: [이전: X → 현재: Y]

3. **시각적 직유 (Visual Literalism)**
   - 추상 비유를 물리적 실체로 100% 변환
   - 금지 단어: "Representing", "Symbolizing", "Concept of"

4. **이미지 묘사에 스타일 키워드 포함 금지**
   - 시스템이 자동으로 추가합니다

지금 바로 위 규칙을 엄격히 준수하여 생성해주세요!"""

        spinner_text = "🎬 AI가 장면을 분석하고 있습니다... (약 2-3분)" if selected_mode == "20_AB" else "🎬 AI가 40개 장면을 분석하고 있습니다... (약 2-3분)"
        
        with st.spinner(spinner_text):
            try:
                result = get_gpt_response(client, system_role, user_prompt)
                
                # 세션 스테이트에 저장
                st.session_state["storyboard_raw"] = result
                st.session_state["storyboard_mode"] = selected_mode
                st.session_state["storyboard_char_url"] = char_url
                st.session_state["storyboard_style_url"] = style_url
                st.session_state["storyboard_style"] = final_style
                st.session_state["storyboard_video_mood"] = video_mood_en
                st.session_state["storyboard_video_mood_kr"] = video_mood_kr
                st.session_state["storyboard_visual_anchor"] = visual_anchor
                
                # 스타일 URL 저장
                if style_url:
                    st.session_state["style_reference_url"] = style_url
                
                success_message = "🎉 20개+A/B (총 40컷)이 생성되었습니다!" if selected_mode == "20_AB" else "🎉 40개 독립 장면이 생성되었습니다!"
                st.success(success_message)
                st.rerun()
                
            except Exception as e:
                st.error(f"오류 발생: {str(e)}")
                return
    
    # ============ 결과 표시 ============
    st.divider()
    
    if "storyboard_raw" in st.session_state and st.session_state["storyboard_raw"]:
        stored_mode = st.session_state.get("storyboard_mode", "40_INDEPENDENT")
        
        st.subheader(f"🎬 생성된 장면")
        
        # 저장된 값 불러오기
        char_url = st.session_state.get("storyboard_char_url", "")
        style_url = st.session_state.get("storyboard_style_url", "")
        final_style = st.session_state.get("storyboard_style", "")
        visual_anchor = st.session_state.get("storyboard_visual_anchor", "")
        style_data = STYLE_GUIDE.get(final_style, {})
        style_keywords = style_data.get("image_keywords", "")
        
        # 적용 설정 안내
        mode_desc = "20개 메인 + A/B 앵글 (총 40컷)" if stored_mode == "20_AB" else "40개 독립 장면"
        
        st.info(f"""
        📌 **적용된 설정:**
        - 🎬 생성 방식: **{mode_desc}**
        - ⚓ Visual Anchor: **{visual_anchor[:50]}{'...' if len(visual_anchor) > 50 else ''}**
        - 🎨 스타일: **{final_style}**
        - 🎥 분위기: **{st.session_state.get('storyboard_video_mood_kr', '-')}**
        - 🧑 캐릭터 참조 (--cref): {'✅ 적용' if char_url else '❌ 미적용'}
        - 🎨 스타일 참조 (--sref): {'✅ 적용 (--sw 1000)' if style_url else '❌ 미적용'}
        - 📐 화면 비율: `--ar 16:9`
        """)
        
        # 모드에 따라 파싱
        if stored_mode == "20_AB":
            scenes = parse_scenes_20_ab(st.session_state["storyboard_raw"])
        else:
            scenes = parse_scenes_40_independent(st.session_state["storyboard_raw"])
        
        if len(scenes) == 0:
            st.error("장면 파싱에 실패했습니다. 다시 생성해주세요.")
            return
        
        st.caption(f"✅ {len(scenes)}개 컷이 생성되었습니다.")
        
        st.divider()
        
        # ============ 실시간 수동 수정 시스템 ============
        st.subheader("✏️ 장면별 실시간 수정")
        st.markdown("""
        각 장면 하단의 편집창에서 **직접 수정**할 수 있습니다.
        """)
        
        st.divider()
        
        # ============ 최종 프롬프트 조립 ============
        final_prompts = []
        
        for i, scene in enumerate(scenes, 1):
            # 장면 키 생성 (수정 내용 저장용)
            if stored_mode == "20_AB":
                scene_key = f"{scene['scene_number']}-{scene['cut_type']}"
                scene_title = f"Scene {scene['scene_number']:02d}-{scene['cut_type']}컷"
            else:
                scene_key = f"{scene['scene_number']}"
                scene_title = f"Scene {scene['scene_number']:02d}"
            
            # 가독성을 위한 컨테이너 스타일
            with st.container():
                st.markdown(f"""
                <div style="
                    border: 3px solid #1f77b4;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 15px 0;
                    background-color: #f0f2f6;
                ">
                """, unsafe_allow_html=True)
                
                with st.expander(f"🎬 {scene_title}", expanded=(i <= 3)):
                    
                    # 영어 프롬프트를 한글로 자동 번역
                    original_english = scene.get('image_prompt', '')
                    
                    # 세션에 번역본이 없으면 자동 번역
                    translation_key = f"korean_translation_{scene_key}"
                    if translation_key not in st.session_state:
                        with st.spinner(f"🤖 {scene_title} 한글 번역 중..."):
                            korean_translation = translate_english_to_korean(client, original_english)
                            st.session_state[translation_key] = korean_translation
                    else:
                        korean_translation = st.session_state[translation_key]
                    
                    # ============ 한글 설명 수정 및 영어 변환 ============
                    st.markdown("### 📖 장면 설명 (한글)")
                    
                    # 한글 설명 입력칸
                    korean_input_key = f"korean_desc_{scene_key}"
                    
                    korean_desc_input = st.text_area(
                        "장면을 한글로 설명하세요",
                        value=korean_translation,
                        height=100,
                        key=korean_input_key,
                        placeholder="예: 여자가 비 오는 거리에서 우산을 쓰고 슬픈 표정으로 서 있다",
                        help="한글로 수정한 후 '영어 프롬프트로 변환' 버튼을 누르세요"
                    )
                    
                    # 영어 변환 버튼
                    col_translate, col_clear = st.columns([3, 1])
                    
                    with col_translate:
                        if st.button(f"🔄 영어 프롬프트로 변환", key=f"translate_{scene_key}", use_container_width=True):
                            if not korean_desc_input.strip():
                                st.error("한글 설명을 입력해주세요.")
                            else:
                                with st.spinner("🤖 GPT가 영어 프롬프트로 변환 중..."):
                                    visual_anchor = st.session_state.get("storyboard_visual_anchor", "")
                                    translated = translate_korean_to_prompt(client, korean_desc_input, visual_anchor)
                                    
                                    if translated and not translated.startswith("변환 실패"):
                                        # 변환된 영어를 override로 저장
                                        set_scene_override(scene_key, translated)
                                        st.success("✅ 영어 프롬프트로 변환 완료!")
                                        st.rerun()
                                    else:
                                        st.error(f"변환 실패: {translated}")
                    
                    with col_clear:
                        if st.button(f"🗑️ 초기화", key=f"clear_korean_{scene_key}", use_container_width=True):
                            # 한글 번역과 override 모두 초기화
                            if translation_key in st.session_state:
                                del st.session_state[translation_key]
                            set_scene_override(scene_key, "")
                            st.info("한글 설명이 초기화되었습니다.")
                            st.rerun()
                    
                    st.divider()
                    
                    # 사용자 수정 확인
                    override = get_scene_override(scene_key)
                    
                    if override:
                        # 사용자가 수정한 경우
                        st.warning("✏️ **사용자 수정 버전이 적용되었습니다.**")
                        
                        st.markdown("**🎬 수정된 장면 묘사**")
                        st.code(override, language=None)
                        
                        step2_prompt = f"{override}, {style_keywords}"
                        actual_image_prompt = override
                        
                    else:
                        # AI 원본 사용
                        st.markdown("**🎬 Step 1: 장면 묘사**")
                        st.code(scene['image_prompt'], language=None)
                        
                        step2_prompt = f"{scene['image_prompt']}, {style_keywords}"
                        actual_image_prompt = scene['image_prompt']
                    
                    # Step 2 표시
                    st.markdown("**✨ Step 2: 최종 Midjourney 프롬프트**")
                    
                    # URL 파라미터 결합
                    url_params = ""
                    if char_url:
                        url_params += f" --cref {char_url}"
                    if style_url:
                        url_params += f" --sref {style_url} --sw 1000"
                    
                    midjourney_prompt = f"/imagine prompt: {step2_prompt}{url_params} --ar 16:9"
                    
                    st.code(midjourney_prompt, language=None)
                    
                    # Motion 프롬프트
                    st.markdown("**🎥 Motion 프롬프트 (Kling/Runway)**")
                    st.success(f"🎬 {scene['motion_prompt']}")
                    
                    st.divider()
                    
                    # ============ 영어 프롬프트 직접 수정 (고급) ============
                    st.markdown("### ✏️ 영어 프롬프트 직접 수정 (고급)")
                    st.caption("💡 위에서 '영어 프롬프트로 변환'을 사용했다면, 여기서 추가 미세 조정이 가능합니다.")
                    
                    current_override = get_scene_override(scene_key)
                    
                    user_edit = st.text_area(
                        f"{scene_title} 영어 프롬프트 직접 수정",
                        value=current_override,
                        height=100,
                        placeholder=f"예: {scene['image_prompt'][:100]}...",
                        key=f"override_{scene_key}",
                        help="영어 프롬프트를 직접 수정할 수 있습니다. 비우면 AI 원본 사용."
                    )
                    
                    col_save, col_reset = st.columns(2)
                    
                    with col_save:
                        if st.button(f"💾 {scene_title} 수정 저장", key=f"save_{scene_key}", use_container_width=True):
                            set_scene_override(scene_key, user_edit)
                            st.success(f"{scene_title} 수정이 저장되었습니다!")
                            st.rerun()
                    
                    with col_reset:
                        if st.button(f"🔄 {scene_title} 원본 복구", key=f"reset_{scene_key}", use_container_width=True):
                            set_scene_override(scene_key, "")
                            if translation_key in st.session_state:
                                del st.session_state[translation_key]
                            st.info(f"{scene_title}를 AI 원본으로 복구했습니다.")
                            st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # 프롬프트 저장
                final_prompts.append({
                    "scene_key": scene_key,
                    "scene_title": scene_title,
                    "korean_desc": korean_translation,
                    "step1_scene": actual_image_prompt,
                    "step2_final": step2_prompt,
                    "midjourney": midjourney_prompt,
                    "motion": scene['motion_prompt'],
                    "is_user_override": bool(override)
                })
        
        # 세션에 최종 프롬프트 저장
        st.session_state["final_prompts"] = final_prompts
        
        st.divider()
        
        # ============ 수정 통계 ============
        user_modified_count = sum(1 for p in final_prompts if p.get("is_user_override"))
        
        if user_modified_count > 0:
            st.success(f"""
            ✏️ **사용자 수정 통계:**
            - 총 {len(scenes)}개 컷 중 **{user_modified_count}개 컷**이 수정되었습니다.
            - 나머지 {len(scenes) - user_modified_count}개는 AI 원본이 사용됩니다.
            """)
        
        st.divider()
        
        # ============ 영상 편집 레시피 ============
        st.subheader("🎬 영상 편집 레시피")
        
        if style_data:
            tab1, tab2, tab3 = st.tabs([
                "📹 스톡 영상 키워드",
                "✨ 특수 효과 & 전환",
                "📋 통합 레시피"
            ])
            
            with tab1:
                st.markdown("### 📹 추천 스톡 영상 검색 키워드")
                st.success("🔍 **무료 스톡 영상 사이트:** Pexels, Pixabay, Videvo, Mixkit")
                
                if style_data.get("video_keywords"):
                    keywords = style_data["video_keywords"]
                    st.code(keywords, language=None)
                    st.caption("👆 위 키워드로 스톡 영상을 검색하세요")
            
            with tab2:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### ✨ 특수 효과")
                    if style_data.get("effects"):
                        st.info(style_data["effects"])
                
                with col2:
                    st.markdown("### 🔄 화면 전환")
                    if style_data.get("transitions"):
                        st.warning(style_data["transitions"])
            
            with tab3:
                st.markdown("### 📋 완전한 편집 가이드")
                
                recipe = f"""# {final_style} - 편집 레시피

## 🎨 스타일
{final_style}

## 📹 스톡 영상 키워드
{style_data.get('video_keywords', '-')}

## ✨ 특수 효과
{style_data.get('effects', '-')}

## 🔄 화면 전환
{style_data.get('transitions', '-')}

## 🎯 사용 방법
1. 위 키워드로 무료 스톡 영상 다운로드
2. 프리미어/다빈치 리졸브에서 편집
3. 추천 효과와 전환 적용
4. Match Cut으로 장면 연결
5. 음악과 싱크 맞추기
"""
                st.text_area("전체 레시피", value=recipe, height=300)
        
        st.divider()
        
        # ============ 전체 프롬프트 복사 섹션 ============
        st.subheader("📋 전체 프롬프트 (복사용)")
        
        tab_mj, tab_motion, tab_all = st.tabs([
            "🖼️ Midjourney 전체",
            "🎥 Motion 전체",
            "📄 통합 전체"
        ])
        
        with tab_mj:
            st.markdown("**Midjourney Discord에 순서대로 붙여넣기:**")
            all_mj = "\n\n".join([
                f"# {p['scene_title']}: {p['korean_desc']}\n{p['midjourney']}"
                for p in final_prompts
            ])
            st.text_area("MJ 프롬프트", value=all_mj, height=400, label_visibility="collapsed")
        
        with tab_motion:
            st.markdown("**Kling/Runway에서 사용:**")
            all_motion = "\n\n".join([
                f"# {p['scene_title']}: {p['korean_desc']}\n{p['motion']}"
                for p in final_prompts
            ])
            st.text_area("Motion", value=all_motion, height=400, label_visibility="collapsed")
        
        with tab_all:
            st.markdown("**전체 데이터:**")
            all_data = "\n\n".join([
                f"{'='*60}\n🎬 {p['scene_title']} {'[USER MODIFIED]' if p.get('is_user_override') else '[AI GENERATED]'}\n{'='*60}\n\n"
                f"[한글 설명]\n{p['korean_desc']}\n\n"
                f"[Step 1: 장면 묘사]\n{p['step1_scene']}\n\n"
                f"[Step 2: 최종 프롬프트]\n{p['step2_final']}\n\n"
                f"[Midjourney]\n{p['midjourney']}\n\n"
                f"[Motion]\n{p['motion']}"
                for p in final_prompts
            ])
            st.text_area("통합", value=all_data, height=400, label_visibility="collapsed")
        
        # 완료 안내
        st.divider()
        st.success(f"""
        🎉 **모든 장면이 완성되었습니다!**
        
        **생성 정보:**
        - 🎬 방식: **{mode_desc}**
        - ⚓ Visual Anchor: 모든 장면 일관성 유지
        - 🔗 Match Cut: 장면 간 연결점 명시
        - ✏️ 사용자 수정: {user_modified_count}/{len(scenes)} 컷
        - 🧑 --cref: {'✅' if char_url else '❌'}
        - 🎨 --sref: {'✅' if style_url else '❌'}
        
        **다음 단계:**
        1. 📸 **Midjourney 프롬프트** 복사 → Discord에서 이미지 생성
        2. 📹 **스톡 영상** 다운로드 (추천 키워드 사용)
        3. 🎬 **Kling/Runway**에 이미지 업로드 + Motion 프롬프트 적용
        4. ✂️ **영상 편집** (Match Cut으로 끊김없이 연결)
        5. 🎵 **음악 합성** (Suno/Udio 가사)
        6. 🚀 **유튜브 업로드**
        
        💡 **무료 스톡 영상:**
        - Pexels: https://www.pexels.com/videos/
        - Pixabay: https://pixabay.com/videos/
        - Videvo: https://www.videvo.net/
        """)
    
    else:
        st.markdown("---")
        st.markdown("""
        ### 🚀 시작하기
        
        1. **장면 생성 방식 선택** (20+A/B or 40개)
        2. **가사 입력** (Tab 1에서 자동 불러오기)
        3. **Visual Anchor 설정**
           - 🤖 **'AI 추천' 버튼** 클릭 (가사 기반 자동 생성)
           - ✍️ **직접 입력** (원하는 주인공 외형)
        4. **URL 입력** (캐릭터 참조 + 스타일 참조)
        5. **스타일 선택** (이미지 미리보기 확인)
        6. **생성 버튼 클릭**
        7. **필요시 각 장면 수동 수정**
        
        > 💡 대서사시 연계 엔진으로 3~4분 영상을 완벽히 채웁니다!
        """)
