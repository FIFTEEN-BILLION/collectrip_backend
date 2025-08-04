# Python 3.11 기반 이미지 사용
FROM python:3.11

# 컨테이너 내부 작업 디렉토리 설정
WORKDIR /app

# requirements 복사 및 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 전체 소스코드 복사
COPY . .

# Django 포트 오픈
EXPOSE 8000

# 서버 실행 명령
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]