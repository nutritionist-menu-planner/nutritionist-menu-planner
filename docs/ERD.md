# ERD 설계서 (Entity Relationship Diagram)

## 문서 목적
영양사 식단 자동 생성 플랫폼의 데이터베이스 구조를 시각화하고, 테이블 간 관계를 명확히 정의합니다.

---

## ERD 다이어그램

### dbdiagram.io 코드

아래 코드를 [dbdiagram.io](https://dbdiagram.io)에 붙여넣으면 ERD를 시각화할 수 있습니다.

```dbml
// 영양사 식단 자동 생성 플랫폼 ERD
// https://dbdiagram.io

// ============================================
// 1. 사용자 관리 (User Management)
// ============================================

Table users {
  id bigserial [pk, increment]
  email varchar(255) [unique, not null]
  password_hash varchar(255) [not null]
  name varchar(100) [not null]
  organization varchar(255) [note: '소속 기관']
  phone varchar(20)
  is_active boolean [default: true, not null]
  created_at timestamp [default: `now()`, not null]
  updated_at timestamp [default: `now()`, not null]
  last_login_at timestamp

  indexes {
    email [unique]
    is_active
  }

  note: '영양사 사용자 계정'
}

// ============================================
// 2. 식단 관리 (Meal Plan Management)
// ============================================

Table meal_plans {
  id bigserial [pk, increment]
  user_id bigint [ref: > users.id, not null]
  year integer [not null, note: '연도 (예: 2026)']
  month integer [not null, note: '월 (1-12)']
  name varchar(255) [not null]
  target_count integer [not null, note: '대상 인원 수']
  budget_per_person decimal(10,2) [note: '1인당 예산 (원)']
  total_budget decimal(12,2) [note: '총 예산 (원)']
  status varchar(20) [not null, default: 'draft', note: 'draft, confirmed, published']
  notes text
  created_at timestamp [default: `now()`, not null]
  updated_at timestamp [default: `now()`, not null]
  confirmed_at timestamp
  published_at timestamp

  indexes {
    (user_id, year, month) [unique]
    (user_id, status)
    created_at
  }

  note: '월별 식단표'
}

Table daily_meals {
  id bigserial [pk, increment]
  meal_plan_id bigint [ref: > meal_plans.id, not null]
  date date [not null]
  day_of_week varchar(10) [not null, note: 'Mon, Tue, Wed, ...']
  is_holiday boolean [default: false, not null]
  holiday_name varchar(100) [note: '공휴일명, 재량휴무 등']
  total_calories decimal(8,2) [note: '총 열량 (kcal)']
  total_price_per_person decimal(10,2) [note: '1인 총 가격 (원)']
  notes text
  created_at timestamp [default: `now()`, not null]
  updated_at timestamp [default: `now()`, not null]

  indexes {
    (meal_plan_id, date) [unique]
    date
  }

  note: '일일 식단'
}

Table meal_items {
  id bigserial [pk, increment]
  daily_meal_id bigint [ref: > daily_meals.id, not null]
  category varchar(20) [not null, note: 'rice, soup, side_dish, dessert']
  name varchar(255) [not null, note: '메뉴명']
  serving_size_g decimal(8,2) [not null, note: '1인분 분량 (g)']
  price_per_person decimal(10,2) [note: '1인분 가격 (원)']
  calories decimal(8,2) [note: '열량 (kcal)']
  cooking_method text [note: '조리 방법 (선택사항)']
  display_order integer [not null, default: 1]
  created_at timestamp [default: `now()`, not null]
  updated_at timestamp [default: `now()`, not null]

  indexes {
    (daily_meal_id, category, display_order)
  }

  note: '식단 구성 요소 (밥/국/반찬/후식)'
}

Table meal_item_ingredients {
  id bigserial [pk, increment]
  meal_item_id bigint [ref: > meal_items.id, not null]
  ingredient_id bigint [ref: > ingredients.id, not null]
  quantity_g decimal(8,2) [not null, note: '사용량 (g)']
  created_at timestamp [default: `now()`, not null]

  indexes {
    (meal_item_id, ingredient_id) [unique]
  }

  note: '식단 항목-식재료 매핑'
}

// ============================================
// 3. 식재료 관리 (Ingredient Management)
// ============================================

Table ingredients {
  id bigserial [pk, increment]
  name varchar(255) [unique, not null, note: '식재료명']
  name_normalized varchar(255) [not null, note: '정규화된 이름']
  category varchar(50) [not null, note: 'vegetable, meat, seafood, grain, etc.']
  unit varchar(20) [not null, note: 'g, kg, ml, l, ea']
  is_seasonal boolean [default: false, not null]
  seasonal_months varchar(50) [note: '제철 월 (예: "3,4,5,6")']
  supply_stability varchar(20) [not null, default: 'stable', note: 'stable, unstable, seasonal']
  origin varchar(100) [note: '원산지']
  storage_method varchar(100) [note: '보관 방법']
  created_at timestamp [default: `now()`, not null]
  updated_at timestamp [default: `now()`, not null]

  indexes {
    name [unique]
    name_normalized
    category
  }

  note: '식재료 마스터'
}

Table ingredient_substitutes {
  id bigserial [pk, increment]
  ingredient_id bigint [ref: > ingredients.id, not null]
  substitute_ingredient_id bigint [ref: > ingredients.id, not null]
  substitution_ratio decimal(5,2) [not null, default: 1.0, note: '대체 비율']
  notes text [note: '대체 시 주의사항']
  created_at timestamp [default: `now()`, not null]

  indexes {
    (ingredient_id, substitute_ingredient_id) [unique]
  }

  note: '대체 식재료 관계'
}

Table suppliers {
  id bigserial [pk, increment]
  name varchar(255) [not null]
  contact_person varchar(100)
  phone varchar(20)
  email varchar(255)
  address text
  business_number varchar(20) [note: '사업자등록번호']
  is_active boolean [default: true, not null]
  created_at timestamp [default: `now()`, not null]
  updated_at timestamp [default: `now()`, not null]

  indexes {
    is_active
  }

  note: '공급업체'
}

Table supplier_items {
  id bigserial [pk, increment]
  supplier_id bigint [ref: > suppliers.id, not null]
  ingredient_id bigint [ref: > ingredients.id, not null]
  price_per_unit decimal(10,2) [not null, note: '단가 (원)']
  unit_size decimal(8,2) [not null, note: '단위 크기 (g, kg 등)']
  availability_status varchar(20) [not null, default: 'available', note: 'available, out_of_stock, discontinued']
  min_order_quantity decimal(8,2) [note: '최소 주문량']
  delivery_days integer [note: '배송 소요일']
  updated_at timestamp [default: `now()`, not null]

  indexes {
    (supplier_id, ingredient_id) [unique]
    availability_status
  }

  note: '공급업체별 식재료 가격/재고'
}

// ============================================
// 4. 영양 정보 (Nutrition Information)
// ============================================

Table nutrition_info {
  id bigserial [pk, increment]
  ingredient_id bigint [ref: - ingredients.id, unique, not null]
  serving_size_g decimal(8,2) [not null, default: 100, note: '기준량 (100g 권장)']
  calories_kcal decimal(8,2) [not null, note: '열량 (kcal)']
  carbohydrate_g decimal(8,2) [not null, note: '탄수화물 (g)']
  protein_g decimal(8,2) [not null, note: '단백질 (g)']
  fat_g decimal(8,2) [not null, note: '지방 (g)']
  sodium_mg decimal(8,2) [not null, note: '나트륨 (mg)']
  sugar_g decimal(8,2) [note: '당류 (g)']
  saturated_fat_g decimal(8,2) [note: '포화지방 (g)']
  cholesterol_mg decimal(8,2) [note: '콜레스테롤 (mg)']
  dietary_fiber_g decimal(8,2) [note: '식이섬유 (g)']
  calcium_mg decimal(8,2) [note: '칼슘 (mg)']
  iron_mg decimal(8,2) [note: '철분 (mg)']
  vitamin_a_ug decimal(8,2) [note: '비타민 A (μg)']
  vitamin_c_mg decimal(8,2) [note: '비타민 C (mg)']
  data_source varchar(100) [note: '데이터 출처']
  updated_at timestamp [default: `now()`, not null]

  indexes {
    ingredient_id [unique]
  }

  note: '식재료별 영양 정보 (100g 기준)'
}

// ============================================
// 5. 알레르기 관리 (Allergen Management)
// ============================================

Table allergens {
  id bigserial [pk, increment]
  name varchar(100) [unique, not null, note: '알레르기명']
  name_en varchar(100) [note: '영문명']
  category varchar(50) [not null, note: 'food_allergy, religious, cultural']
  severity varchar(20) [not null, note: 'high, medium, low']
  description text
  is_mandatory_label boolean [default: false, not null, note: '식약처 필수 표시 대상']
  created_at timestamp [default: `now()`, not null]

  indexes {
    name [unique]
    category
  }

  note: '알레르기 유발 식품 (식약처 21종)'
}

Table ingredient_allergens {
  id bigserial [pk, increment]
  ingredient_id bigint [ref: > ingredients.id, not null]
  allergen_id bigint [ref: > allergens.id, not null]
  contamination_level varchar(20) [not null, note: 'contains, may_contain, traces']
  notes text
  created_at timestamp [default: `now()`, not null]

  indexes {
    (ingredient_id, allergen_id) [unique]
    allergen_id
  }

  note: '식재료-알레르기 매핑'
}

// ============================================
// 6. 이력 관리 (History Management)
// ============================================

Table meal_plan_history {
  id bigserial [pk, increment]
  meal_plan_id bigint [ref: > meal_plans.id, not null]
  meal_item_id bigint [ref: > meal_items.id, note: '수정된 항목 (nullable)']
  user_id bigint [ref: > users.id, not null]
  action_type varchar(50) [not null, note: 'generate, edit_menu, edit_ingredient, regenerate, confirm, publish']
  changed_at timestamp [default: `now()`, not null]
  before_value jsonb [note: '변경 전 값']
  after_value jsonb [note: '변경 후 값']
  reason text [note: '변경 사유']

  indexes {
    meal_plan_id
    (meal_plan_id, changed_at)
    user_id
  }

  note: '식단 변경 이력'
}

// ============================================
// 7. 사용자 활동 추적 (User Activity Tracking)
// ============================================

Table user_activity_log {
  id bigserial [pk, increment]
  user_id bigint [ref: > users.id, not null]
  activity_type varchar(50) [not null, note: 'login, view, create, edit, upload']
  activity_at timestamp [default: `now()`, not null]
  ip_address inet
  user_agent text

  indexes {
    user_id
    activity_at
    activity_type
  }

  note: 'MAU 추적용 사용자 활동 로그'
}

Table user_favorites {
  id bigserial [pk, increment]
  user_id bigint [ref: > users.id, not null]
  item_type varchar(50) [not null, note: 'meal_item, ingredient']
  item_id bigint [not null]
  added_at timestamp [default: `now()`, not null]
  usage_count integer [default: 0, not null]

  indexes {
    (user_id, item_type, item_id) [unique]
    user_id
  }

  note: '즐겨찾기 (재사용률 추적)'
}

// ============================================
// 8. KPI 집계 테이블 (KPI Aggregation)
// ============================================

Table monthly_active_users {
  id bigserial [pk, increment]
  year_month date [not null, note: 'YYYY-MM-01 형식']
  total_active_users integer [not null]
  new_users integer [not null]
  returning_users integer [not null]
  churned_users integer [not null]
  created_at timestamp [default: `now()`, not null]

  indexes {
    year_month [unique]
  }

  note: '월간 활성 사용자 집계'
}

Table meal_plan_time_tracking {
  id bigserial [pk, increment]
  meal_plan_id bigint [ref: - meal_plans.id, unique, not null]
  user_id bigint [ref: > users.id, not null]
  started_at timestamp [not null]
  generated_at timestamp
  confirmed_at timestamp
  total_edit_time_seconds integer [note: '총 수정 시간 (초)']
  baseline_time_hours decimal(5,2) [note: '기존 방식 소요 시간 (시간)']

  indexes {
    meal_plan_id [unique]
    user_id
  }

  note: '식단 편성 시간 추적'
}

Table meal_plan_reuse_tracking {
  id bigserial [pk, increment]
  meal_plan_id bigint [ref: > meal_plans.id, not null]
  user_id bigint [ref: > users.id, not null]
  reuse_type varchar(50) [not null, note: 'copy, menu_reuse, favorite, pattern']
  source_meal_plan_id bigint [ref: > meal_plans.id]
  source_item_id bigint
  reused_at timestamp [default: `now()`, not null]

  indexes {
    meal_plan_id
    user_id
  }

  note: '재사용률 추적'
}
```

---

## Task 1-2-1: 핵심 테이블 목록 및 역할 정의

### 1. 사용자 관리 (User Management)

#### users (영양사 계정)
**역할**: 플랫폼 사용자 (영양사) 인증 및 관리

**핵심 컬럼**:
- `email`: 로그인 ID (유니크)
- `password_hash`: 암호화된 비밀번호
- `organization`: 소속 기관
- `is_active`: 계정 활성화 여부

**비즈니스 규칙**:
- 이메일 중복 불가
- 비밀번호는 bcrypt로 해시화
- 탈퇴 시 `is_active = false` (Soft delete)

---

### 2. 식단 관리 (Meal Plan Management)

#### meal_plans (월별 식단표)
**역할**: 월 단위 식단표 메타데이터 관리

**핵심 컬럼**:
- `user_id`: 작성자 (영양사)
- `year`, `month`: 식단 연월
- `status`: 상태 (draft, confirmed, published)
- `target_count`: 대상 인원
- `budget_per_person`, `total_budget`: 예산 정보

**비즈니스 규칙**:
- 한 영양사는 같은 연월에 하나의 식단표만 생성 가능
- 상태 전이: draft → confirmed → published

#### daily_meals (일일 식단)
**역할**: 특정 날짜의 식단 관리

**핵심 컬럼**:
- `meal_plan_id`: 소속 식단표
- `date`: 급식 날짜
- `is_holiday`: 휴무일 여부
- `total_calories`, `total_price_per_person`: 집계 정보

**비즈니스 규칙**:
- 한 식단표에서 날짜는 유니크
- 휴무일에는 meal_item이 없음

#### meal_items (식단 구성 요소)
**역할**: 밥/국/반찬/후식 개별 항목 관리

**핵심 컬럼**:
- `daily_meal_id`: 소속 일일 식단
- `category`: 카테고리 (rice, soup, side_dish, dessert)
- `name`: 메뉴명
- `serving_size_g`: 1인분 분량
- `display_order`: 표시 순서

**비즈니스 규칙**:
- 카테고리별로 최소 1개 이상 (dessert 제외)
- display_order로 UI 정렬

#### meal_item_ingredients (식단 항목-식재료 매핑)
**역할**: 메뉴의 레시피 구성 (어떤 식재료를 얼마나 사용하는지)

**핵심 컬럼**:
- `meal_item_id`: 식단 항목
- `ingredient_id`: 사용 식재료
- `quantity_g`: 사용량

**비즈니스 규칙**:
- 한 메뉴에 같은 식재료 중복 불가
- 영양소 및 가격 계산의 기준 데이터

---

### 3. 식재료 관리 (Ingredient Management)

#### ingredients (식재료 마스터)
**역할**: 식재료 기본 정보 관리

**핵심 컬럼**:
- `name`: 식재료명 (유니크)
- `name_normalized`: 정규화된 이름 (중복 검사용)
- `category`: 카테고리 (vegetable, meat, seafood, grain, dairy, seasoning, processed, other)
- `supply_stability`: 수급 안정성 (stable, unstable, seasonal)

**비즈니스 규칙**:
- 이름 중복 불가
- 정규화된 이름으로 유사 식재료 검색

#### ingredient_substitutes (대체 식재료)
**역할**: 식재료 대체 관계 관리

**핵심 컬럼**:
- `ingredient_id`: 원 식재료
- `substitute_ingredient_id`: 대체 식재료
- `substitution_ratio`: 대체 비율 (1.0 = 1:1)

**비즈니스 규칙**:
- 원 식재료와 대체 식재료는 다른 ID
- 양방향 관계 가능 (A→B, B→A 모두 등록)

#### suppliers (공급업체)
**역할**: 식재료 공급업체 정보 관리

**핵심 컬럼**:
- `name`: 업체명
- `contact_person`: 담당자
- `is_active`: 활성 상태

#### supplier_items (공급업체별 식재료)
**역할**: 공급업체별 가격 및 재고 정보

**핵심 컬럼**:
- `supplier_id`: 공급업체
- `ingredient_id`: 식재료
- `price_per_unit`: 단가
- `availability_status`: 재고 상태 (available, out_of_stock, discontinued)

**비즈니스 규칙**:
- 같은 업체-식재료 조합은 하나만
- 가격 계산 시 최저가 우선

---

### 4. 영양 정보 (Nutrition Information)

#### nutrition_info (영양 정보)
**역할**: 식재료별 영양소 정보 저장

**핵심 컬럼**:
- `ingredient_id`: 식재료 (1:1 관계)
- `serving_size_g`: 기준량 (100g 권장)
- `calories_kcal`, `carbohydrate_g`, `protein_g`, `fat_g`, `sodium_mg`: 필수 영양소
- 선택 영양소: sugar, saturated_fat, cholesterol, dietary_fiber, calcium, iron, vitamins

**비즈니스 규칙**:
- 100g 기준으로 저장 (계산 편의성)
- 1인분 영양소 = (영양소/100g) × 1인분 분량(g)

---

### 5. 알레르기 관리 (Allergen Management)

#### allergens (알레르기 유발 식품)
**역할**: 알레르기 유발 물질 마스터

**핵심 컬럼**:
- `name`: 알레르기명 (유니크)
- `category`: 카테고리 (food_allergy, religious, cultural)
- `severity`: 심각도 (high, medium, low)
- `is_mandatory_label`: 식약처 필수 표시 대상

**비즈니스 규칙**:
- 식약처 21종은 시드 데이터로 제공
- 커스텀 알레르기 추가 가능

#### ingredient_allergens (식재료-알레르기 매핑)
**역할**: 식재료별 알레르기 정보

**핵심 컬럼**:
- `ingredient_id`: 식재료
- `allergen_id`: 알레르기
- `contamination_level`: 오염 수준 (contains, may_contain, traces)

**비즈니스 규칙**:
- contains: 반드시 제외
- may_contain: 사용자 설정에 따라 제외 여부 결정
- traces: 미량, 일반적으로 허용

---

### 6. 이력 관리 (History Management)

#### meal_plan_history (식단 변경 이력)
**역할**: 식단 수정 이력 추적

**핵심 컬럼**:
- `meal_plan_id`: 식단표
- `meal_item_id`: 수정된 항목 (nullable)
- `action_type`: 액션 유형 (generate, edit_menu, edit_ingredient, regenerate, confirm, publish)
- `before_value`, `after_value`: 변경 전후 값 (JSONB)
- `reason`: 변경 사유

**비즈니스 규칙**:
- 모든 변경 사항은 자동 기록
- JSONB로 유연한 데이터 구조 지원

---

### 7. 사용자 활동 추적 (User Activity Tracking)

#### user_activity_log (사용자 활동 로그)
**역할**: MAU 계산용 활동 로그

**핵심 컬럼**:
- `user_id`: 사용자
- `activity_type`: 활동 유형 (login, view, create, edit, upload)
- `activity_at`: 활동 시각

**비즈니스 규칙**:
- 월간 활성 사용자 집계에 사용
- 개인정보 보호를 위해 2년 후 자동 삭제

#### user_favorites (즐겨찾기)
**역할**: 재사용률 추적

**핵심 컬럼**:
- `user_id`: 사용자
- `item_type`: 항목 유형 (meal_item, ingredient)
- `item_id`: 항목 ID
- `usage_count`: 사용 횟수

**비즈니스 규칙**:
- 즐겨찾기 추가 시 재사용 의도로 간주
- usage_count로 인기도 추적

---

### 8. KPI 집계 테이블 (KPI Aggregation)

#### monthly_active_users (월간 활성 사용자)
**역할**: MAU 집계 데이터 저장

**핵심 컬럼**:
- `year_month`: 연월 (YYYY-MM-01)
- `total_active_users`: 총 활성 사용자
- `new_users`: 신규 가입자
- `returning_users`: 재방문 사용자
- `churned_users`: 이탈 사용자

**비즈니스 규칙**:
- 매월 1일 자동 집계
- user_activity_log 기반 계산

#### meal_plan_time_tracking (식단 편성 시간 추적)
**역할**: 식단 편성 시간 감소율 측정

**핵심 컬럼**:
- `meal_plan_id`: 식단표 (1:1)
- `started_at`: 시작 시각
- `generated_at`: 생성 완료 시각
- `confirmed_at`: 확정 시각
- `total_edit_time_seconds`: 총 수정 시간
- `baseline_time_hours`: 기존 방식 소요 시간

**비즈니스 규칙**:
- 식단 생성 시 자동 기록
- KPI 계산에 사용

#### meal_plan_reuse_tracking (재사용률 추적)
**역할**: 식단 재사용 행동 추적

**핵심 컬럼**:
- `meal_plan_id`: 식단표
- `reuse_type`: 재사용 유형 (copy, menu_reuse, favorite, pattern)
- `source_meal_plan_id`: 원본 식단 (복사인 경우)

**비즈니스 규칙**:
- 재사용 행동 발생 시 자동 기록
- 재사용률 KPI 계산에 사용

---

## Task 1-2-2: 테이블 간 관계 정의

### 1:N 관계 (One-to-Many)

| Parent (1) | Child (N) | 관계 설명 | CASCADE 규칙 |
|-----------|----------|----------|-------------|
| users | meal_plans | 한 영양사는 여러 식단표 작성 | ON DELETE CASCADE |
| meal_plans | daily_meals | 한 식단표는 여러 일일 식단 포함 | ON DELETE CASCADE |
| daily_meals | meal_items | 한 일일 식단은 여러 메뉴 항목 포함 | ON DELETE CASCADE |
| meal_items | meal_item_ingredients | 한 메뉴 항목은 여러 식재료 사용 | ON DELETE CASCADE |
| ingredients | ingredient_allergens | 한 식재료는 여러 알레르기 포함 가능 | ON DELETE CASCADE |
| suppliers | supplier_items | 한 공급업체는 여러 식재료 공급 | ON DELETE CASCADE |
| users | user_favorites | 한 사용자는 여러 즐겨찾기 보유 | ON DELETE CASCADE |

### N:M 관계 (Many-to-Many)

| Entity A | Entity B | Junction Table | 설명 |
|---------|---------|----------------|------|
| meal_items | ingredients | meal_item_ingredients | 메뉴-식재료 다대다 관계 |
| ingredients | allergens | ingredient_allergens | 식재료-알레르기 다대다 관계 |
| suppliers | ingredients | supplier_items | 공급업체-식재료 다대다 관계 |

### 1:1 관계 (One-to-One)

| Table A | Table B | 관계 설명 |
|---------|---------|----------|
| ingredients | nutrition_info | 한 식재료는 하나의 영양 정보 보유 |
| meal_plans | meal_plan_time_tracking | 한 식단표는 하나의 시간 추적 레코드 |

### 자기 참조 관계 (Self-Referencing)

| Table | 관계 설명 |
|-------|----------|
| ingredients | ingredient_substitutes를 통한 대체 식재료 관계 |

---

## Task 1-2-3: 식단 이력 관리 구조 설계

### 이력 관리 방식: Snapshot 방식

**선택 사유**:
- Event Sourcing 대비 단순한 구현
- 변경 전후 비교가 용이
- JSONB로 유연한 데이터 구조

### meal_plan_history 상세 설계

#### action_type 정의

| Action Type | 설명 | before_value | after_value |
|------------|------|--------------|-------------|
| `generate` | 식단 자동 생성 | null | {meal_plan_id, config} |
| `edit_menu` | 메뉴 변경 | {old_menu_name} | {new_menu_name} |
| `edit_ingredient` | 식재료 변경 | {old_ingredients[]} | {new_ingredients[]} |
| `regenerate` | 식단 재생성 | {old_meal_items[]} | {new_meal_items[]} |
| `confirm` | 식단 확정 | {status: 'draft'} | {status: 'confirmed'} |
| `publish` | 식단 배포 | {status: 'confirmed'} | {status: 'published'} |

#### JSONB 스키마 예시

```json
// edit_menu 예시
{
  "meal_item_id": 123,
  "daily_meal_id": 45,
  "date": "2026-01-15",
  "category": "side_dish",
  "before": {
    "name": "감자조림",
    "ingredients": [
      {"id": 10, "name": "감자", "quantity_g": 150}
    ]
  },
  "after": {
    "name": "당근조림",
    "ingredients": [
      {"id": 11, "name": "당근", "quantity_g": 120}
    ]
  }
}
```

### 롤백 가능 여부

**현재 설계**: 롤백 미지원 (MVP)

**이유**:
- 복잡도 증가
- 영양사의 최종 승인을 전제로 함
- 필요 시 이력 참고하여 수동 복원 가능

**향후 확장**:
- Phase 2에서 "이전 버전으로 복원" 기능 추가 검토
- `meal_plan_history`의 `before_value`를 이용한 롤백 구현

---

## Task 1-2-4: ERD 다이어그램 작성 및 리뷰

### ERD 시각화 방법

1. **온라인 도구 사용 (권장)**
   - https://dbdiagram.io 접속
   - 위의 dbdiagram.io 코드 복사
   - 붙여넣기 → 자동으로 ERD 생성

2. **로컬 도구 사용**
   - draw.io (https://app.diagrams.net/)
   - ERDPlus (https://erdplus.com/)
   - MySQL Workbench

### ERD 저장

생성된 ERD 이미지는 `docs/images/ERD.png`에 저장 예정

---

## 데이터베이스 제약 조건 정리

### Primary Keys
- 모든 테이블: `id BIGSERIAL PRIMARY KEY`

### Foreign Keys with CASCADE

```sql
-- 예시: meal_plans → users
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE

-- 예시: daily_meals → meal_plans
FOREIGN KEY (meal_plan_id) REFERENCES meal_plans(id) ON DELETE CASCADE
```

### Unique Constraints

| Table | Unique Constraint | 설명 |
|-------|------------------|------|
| users | email | 이메일 중복 방지 |
| meal_plans | (user_id, year, month) | 영양사별 연월 중복 방지 |
| daily_meals | (meal_plan_id, date) | 식단표별 날짜 중복 방지 |
| ingredients | name | 식재료명 중복 방지 |
| nutrition_info | ingredient_id | 1:1 관계 보장 |
| allergens | name | 알레르기명 중복 방지 |

### Check Constraints

```sql
-- meal_plans
CHECK (month >= 1 AND month <= 12)
CHECK (target_count > 0)
CHECK (budget_per_person >= 0)
CHECK (status IN ('draft', 'confirmed', 'published'))

-- meal_items
CHECK (serving_size_g > 0)
CHECK (price_per_person >= 0)
CHECK (category IN ('rice', 'soup', 'side_dish', 'dessert'))

-- ingredients
CHECK (category IN ('vegetable', 'meat', 'seafood', 'grain', 'dairy', 'seasoning', 'processed', 'other'))
CHECK (supply_stability IN ('stable', 'unstable', 'seasonal'))

-- nutrition_info
CHECK (serving_size_g > 0)
CHECK (calories_kcal >= 0)
-- 모든 영양소 >= 0

-- allergens
CHECK (severity IN ('high', 'medium', 'low'))
CHECK (category IN ('food_allergy', 'religious', 'cultural'))

-- ingredient_allergens
CHECK (contamination_level IN ('contains', 'may_contain', 'traces'))
```

### Indexes

성능 최적화를 위한 주요 인덱스:

```sql
-- 조회 성능
CREATE INDEX idx_meal_plans_user_status ON meal_plans(user_id, status);
CREATE INDEX idx_daily_meals_date ON daily_meals(date);
CREATE INDEX idx_meal_items_category ON meal_items(daily_meal_id, category, display_order);

-- 검색 성능
CREATE INDEX idx_ingredients_normalized ON ingredients(name_normalized);
CREATE INDEX idx_ingredients_category ON ingredients(category);

-- 집계 성능
CREATE INDEX idx_user_activity_log_user_date ON user_activity_log(user_id, activity_at);
CREATE INDEX idx_meal_plan_history_plan_date ON meal_plan_history(meal_plan_id, changed_at);
```

---

## 다음 단계

Epic 1-2 완료 후:
- **Epic 1-3**: PostgreSQL 스키마 구현
  - DDL 스크립트 작성
  - Alembic 마이그레이션 설정
  - 시드 데이터 준비

---

## 참고 문서
- [DOMAIN_MODEL.md](./DOMAIN_MODEL.md) - 도메인 모델 정의서
- [task.md](./task.md) - 개발 Task 관리
