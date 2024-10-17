# gitfolio_AI

```
/gitfolio-ai
│
├── /app
│   ├── __init__.py
│   ├── main.py               # FastAPI 엔트리포인트
│   ├── config.py             # 환경 변수 및 설정 관리
│   ├── /api
│   │   ├── __init__.py
│   │   ├── v1
│   │   │   ├── __init__.py
│   │   │   ├── routes.py     # API 라우팅 관리
│   ├── /data
│   │   ├── __init__.py
│   │   ├── mongodb.py   # MonggoDB 세팅 dto
│   ├── /dto
│   │   ├── __init__.py
│   │   ├── resume_dto.py  # FastAPI Pydantic 스키마 정의
│   ├── /utils
│   │   ├── __init__.py
│   │   ├── token_utils.py    # 토큰 계산 및 유틸리티 함수들
│   │   ├── text_utils.py     # 텍스트 전처리 및 기타 유틸리티 함수들
│   ├── /services
│   │   ├── __init__.py
│   │   ├── github_service.py # GitHub 관련 로직 (API 호출 등)
│   │   ├── ai_service.py     # OpenAI GPT 모델 호출 로직
│   ├── /prompts
│   │   ├── __init__.py
│   │   ├── resume_prompt.py  # GPT 프롬프트 템플릿 관리
│   └── /tests
│       ├── __init__.py
│       ├── test_routes.py    # API 라우팅 테스트
│
├── .env                      # 환경 변수 (API 키 등)
├── requirements.txt          # 의존성 패키지 목록
├── Dockerfile                # Docker 설정 파일
├── README.md                 # 프로젝트 설명
└── .gitignore                # Git 관리에서 제외할 파일 목록
```
