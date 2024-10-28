from pydantic_settings import BaseSettings
from app.config.constant import GPT_MODEL, MAX_TOTAL_TOKENS, PROMPT_TOKEN_RESERVE, MAX_OUTPUT_TOKENS, MAX_CONTENT_TOKENS, DEFAULT_HOST, DEFAULT_PORT

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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()