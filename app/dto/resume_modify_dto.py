from pydantic import BaseModel
from typing import List, Optional

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

class ResumeResponseDto(BaseModel):
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
    projects: List[ProjectResponse]
    links: Optional[List[Link]]  # null 가능
    educations: List[Education]
    certificates: List[Certificate]
    
class UpdateRequestDto(BaseModel):
    selectedText: str
    requirement: str
    resumeInfo: ResumeResponseDto
    
class ProjectTitleDto(BaseModel):
    projectTitle: str
    
class RoleAndTaskDto(BaseModel):
    roleAndTask: List[str]
    
class TroubleShootingDto(BaseModel):
    problem: str
    hypothesis: str
    tring: str
    result: str
    
class StarDto(BaseModel):
    situation: str
    task: str
    action: str
    result: str