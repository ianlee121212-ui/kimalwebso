import streamlit as st
import requests
import os

# FastAPI 백엔드 URL 설정 (Docker-compose 환경 및 로컬 환경 호환성 고려)
# EC2 배포 시에는 docker-compose 내부 네트워크 이름(http://backend:8000)을 사용하게 됩니다.
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Webnovel Planner", page_icon="✍️", layout="centered")

st.title("✍️ 웹소설 작가를 위한 장르 및 플롯 맞춤 추천 시스템")
st.write("당신의 집필 성향과 선호하는 키워드를 기반으로 최적의 웹소설 웹 패스를 추천합니다.")
st.markdown("---")

# 1. 사용자 입력 컴포넌트 구성 (차별화된 UI 레이아웃)
col1, col2 = st.columns(2)

with col1:
    target_audience = st.radio("🎯 타겟 독자층 선택", ["남성향", "여성향"])
    main_trope = list_box = st.selectbox(
        "🔑 핵심 웹소설 트로프(Trope)", 
        ["회빙환(회귀/빙의/환생)", "전문가", "성장물"]
    )

with col2:
    preferred_tone = st.select_slider(
        "🎭 선호하는 작품 분위기/톤",
        options=["가벼움", "무거움", "피폐"]
    )
    writing_speed = st.slider("📅 주당 연재 가능한 분량 (편)", 1, 7, 3)

# 2. 추천 요청 버튼 및 통신
if st.button("🔥 내 맞춤형 연재 가이드 가져오기"):
    # FastAPI에 전달할 페이로드 데이터
    payload = {
        "preferred_tone": preferred_tone,
        "main_trope": main_trope,
        "target_audience": target_audience,
        "writing_speed": writing_speed
    }
    
    try:
        with st.spinner("FastAPI 백엔드 엔진에서 추천 결과를 분석 중입니다..."):
            # FastAPI의 /recommend 엔드포인트 호출
            response = requests.post(f"{BACKEND_URL}/recommend", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                # 3. FastAPI의 응답 결과를 받아 화면에 예쁘게 표시
                st.success("✅ 추천 결과가 생성되었습니다!")
                
                st.subheader("📚 추천 장르 카테고리")
                st.info(", ".join(result["recommended_genres"]))
                
                st.subheader("💡 플롯 빌딩 핵심 팁")
                st.write(result["plot_tip"])
                
                st.subheader("🚀 연재 및 집필 전략")
                st.warning(result["recommended_strategy"])
                
                st.metric(label="🍀 오늘 작가님께 추천하는 웹소설 행운의 키워드", value=result["lucky_keyword"])
            else:
                st.error(f"백엔드 서버 오류가 발생했습니다. (코드: {response.status_code})")
                
    except requests.exceptions.ConnectionError:
        st.error("⚠️ FastAPI 백엔드 서버에 연결할 수 없습니다. Docker 컨테이너 상태를 확인하세요.")
