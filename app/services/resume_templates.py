from app.config.settings import settings
from app.dto.resume_dto import ResumeResponse, Project
from app.services.gpt_service import generate_role_and_task, generate_aboutme
from app.services.stack_service import generate_techstack

def basic_format(project_summaries, techstack, aboutme, role_and_task):
    for project in project_summaries:
        project.roleAndTask = role_and_task # roleAndTask 필드에 값 할당
    return ResumeResponse(
        projects=project_summaries,
        techStack=techstack,
        aboutMe=aboutme
    )
    
# def star_format():
    
def gitfolio_format(project_summaries, techstack, aboutme, trouble_shooting, role_and_task):
    for project in project_summaries:
        project.roleAndTask = role_and_task  # roleAndTask 필드에 값 할당
        project.troubleShooting = trouble_shooting # troubleshooting 필드에 값 할당
    return ResumeResponse(
        projects=project_summaries,
        techStack=techstack,
        aboutMe=aboutme
    )