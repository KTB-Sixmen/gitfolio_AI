from pydantic import BaseModel, HttpUrl
from typing import List

# 요청 데이터 모델
class ResumeRequest(BaseModel):
    githubID: str
    personalRepo: HttpUrl
    selectedRepo: List[HttpUrl]
    requirements: str

# 응답 데이터 모델 - 프로젝트 정보
class Project(BaseModel):
    projectName: str
    projectStartedAt: str  # YYYY-MM 형식
    projectEndedAt: str  # YYYY-MM 형식
    skillSet: str
    projectDescription: str
    repoLink: HttpUrl

# 응답 데이터 모델 - 전체 이력서
class ResumeResponse(BaseModel):
    projects: List[Project]
    techStack: List[str]
    aboutMe: str
