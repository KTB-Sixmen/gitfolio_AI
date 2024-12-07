# 프롬프트 설정
CODE_SUMMARY_PROMPT = (
    "Review the entire code to summarize the project's overview and highlight "
    "its main features. Additionally, if possible, include any issues encountered, "
    "how they were resolved, and the outcomes achieved."
)

PR_SUMMARY_PROMPT = (
    "Analyze the title and detailed information of the content developed by the user "
    "to identify the problems solved, the approach taken, and the results achieved, "
    "and provide a summary."
)

# + - diff부분인걸 알아차려서 할것.
COMMIT_DIFF_SUMMARY_PROMPT = (
    "Review each code to understand how the project was developed, identify the contributions "
    "made to the project, and determine what kind of developer the user is."
)

FINAL_SUMMARY_PROMPT = (
    "Focusing on understanding the key aspects, features, issues resolved, and outcomes, "
    "to provide a clear overview."
)

FINAL_PROJECT_PROMPT = (
    "Write concisely and clearly, highlighting your unique strengths rather than common development details."
)

# 샘플에 너무 편향되는 감이 있을수 있음.
SIMPLIFY_PROJECT_PROMPT = (
    f"sample text:\n"
    f"**projectName: 식당어때? (LLM을 활용한 리뷰기반 식당 추천시스템)** - **KakaoTech Bootcamp 생성형 AI**\n\n"
    f"skillSet: (텍스트기반 비정형 데이터 파이프라인, Sentence-BERT, KcELENTRA, Elastic Search, HDBSCAN)\n\n"
    f"projectDescription: *사용자가 원하는 위치와 음식을 받아 AI모델이 식당들을 평가를 진행하여 랭킹화해서 제공하고 리뷰의 전반적인 내용을 클러스터링을 활용하여 제공하는 서비스. "
    f"카카오맵에서 식당 리뷰를 셀리니움과 멀티프로세싱을 사용해 12만개 크롤링한후 분석하였고, elastic search에 저장하고 전처리, 레이블링을 진행하는 데이터 파이프라인을 만들었으며 "
    f"KcELECTRA 모델과 전처리된 데이터를 기반으로 모델을 만들고 wandb로 모델 결과를 시각화해봄. 이 만든 모델과 BiLSTM로 만든 모델을 앙상블과정을 통해 랭킹화하는 api를 fastapi통해 만듬. "
    f"추가로 umap과 hdbscan 활용하여 식당리뷰를 클러스터링 api를 만들어 가장 많이 군집화된 리뷰단어들을 리턴하는 부분을 구축함. 초기 모델은 응답까지 222초 걸리던것을 애자일한 협업과정을 "
    f"거쳐 디비생성, 배치사용등의 필요성을 느끼고 개선하여 응답속도를 26초까지 향상함.*\n\n"
)

# testing용
ABOUTME_TECHSTACK_PROMPT = (
    "안녕하세요! **’Comfort-Zone에서 벗어나 끊임없이 도전을 하는 개발자’** 입니다."
    "- Self-Motivation: 어떤 일이든 관심이 생기면 망설임 없이 도전하여 실행에 옮깁니다."
    "- Optimization-Driven: 코드 한 줄 까지도 성능 최적화에 집중하여 시스템의 효율성과 비즈니스 가치를 극대화합니다."
    "- Collaborative-Growth: 개인적인 성장을 넘어서, 함께 공유하며 발전하는 문화를 추구합니다."
)

ABOUTME_PROMPT = (
    "Provide a response by deriving 1-2 key descriptive words related to the given information, "
    "then explain the meaning of those words as they relate to the applicant's traits or qualifications.\n\n"
    "The final 'About Me' should consist of three concise points, each formatted as follows:\n"
    "<English keyword>: <Korean explanation>\n"
    "Example:\n"
    "- Proactive Development: 필요한 미래를 앞당기기 위해 새로운 도전에 적극적으로 임합니다.\n"
    "- Collaborative Growth: 서로의 역량을 극대화하며 함께 성장할 수 있는 환경을 만듭니다.\n"
    "- Adaptive Thinking: 변화에 유연하게 대응하며 창의적인 접근 방식을 추구합니다."
    "When writing the response:\n"
        "1. Highlight the applicant's proactive attitude and problem-solving skills.\n"
        "2. Ensure the tone remains professional, and the explanation is concise.\n"
        "3. Use metaphorical or creative expressions to enhance engagement, avoiding direct repetition of the input text.\n"
        "4. Ensure each point reflects the provided company values and GitHub data."
)

RESUME_UPDATE_PROMPT = (
        "Update the provided `selected_text` based on the user's request. "
        "Modify only the specified text, and ensure the updated text aligns with the tone and style of the surrounding context. "
        "Return only the modified text without altering the structure or other parts of the resume."
)

PROJECT_TITLE_PROMPT = (
    "Return the best project title as plain text. "
    "Do not include any additional explanation, formatting, or context. "
    "Only provide the title itself."
)

ROLE_AND_TASK_PROMPT = (
    "Create a summary of the main roles and responsibilities based on the provided data. "
    "Use bullet points to list the key actions and tasks performed. Each point should:\n"
    "- Begin with an action verb.\n"
    "- Be concise and specific.\n"
    "- Clearly reflect the user's contributions and achievements.\n\n"
    "- Follow this pattern:"
    "- Performed [specific action] to achieve [specific result], improving/enhancing [specific metric] by [quantifiable amount].  "    
    "- Identified [specific issue] and implemented [specific action], resulting in a performance improvement of [quantifiable amount]."  
    "- Utilized [specific tool or library] to develop/implement [specific functionality or feature]. " 
    "For example:\n"
    "- Designed and implemented Redis caching to improve API response times by 30%.\n"
    "- Refactored MongoDB queries to reduce average query time by 55.4%.\n"
    "- Developed an event-driven architecture using Kafka for real-time notifications."
)

TROUBLE_SHOOTING_PROMPT = ()