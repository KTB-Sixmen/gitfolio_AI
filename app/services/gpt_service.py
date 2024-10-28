from openai import OpenAI
from app.config.settings import settings
from app.prompts.resume_prompt import CODE_SUMMARY_PROMPT, PR_SUMMARY_PROMPT, COMMIT_DIFF_SUMMARY_PROMPT, FINAL_PROJECT_PROMPT, FINAL_SUMMARY_PROMPT
import tiktoken 

# GPT를 사용한 요약 함수
def summarize_text(text, openai_api_key, max_output_tokens, prompt):
    try:
        if not text.strip():  # 텍스트가 비어 있는 경우 처리
            print("No text provided for summarization. Skipping...")
            return ""

        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model=settings.GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are a senior developer who wrote the code I provided. Summarize the project by extracting key points from the code and text, and present meaningful information in a concise way, in Korean."},
                {"role": "user", "content": f"{text}"},
                {"role": "assistant", "content": f"{prompt}"}
            ],
            max_tokens=max_output_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error during summarization: {e}")
        return ""

# 코드 텍스트를 토큰 단위로 슬라이싱하여 GPT에 요약 요청
def slice_and_summarize(all_code, openai_api_key, max_output_tokens=settings.max_output_tokens, token_limit=settings.max_content_tokens, prompt=CODE_SUMMARY_PROMPT):
    try:
        if not all_code.strip():  # 텍스트가 없으면 스킵
            print("No code provided for summarization. Skipping...")
            return ""

        summaries = []
        print("Summarizing the full content...")
        enc = tiktoken.encoding_for_model(settings.GPT_MODEL)  # 토큰화 엔코더 생성
        tokens = enc.encode(all_code)

        for i in range(0, len(tokens), token_limit):
            part_tokens = tokens[i:i + token_limit]
            part_text = enc.decode(part_tokens)
            print(f"Summarizing part from token {i} to {i + token_limit}")
            summary = summarize_text(part_text, openai_api_key, max_output_tokens, prompt)
            summaries.append(summary)

        return "\n\n".join(summaries)
    except Exception as e:
        print(f"Error during slicing and summarizing: {e}")
        return ""

# 최종 요약: 길이가 여전히 길면 반복적으로 최종 요약
def final_summarization(summary_text, openai_api_key, max_output_tokens=settings.max_output_tokens, prompt=FINAL_SUMMARY_PROMPT):
    try:
        if not summary_text.strip():  # 텍스트가 없으면 스킵
            print("No text provided for final summarization. Skipping...")
            return ""    

        enc = tiktoken.encoding_for_model(settings.GPT_MODEL)
        tokens = enc.encode(summary_text)

        while len(tokens) > max_output_tokens:
            print(f"Final summarization is too long ({len(tokens)} tokens), re-summarizing...")
            summary_text = summarize_text(summary_text, openai_api_key, max_output_tokens, prompt)
            tokens = enc.encode(summary_text)
        
        return summary_text
    except Exception as e:
        print(f"Error during final summarization: {e}")
        return ""