# 🎁 Collectrip Backend Server

[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-20.10-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)

여행의 추억을 완성하는 마지막 한 조각, 나만의 기념품을 찾아 떠나는 여정. **Collectrip**은 대한민국 관광 데이터와 AI를 기반으로 사용자에게 개인화된 기념품을 추천하고, 이를 수집하는 즐거움을 더하는 '기념품 큐레이션 및 도감 수집 플랫폼'입니다.

<br>

## ✨ 주요 기능 (Key Features)

-   **AI 기반 개인화 추천**: 사용자의 여행지, 선물 대상, 관심 키워드를 바탕으로 GPT가 리뷰를 분석하여 최적의 기념품을 추천합니다.
-   **지도 기반 위치 안내**: 추천된 기념품을 판매하는 상점의 위치를 Kakao Map API를 통해 정확하게 안내하고, 경로 정보를 제공합니다.
-   **도감 수집 시스템**: GPS 또는 사진 인증을 통해 실제로 방문한 상점의 기념품을 '나만의 도감'에 수집할 수 있습니다.
-   **게이미피케이션**: 특정 지역의 기념품을 모두 수집하거나 특별한 조건을 달성하면 '배지'를 획득하여 성취감을 느낄 수 있습니다.

<br>

## 🏛️ 아키텍처 (Architecture)

### 데이터 흐름

```
1. 사용자 (React Native)
   - 여행지, 키워드 입력
   - GPS/사진 정보 전송
      │
      ▼
2. Collectrip 백엔드 (Django)
   - API 요청 처리
   - 비즈니스 로직 수행
      │
      ├─► 3. TourAPI & GPT
      │   - TourAPI: 기념품점(A04), 쇼핑(A0401) 등 데이터 조회
      │   - GPT API: 장소 설명(overview) 및 리뷰 요약/태깅/긍정도 분석
      │
      ├─► 4. 데이터베이스 (MySQL)
      │   - 사용자, 콘텐츠, 도감, 배지 정보 저장 및 조회
      │
      ▼
5. 사용자 (React Native)
   - 개인화 추천 결과 + 지도 정보 수신
   - 도감/배지 획득 결과 확인
```

### 데이터베이스 스키마 (ERD)

> 프로젝트의 데이터베이스 구조입니다. 자세한 내용은 Notion 문서를 참고해주세요.
>
> _(여기에 ERD 이미지를 삽입하거나, 이미지 파일을 프로젝트에 추가 후 링크할 수 있습니다.)_
> ![ERD](path/to/your/erd_image.png)

<br>

## 🛠️ 기술 스택 (Tech Stack)

| 구분          | 기술                                                                                                         |
| ------------- | ------------------------------------------------------------------------------------------------------------ |
| **Backend** | <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django"> <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python">                         |
| **Database** | <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql">                                 |
| **Infra** | <img src="https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazon-aws"> <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker"> |
| **API** | TourAPI, KakaoMap API, OpenAI GPT API                                                                        |
| **Etc** | Git, Gitmoji, Notion, Discord                                                                                |

<br>

## 🚀 시작하기 (Getting Started)

### 1. 사전 요구사항

-   Python 3.11+
-   Docker & Docker Compose

### 2. 프로젝트 클론 및 설정

```bash
# 1. 원격 저장소를 로컬에 복제합니다.
git clone [https://github.com/FIFTEEN-BILLION/collectrip_backend.git](https://github.com/FIFTEEN-BILLION/collectrip_backend.git)
cd collectrip_backend

# 2. 환경변수 파일을 설정합니다.
# .env.example 파일을 복사하여 .env 파일을 생성하고, 내부의 값을 채워주세요.
cp .env.example .env
```

**`.env` 파일 설정 예시**

```
# Django
SECRET_KEY=your_django_secret_key

# Database
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=3306

# API Keys
TOUR_API_KEY=your_tour_api_service_key
KAKAO_API_KEY=your_kakao_api_key
OPENAI_API_KEY=your_openai_api_key
```

### 3. Docker 컨테이너 실행

```bash
# Docker Compose를 사용하여 백엔드 서버와 데이터베이스를 실행합니다.
docker-compose up --build -d

# 데이터베이스 스키마를 적용합니다.
docker-compose exec backend python manage.py migrate

# 슈퍼유저(관리자)를 생성할 경우
docker-compose exec backend python manage.py createsuperuser
```

서버는 `localhost:8000`에서 실행됩니다.

<br>

## 👨‍💻 팀 및 역할 분담 (Team & Roles)

| 역할                   | 담당자 | 주요 담당 기능                                                                         |
| ---------------------- | ------ | -------------------------------------------------------------------------------------- |
| 👤 **사용자 담당 (User-Side)** | 정재훈 | 소셜 로그인, 마이페이지, 도감/배지 조회, 배지 획득 시스템, 인증 로직, 찜하기 등 |
| 💾 **데이터 담당 (Data-Side)** | 천진영 | TourAPI/GPT 연동, 개인화 큐레이션 로직, DB 모델링, 지도 데이터 처리, 데이터 파이프라인 |

<br>

## 🤝 협업 절차 (Contribution Guideline)

모든 작업은 아래의 절차를 따르는 것을 원칙으로 합니다.

1.  **`Issue 생성`**: 모든 작업은 GitHub Issue를 생성하는 것에서 시작합니다. 할당(Assignee), 라벨(Label)을 명확하게 지정합니다.

2.  **`Branch 생성`**: `develop` 브랜치에서 자신의 작업을 위한 브랜치를 생성합니다.
    -   브랜치명: `[type]/#[이슈번호]-[작업내용]`
    -   예시: `feat/#10-setup-kakao-login`

3.  **`코드 작성 및 Commit`**: 기능을 구현하고, 작업 단위별로 커밋을 남깁니다.
    -   커밋 메시지: `[깃모지] [타입]: [작업 요약]`
    -   예시: `✨ feat: 카카오 소셜 로그인 API 구현`
    -   본문에는 상세 설명과 `Resolves: #[이슈번호]`를 반드시 포함합니다.

4.  **`Pull Request (PR) 생성`**: 작업이 완료되면 `develop` 브랜치로 PR을 생성합니다.
    -   PR 템플릿의 모든 항목을 꼼꼼하게 작성합니다.
    -   **코드 리뷰어(Reviewer)로 상대방을 반드시 지정합니다.**

5.  **`코드 리뷰`**: **상대방의 코드를 리뷰하는 것을 최우선 순위**로 합니다.
    -   데이터 담당(천진영)의 PR은 사용자 담당(정재훈)이 리뷰합니다.
    -   사용자 담당(정재훈)의 PR은 데이터 담당(천진영)이 리뷰합니다.
    -   수정 요청(Request changes)이나 칭찬(Comment), 승인(Approve)을 통해 피드백을 남깁니다.

6.  **`Merge`**: 코드 리뷰에서 `Approve`를 받으면 PR을 `develop` 브랜치에 병합합니다. 병합 후에는 작업 브랜치를 삭제합니다.

<br>

## 📜 API 명세 (API Specification)

<details>
<summary>👉 클릭하여 전체 API 엔드포인트 목록 확인하기</summary>

**Base URL**: `/api/v1`

---

#### Authentication (인증)

-   `POST /auth/{provider}/`: 소셜 로그인 (카카오/구글)
-   `POST /auth/token/refresh/`: JWT 토큰 재발급

#### Users & MyPage (사용자 & 마이페이지)

-   `GET /users/me/`: 내 정보 조회
-   `PATCH /users/me/`: 내 정보 수정
-   `GET /users/me/collections/`: 내가 수집한 도감 목록 조회
-   `GET /users/me/badges/`: 내가 획득한 배지 목록 조회

#### Curation & Data (큐레이션 & 데이터)

-   `POST /curations/`: 조건에 맞는 기념품 추천 요청
-   `GET /contents/{content_id}/`: 특정 콘텐츠(기념품) 상세 정보 조회

#### Collections (도감 & 게이미피케이션)

-   `POST /collections/auth/gps/`: GPS 기반 방문 인증 및 도감 추가
-   `POST /collections/auth/photo/`: 사진 기반 방문 인증 및 도감 추가

---

</details>
