# 데이터베이스 스키마 구현 가이드

## 문서 목적
PostgreSQL 데이터베이스 스키마를 구현하고 관리하는 방법을 안내합니다.

---

## 데이터베이스 설정

### 1. PostgreSQL 설치 및 설정

#### Option A: 로컬 설치
```bash
# PostgreSQL 14 이상 설치 (Windows)
# https://www.postgresql.org/download/windows/

# 데이터베이스 생성
createdb nutritionist_menu_planner
```

#### Option B: Docker 사용 (권장)
```bash
# Docker로 PostgreSQL 실행
docker run --name nutritionist-postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=nutritionist_menu_planner \
  -p 5432:5432 \
  -d postgres:14

# 컨테이너 상태 확인
docker ps

# 데이터베이스 접속 테스트
docker exec -it nutritionist-postgres psql -U postgres -d nutritionist_menu_planner
```

### 2. 환경 변수 설정

`.env` 파일 생성 (backend 디렉토리):
```bash
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/nutritionist_menu_planner
```

---

## Alembic 마이그레이션

### 초기 마이그레이션 실행

```bash
cd backend

# 1. 최신 마이그레이션 적용
poetry run alembic upgrade head

# 2. 현재 리비전 확인
poetry run alembic current

# 3. 마이그레이션 히스토리 확인
poetry run alembic history
```

### 예상 출력
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001, Initial database schema
INFO  [alembic.runtime.migration] Running upgrade 001 -> 002, Seed allergen data
```

---

## 마이그레이션 상세 설명

### Migration 001: Initial Database Schema

**목적**: 18개 핵심 테이블 생성

**생성되는 테이블**:
1. `users` - 사용자 관리
2. `meal_plans` - 식단표
3. `daily_meals` - 일일 식단
4. `meal_items` - 식단 구성 요소
5. `meal_item_ingredients` - 식단-식재료 매핑
6. `ingredients` - 식재료 마스터
7. `ingredient_substitutes` - 대체 식재료
8. `suppliers` - 공급업체
9. `supplier_items` - 공급업체 식재료
10. `nutrition_info` - 영양 정보
11. `allergens` - 알레르기
12. `ingredient_allergens` - 식재료-알레르기 매핑
13. `meal_plan_history` - 식단 이력
14. `user_activity_log` - 사용자 활동 로그
15. `user_favorites` - 즐겨찾기
16. `monthly_active_users` - MAU 집계
17. `meal_plan_time_tracking` - 시간 추적
18. `meal_plan_reuse_tracking` - 재사용 추적

**생성되는 인덱스**: 30개 이상

**제약 조건**:
- Primary Keys: 모든 테이블
- Foreign Keys: 외래키 관계
- Unique Constraints: 중복 방지
- Check Constraints: 데이터 유효성 검증

### Migration 002: Seed Allergen Data

**목적**: 식약처 21종 알레르기 유발 식품 시드 데이터 추가

**데이터**:
- 고위험(High): 난류, 우유, 메밀, 땅콩, 밀, 게, 새우, 아황산류, 호두, 조개류
- 중위험(Medium): 대두, 고등어, 돼지고기, 복숭아, 닭고기, 쇠고기, 오징어, 잣, 알류
- 저위험(Low): 토마토, 밤

---

## 새로운 마이그레이션 생성

### 자동 생성 (권장)
```bash
# SQLAlchemy 모델 변경 후 자동으로 마이그레이션 생성
poetry run alembic revision --autogenerate -m "Add new column to users table"
```

### 수동 생성
```bash
# 빈 마이그레이션 파일 생성
poetry run alembic revision -m "Custom migration"
```

---

## 마이그레이션 관리

### 업그레이드
```bash
# 최신 버전으로 업그레이드
poetry run alembic upgrade head

# 특정 리비전으로 업그레이드
poetry run alembic upgrade 002

# 다음 리비전으로 하나씩 업그레이드
poetry run alembic upgrade +1
```

### 다운그레이드
```bash
# 이전 버전으로 다운그레이드
poetry run alembic downgrade -1

# 특정 리비전으로 다운그레이드
poetry run alembic downgrade 001

# 전체 롤백 (주의!)
poetry run alembic downgrade base
```

### 현재 상태 확인
```bash
# 현재 리비전 확인
poetry run alembic current

# 마이그레이션 히스토리
poetry run alembic history --verbose
```

---

## 데이터베이스 초기화 (개발 전용)

```bash
# 모든 테이블 삭제 후 재생성
poetry run alembic downgrade base
poetry run alembic upgrade head
```

---

## 스키마 검증

### 1. 테이블 목록 확인
```sql
-- PostgreSQL에서 실행
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

### 2. 특정 테이블 구조 확인
```sql
-- meal_plans 테이블 구조
\d meal_plans

-- 또는
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'meal_plans'
ORDER BY ordinal_position;
```

### 3. 외래키 확인
```sql
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
ORDER BY tc.table_name;
```

### 4. 인덱스 확인
```sql
SELECT
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
```

---

## 테이블별 데이터 타입

### 주요 데이터 타입 사용 이유

| 타입 | 사용 테이블 | 이유 |
|------|------------|------|
| BIGSERIAL | 모든 테이블의 id | 대용량 데이터 대비 (2^63-1까지) |
| DECIMAL(10,2) | 가격 관련 | 정확한 금액 계산 (부동소수점 오차 방지) |
| DECIMAL(8,2) | 영양소, 분량 | 정확한 소수점 계산 |
| TIMESTAMP | 시간 정보 | 시간대 포함 시각 저장 |
| JSONB | meal_plan_history | 유연한 구조 + 인덱싱 가능 |
| INET | IP 주소 | IP 주소 저장 및 검색 최적화 |

---

## 성능 최적화

### 인덱스 전략

#### 1. 단일 컬럼 인덱스
```sql
-- 자주 검색되는 컬럼
CREATE INDEX ix_users_email ON users(email);
CREATE INDEX ix_ingredients_name ON ingredients(name);
```

#### 2. 복합 인덱스
```sql
-- 함께 검색되는 컬럼들
CREATE INDEX ix_meal_plans_user_status ON meal_plans(user_id, status);
CREATE INDEX ix_meal_items_daily_meal_category ON meal_items(daily_meal_id, category, display_order);
```

#### 3. 유니크 인덱스
```sql
-- 중복 방지 + 검색 성능
CREATE UNIQUE INDEX uq_meal_plans_user_year_month ON meal_plans(user_id, year, month);
```

### 쿼리 성능 분석
```sql
-- 쿼리 실행 계획 확인
EXPLAIN ANALYZE
SELECT * FROM meal_plans WHERE user_id = 1 AND status = 'draft';

-- 느린 쿼리 로그 확인
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
```

---

## 백업 및 복구

### 백업
```bash
# 전체 데이터베이스 백업
pg_dump -U postgres nutritionist_menu_planner > backup_$(date +%Y%m%d).sql

# 압축 백업
pg_dump -U postgres nutritionist_menu_planner | gzip > backup_$(date +%Y%m%d).sql.gz

# Docker 환경
docker exec nutritionist-postgres pg_dump -U postgres nutritionist_menu_planner > backup.sql
```

### 복구
```bash
# SQL 파일로 복구
psql -U postgres nutritionist_menu_planner < backup_20260107.sql

# 압축 파일로 복구
gunzip -c backup_20260107.sql.gz | psql -U postgres nutritionist_menu_planner

# Docker 환경
docker exec -i nutritionist-postgres psql -U postgres nutritionist_menu_planner < backup.sql
```

---

## 트러블슈팅

### 1. 마이그레이션 실패

**증상**: `alembic upgrade head` 실패

**해결 방법**:
```bash
# 현재 상태 확인
poetry run alembic current

# 마이그레이션 히스토리 확인
poetry run alembic history

# 수동으로 리비전 테이블 확인
SELECT * FROM alembic_version;

# 강제로 특정 리비전으로 설정 (주의!)
poetry run alembic stamp 001
```

### 2. 데이터베이스 연결 실패

**증상**: `could not connect to server`

**해결 방법**:
1. PostgreSQL 서비스 실행 확인
2. `.env` 파일의 DATABASE_URL 확인
3. 방화벽/네트워크 설정 확인

### 3. 외래키 제약 조건 위반

**증상**: `violates foreign key constraint`

**해결 방법**:
```sql
-- 외래키 비활성화 (개발 전용)
ALTER TABLE table_name DISABLE TRIGGER ALL;

-- 데이터 수정 후 재활성화
ALTER TABLE table_name ENABLE TRIGGER ALL;
```

---

## 개발 워크플로우

### 1. 새로운 기능 개발 시
```bash
# 1. 모델 변경 (app/models/*.py)
# 2. 마이그레이션 생성
poetry run alembic revision --autogenerate -m "Add feature X"

# 3. 마이그레이션 파일 검토 및 수정
# 4. 마이그레이션 적용
poetry run alembic upgrade head

# 5. 테스트
poetry run pytest tests/test_models.py
```

### 2. 프로덕션 배포 시
```bash
# 1. 백업
pg_dump -U postgres nutritionist_menu_planner > backup_before_migration.sql

# 2. 마이그레이션 적용
poetry run alembic upgrade head

# 3. 검증
poetry run alembic current
```

---

## 다음 단계

Schema 구현 완료 후:
- **Phase 2**: Backend API 구현
  - FastAPI 라우터 작성
  - SQLAlchemy 모델 작성
  - Pydantic 스키마 작성

---

## 참고 문서
- [ERD.md](./ERD.md) - ERD 설계서
- [DOMAIN_MODEL.md](./DOMAIN_MODEL.md) - 도메인 모델 정의서
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
