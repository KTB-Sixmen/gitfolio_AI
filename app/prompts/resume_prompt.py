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