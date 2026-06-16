from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import random

app = FastAPI(title="Novel Genre & Plot Recommender API")

class UserInput(BaseModel):
    vunwigi: str       
    syoje: str     
    hyang: str     
    speed: int      

@app.get("/")
def read_root():
    return {"message": "Novel Recommendation API is running!"}

@app.post("/recommend")
def get_recommendation(data: UserInput):
    recommended = []
    tip = ""
    
    if data.hyang == "남성향":
        if data.syoje == "회빙환(회귀/빙의/환생)":
            recommended = ["현대 판타지", "재벌물", "대체역사"]
            tip = "사이다 터뜨리는 슈퍼맨이 되어보세요."
        elif data.syoje == "전문가":
            recommended = ["전문가물 (의사/개발자)", "스포츠 판타지"]
            tip = "천재물로 대표되는 전문가 되어보셈."
        else:
            recommended = ["정통 판타지", "퓨전 무협"]
            tip = "조금 진부해도 정석전인 장르속에서 살아봐요."
            
    else: 
        if data.hyang == "회빙환(회귀/빙의/환생)":
            recommended = ["로맨스 판타지", "육아물", "악녀물"]
            tip = "감정서사 극한을 추구해보세요."
        else:
            recommended = ["현대 로맨스", "걸크러시 판타지"]
            tip = "감정서사의 극한을 추구해보세요."

    if data.vunwigi == "무거움" or data.vunwigi == "피폐":
        tip += "꽤 심적 타격 받을 것입니다."
    
    strategy = "주 5회 이상" if data.speed >= 4 else "1-2회 게으른 외국파 작가"

    return {
        "status": "success",
        "recommended": recommended,
        "recommendedstra": strategy,
        "tip": tip,
        "keyword": random.choice(["먼치킨", "TS", "이혼", "착각", "날먹"])
    }
