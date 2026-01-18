"""
tabs/storyboard.py - 스토리보드 생성 탭 (Tab 3)
최종 통합 버전: 이미지 프롬프트 + 영상 모션 프롬프트 동시 생성
"""

import streamlit as st
from utils import get_gpt_response


SYSTEM_ROLE = """당신은 세계적인 뮤직비디오 연출가(Director)입니다.

## 당신의 핵심 임무
가사의 기승전결을 분석하여 10개의 영화적 장면(Scene)을 구성하고,
각 장면에 대해 **[이미지 묘사]**와 **[카메라/움직임 지시]**를 작성합니다.

## 출력 형식 (매우 중요! 반드시 준수!)

### 구분자 규칙:
- **장면과 장면 사이**: `|||` (파이프 3개)로 구분
- **이미지 묘사와 모션 묘사 사이**: `@@@` (골뱅이 3개)로 구분

### 출력 예시:
A melancholic girl with silver hair standing alone in the rain, neon-lit cyberpunk city street, reflections on wet ground, emotional expression, tears mixing with raindrops @@@ Slow cinematic zoom in on her face, rain particles falling in slow motion, neon lights flickering softly, camera gradually getting closer ||| She looks up at the dark sky, hope in her eyes, city lights creating a halo effect around her silhouette, dramatic lighting @@@ Camera slowly pans upward following her gaze, transitioning from her face to the vast night sky, gentle upward movement ||| ...

### 이미지 묘사 작성 규칙:
1. 캐릭터의 포즈, 표정, 위치를 구체적으로
2. 배경과 환경을 상세히 묘사
3. 조명, 색감, 분위기를 포함
4. 영어로 작성 (Midjourney 최적화)
5. 가사의 감정과 내용을 시각적으로 표현

### 모션 묘사 작성 규칙:
1. 카메라 움직임 (zoom in/out, pan, tilt, dolly, tracking)
2. 피사체의 동작 (walking, turning, reaching out)
3. 환경 효과 (rain falling, wind blowing, lights flickering)
4. 속도감 (slow motion, normal speed, time-lapse)
5. 영어로 작성 (Kling/Runway 최적화)

### 10개 장면 구성 가이드:
- Scene 1-2: 도입부 (Intro/설정)
- Scene 3-4: 전개 (Verse 발전)
- Scene 5-6: 고조 (Pre-Chorus/Chorus)
- Scene 7-8: 클라이맥스 (Bridge/절정)
- Scene 9-10: 마무리 (Outro/여운)

## 절대 규칙
1. 정확히 10개의 장면을 생성할 것
2. 각 장면은 반드시 `|||`로 구분할 것
3. 각 장면 내에서 이미지와 모션은 `@@@`로 구분할 것
4. 가사의 실제 내용과 감정을 반영할 것
5. 모든 묘사는 영어로 작성할 것
6. 다른 설명이나 번호 없이 순수 프롬프트만 출력할 것"""


def parse_scenes(gpt_response: str) -> list:
    """
    GPT 응답을 파싱하여 장면 리스트를 반환합니다.
    
    Args:
        gpt_response: GPT 응답 텍스트 (|||와 @@@로 구분됨)
        
    Returns:
        list: [{"image_prompt": str, "motion_prompt": str}, ...]
    """
    scenes = []
    
    # 1단계: |||로 장면 분리
    raw_scenes = gpt_response.split("|||")
    
    for raw_scene in raw_scenes:
        raw_scene = raw_scene.strip()
        
        if not raw_scene:
            continue
        
        # 2단계: @@@로 이미지/모션 분리
        if "@@@" in raw_scene:
            parts = raw_scene.split("@@@")
            image_prompt = parts[0].strip()
            motion_prompt = parts[1].strip() if len(parts) > 1 else ""
        else:
            # @@@가 없으면 전체를 이미지 프롬프트로 사용
            image_prompt = raw_scene
            motion_prompt = ""
        
        # 모션 프롬프트가 비어있으면 기본값 할당
        if not motion_prompt:
            motion_prompt = "Cinematic slow motion, gentle camera movement, atmospheric lighting shifts"
        
        scenes.append({
            "image_prompt": image_prompt,
            "motion_prompt": motion_prompt
        })
    
    return scenes


def render(client):
    """
    스토리보드 탭을 렌더링합니다.
    
    Args:
        client: OpenAI 클라이언트 인스턴스
    """
    st.header("🎬 Step 3: 스토리보드 & 프롬프트 생성")
    st.markdown("""
    가사를 분석하여 **10개 장면**의 프롬프트를 생성합니다.
    
    > 🎥 *"Midjourney 이미지 프롬프트 + Kling/Runway 모션 프롬프트를 한 번에!"*
    """)
    
    # 핵심 기능 안내
    st.success("""
    ✨ **이 탭에서 생성되는 것들:**
    
    1. **🖼️ Midjourney 프롬프트** - `--cref` 파라미터로 캐릭터 일관성 유지
    2. **🎥 Motion 프롬프트** - Kling, Runway, Pika 등 영상 생성 AI용
    """)
    
    st.divider()
    
    # 입력 영역
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 가사 입력")
        
        # Tab 1에서 저장된 가사 불러오기
        default_lyrics = st.session_state.get("lyrics", "")
        
        lyrics_input = st.text_area(
            "뮤직비디오에 사용할 가사",
            value=default_lyrics,
            height=300,
            placeholder="""[Verse 1]
여기에 가사를 입력하세요...

[Chorus]
후렴구 가사...

Tab 1에서 생성한 가사를 붙여넣거나 직접 입력하세요.""",
            help="가사를 기반으로 10개의 장면이 생성됩니다"
        )
        
        if default_lyrics:
            st.caption("💡 Tab 1에서 생성한 가사가 자동으로 불러와졌습니다.")
    
    with col2:
        st.subheader("🔗 마스터 이미지 URL")
        
        # Tab 2에서 저장된 URL 불러오기
        default_url = st.session_state.get("master_image_url", "")
        
        master_url = st.text_input(
            "캐릭터 참조용 이미지 URL",
            value=default_url,
            placeholder="https://cdn.midjourney.com/...",
            help="Tab 2에서 Midjourney로 생성한 캐릭터 이미지 URL"
        )
        
        if default_url:
            st.caption("💡 Tab 2에서 저장한 URL이 불러와졌습니다.")
        else:
            st.warning("⚠️ 마스터 이미지 URL이 없습니다. Tab 2에서 먼저 생성해주세요.")
        
        # 아트 스타일
        st.subheader("🎨 아트 스타일")
        
        default_style = st.session_state.get("character_style", "")
        
        art_style = st.selectbox(
            "일관된 아트 스타일 선택",
            options=[
                "Studio Ghibli style, warm colors, soft lighting",
                "Japanese anime style, vibrant colors, dynamic",
                "Cyberpunk illustration, neon lights, futuristic",
                "Pixar 3D animation style, expressive, detailed",
                "Korean webtoon style, clean lines, emotional",
                "Watercolor illustration, soft, dreamy",
                "Dark fantasy style, dramatic lighting, mysterious",
                "Photorealistic, cinematic, high detail",
                "Retro 90s anime style, nostalgic, vibrant"
            ],
            index=0
        )
        
        # 영상 분위기
        st.subheader("🎥 영상 분위기")
        
        video_mood = st.selectbox(
            "전체 영상 톤",
            options=[
                "Cinematic and emotional",
                "Dreamy and ethereal",
                "Energetic and dynamic",
                "Melancholic and slow",
                "Mysterious and dark",
                "Bright and hopeful",
                "Nostalgic and warm"
            ]
        )
    
    st.divider()
    
    # 생성 버튼
    if st.button("🎬 10개 장면 프롬프트 생성", type="primary", use_container_width=True):
        # 유효성 검사
        if not lyrics_input.strip():
            st.error("가사를 입력해주세요.")
            return
        
        if not master_url.strip():
            st.error("마스터 이미지 URL을 입력해주세요. (Tab 2에서 생성)")
            return
        
        if client is None:
            st.error("API 키가 설정되지 않았습니다. secrets.toml 파일을 확인해주세요.")
            return
        
        # 프롬프트 구성
        user_prompt = f"""다음 가사를 분석하여 뮤직비디오용 10개 장면의 프롬프트를 작성해주세요.

## 가사
{lyrics_input}

## 스타일 정보
- 아트 스타일: {art_style}
- 영상 분위기: {video_mood}

## 출력 규칙 (반드시 준수!)
1. 정확히 10개의 장면을 생성하세요.
2. 장면과 장면 사이는 `|||`로 구분하세요.
3. 각 장면 내에서 이미지 묘사와 모션 묘사는 `@@@`로 구분하세요.
4. 가사의 실제 내용, 감정, 스토리를 반영하여 시각화하세요.
5. 설명 없이 프롬프트만 출력하세요.

## 출력 형식
[이미지묘사1] @@@ [모션묘사1] ||| [이미지묘사2] @@@ [모션묘사2] ||| ... (10개)

지금 바로 10개 장면의 프롬프트를 생성하세요!"""

        with st.spinner("🎬 스토리보드를 기획하고 있습니다... (약 30초~1분 소요)"):
            try:
                result = get_gpt_response(client, SYSTEM_ROLE, user_prompt)
                
                # 세션 스테이트에 저장
                st.session_state["storyboard_raw"] = result
                st.session_state["storyboard_url"] = master_url
                st.session_state["storyboard_style"] = art_style
                st.session_state["storyboard_video_mood"] = video_mood
                
                st.success("🎉 스토리보드가 생성되었습니다!")
                
            except Exception as e:
                st.error(str(e))
                return
    
    # 결과 표시
    st.divider()
    
    if "storyboard_raw" in st.session_state and st.session_state["storyboard_raw"]:
        st.subheader("🎬 생성된 10개 장면")
        
        master_url = st.session_state.get("storyboard_url", "")
        art_style = st.session_state.get("storyboard_style", "")
        
        # 적용 파라미터 안내
        st.info(f"""
        📌 **적용된 설정:**
        - 🎨 스타일: `{art_style[:30]}...`
        - 🔗 캐릭터 참조: `--cref {master_url[:40]}...`
        - 📐 화면 비율: `--ar 16:9`
        """)
        
        # GPT 결과 파싱
        scenes = parse_scenes(st.session_state["storyboard_raw"])
        
        if len(scenes) == 0:
            st.error("장면 파싱에 실패했습니다. 다시 생성해주세요.")
            with st.expander("🔍 원본 데이터 확인"):
                st.text(st.session_state["storyboard_raw"])
            return
        
        # 파싱된 장면 수 표시
        st.caption(f"✅ {len(scenes)}개 장면이 파싱되었습니다.")
        
        # 최종 프롬프트 저장용 리스트
        final_prompts = []
        
        # 각 장면 렌더링
        for i, scene in enumerate(scenes[:10], 1):
            with st.expander(f"🎬 Scene {i}", expanded=(i <= 3)):
                
                # Midjourney 프롬프트 구성
                midjourney_prompt = f"/imagine prompt: {art_style}, {scene['image_prompt']} --cref {master_url} --ar 16:9"
                
                # 이미지 프롬프트 섹션
                st.markdown("**🖼️ Midjourney 이미지 프롬프트:**")
                st.code(midjourney_prompt, language=None)
                
                # 모션 프롬프트 섹션
                st.markdown("**🎥 Motion 프롬프트 (Kling/Runway/Pika용):**")
                st.success(f"🎬 {scene['motion_prompt']}")
                
                # 최종 프롬프트 리스트에 추가
                final_prompts.append({
                    "scene": i,
                    "midjourney": midjourney_prompt,
                    "motion": scene['motion_prompt'],
                    "image_desc": scene['image_prompt']
                })
        
        # 세션에 최종 프롬프트 저장
        st.session_state["final_prompts"] = final_prompts
        
        st.divider()
        
        # 전체 프롬프트 복사 섹션
        st.subheader("📋 전체 프롬프트 (복사용)")
        
        tab_mj, tab_motion, tab_all = st.tabs([
            "🖼️ Midjourney 전체", 
            "🎥 Motion 전체", 
            "📄 통합 전체"
        ])
        
        with tab_mj:
            st.markdown("**Midjourney Discord에 순서대로 붙여넣기:**")
            all_mj_prompts = "\n\n".join([
                f"# Scene {p['scene']}\n{p['midjourney']}"
                for p in final_prompts
            ])
            st.text_area(
                "Midjourney 프롬프트 전체",
                value=all_mj_prompts,
                height=400,
                label_visibility="collapsed"
            )
        
        with tab_motion:
            st.markdown("**Kling/Runway/Pika에 사용할 모션 프롬프트:**")
            all_motion_prompts = "\n\n".join([
                f"# Scene {p['scene']}\n{p['motion']}"
                for p in final_prompts
            ])
            st.text_area(
                "Motion 프롬프트 전체",
                value=all_motion_prompts,
                height=400,
                label_visibility="collapsed"
            )
        
        with tab_all:
            st.markdown("**전체 데이터 (이미지 + 모션):**")
            all_prompts = "\n\n".join([
                f"{'='*50}\n🎬 SCENE {p['scene']}\n{'='*50}\n\n"
                f"[Midjourney]\n{p['midjourney']}\n\n"
                f"[Motion]\n{p['motion']}"
                for p in final_prompts
            ])
            st.text_area(
                "전체 프롬프트",
                value=all_prompts,
                height=400,
                label_visibility="collapsed"
            )
        
        # 완료 안내
        st.divider()
        st.success("""
        🎉 **모든 준비가 완료되었습니다!**
        
        **다음 단계:**
        1. **Midjourney 프롬프트**를 Discord에서 실행하여 10개 이미지 생성
        2. 생성된 이미지를 **Kling/Runway/Pika**에 업로드
        3. 각 이미지에 해당하는 **Motion 프롬프트**를 입력하여 영상 생성
        4. 10개 영상 클립을 편집 소프트웨어에서 조합하면 뮤직비디오 완성! 🎬
        """)
        
        # 원본 데이터 확인 (디버깅용)
        with st.expander("🔍 원본 GPT 응답 확인 (디버깅용)"):
            st.text(st.session_state["storyboard_raw"])
    
    # 아직 결과가 없을 때 가이드 표시
    else:
        st.markdown("---")
        st.markdown("""
        ### 🚀 시작하기
        
        1. **가사**를 입력하세요 (Tab 1에서 생성했다면 자동으로 불러옵니다)
        2. **마스터 이미지 URL**을 입력하세요 (Tab 2에서 생성)
        3. **아트 스타일**과 **영상 분위기**를 선택하세요
        4. **생성 버튼**을 클릭하면 10개 장면의 프롬프트가 만들어집니다!
        
        > 💡 각 장면마다 **Midjourney 이미지 프롬프트**와 **Motion 프롬프트**가 함께 생성됩니다.
        """)