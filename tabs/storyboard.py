"""
tabs/storyboard.py - 스토리보드 생성 탭 (Tab 3)
한글 UI 매핑 + 이미지 일관성 강제 프롬프트 조립 + 한글 설명 표시
"""

import streamlit as st
from utils import get_gpt_response


# ============ 한글-영어 매핑 딕셔너리 ============

ART_STYLE_MAP = {
    "지브리 스타일 (따뜻하고 섬세한)": "Studio Ghibli style, warm colors, soft lighting, hand-painted aesthetic",
    "일본 애니메이션 (선명하고 역동적)": "Japanese anime style, vibrant colors, dynamic, cel-shaded",
    "픽사/디즈니 3D (귀엽고 생동감)": "Pixar Disney 3D animation style, expressive, detailed, vibrant",
    "실사 영화 (사실적이고 시네마틱)": "Photorealistic, cinematic lighting, high detail, movie still",
    "사이버펑크 (네온, 미래적)": "Cyberpunk illustration, neon lights, futuristic, high contrast",
    "한국 웹툰 (깔끔하고 감성적)": "Korean webtoon style, clean lines, emotional, soft shading",
    "수채화 (부드럽고 몽환적)": "Watercolor illustration, soft edges, dreamy atmosphere, artistic",
    "다크 판타지 (어둡고 신비로운)": "Dark fantasy style, dramatic lighting, mysterious, gothic",
    "90년대 레트로 애니 (복고풍 감성)": "Retro 90s anime style, nostalgic, cel shading, vibrant colors"
}

VIDEO_MOOD_MAP = {
    "시네마틱 감성 (영화 같은)": "Cinematic and emotional",
    "몽환적/꿈같은": "Dreamy and ethereal",
    "역동적/에너지 넘치는": "Energetic and dynamic",
    "멜랑콜리/잔잔한": "Melancholic and slow",
    "미스터리/어두운": "Mysterious and dark",
    "밝고 희망찬": "Bright and hopeful",
    "향수/따뜻한": "Nostalgic and warm"
}

# 한글 옵션 리스트 (UI 표시용)
ART_STYLE_OPTIONS = list(ART_STYLE_MAP.keys())
VIDEO_MOOD_OPTIONS = list(VIDEO_MOOD_MAP.keys())


SYSTEM_ROLE = """당신은 세계적인 뮤직비디오 연출가(Director)입니다.

## 당신의 핵심 임무
가사의 기승전결을 분석하여 10개의 영화적 장면(Scene)을 구성하고,
각 장면에 대해 **[한글 설명]**, **[이미지 묘사]**, **[카메라/움직임 지시]**를 작성합니다.

## 출력 형식 (매우 중요! 반드시 준수!)

### 구분자 규칙:
- **장면과 장면 사이**: `|||` (파이프 3개)로 구분
- **한글 설명과 이미지 묘사 사이**: `###` (샵 3개)로 구분
- **이미지 묘사와 모션 묘사 사이**: `@@@` (골뱅이 3개)로 구분

### 출력 예시:
빗속에서 슬픈 표정으로 서 있는 소녀 ### A melancholic girl standing in rain, emotional expression, wet streets @@@ Slow zoom in, rain falling ||| 하늘을 올려다보며 희망을 품는 모습 ### She looks up at sky, hope in eyes @@@ Camera pans upward ||| ...

### 한글 설명 작성 규칙:
1. 해당 장면의 핵심 내용을 한 문장으로 요약
2. 사용자가 장면을 쉽게 이해할 수 있도록 구체적으로
3. 20-30자 내외로 간결하게
4. 가사의 감정과 스토리를 반영

### 이미지 묘사 작성 규칙:
1. 캐릭터의 포즈, 표정, 위치를 구체적으로
2. 배경과 환경을 상세히 묘사
3. 조명, 색감, 분위기를 포함
4. **영어로 작성** (Midjourney 최적화)
5. **아트 스타일은 포함하지 마세요** (시스템이 자동으로 추가합니다)

### 모션 묘사 작성 규칙:
1. 카메라 움직임 (zoom in/out, pan, tilt, dolly)
2. 피사체의 동작 (walking, turning, reaching out)
3. 환경 효과 (rain falling, wind blowing)
4. **영어로 작성** (Kling/Runway 최적화)

### 10개 장면 구성:
- Scene 1-2: 도입부 (Intro)
- Scene 3-4: 전개 (Verse)
- Scene 5-6: 고조 (Chorus)
- Scene 7-8: 클라이맥스 (Bridge)
- Scene 9-10: 마무리 (Outro)

## 절대 규칙
1. 정확히 10개의 장면을 생성
2. 각 장면은 `|||`로 구분
3. 한글설명, 이미지, 모션은 각각 `###`, `@@@`로 구분
4. 가사의 실제 내용과 감정을 반영
5. 모든 이미지/모션 묘사는 **영어**로
6. **아트 스타일/화풍은 묘사에 포함하지 말 것!**"""


def parse_scenes(gpt_response: str) -> list:
    """GPT 응답을 파싱하여 장면 리스트를 반환합니다."""
    scenes = []
    raw_scenes = gpt_response.split("|||")
    
    for raw_scene in raw_scenes:
        raw_scene = raw_scene.strip()
        if not raw_scene:
            continue
        
        korean_desc = ""
        image_prompt = ""
        motion_prompt = ""
        
        # 한글 설명과 나머지 분리
        if "###" in raw_scene:
            parts = raw_scene.split("###")
            korean_desc = parts[0].strip()
            remaining = parts[1].strip() if len(parts) > 1 else ""
        else:
            remaining = raw_scene
            korean_desc = "장면 설명"
        
        # 이미지와 모션 분리
        if "@@@" in remaining:
            parts = remaining.split("@@@")
            image_prompt = parts[0].strip()
            motion_prompt = parts[1].strip() if len(parts) > 1 else ""
        else:
            image_prompt = remaining
            motion_prompt = ""
        
        if not motion_prompt:
            motion_prompt = "Cinematic slow motion, gentle camera movement, atmospheric lighting"
        
        scenes.append({
            "korean_desc": korean_desc,
            "image_prompt": image_prompt,
            "motion_prompt": motion_prompt
        })
    
    return scenes


def render(client):
    """스토리보드 탭을 렌더링합니다."""
    
    st.header("🎬 Step 3: 스토리보드 & 프롬프트 생성")
    st.markdown("""
    가사를 분석하여 **10개 장면**의 프롬프트를 생성합니다.
    
    > 🎥 *"Midjourney 이미지 프롬프트 + Kling/Runway 모션 프롬프트를 한 번에!"*
    """)
    
    st.success("""
    ✨ **이 탭에서 생성되는 것들:**
    1. **🖼️ Midjourney 프롬프트** - `--cref`로 캐릭터 일관성 유지
    2. **🎥 Motion 프롬프트** - Kling, Runway, Pika용
    3. **📖 한글 장면 설명** - 각 장면의 내용을 쉽게 파악
    """)
    
    st.divider()
    
    # ============ 입력 영역 ============
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 가사 입력")
        default_lyrics = st.session_state.get("lyrics", "")
        
        lyrics_input = st.text_area(
            "뮤직비디오에 사용할 가사",
            value=default_lyrics,
            height=300,
            placeholder="[Verse 1]\n여기에 가사를 입력하세요...",
            help="가사를 기반으로 10개의 장면이 생성됩니다"
        )
        
        if default_lyrics:
            st.caption("💡 Tab 1에서 생성한 가사가 자동으로 불러와졌습니다.")
    
    with col2:
        st.subheader("🔗 마스터 이미지 URL")
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
            st.warning("⚠️ 마스터 이미지 URL이 없습니다.")
        
        # ============ 아트 스타일 (한글 매핑) ============
        st.subheader("🎨 아트 스타일")
        
        art_style_kr = st.selectbox(
            "일관된 아트 스타일 선택",
            options=ART_STYLE_OPTIONS,
            help="모든 10개 장면에 동일하게 적용됩니다"
        )
        
        # 선택된 영어값 미리보기
        st.caption(f"🔤 영어값: `{ART_STYLE_MAP[art_style_kr][:35]}...`")
        
        # ============ 영상 분위기 (한글 매핑) ============
        st.subheader("🎥 영상 분위기")
        
        video_mood_kr = st.selectbox(
            "전체 영상 톤",
            options=VIDEO_MOOD_OPTIONS
        )
        
        st.caption(f"🔤 영어값: `{VIDEO_MOOD_MAP[video_mood_kr]}`")
    
    st.divider()
    
    # ============ 생성 버튼 ============
    if st.button("🎬 10개 장면 프롬프트 생성", type="primary", use_container_width=True):
        if not lyrics_input.strip():
            st.error("가사를 입력해주세요.")
            return
        if not master_url.strip():
            st.error("마스터 이미지 URL을 입력해주세요. (Tab 2에서 생성)")
            return
        if client is None:
            st.error("API 키가 설정되지 않았습니다.")
            return
        
        # ============ 영어값 변환 (핵심!) ============
        art_style_en = ART_STYLE_MAP[art_style_kr]
        video_mood_en = VIDEO_MOOD_MAP[video_mood_kr]
        
        user_prompt = f"""다음 가사를 분석하여 뮤직비디오용 10개 장면의 프롬프트를 작성해주세요.

## 가사
{lyrics_input}

## 스타일 정보
- 영상 분위기: {video_mood_en}

## ⚠️ 매우 중요한 출력 형식 ⚠️

각 장면은 **반드시** 다음 구조로 작성하세요:
1. 한글 설명 (20-40자) ← 절대 생략 금지!
2. ### (구분자)
3. 영어 이미지 묘사
4. @@@ (구분자)  
5. 영어 모션 묘사

장면 사이는 ||| 로 구분합니다.

## 출력 예시 (반드시 이 형식을 따라주세요!)

어두운 방에서 혼란스러워하는 남자 ### A man standing in a dark room, surrounded by glowing symbols @@@ Slow zoom in, symbols flickering ||| 불타는 동전을 들고 절망하는 모습 ### Hands holding a melting coin in fiery inferno @@@ Camera pulls back ||| ...

⚠️ 주의사항:
- 한글 설명은 **절대 생략하지 마세요**
- 각 장면 앞에 **반드시 한글 설명 + ###** 이 있어야 합니다
- 아트 스타일은 묘사에 포함하지 마세요
- 다른 설명 없이 위 형식으로만 출력하세요

지금 바로 정확히 10개 장면을 위 형식으로 생성해주세요!"""

        with st.spinner("🎬 스토리보드를 기획하고 있습니다... (약 30초~1분)"):
            try:
                result = get_gpt_response(client, SYSTEM_ROLE, user_prompt)
                
                # 세션 스테이트에 저장 (한글/영어 모두)
                st.session_state["storyboard_raw"] = result
                st.session_state["storyboard_url"] = master_url
                st.session_state["storyboard_style"] = art_style_en  # 영어값
                st.session_state["storyboard_style_kr"] = art_style_kr  # 한글값
                st.session_state["storyboard_video_mood"] = video_mood_en  # 영어값
                st.session_state["storyboard_video_mood_kr"] = video_mood_kr  # 한글값
                
                st.success("🎉 스토리보드가 생성되었습니다!")
                
            except Exception as e:
                st.error(str(e))
                return
    
    # ============ 결과 표시 ============
    st.divider()
    
    if "storyboard_raw" in st.session_state and st.session_state["storyboard_raw"]:
        st.subheader("🎬 생성된 10개 장면")
        
        # 저장된 값 불러오기
        master_url = st.session_state.get("storyboard_url", "")
        art_style_en = st.session_state.get("storyboard_style", "")
        art_style_kr = st.session_state.get("storyboard_style_kr", art_style_en)
        
        # 적용 파라미터 안내
        st.info(f"""
        📌 **적용된 설정 (모든 장면에 동일하게 적용):**
        - 🎨 스타일: **{art_style_kr}**
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
        
        st.caption(f"✅ {len(scenes)}개 장면이 파싱되었습니다.")
        
        # ============ 최종 프롬프트 조립 (이미지 일관성 강제!) ============
        final_prompts = []
        
        for i, scene in enumerate(scenes[:10], 1):
            with st.expander(f"🎬 Scene {i}", expanded=(i <= 3)):
                
                # ★ 한글 설명 먼저 표시 (핵심 수정 사항!)
                if scene.get('korean_desc'):
                    st.info(f"📖 **장면 설명:** {scene['korean_desc']}")
                
                # ★★★ 프롬프트 조립 공식 (핵심!) ★★★
                # 포맷: /imagine prompt: {스타일}, {장면묘사} --cref {URL} --ar 16:9
                midjourney_prompt = f"/imagine prompt: {art_style_en}, {scene['image_prompt']} --cref {master_url} --ar 16:9"
                
                st.markdown("**🖼️ Midjourney 이미지 프롬프트:**")
                st.code(midjourney_prompt, language=None)
                
                st.markdown("**🎥 Motion 프롬프트 (Kling/Runway/Pika용):**")
                st.success(f"🎬 {scene['motion_prompt']}")
                
                final_prompts.append({
                    "scene": i,
                    "korean_desc": scene.get('korean_desc', ''),
                    "midjourney": midjourney_prompt,
                    "motion": scene['motion_prompt'],
                    "image_desc": scene['image_prompt']
                })
        
        # 세션에 최종 프롬프트 저장
        st.session_state["final_prompts"] = final_prompts
        
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
            all_mj_prompts = "\n\n".join([
                f"# Scene {p['scene']}: {p['korean_desc']}\n{p['midjourney']}"
                for p in final_prompts
            ])
            st.text_area("MJ 프롬프트", value=all_mj_prompts, height=400, label_visibility="collapsed")
        
        with tab_motion:
            st.markdown("**Kling/Runway/Pika에 사용할 모션 프롬프트:**")
            all_motion_prompts = "\n\n".join([
                f"# Scene {p['scene']}: {p['korean_desc']}\n{p['motion']}"
                for p in final_prompts
            ])
            st.text_area("Motion 프롬프트", value=all_motion_prompts, height=400, label_visibility="collapsed")
        
        with tab_all:
            st.markdown("**전체 데이터 (한글설명 + 이미지 + 모션):**")
            all_prompts = "\n\n".join([
                f"{'='*50}\n🎬 SCENE {p['scene']}\n{'='*50}\n\n"
                f"[한글 설명]\n{p['korean_desc']}\n\n"
                f"[Midjourney]\n{p['midjourney']}\n\n"
                f"[Motion]\n{p['motion']}"
                for p in final_prompts
            ])
            st.text_area("전체 프롬프트", value=all_prompts, height=400, label_visibility="collapsed")
        
        # 완료 안내
        st.divider()
        st.success("""
        🎉 **모든 준비가 완료되었습니다!**
        
        **다음 단계:**
        1. **Midjourney 프롬프트**를 Discord에서 실행 → 10개 이미지 생성
        2. 생성된 이미지를 **Kling/Runway/Pika**에 업로드
        3. 각 이미지에 해당하는 **Motion 프롬프트** 입력 → 영상 생성
        4. 10개 영상 클립을 편집 소프트웨어에서 조합 → 뮤직비디오 완성! 🎬
        """)
        
        with st.expander("🔍 원본 GPT 응답 확인 (디버깅용)"):
            st.text(st.session_state["storyboard_raw"])
    
    else:
        st.markdown("---")
        st.markdown("""
        ### 🚀 시작하기
        
        1. **가사**를 입력하세요 (Tab 1에서 생성했다면 자동으로 불러옵니다)
        2. **마스터 이미지 URL**을 입력하세요 (Tab 2에서 생성)
        3. **아트 스타일**과 **영상 분위기**를 선택하세요
        4. **생성 버튼**을 클릭하면 10개 장면의 프롬프트가 만들어집니다!
        
        > 💡 모든 장면에 **동일한 아트 스타일**과 **마스터 이미지 URL**이 적용되어 일관성이 유지됩니다!
        """)
