# 모델 관련 설정
GPT_MODEL = 'gpt-4o-mini'  # 사용할 OpenAI 모델 이름

# 토큰 제한 설정
MAX_TOTAL_TOKENS = 128000       # 전체 토큰 제한
PROMPT_TOKEN_RESERVE = 1000      # 프롬프트에 사용할 토큰을 남겨두는 양
MAX_OUTPUT_TOKENS = 4000         # 최대 아웃풋 토큰
MAX_CONTENT_TOKENS = MAX_TOTAL_TOKENS - PROMPT_TOKEN_RESERVE - MAX_OUTPUT_TOKENS  # 최대 컨텐츠 토큰 수

# 데이터 저장 위치
DEFAULT_DATA = 'app/data'
CODE_DATA = 'app/data/code'
PR_DATA = 'app/data/pr'
COMMIT_DATA = 'app/data/commit'
PROJECT_DATA = 'app/data/project'
REPO_DIRECTORY = 'app/data/repo'