# Nutritionist Menu Planner - Backend

FastAPI 기반 영양사 식단 자동 생성 플랫폼 백엔드 API

## 기술 스택

- **Framework**: FastAPI 0.115+
- **Language**: Python 3.11+
- **Database**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0 (Async)
- **Migration**: Alembic
- **Authentication**: JWT (python-jose)
- **Validation**: Pydantic v2

## 요구사항

- Python 3.11 이상
- Poetry (패키지 관리 도구)
- PostgreSQL 14 이상

## 설치 방법

### 1. Poetry 설치

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. 의존성 설치

```bash
cd backend
poetry install
```

### 3. 환경 변수 설정

```bash
# .env.example 파일을 .env로 복사
cp .env.example .env

# .env 파일을 편집하여 실제 값 입력
# 특히 DATABASE_URL과 SECRET_KEY는 반드시 변경
```

### 4. PostgreSQL 설정

#### Option A: 로컬 설치

```bash
# PostgreSQL 설치 후
createdb nutritionist_menu_planner
```

#### Option B: Docker 사용

```bash
docker run --name nutritionist-postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=nutritionist_menu_planner \
  -p 5432:5432 \
  -d postgres:14
```

### 5. 데이터베이스 마이그레이션

```bash
# Alembic 초기화 (이미 완료된 경우 생략)
poetry run alembic init alembic

# 마이그레이션 실행
poetry run alembic upgrade head
```

## 실행 방법

### 개발 서버 실행

```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

또는

```bash
poetry run python -m app.main
```

서버 실행 후 브라우저에서 접속:
- API 문서: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 프로젝트 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 애플리케이션 진입점
│   ├── config.py            # 환경 변수 및 설정
│   ├── database.py          # 데이터베이스 연결 설정
│   ├── dependencies.py      # FastAPI dependencies
│   │
│   ├── models/              # SQLAlchemy 모델
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── meal_plan.py
│   │   ├── ingredient.py
│   │   └── ...
│   │
│   ├── schemas/             # Pydantic 스키마
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── meal_plan.py
│   │   ├── ingredient.py
│   │   └── ...
│   │
│   ├── routers/             # API 라우터
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── meal_plans.py
│   │   ├── ingredients.py
│   │   └── ...
│   │
│   ├── services/            # 비즈니스 로직
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── meal_plan_service.py
│   │   ├── file_parser_service.py
│   │   └── ...
│   │
│   ├── utils/               # 유틸리티 함수
│   │   ├── __init__.py
│   │   ├── security.py
│   │   ├── validators.py
│   │   └── ...
│   │
│   └── core/                # 핵심 설정
│       ├── __init__.py
│       ├── security.py
│       ├── logging.py
│       └── exceptions.py
│
├── alembic/                 # 데이터베이스 마이그레이션
│   ├── versions/
│   └── env.py
│
├── tests/                   # 테스트
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_meal_plans.py
│   └── ...
│
├── uploads/                 # 업로드 파일 저장 (gitignore)
├── pyproject.toml           # Poetry 의존성 관리
├── .env.example             # 환경 변수 예시
├── .env                     # 환경 변수 (gitignore)
└── README.md                # 이 파일
```

## 개발 가이드

### 코드 포맷팅

```bash
# Black으로 코드 포맷팅
poetry run black .

# Ruff로 린팅
poetry run ruff check .

# Ruff로 자동 수정
poetry run ruff check --fix .
```

### 타입 체크

```bash
poetry run mypy app/
```

### 테스트 실행

```bash
# 모든 테스트 실행
poetry run pytest

# 커버리지 포함 테스트
poetry run pytest --cov=app --cov-report=html

# 특정 테스트 파일 실행
poetry run pytest tests/test_auth.py

# 특정 테스트 함수 실행
poetry run pytest tests/test_auth.py::test_login
```

### 데이터베이스 마이그레이션

```bash
# 새로운 마이그레이션 생성
poetry run alembic revision --autogenerate -m "Add user table"

# 마이그레이션 적용
poetry run alembic upgrade head

# 마이그레이션 롤백
poetry run alembic downgrade -1

# 마이그레이션 히스토리 확인
poetry run alembic history
```

## API 엔드포인트

### 인증 (Authentication)
- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인
- `POST /api/auth/refresh` - 토큰 갱신

### 식단 관리 (Meal Plans)
- `GET /api/meal-plans` - 식단 목록 조회
- `GET /api/meal-plans/{id}` - 식단 상세 조회
- `POST /api/meal-plans/generate` - 식단 자동 생성
- `POST /api/meal-plans/upload` - 기존 식단 업로드
- `PUT /api/meal-plans/{id}` - 식단 수정
- `DELETE /api/meal-plans/{id}` - 식단 삭제
- `GET /api/meal-plans/{id}/history` - 식단 이력 조회

### 식재료 관리 (Ingredients)
- `GET /api/ingredients` - 식재료 목록 조회
- `POST /api/ingredients` - 식재료 추가
- `PUT /api/ingredients/{id}` - 식재료 수정
- `DELETE /api/ingredients/{id}` - 식재료 삭제

### 파일 업로드 (Files)
- `POST /api/files/upload` - 파일 업로드

### 헬스 체크
- `GET /health` - 서버 상태 확인

자세한 API 문서는 서버 실행 후 `/docs` 페이지에서 확인하세요.

## 환경 변수 설명

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `APP_NAME` | 애플리케이션 이름 | Nutritionist Menu Planner |
| `APP_ENV` | 환경 (development, production) | development |
| `DEBUG` | 디버그 모드 | True |
| `DATABASE_URL` | PostgreSQL 연결 문자열 | - |
| `SECRET_KEY` | JWT 암호화 키 | - |
| `ALGORITHM` | JWT 알고리즘 | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access Token 만료 시간 (분) | 30 |
| `CORS_ORIGINS` | CORS 허용 도메인 | http://localhost:3000 |
| `MAX_UPLOAD_SIZE` | 최대 업로드 파일 크기 (bytes) | 10485760 (10MB) |

## 트러블슈팅

### PostgreSQL 연결 오류

```
sqlalchemy.exc.OperationalError: could not connect to server
```

**해결 방법**:
1. PostgreSQL이 실행 중인지 확인
2. `.env` 파일의 `DATABASE_URL` 확인
3. 데이터베이스가 생성되어 있는지 확인

### Poetry 의존성 설치 오류

```
[Errno 2] No such file or directory: 'python'
```

**해결 방법**:
1. Python 3.11 이상이 설치되어 있는지 확인
2. Poetry가 올바른 Python 버전을 사용하도록 설정
   ```bash
   poetry env use python3.11
   ```

### Alembic 마이그레이션 오류

```
alembic.util.exc.CommandError: Can't locate revision identified by 'head'
```

**해결 방법**:
1. 마이그레이션 파일이 있는지 확인
2. 초기 마이그레이션 생성
   ```bash
   poetry run alembic revision --autogenerate -m "Initial migration"
   ```

## 기여 가이드

1. 브랜치 전략은 [GIT_WORKFLOW.md](../docs/GIT_WORKFLOW.md) 참조
2. 코드 컨벤션은 [CODE_CONVENTIONS.md](../docs/CODE_CONVENTIONS.md) 참조
3. PR 생성 시 [PULL_REQUEST_TEMPLATE.md](../.github/PULL_REQUEST_TEMPLATE.md) 사용

## 라이센스

MIT License

## 문의

프로젝트 관련 문의는 이슈 트래커를 사용해주세요.
