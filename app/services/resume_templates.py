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
    

def star_format(project_summaries, techstack, aboutme, star_summary):
    for project in project_summaries:
        project.projectDescription = star_summary  # STAR 요약 내용을 필드에 할당
    return ResumeResponse(
        projects=project_summaries,
        techStack=techstack,
        aboutMe=aboutme
    )
    
def gitfolio_format(project_summaries, techstack, aboutme, trouble_shooting, role_and_task):
    for project in project_summaries:
        project.roleAndTask = role_and_task  # roleAndTask 필드에 값 할당
        project.troubleShooting = trouble_shooting # troubleshooting 필드에 값 할당
    return ResumeResponse(
        projects=project_summaries,
        techStack=techstack,
        aboutMe=aboutme
    )
    
def generate_resume_response(template, project_summaries, techstack, aboutme, role_and_task=None, trouble_shooting=None, star_summary=None):
    """
    템플릿에 맞는 이력서 응답을 생성
    """
    try:
        print("Generated project summaries:", project_summaries)
        
        # 템플릿에 따라 응답 생성
        if template == "basic":
            return basic_format(project_summaries, techstack, aboutme, role_and_task)

        elif template == "gitfolio":
            return gitfolio_format(project_summaries, techstack, aboutme, trouble_shooting, role_and_task)

        elif template == "star":
            return star_format(project_summaries, techstack, aboutme, star_summary)

        else:
            raise ValueError("Invalid template type provided.")

    except Exception as e:
        print(f"Error generating resume response: {e}")
        return {"error": str(e)}