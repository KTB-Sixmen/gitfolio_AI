from pydantic_settings import BaseSettings
from app.config.constant import GPT_MODEL, MAX_TOTAL_TOKENS, PROMPT_TOKEN_RESERVE, MAX_OUTPUT_TOKENS, MAX_CONTENT_TOKENS, DEFAULT_HOST, DEFAULT_PORT, DEFAULT_DATA, CODE_DATA, PR_DATA, COMMIT_DATA, PROJECT_DATA 
from app.prompts.resume_prompt import CODE_SUMMARY_PROMPT, PR_SUMMARY_PROMPT, COMMIT_DIFF_SUMMARY_PROMPT, FINAL_SUMMARY_PROMPT, FINAL_PROJECT_PROMPT

class Settings(BaseSettings):
    # API 키
    openai_api_key: str
    github_token: str

    # 서버 설정
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT

    # 토큰 및 모델 관련 상수
    gpt_model: str = GPT_MODEL
    max_total_tokens: int = MAX_TOTAL_TOKENS
    prompt_token_reserve: int = PROMPT_TOKEN_RESERVE
    max_output_tokens: int = MAX_OUTPUT_TOKENS
    max_content_tokens: int = MAX_CONTENT_TOKENS

    # 데이터 저장 위치
    default_data: str = DEFAULT_DATA
    code_data: str = CODE_DATA
    pr_data: str = PR_DATA 
    commit_data: str = COMMIT_DATA
    project_data: str = PROJECT_DATA 

    # Prompt 세팅
    code_summary_prompt: str = CODE_SUMMARY_PROMPT
    pr_summary_prompt: str = PR_SUMMARY_PROMPT
    commit_diff_summary_prompt: str = COMMIT_DIFF_SUMMARY_PROMPT
    final_summary_prompt: str = FINAL_SUMMARY_PROMPT
    final_project_prompt: str = FINAL_PROJECT_PROMPT

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()