from app.config.settings import settings
from app.dto.resume_dto import ResumeResponse, Project

def basic_format(project_summaries, techstack, aboutme, role_and_task):
    for project in project_summaries:
        project.roleAndTask = role_and_task # roleAndTask 필드에 값 할당
    return ResumeResponse(
        projects=project_summaries,
        techStack=techstack,
        aboutMe=aboutme
    )
    
# def star_format():
    
# def gitfolio_format():