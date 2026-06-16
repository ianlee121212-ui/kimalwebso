import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
st.set_page_config(page_title="Websosal plannerr", layout="centered")

st.title("장르 및 플롯 추천 시스템")
st.write("집필 성향과 선호 키워드 기반으로 추천합니다.")
st.markdown("***")

col1, col2 = st.columns(2)

with col1:
    target_audience = st.radio("타겟층 선택", ["남성향", "여성향"])
    main_trope = st.selectbox(
        "웹소설 뼈대 소재", 
        ["회빙환(회귀/빙의/환생)", "전문가", "성장물"]
    )

with col2:
    preferred_tone = st.select_slider(
        "선호하는 분위기",
        options=["가벼움", "무거움", "피폐"]
    )
    writing_speed = st.slider("연재 분량 편", 1, 7, 3)

if st.button("연재 가이드"):
    payload = {
        "vunwigi": preferred_tone,
        "syoje": main_trope,
        "hyang": target_audience,
        "speed": writing_speed
    }
    
    try:
        with st.spinner("분석 중입니다..."):
            response = requests.post(f"{BACKEND_URL}/recommend", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                st.success("결과 계산 완료")
                
                st.subheader("카테고리")
                st.info(", ".join(result["recommended"]))
                
                st.subheader("팁")
                st.write(result["tip"])
                
                st.subheader("전략")
                st.warning(result["recommendedstra"])
                
                st.metric(label="요즘 유행하는 웹소설 키워드 랜덤", value=result["keyword"])
            else:
                st.error(f"서버 오류가 발생했습니다. (코드: {response.status_code})")
                
    except requests.exceptions.ConnectionError:
        st.error("서버에 연결할 수 없습니다.")
