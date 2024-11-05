# Base image
FROM python:3.12-alpine

# 작업 디렉토리 설정
WORKDIR /app

# GitPython 라이브러리가 git 실행파일에 의존해서 도커 컨테이너에 git 을 실행해줘야 한다.
RUN apk update && apk add git

# 필요 파일 복사
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 애플리케이션 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]