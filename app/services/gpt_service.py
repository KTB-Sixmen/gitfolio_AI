from openai import OpenAI
from app.config.settings import settings
from app.dto.resume_dto import GptProject
from app.dto.resume_modify_dto import ResumeResponseDto, ProjectTitleDto, RoleAndTaskDto
from app.services.github_service import get_github_profile_and_repos, project_title_candidate
import tiktoken 
import json
import os
import pprint

# GPT를 사용한 요약 함수
def summarize_text(text, openai_api_key, requirements, max_output_tokens, prompt):
    try:
        if not text.strip():  # 텍스트가 비어 있는 경우 처리
            print("No text provided for summarization. Skipping...")
            return ""

        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model=settings.gpt_model,
            messages=[
                {"role": "system", "content": "You are a senior developer who wrote the code I provided. Summarize the project by extracting key points from the code and text, and present meaningful information in a concise way, in Korean."},
                {"role": "user", "content": f"{text}"},
                {"role": "assistant", "content": f"{prompt}, focus on {requirements}"}
            ],
            max_tokens=max_output_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error during summarization: {e}")
        return ""

# 코드 텍스트를 토큰 단위로 슬라이싱하여 GPT에 요약 요청
def slice_and_summarize(all_code, openai_api_key, requirements, max_output_tokens=settings.max_output_tokens, token_limit=settings.max_content_tokens, prompt=settings.code_summary_prompt):
    try:
        if not all_code.strip():  # 텍스트가 없으면 스킵
            print("No code provided for summarization. Skipping...")
            return ""

        summaries = []
        print("Summarizing the full content...")
        enc = tiktoken.encoding_for_model(settings.gpt_model)  # 토큰화 엔코더 생성
        tokens = enc.encode(all_code)

        for i in range(0, len(tokens), token_limit):
            part_tokens = tokens[i:i + token_limit]
            part_text = enc.decode(part_tokens)
            print(f"Summarizing part from token {i} to {i + token_limit}")
            summary = summarize_text(part_text, openai_api_key, requirements, max_output_tokens, prompt)
            summaries.append(summary)

        return "\n\n".join(summaries)
    except Exception as e:
        print(f"Error during slicing and summarizing: {e}")
        return ""

# 최종 요약: 길이가 여전히 길면 반복적으로 최종 요약
def final_summarization(summary_text, openai_api_key, requirements, max_output_tokens=settings.max_output_tokens, prompt=settings.final_summary_prompt):
    try:
        if not summary_text.strip():  # 텍스트가 없으면 스킵
            print("No text provided for final summarization. Skipping...")
            return ""    

        enc = tiktoken.encoding_for_model(settings.gpt_model)
        tokens = enc.encode(summary_text)

        while len(tokens) > max_output_tokens:
            print(f"Final summarization is too long ({len(tokens)} tokens), re-summarizing...")
            summary_text = summarize_text(summary_text, openai_api_key, requirements, max_output_tokens, prompt)
            tokens = enc.encode(summary_text)
        
        return summary_text
    except Exception as e:
        print(f"Error during final summarization: {e}")
        return ""

# 최종 프로젝트 요약을 생성하는 새로운 함수
def generate_project_summary(code_summary, pr_summary, commit_summary, openai_api_key, requirements, prompt=settings.final_project_prompt) -> GptProject:
    try:
        # 요약 요청
        print("Generating final project summary...")
        if not code_summary.strip() and not pr_summary.strip() and not commit_summary.strip():  # 텍스트가 비어 있는 경우 처리
            print("No text provided for summarization. Skipping...")
            return ""

        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model=settings.gpt_model,
            messages=[
                {"role": "system", "content": "As a senior developer, review the provided project summaries and detail the project overview, the specific parts you worked on (organized by main features), including encountered issues, solutions applied, and the results achieved. Summarize in Korean, using concise phrases rather than full sentences for clarity."},
                {"role": "user",
                        "content": (
                            f"Summarize the project's overview using `{code_summary}`, noting its direction, encountered issues, solutions, and results. "
                            f"Then, use `{pr_summary}` to describe how these issues were addressed and the development process. "
                            f"Finally, refer to `{commit_summary}` to review the user's code contributions, summarizing how they resolved problems and the outcomes achieved. "
                            "Highlight the parts personally implemented by the user.")},
                {"role": "assistant", "content": f"{prompt}, focus on {requirements}"}
            ],
            max_tokens=settings.max_output_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error during summarization: {e}")
        return ""
    
# 최종 프로젝트 요약을 생성하는 새로운 함수 _ JSON 형태로 리턴
def generate_project_summary_byJson(code_summary, pr_summary, commit_summary, openai_api_key, requirements, prompt=settings.final_project_prompt) -> GptProject:
    try:
        # 요약 요청
        print("Generating final project summary...")
        if not code_summary.strip() and not pr_summary.strip() and not commit_summary.strip():  # 텍스트가 비어 있는 경우 처리
            print("No text provided for summarization. Skipping...")
            return GptProject(projectName="", skillSet="", projectDescription="")

        # beta, parse형태로 구성됨. 주기적으로 공식문서 업데이트 확인할것
        client = OpenAI(api_key=openai_api_key)
        response = client.beta.chat.completions.parse(
            model=settings.gpt_model,
            messages=[
                {"role": "system", "content": "As a senior developer, review the provided project summaries and detail the project overview, the specific parts you worked on (organized by main features), including encountered issues, solutions applied, and the results achieved. Summarize in Korean, using concise phrases rather than full sentences for clarity."},
                {"role": "user",
                        "content": (
                            f"Summarize the project's overview using `{code_summary}`, noting its direction, encountered issues, solutions, and results. "
                            f"Then, use `{pr_summary}` to describe how these issues were addressed and the development process. "
                            f"Finally, refer to `{commit_summary}` to review the user's code contributions, summarizing how they resolved problems and the outcomes achieved. "
                            "Highlight the parts personally implemented by the user.")},
                {"role": "assistant", "content": f"{prompt}, focus on {requirements}"}
            ],
            max_tokens=settings.max_output_tokens,
            response_format=GptProject,
        )

        # GPT 응답 파싱
        response_text = response.choices[0].message.parsed

        # GptProject 객체로 반환
        return response_text

    except Exception as e:
        print(f"Error during summarization: {e}")
        return GptProject(projectName="", skillSet="", projectDescription="")
    
# 최종 요약된 부분, 더 간략화 시키기 및 Json형태 포맷으로 정리
def simplify_project_summary_byJson(summary_text, openai_api_key, requirements, prompt=settings.simplify_project_prompt):
    try:
        if not summary_text.strip():  # 텍스트가 비어 있는 경우 처리
            print("No text provided for summarization. Skipping...")
            return GptProject(projectName="", skillSet="", projectDescription="")

        print("Generating simplified project summary in JSON format...")

        # beta, parse형태로 구성됨. 주기적으로 공식문서 업데이트 확인할것
        client = OpenAI(api_key=openai_api_key)
        response = client.beta.chat.completions.parse(
            model=settings.gpt_model,
            messages=[
                {
                    "role": "system", 
                    "content": "As a senior developer, you are aiming to summarize your projects in Markdown format in Korean to efficiently highlight them on your resume for recruiters. Use concise phrases instead of full sentences to enhance clarity, emphasizing key strengths and unique aspects."
                },
                {
                    "role": "user",
                    "content": (
                        f"Summary Text:\n{summary_text}\n\n"
                        "Please use the format to structure the summary based on the text provided(sample text). But, Do not use the context in the format. only use this in the structure and how to write the sentence."
                    )
                },
                {"role": "assistant", "content": f"focus on {requirements}"}
            ],
            max_tokens=settings.max_output_tokens,
            response_format=GptProject,
        )

        # GPT 응답 파싱
        response_text = response.choices[0].message.parsed

        # GptProject 객체로 반환
        return response_text

    except Exception as e:
        print(f"An error occurred while simplifying the summary: {e}")
        return GptProject(projectName="", skillSet="", projectDescription="")
    
# 어바웃미 생성    
def generate_aboutme(openai_api_key, prompt=settings.aboutme_prompt):
    try:
        # 요약 요청
        print("Generating about me...")
        
        # # 1. JSON 파일에서 회사 정보 읽기 - 상대경로로 수정해야 함
        # json_file_path = os.path.join("/Users/eunma/Documents/GitHub/gitfolio_AI/app/data/dependencies/company_info.json")
        # with open(json_file_path, "r", encoding="utf-8") as f:
        #     company_data = json.load(f)
        
        # 1-1. 하나의 공동 인재상으로 만든 회사 정보
        company_data = {
            "companies": [
                {
                    "name": "Dream Company",
                    "slogan": "도전, 소통, 창의로 더 나은 미래를 만드는 회사",
                    "description": "Dream Company는 도전과 창의를 통해 새로운 가치를 창출하며, 소통과 협력을 바탕으로 고객과 사회에 긍정적인 영향을 미칩니다. 우리는 탁월한 실행력과 윤리적 책임감을 통해 지속 가능한 성장을 추구합니다.",
                    "values": [
                        "끊임없는 열정과 도전정신으로 기존의 한계를 뛰어넘습니다.",
                        "높은 목표를 설정하고 이를 달성하기 위해 치열하게 고민하고 실행합니다.",
                        "구성원 간 신뢰를 바탕으로 협력하며 팀워크를 중시합니다.",
                        "다양한 배경과 시각을 존중하며 포용적인 문화를 지향합니다.",
                        "사용자에게 가치를 더하고 기대를 뛰어넘는 경험을 제공합니다.",
                        "정직과 투명성을 바탕으로 신뢰를 쌓으며, 공정한 경쟁을 추구합니다.",
                        "목표를 향해 몰입하며, 신속하고 기민하게 실행합니다.",
                        "전문성과 역량을 꾸준히 배양하며, 개인과 조직의 성장을 동시에 추구합니다.",
                        "사회적 책임을 다하며 지속 가능한 성장을 지향합니다."
                    ]
                }
            ]
        }


        # 2. 통합된 회사 정보 사용
        company_info = company_data["companies"][0]

        # GitHub README 토큰 호출
        github_readme, github_repos = get_github_profile_and_repos(settings.gh_token)
        # github_repos = "\n".join([f"- {project.projectName}: {project.projectDescription}" for project in project_summaries])

        # OpenAI API 호출
        client = OpenAI(api_key=openai_api_key)
        response = client.beta.chat.completions.parse(
            model=settings.gpt_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional assistant specializing in creating an 'About Me' section for job applications. "
                        "Your task is to derive concise and compelling statements based on the provided information. "
                        "While utilizing the company information to craft relevant responses, avoid directly mentioning the company's name, slogan, or other identifying details. "
                        "Instead, focus on aligning the applicant's traits and qualifications with the company's values and mission."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        "Company Information:\n"
                        f"- Name: {company_info['name']}\n"
                        f"- Slogan: {company_info['slogan']}\n"
                        f"- Description: {company_info['description']}\n"
                        f"- Values: {" ".join(company_info['values'])}\n\n"
                        "GitHub Profile:\n"
                        f"{github_readme}\n\n"
                        "GitHub Repositories:\n"
                        f"{github_repos}\n\n"
                    )
                },
                {
                    "role": "assistant",
                    "content": f"Sample summary format: {prompt}."
                }
            ],
            max_tokens=settings.max_output_tokens,
        
        )
        pprint.pprint(response)

        # 응답 파싱
        response_text = response.choices[0].message.content
        # GptAboutme 객체로 반환
        return response_text

    except Exception as e:
        print(f"Error generating About Me: {e}")
        return ""
    
# 이력서 수정    
def resume_update(openai_api_key, requirements, selected_text, context_data, prompt=settings.resume_update_prompt) :
    try:
        # 선택된 텍스트가 없을 때 처리
        if not selected_text or not selected_text.strip():
            print("Error: Selected text is empty or missing.")
            return context_data # 오류 발생시 기존 데이터 반환
        
        # 수정 요구사항이 없을 때 처리
        if not requirements or not requirements.strip():
            print("Error: User request (requirements) is empty or missing.")
            return context_data # 오류 발생시 기존 데이터 반환
        
        # 수정 요청
        print("이력서 수정")
        
        # OpenAI API 호출
        client = OpenAI(api_key=openai_api_key) 
        response = client.beta.chat.completions.parse(
            model=settings.gpt_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly and professional resume modification expert."
                        "Your task is to update only the specified sections of the resume based on the user's request while leaving all other parts unchanged." 
                        "Ensure the modifications are concise, professional, and aligned with the tone of the original resume."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        "Context Data:\n"
                        f"{json.dumps(context_data, indent=4)}\n\n"
                        "Selected Text:\n"
                        f"{selected_text}\n\n"
                        # "Key Path:\n"
                        # f"{key_path}\n\n"
                        "User Request:\n"
                        f"{requirements}\n\n"
                        "Please update the selected text based on the instructions provided."
                    )
                },
                {
                    "role": "assistant",
                    "content": f"Sample summary format: {prompt}."
                }
            ],
            max_tokens=settings.max_output_tokens,
            response_format=ResumeResponseDto
        )
        
        # GPT 응답 파싱
        response_text = response.choices[0].message.parsed
        
        # ResumeResponseDto 객체로 반환
        return response_text

        
    except Exception as e:
        print(f"Error modifying resume with GPT: {e}")
        return context_data  # 오류 발생 시 기존 데이터 반환

# 이력서 제목 생성
def create_project_title(openai_api_key, gh_token, repo_url, prompt=settings.project_title_prompt):
    try:
        # 제목 후보 가져오기
        title_candidates = project_title_candidate(gh_token, repo_url)
        title_candidate_1 = title_candidates.get("title_candidate_1", "")
        title_candidate_2 = title_candidates.get("title_candidate_2", "")
        title_candidate_3 = title_candidates.get("title_candidate_3", "")
        
        # 후보 검증 및 최종 제목 결정
        if title_candidate_1 == title_candidate_2:
            print("Title Candidate 1 and 2 are identical.")
            title = {"projectTitle": title_candidate_1}
            return title
        
        print("프로젝트 제목을 추론합니다.")
        
        # OpenAI API 호출
        client = OpenAI(api_key=openai_api_key) 
        response = client.beta.chat.completions.parse(
            model=settings.gpt_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional assistant tasked with deciding the best project title. "
                        "Evaluate the provided title candidates and choose the most appropriate one. "
                        "Focus on clarity, relevance, and alignment with typical project naming conventions."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        "You are tasked with evaluating and determining the best project title based on the following candidates:\n\n"
                        f"title_candidate_1 (Repository Name):\n{title_candidate_1}\n\n"
                        f"title_candidate_2 (README First Line):\n{title_candidate_2}\n\n"
                        f"title_candidate_3 (Topics):\n{title_candidate_3}\n\n"
                        "Candidate 1 and 2 are the primary sources for the project title as they are likely to directly reflect the project’s purpose. "
                        "Evaluate these first to infer a suitable title. "
                        "If these candidates lack sufficient clarity or relevance, use Candidate 3 (Topics) to provide additional context or inspiration for the title.\n\n"
                        "Your decision should prioritize the following criteria:\n"
                        "- Clarity: The title should be easy to understand and intuitive.\n"
                        "- Relevance: The title should accurately represent the project’s purpose, functionality, or key features.\n"
                        "- Alignment: The title should align with common naming conventions for projects of this type.\n\n"
                        "If none of the candidates are appropriate, synthesize information from all three candidates to create a new title that best fits the project.\n\n"
                        "Be concise and professional in your suggestion."
                    )
                },
                {
                    "role": "assistant",
                    "content": f"Sample summary format: {prompt}."
                }
            ],
            max_tokens=settings.max_output_tokens,
            response_format=ProjectTitleDto
        )
        # GPT 응답 파싱
        response_text = response.choices[0].message.parsed
        
        # 최종 리턴값 확인 - 테스트용
        print(f"Final Response Text: {response_text}")
        
        # ProjectTitleDto 객체로 반환
        return response_text

        
    except Exception as e:
        print(f"Error modifying resume with GPT: {e}")
        return {
            "projectTitle": "",
            "title_candidates": {
                "title_candidate_1": "",
                "title_candidate_2": "",
                "title_candidate_3": ""
            }
        }

# 맡은 업무 생성        
def generate_role_and_task(openai_api_key,code_summary, pr_summary, commit_summary, requirements, prompt=settings.role_and_task_prompt):
    try:
        # 담당업무 생성
        print("Generating Role and Task...")
        
        # 어떤 정보를 가져올건지 로직 구현
        if not code_summary.strip() and not pr_summary.strip() and not commit_summary.strip():  # 텍스트가 비어 있는 경우 처리
            print("No text provided for summarization. Skipping...")
            return
                
        # gpt 호출
        client = OpenAI(api_key=openai_api_key)
        response = client.beta.chat.completions.parse(
            model=settings.gpt_model,
            messages=[
                {"role": "system", 
                 "content": (
                     "You are a professional assistant specializing in extracting roles and responsibilities from project data. "
                     "Your task is to identify the key responsibilities and actions taken by the user based on the provided summaries."
                 )},
                {"role": "user", 
                 "content": (
                     f"Analyze the following data and extract the main roles and responsibilities:\n\n"
                     f"### Code Summary:\n{code_summary}\n\n"
                     f"### PR Summary:\n{pr_summary}\n\n"
                     f"### Commit Summary:\n{commit_summary}\n\n"
                     f"### Requirements:\n{requirements}\n\n"
                     "Please provide the roles and responsibilities in a concise list format."
                 )},
                {"role": "assistant", "content": f"{prompt}, focus on {requirements}"}
            ],
            max_tokens=settings.max_output_tokens,
            response_format=RoleAndTaskDto,
        )
        # GPT 응답 파싱
        response_text = response.choices[0].message.parsed

        # Role and task 객체로 반환
        return response_text

    except Exception as e:
        print(f"Error during summarization: {e}")
        return RoleAndTaskDto(roleAndTask="")