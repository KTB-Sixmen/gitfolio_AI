from pydantic import BaseModel, HttpUrl
from typing import List, Optional

# 요청 데이터 모델
class ResumeRequest(BaseModel):
    githubID: str
    githubName: str
    personalRepo: HttpUrl
    selectedRepo: List[HttpUrl]
    requirements: str
    template: str

# 응답 데이터 모델 - 프로젝트 정보
class Project(BaseModel):
    projectName: str
    projectStartedAt: str  # YYYY-MM-DD 형식
    projectEndedAt: str  # YYYY-MM-DD 형식
    skillSet: str
    repoLink: HttpUrl
    # 선택적 필드
    projectDescription: Optional[str] = None # 자율 생성 템플릿
    roleAndTask: Optional[List[str]] = None  # BASIC 템플릿에서 사용   
    troubleShooting: Optional[str] = None   # STAR 템플릿에서 사용

# gpt 프로젝트 요약문, json형태
class GptProject(BaseModel):
    projectName: str
    skillSet: str
    projectDescription: str

# aboutme, techstack, json형태
class GptAboutmeTechstack(BaseModel):
    techStack: List[str]
    aboutMe: str

# 응답 데이터 모델 - 전체 이력서
class ResumeResponse(BaseModel):
    projects: List[Project]
    techStack: List[str]
    aboutMe: str
