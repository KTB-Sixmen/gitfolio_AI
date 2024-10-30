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

# 너무 편향되는 감이 있음
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