FROM --platform=linux/amd64 python:3.12-alpine

# build-arg 선언 - 빌드 시 전달받을 환경변수들
ARG OPENAI_API_KEY
ARG GH_TOKEN
ARG HOST
ARG PORT

# 작업 디렉토리 설정
WORKDIR /app

# GitPython 라이브러리가 git 실행파일에 의존해서 도커 컨테이너에 git 을 실행해줘야 한다.
RUN apk update && apk add git

# ARG로 받은 값들을 ENV로 설정하여 이미지에 포함
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV GH_TOKEN=${GH_TOKEN}
ENV HOST=${HOST}
ENV PORT=${PORT}

# 필요 파일 복사
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 애플리케이션 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]