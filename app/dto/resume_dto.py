from pydantic import BaseModel, HttpUrl
from typing import List, Union, Optional, Literal


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
    # type: str
    type: Literal['BASIC'] = "BASIC"
    projectName: str
    projectStartedAt: str  # YYYY-MM-DD 형식
    projectEndedAt: str  # YYYY-MM-DD 형식
    skillSet: str
    roleAndTask: List[str] # BASIC 템플릿에서 사용  
    repoLink: str

class StarDto(BaseModel):
    situation: str
    task: str
    action: str
    result: str
    
class ProjectTitleDto(BaseModel):
    projectTitle: str
    
class RoleAndTaskDto(BaseModel):
    roleAndTask: List[str]
    
class TroubleShootingDto(BaseModel):
    problem: str
    hypothesis: str
    tring: str
    result: str
    
# class Basic(Project):
    # type: str = "BASIC"
    
class StarProject(Project):
    # type: str = "STAR"
    type: Literal['STAR'] = "STAR"
    star: StarDto
    
class GitfolioProject(Project):
    # type: str = "GITFOLIO"
    type: Literal['GITFOLIO'] = "GITFOLIO"
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

class WorkExperience(BaseModel):
    companyName: str
    departmentName: str
    role: str
    workType: str  # FULL_TIME, PART_TIME 등
    employmentStatus: str  # EMPLOYMENT, UNEMPLOYMENT 등
    startedAt: str  # YYYY-MM 형식
    endedAt: Optional[str]  # YYYY-MM 형식 또는 빈 값

class ProjectResponse(BaseModel):
    projectName: str
    projectStartedAt: str  # YYYY.MM 형식
    projectEndedAt: str  # YYYY.MM 형식
    skillSet: str
    projectDescription: str
    repoLink: str
    
class Link(BaseModel):
    linkTitle: str
    linkUrl: str

class Education(BaseModel):
    schoolType: str  # UNIVERSITY_BACHELOR 등
    schoolName: str
    major: str
    graduationStatus: str  # ATTENDING, GRADUATED 등
    startedAt: str  # YYYY-MM 형식
    endedAt: Optional[str]  # YYYY-MM 형식 또는 빈 값

class Certificate(BaseModel):
    certificateName: str
    certificateGrade: str
    certificatedAt: str  # YYYY-MM 형식
    certificateOrganization: str

# 응답 데이터 모델 - 전체 이력서
class ResumeResponseDto(BaseModel):
    template: str
    resumeId: str
    memberId: int
    memberName: str
    avatarUrl: str
    email: str
    position: str
    techStack: List[str]
    aboutMe: str
    tags: Optional[List[str]]  # null 가능
    workExperiences: List[WorkExperience]
    # projects: List[ProjectResponse]
    projects: List[Union[Project, StarProject, GitfolioProject]]
    links: Optional[List[Link]]  # null 가능
    educations: List[Education]
    certificates: List[Certificate]
    
class updateResumeDto(BaseModel):
    template: str
    resumeId: str
    memberId: int
    memberName: str
    avatarUrl: str
    email: str
    position: str
    techStack: List[str]
    aboutMe: str
    tags: Optional[List[str]]  # null 가능
    workExperiences: List[WorkExperience]
    projects: List[Union[Project, StarProject, GitfolioProject]]  # 추가된 필드
    links: Optional[List[Link]]  # null 가능
    educations: List[Education]
    certificates: List[Certificate]
    
class UpdateRequestDto(BaseModel):
    selectedText: str
    requirement: str
    resumeInfo: updateResumeDto