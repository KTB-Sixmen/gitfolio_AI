# gitfolio_AI
- Python 3.10 이상
- `pip install -r requirements.txt`
- 메인 서버 파일(main.py) 실행: `uvicorn main:app --reload`


```
/GITFOLIO_AI
│
├── /app
│   ├── __init__.py
│   ├── main.py               # FastAPI 엔트리포인트
│   ├── /api
│   │   ├── __init__.py
│   │   ├── /v1
│   │   │   ├── __init__.py
│   │   │   └── routes.py     # API 라우팅 관리
│   ├── /config
│   │   ├── __init__.py
│   │   ├── constant.py       # 상수 설정 파일
│   │   └── settings.py       # 환경 변수 및 설정 관리
│   ├── /data                 # 데이터 파일
│   │   ├── __init__.py
│   │   ├── code
│   │   ├── commit
│   │   ├── pr
│   │   └── project
│   ├── /dto
│   │   ├── __init__.py
│   │   └── resume_dto.py     # FastAPI Pydantic 스키마 정의
│   ├── /prompts
│   │   ├── __init__.py
│   │   └── resume_prompt.py  # GPT 프롬프트 템플릿 관리
│   ├── /services
│   │   ├── __init__.py
│   │   ├── data_service.py   # 데이터 서비스
│   │   ├── github_service.py # GitHub 관련 로직 (API 호출 등)
│   │   └── gpt_service.py    # OpenAI GPT 모델 호출 로직
│   ├── /tests
│   │   ├── __init__.py
│   │   └── test_routes.py    # API 라우팅 테스트
│   └── /utils
│       ├── __init__.py
│       └── token_utils.py    # 토큰 계산 및 유틸리티 함수들
│
├── pretrained_model          # 사전 학습된 모델 파일 저장 폴더
├── .env                      # 환경 변수 (API 키 등)
├── .gitignore                # Git 관리에서 제외할 파일 목록
├── Dockerfile                # Docker 설정 파일
├── README.md                 # 프로젝트 설명
└── requirements.txt          # 의존성 패키지 목록
```

