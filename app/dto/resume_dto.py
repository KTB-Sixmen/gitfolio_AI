from pydantic import BaseModel, HttpUrl
from typing import List, Union
from app.dto.resume_modify_dto import StarDto, TroubleShootingDto


# 요청 데이터 모델
class ResumeRequest(BaseModel):
    githubID: str
    githubName: str
    personalRepo: HttpUrl
    selectedRepo: List[HttpUrl]
    requirements: str
    template: str

# 응답 데이터 모델 - 프로젝트 정보(공통DTO)
class Project(BaseModel):
    projectName: str
    projectStartedAt: str  # YYYY-MM-DD 형식
    projectEndedAt: str  # YYYY-MM-DD 형식
    skillSet: str
    roleAndTask: List[str] # BASIC 템플릿에서 사용  
    repoLink: HttpUrl

class StarProject(Project):
    star: StarDto
class GitfolioProject(Project):
    troubleShooting: TroubleShootingDto

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
    template: str
    techStack: List[str]
    aboutMe: str
    projects: List[Union[Project, StarProject, GitfolioProject]]
