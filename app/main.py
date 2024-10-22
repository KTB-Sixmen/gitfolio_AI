from fastapi import FastAPI
from app.api.v1 import routes
from app.dto.resume_dto import ResumeRequest, ResumeResponse 

app = FastAPI()

app.include_router(routes.router)

#testing
@app.get("/")
def read_root():
    return {"message": "Resume AI Service"}

# /api/resumes 엔드포인트 정의
@app.post("/api/resumes", response_model=ResumeResponse)
async def generate_resume(request: ResumeRequest):
    # 요청 데이터를 출력
    print(f"GitHub ID: {request.githubID}")
    print(f"Personal Repo: {request.personalRepo}")
    print(f"Selected Repos: {request.selectedRepo}")
    print(f"Requirements: {request.requirements}")

    # 더미 데이터로 응답
    dummy_data = {
        "projects": [
            {
                "projectName": "DREAM, 생성형AI 스토리",
                "projectStartedAt": "2024-09",
                "projectEndedAt": "2024-09",
                "skillSet": "RAG, Langchain, GPT4, DALL.E",
                "projectDescription": "<p><strong>메시징 시스템 통계 조회 API 성능 개선 (4.75s -> 41ms)</strong></p><p>의사의 회진 일정을 환자에게 메시지로 전송하는 시스템의 통계 서비스 API의 성능을 개선했습니다.</p><p>한 달간의 통계를 조회할 때 약 5초가 소요되던 API의 병목 지점을 찾아내고 수정하여 50ms 이하의 속도로 개선했습니다.</p>",
                "repoLink": "https://github.com/ilmin/gen-ai-dream"
            },
            {
                "projectName": "추천 시스템 개발",
                "projectStartedAt": "2024-07",
                "projectEndedAt": "2024-08",
                "skillSet": "KcELENTRA, BiLSTM, HDBSCAN",
                "projectDescription": "<p><strong>식당 리뷰 기반 추천 시스템 개발</strong></p><p>HDBSCAN과 ONNX를 활용하여 리뷰 데이터를 기반으로 한 식당 추천 시스템을 구축했습니다.</p><p>KcELECTRA와 BiLSTM 앙상블 모델을 통해 응답 속도를 222초에서 26초로 개선했습니다.</p>",
                "repoLink": "https://github.com/ilmin/recommendation-system"
            }
        ],
        "techStack": ["Kotlin", "Java", "Python", "ONNX"],
        "aboutMe": "안녕하세요! ’Comfort-Zone에서 벗어나 끊임없이 도전을 하는 개발자’ 조일민입니다.\n- Self-Motivation: 어떤 일이든 관심이 생기면 망설임 없이 도전하여 실행에 옮깁니다.\n- Optimization-Driven: 코드 한 줄까지도 성능 최적화에 집중하여 시스템의 효율성과 비즈니스 가치를 극대화합니다.\n- Collaborative Growth: 개인적인 성장을 넘어서, 함께 공유하며 발전하는 문화를 추구합니다."
    }

    return dummy_data