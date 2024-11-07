from openai import OpenAI
from app.config.settings import settings
from app.dto.resume_dto import GptProject
import tiktoken 

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
                    "content": "You are an assistant that formats project summaries in MarkDown for review purposes. As a senior developer, summarize in Korean using concise phrases rather than full sentences for clarity. Highlight key strengths or unique aspects from a senior developer's perspective."
                },
                {
                    "role": "user",
                    "content": (
                        f"Summary Text:\n{summary_text}\n\n"
                        "Please use the format to structure the summary based on the text provided(sample text). But, Do not use the context in the format. only use this in the structure and how to write the sentence."
                    )
                },
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
        print(f"An error occurred while simplifying the summary: {e}")
        return GptProject(projectName="", skillSet="", projectDescription="")