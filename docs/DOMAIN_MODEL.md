# 도메인 모델 정의서 (Domain Model Definition)

## 문서 목적
영양사 식단 자동 생성 플랫폼의 핵심 비즈니스 도메인을 데이터 구조로 변환하여 정의합니다.

---

## 도메인 개요

본 시스템은 다음과 같은 핵심 도메인으로 구성됩니다:

### 1. 식단 관리 도메인 (Meal Plan Management)
- **Meal Plan** (식단표): 월 단위 식단표
- **Daily Meal** (일일 식단): 특정 날짜의 식단
- **Meal Item** (식단 구성 요소): 밥/국/반찬 개별 항목

### 2. 식재료 관리 도메인 (Ingredient Management)
- **Ingredient** (식재료): 식재료 마스터 데이터
- **Supplier** (공급업체): 식재료 공급업체
- **Supplier Item** (공급업체 식재료): 공급업체별 가격 및 재고 정보

### 3. 영양 정보 도메인 (Nutrition Information)
- **Nutrition Info** (영양 정보): 식재료 및 메뉴의 영양소 정보

### 4. 알레르기 관리 도메인 (Allergen Management)
- **Allergen** (알레르기 유발 식품): 알레르기 유발 물질
- **Ingredient Allergen** (식재료-알레르기 매핑): 식재료별 알레르기 정보

### 5. 사용자 관리 도메인 (User Management)
- **User** (영양사): 플랫폼 사용자 (영양사)

### 6. 이력 관리 도메인 (History Management)
- **Meal Plan History** (식단 변경 이력): 식단 수정 이력 추적

---

## 엔티티 관계도 (Entity Relationship)

```
User (영양사)
  │
  ├─── has many ──→ Meal Plan (식단표)
  │                      │
  │                      ├─── has many ──→ Daily Meal (일일 식단)
  │                      │                       │
  │                      │                       └─── has many ──→ Meal Item (식단 항목)
  │                      │                                              │
  │                      │                                              └─── references ──→ Ingredient
  │                      │
  │                      └─── has many ──→ Meal Plan History (식단 이력)
  │
  └─── has many ──→ User Favorites (즐겨찾기)

Ingredient (식재료)
  │
  ├─── has one ──→ Nutrition Info (영양 정보)
  │
  ├─── has many ──→ Ingredient Allergen (알레르기 매핑)
  │                       │
  │                       └─── references ──→ Allergen (알레르기)
  │
  └─── has many ──→ Supplier Item (공급업체 식재료)
                          │
                          └─── references ──→ Supplier (공급업체)
```

---

## 핵심 비즈니스 규칙

### 1. 식단 생성 규칙
- 하나의 식단표(Meal Plan)는 특정 연월(year-month)에 대응
- 하나의 일일 식단(Daily Meal)은 하나의 날짜에만 존재
- 휴무일에는 일일 식단이 생성되지 않음
- 식단 상태: `draft` (초안) → `confirmed` (확정) → `published` (배포)

### 2. 식단 구성 규칙
- 하나의 일일 식단은 여러 Meal Item으로 구성
- Meal Item의 카테고리: `rice` (밥), `soup` (국), `side_dish` (반찬), `dessert` (후식)
- 각 카테고리별로 최소 1개 이상의 항목 필요 (dessert 제외)

### 3. 영양소 계산 규칙
- 영양 정보는 100g 기준으로 저장
- 1인분 영양소는 `(영양소/100g) × 1인분 분량(g)` 로 계산
- 일일 영양소 합계는 모든 Meal Item의 합

### 4. 알레르기 필터링 규칙
- 사용자가 제외할 알레르기 목록 지정 가능
- 해당 알레르기 포함 식재료는 자동 생성 시 제외
- 수동 추가 시 경고 표시

### 5. 가격 계산 규칙
- 1인분 가격은 공급업체 가격 기준
- 여러 공급업체가 있는 경우 최저가 우선
- 공급 불가능한 식재료는 가격 계산에서 제외

### 6. 데이터 소유권 규칙
- 모든 식단 데이터는 생성한 영양사에게 귀속
- 다른 영양사의 데이터는 조회 불가
- 공유 기능은 MVP에서 제외 (향후 확장)

---

## 엔티티 상세 정의

각 엔티티의 상세 정의는 아래 문서를 참조하세요:

### Task 1-1-1: Meal Plan (식단표)
[상세 정의 보기](#task-1-1-1-meal-plan-entity)

### Task 1-1-2: Meal Item (식단 구성 요소)
[상세 정의 보기](#task-1-1-2-meal-item-entity)

### Task 1-1-3: Ingredient (식재료)
[상세 정의 보기](#task-1-1-3-ingredient-entity)

### Task 1-1-4: Nutrition Info (영양 정보)
[상세 정의 보기](#task-1-1-4-nutrition-info-structure)

### Task 1-1-5: Allergen (알레르기)
[상세 정의 보기](#task-1-1-5-allergen-model)

---

## Task 1-1-1: Meal Plan Entity

### 비즈니스 요구사항
- 영양사는 월 단위로 식단표를 생성
- 식단표는 초안(draft), 확정(confirmed), 배포(published) 상태를 가짐
- 식단표는 대상 인원 수, 예산 정보를 포함
- 식단표 생성 시점과 최종 수정 시점 추적 필요

### 데이터 모델

#### Meal Plan (식단표)
| 속성명 | 타입 | 필수 | 설명 |
|--------|------|------|------|
| id | BIGINT | Y | 기본키 |
| user_id | BIGINT | Y | 작성자 (영양사) FK |
| year | INTEGER | Y | 연도 (예: 2026) |
| month | INTEGER | Y | 월 (1-12) |
| name | VARCHAR(255) | Y | 식단표 이름 (예: "2026년 1월 급식 식단") |
| target_count | INTEGER | Y | 대상 인원 수 |
| budget_per_person | DECIMAL(10,2) | N | 1인당 예산 (원) |
| total_budget | DECIMAL(12,2) | N | 총 예산 (원) |
| status | VARCHAR(20) | Y | 상태 (draft, confirmed, published) |
| notes | TEXT | N | 비고 |
| created_at | TIMESTAMP | Y | 생성일시 |
| updated_at | TIMESTAMP | Y | 수정일시 |
| confirmed_at | TIMESTAMP | N | 확정일시 |
| published_at | TIMESTAMP | N | 배포일시 |

**제약 조건**:
- `(user_id, year, month)` 조합은 유니크 (한 영양사는 같은 연월에 하나의 식단표만 생성)
- `status` 는 ENUM: `'draft'`, `'confirmed'`, `'published'`
- `month` 는 1-12 사이 값 (CHECK 제약)
- `target_count` > 0
- `budget_per_person` >= 0
- `total_budget` >= 0

**인덱스**:
- PRIMARY KEY: `id`
- INDEX: `(user_id, year, month)`
- INDEX: `(user_id, status)`
- INDEX: `created_at`

#### Daily Meal (일일 식단)
| 속성명 | 타입 | 필수 | 설명 |
|--------|------|------|------|
| id | BIGINT | Y | 기본키 |
| meal_plan_id | BIGINT | Y | 식단표 FK |
| date | DATE | Y | 급식 날짜 |
| day_of_week | VARCHAR(10) | Y | 요일 (Mon, Tue, ...) |
| is_holiday | BOOLEAN | Y | 휴무일 여부 |
| holiday_name | VARCHAR(100) | N | 휴무일 이름 (공휴일, 재량휴무 등) |
| total_calories | DECIMAL(8,2) | N | 총 열량 (kcal) |
| total_price_per_person | DECIMAL(10,2) | N | 1인 총 가격 (원) |
| notes | TEXT | N | 비고 |
| created_at | TIMESTAMP | Y | 생성일시 |
| updated_at | TIMESTAMP | Y | 수정일시 |

**제약 조건**:
- `(meal_plan_id, date)` 조합은 유니크
- `is_holiday` 가 TRUE면 Meal Item이 없어야 함 (애플리케이션 레벨 체크)

**인덱스**:
- PRIMARY KEY: `id`
- UNIQUE INDEX: `(meal_plan_id, date)`
- INDEX: `date`

### 상태 전이도

```
[draft] ──확정──→ [confirmed] ──배포──→ [published]
   ↑                   ↓                    ↓
   └─────────수정─────┘                    │
   └────────────────────수정(재배포)───────┘
```

### 비즈니스 로직

#### 1. 식단 생성
```python
def create_meal_plan(user_id: int, year: int, month: int, config: dict) -> MealPlan:
    """
    새로운 식단표 생성

    1. 연월 중복 체크
    2. 공휴일 및 주말 계산
    3. 급식일 목록 생성
    4. 각 급식일에 대해 Daily Meal 생성 (is_holiday=False)
    5. 상태는 'draft'로 초기화
    """
    pass
```

#### 2. 식단 확정
```python
def confirm_meal_plan(meal_plan_id: int) -> MealPlan:
    """
    식단표 확정

    1. 모든 Daily Meal에 Meal Item이 있는지 확인
    2. 영양 기준 충족 여부 확인
    3. 예산 초과 여부 확인
    4. 상태를 'confirmed'로 변경
    5. confirmed_at 시각 기록
    """
    pass
```

#### 3. 식단 배포
```python
def publish_meal_plan(meal_plan_id: int) -> MealPlan:
    """
    식단표 배포

    1. 상태가 'confirmed'인지 확인
    2. 상태를 'published'로 변경
    3. published_at 시각 기록
    4. (선택) 외부 시스템 연동 (발주, 게시판 등)
    """
    pass
```

---

## Task 1-1-2: Meal Item Entity

### 비즈니스 요구사항
- 일일 식단은 밥, 국, 반찬, 후식으로 구성
- 각 항목은 1인분 기준 분량과 가격 정보를 포함
- 조리 방법 정보 포함 여부는 선택사항 (MVP에서는 단순 메뉴명만)

### 데이터 모델

#### Meal Item (식단 구성 요소)
| 속성명 | 타입 | 필수 | 설명 |
|--------|------|------|------|
| id | BIGINT | Y | 기본키 |
| daily_meal_id | BIGINT | Y | 일일 식단 FK |
| category | VARCHAR(20) | Y | 카테고리 (rice, soup, side_dish, dessert) |
| name | VARCHAR(255) | Y | 메뉴명 (예: "백미밥", "된장찌개") |
| serving_size_g | DECIMAL(8,2) | Y | 1인분 분량 (그램) |
| price_per_person | DECIMAL(10,2) | N | 1인분 가격 (원) |
| calories | DECIMAL(8,2) | N | 열량 (kcal) |
| cooking_method | TEXT | N | 조리 방법 (선택사항, MVP 제외) |
| display_order | INTEGER | Y | 표시 순서 (1, 2, 3, ...) |
| created_at | TIMESTAMP | Y | 생성일시 |
| updated_at | TIMESTAMP | Y | 수정일시 |

**제약 조건**:
- `category` 는 ENUM: `'rice'`, `'soup'`, `'side_dish'`, `'dessert'`
- `serving_size_g` > 0
- `price_per_person` >= 0
- `calories` >= 0
- `display_order` >= 1

**인덱스**:
- PRIMARY KEY: `id`
- INDEX: `(daily_meal_id, category, display_order)`

#### Meal Item Ingredient (식단 항목-식재료 매핑)
| 속성명 | 타입 | 필수 | 설명 |
|--------|------|------|------|
| id | BIGINT | Y | 기본키 |
| meal_item_id | BIGINT | Y | 식단 항목 FK |
| ingredient_id | BIGINT | Y | 식재료 FK |
| quantity_g | DECIMAL(8,2) | Y | 사용량 (그램) |
| created_at | TIMESTAMP | Y | 생성일시 |

**제약 조건**:
- `(meal_item_id, ingredient_id)` 조합은 유니크
- `quantity_g` > 0

**인덱스**:
- PRIMARY KEY: `id`
- UNIQUE INDEX: `(meal_item_id, ingredient_id)`

### 카테고리별 기본 분량 가이드

| 카테고리 | 기본 분량 (g) | 설명 |
|----------|--------------|------|
| rice | 210 | 백미밥 기준 1공기 |
| soup | 200-300 | 국/찌개 1인분 |
| side_dish | 50-100 | 반찬 1인분 (메뉴에 따라 상이) |
| dessert | 100-150 | 후식 (과일, 음료 등) |

### 비즈니스 로직

#### 1. 메뉴 항목 추가
```python
def add_meal_item(
    daily_meal_id: int,
    category: str,
    name: str,
    ingredients: list[dict]  # [{"ingredient_id": 1, "quantity_g": 100}, ...]
) -> MealItem:
    """
    일일 식단에 메뉴 항목 추가

    1. 카테고리 유효성 검증
    2. Meal Item 생성
    3. 각 식재료에 대해 Meal Item Ingredient 생성
    4. 영양소 자동 계산 (각 식재료 영양소 × 사용량 합산)
    5. 가격 자동 계산 (각 식재료 가격 × 사용량 합산)
    6. Daily Meal의 총 열량 및 가격 업데이트
    """
    pass
```

#### 2. 메뉴 항목 수정
```python
def update_meal_item(
    meal_item_id: int,
    ingredients: list[dict] = None,
    **kwargs
) -> MealItem:
    """
    메뉴 항목 수정

    1. Meal Item 정보 업데이트
    2. 식재료 변경 시 Meal Item Ingredient 재생성
    3. 영양소 및 가격 재계산
    4. Daily Meal의 총 열량 및 가격 업데이트
    5. Meal Plan History 기록
    """
    pass
```

---

## Task 1-1-3: Ingredient Entity

### 비즈니스 요구사항
- 식재료 마스터 데이터 관리
- 대체 식재료 관계 설정 (예: 닭고기 → 두부)
- 계절성 및 수급 안정성 속성 포함

### 데이터 모델

#### Ingredient (식재료)
| 속성명 | 타입 | 필수 | 설명 |
|--------|------|------|------|
| id | BIGINT | Y | 기본키 |
| name | VARCHAR(255) | Y | 식재료명 (예: "당근(국내산)") |
| name_normalized | VARCHAR(255) | Y | 정규화된 이름 (예: "당근") |
| category | VARCHAR(50) | Y | 카테고리 (vegetable, meat, seafood, grain, etc.) |
| unit | VARCHAR(20) | Y | 단위 (g, kg, ea) |
| is_seasonal | BOOLEAN | Y | 계절성 여부 |
| seasonal_months | VARCHAR(50) | N | 제철 월 (예: "3,4,5,6" → 3-6월) |
| supply_stability | VARCHAR(20) | Y | 수급 안정성 (stable, unstable, seasonal) |
| origin | VARCHAR(100) | N | 원산지 (예: "국내산", "미국산") |
| storage_method | VARCHAR(100) | N | 보관 방법 |
| created_at | TIMESTAMP | Y | 생성일시 |
| updated_at | TIMESTAMP | Y | 수정일시 |

**제약 조건**:
- `name` 은 유니크
- `category` 는 ENUM: `'vegetable'`, `'meat'`, `'seafood'`, `'grain'`, `'dairy'`, `'seasoning'`, `'processed'`, `'other'`
- `unit` 는 ENUM: `'g'`, `'kg'`, `'ml'`, `'l'`, `'ea'`
- `supply_stability` 는 ENUM: `'stable'`, `'unstable'`, `'seasonal'`

**인덱스**:
- PRIMARY KEY: `id`
- UNIQUE INDEX: `name`
- INDEX: `name_normalized`
- INDEX: `category`

#### Ingredient Substitute (대체 식재료)
| 속성명 | 타입 | 필수 | 설명 |
|--------|------|------|------|
| id | BIGINT | Y | 기본키 |
| ingredient_id | BIGINT | Y | 원 식재료 FK |
| substitute_ingredient_id | BIGINT | Y | 대체 식재료 FK |
| substitution_ratio | DECIMAL(5,2) | Y | 대체 비율 (1.0 = 1:1) |
| notes | TEXT | N | 대체 시 주의사항 |
| created_at | TIMESTAMP | Y | 생성일시 |

**제약 조건**:
- `(ingredient_id, substitute_ingredient_id)` 조합은 유니크
- `ingredient_id` ≠ `substitute_ingredient_id`
- `substitution_ratio` > 0

**인덱스**:
- PRIMARY KEY: `id`
- UNIQUE INDEX: `(ingredient_id, substitute_ingredient_id)`

### 카테고리 정의

| 카테고리 | 설명 | 예시 |
|----------|------|------|
| vegetable | 채소류 | 당근, 양파, 배추, 감자 |
| meat | 육류 | 쇠고기, 돼지고기, 닭고기 |
| seafood | 수산물 | 고등어, 멸치, 오징어 |
| grain | 곡물류 | 쌀, 밀가루, 보리 |
| dairy | 유제품 | 우유, 치즈, 요구르트 |
| seasoning | 조미료 | 간장, 된장, 고추장 |
| processed | 가공식품 | 햄, 소시지, 두부 |
| other | 기타 | 해당되지 않는 식재료 |

### 비즈니스 로직

#### 1. 식재료 등록
```python
def create_ingredient(
    name: str,
    category: str,
    **kwargs
) -> Ingredient:
    """
    새로운 식재료 등록

    1. 중복 이름 체크 (유사도 검사)
    2. 이름 정규화 (예: "당근(국내산)" → "당근")
    3. Ingredient 생성
    4. (선택) Nutrition Info 자동 조회 (식품의약품안전처 API 연동)
    """
    pass
```

#### 2. 대체 식재료 추천
```python
def suggest_substitutes(ingredient_id: int) -> list[Ingredient]:
    """
    대체 가능한 식재료 추천

    1. 동일 카테고리 내 식재료 조회
    2. 영양소 유사도 계산
    3. 가격 및 수급 안정성 고려
    4. 추천 목록 반환 (우선순위 정렬)
    """
    pass
```

---

## Task 1-1-4: Nutrition Info Structure

### 비즈니스 요구사항
- 영양사 협회 권장 기준 충족 여부 확인 필요
- 100g 기준 영양소 저장 (계산 편의성)
- 주요 영양소: 열량, 탄수화물, 단백질, 지방, 나트륨

### 데이터 모델

#### Nutrition Info (영양 정보)
| 속성명 | 타입 | 필수 | 설명 |
|--------|------|------|------|
| id | BIGINT | Y | 기본키 |
| ingredient_id | BIGINT | Y | 식재료 FK (UNIQUE) |
| serving_size_g | DECIMAL(8,2) | Y | 기준량 (100g 권장) |
| calories_kcal | DECIMAL(8,2) | Y | 열량 (kcal) |
| carbohydrate_g | DECIMAL(8,2) | Y | 탄수화물 (g) |
| protein_g | DECIMAL(8,2) | Y | 단백질 (g) |
| fat_g | DECIMAL(8,2) | Y | 지방 (g) |
| sodium_mg | DECIMAL(8,2) | Y | 나트륨 (mg) |
| sugar_g | DECIMAL(8,2) | N | 당류 (g) |
| saturated_fat_g | DECIMAL(8,2) | N | 포화지방 (g) |
| cholesterol_mg | DECIMAL(8,2) | N | 콜레스테롤 (mg) |
| dietary_fiber_g | DECIMAL(8,2) | N | 식이섬유 (g) |
| calcium_mg | DECIMAL(8,2) | N | 칼슘 (mg) |
| iron_mg | DECIMAL(8,2) | N | 철분 (mg) |
| vitamin_a_ug | DECIMAL(8,2) | N | 비타민 A (μg) |
| vitamin_c_mg | DECIMAL(8,2) | N | 비타민 C (mg) |
| data_source | VARCHAR(100) | N | 데이터 출처 (예: "식약처 DB", "수동 입력") |
| updated_at | TIMESTAMP | Y | 수정일시 |

**제약 조건**:
- `ingredient_id` 는 유니크 (1:1 관계)
- 모든 영양소 값 >= 0
- `serving_size_g` = 100 (권장, 계산 편의성)

**인덱스**:
- PRIMARY KEY: `id`
- UNIQUE INDEX: `ingredient_id`

### 영양 기준 (성인 1일 권장량 기준)

| 영양소 | 1일 권장량 | 비고 |
|--------|-----------|------|
| 열량 | 2000 kcal | 성인 남성 기준 |
| 탄수화물 | 324 g | 총 열량의 65% |
| 단백질 | 55 g | 총 열량의 15% |
| 지방 | 50 g | 총 열량의 20% |
| 나트륨 | 2000 mg | 세계보건기구(WHO) 권장 |
| 식이섬유 | 25 g | - |

### 비즈니스 로직

#### 1. 영양소 계산 (1인분 기준)
```python
def calculate_nutrition(
    ingredient_id: int,
    quantity_g: float
) -> dict:
    """
    특정 분량의 영양소 계산

    1. Nutrition Info 조회
    2. 비율 계산: (quantity_g / serving_size_g)
    3. 각 영양소에 비율 곱하기
    4. 결과 반환

    예: 당근 150g
    - 당근 100g당 열량: 40 kcal
    - 150g 열량: 40 × (150/100) = 60 kcal
    """
    pass
```

#### 2. 영양 기준 충족도 계산
```python
def calculate_nutrition_score(
    total_nutrition: dict,
    target_nutrition: dict
) -> float:
    """
    영양 기준 충족도 점수 계산 (0-100점)

    1. 각 영양소별 충족률 계산: (실제 / 목표) × 100
    2. 부족한 경우 감점, 과다한 경우도 감점
    3. 허용 범위: 90-110%
    4. 가중치 적용:
       - 열량: 30%
       - 탄수화물: 20%
       - 단백질: 20%
       - 지방: 15%
       - 나트륨: 15%
    5. 최종 점수 반환
    """
    pass
```

---

## Task 1-1-5: Allergen Model

### 비즈니스 요구사항
- 식품의약품안전처 표시 대상 알레르기 유발 식품 관리
- 종교적/문화적 제한 식품 포함 여부는 확장 단계에서 결정
- 식재료별 알레르기 매핑

### 데이터 모델

#### Allergen (알레르기 유발 식품)
| 속성명 | 타입 | 필수 | 설명 |
|--------|------|------|------|
| id | BIGINT | Y | 기본키 |
| name | VARCHAR(100) | Y | 알레르기명 (예: "땅콩") |
| name_en | VARCHAR(100) | N | 영문명 (예: "Peanut") |
| category | VARCHAR(50) | Y | 카테고리 (food_allergy, religious, cultural) |
| severity | VARCHAR(20) | Y | 심각도 (high, medium, low) |
| description | TEXT | N | 설명 |
| is_mandatory_label | BOOLEAN | Y | 식약처 필수 표시 대상 여부 |
| created_at | TIMESTAMP | Y | 생성일시 |

**제약 조건**:
- `name` 은 유니크
- `category` 는 ENUM: `'food_allergy'`, `'religious'`, `'cultural'`
- `severity` 는 ENUM: `'high'`, `'medium'`, `'low'`

**인덱스**:
- PRIMARY KEY: `id`
- UNIQUE INDEX: `name`
- INDEX: `category`

#### Ingredient Allergen (식재료-알레르기 매핑)
| 속성명 | 타입 | 필수 | 설명 |
|--------|------|------|------|
| id | BIGINT | Y | 기본키 |
| ingredient_id | BIGINT | Y | 식재료 FK |
| allergen_id | BIGINT | Y | 알레르기 FK |
| contamination_level | VARCHAR(20) | Y | 오염 수준 (contains, may_contain, traces) |
| notes | TEXT | N | 비고 |
| created_at | TIMESTAMP | Y | 생성일시 |

**제약 조건**:
- `(ingredient_id, allergen_id)` 조합은 유니크
- `contamination_level` 는 ENUM: `'contains'` (포함), `'may_contain'` (포함 가능), `'traces'` (미량)

**인덱스**:
- PRIMARY KEY: `id`
- UNIQUE INDEX: `(ingredient_id, allergen_id)`
- INDEX: `allergen_id`

### 식약처 표시 대상 알레르기 유발 식품 (21종)

| 번호 | 알레르기명 | 영문명 | 심각도 |
|------|-----------|--------|--------|
| 1 | 난류(계란) | Eggs | High |
| 2 | 우유 | Milk | High |
| 3 | 메밀 | Buckwheat | High |
| 4 | 땅콩 | Peanuts | High |
| 5 | 대두 | Soybeans | Medium |
| 6 | 밀 | Wheat | High |
| 7 | 고등어 | Mackerel | Medium |
| 8 | 게 | Crab | High |
| 9 | 새우 | Shrimp | High |
| 10 | 돼지고기 | Pork | Medium |
| 11 | 복숭아 | Peach | Medium |
| 12 | 토마토 | Tomato | Low |
| 13 | 아황산류 | Sulfites | High |
| 14 | 호두 | Walnut | High |
| 15 | 닭고기 | Chicken | Medium |
| 16 | 쇠고기 | Beef | Medium |
| 17 | 오징어 | Squid | Medium |
| 18 | 조개류 | Shellfish | High |
| 19 | 잣 | Pine Nuts | Medium |
| 20 | 알류 | Nuts (general) | High |
| 21 | 밤 | Chestnut | Low |

### 비즈니스 로직

#### 1. 알레르기 필터링
```python
def filter_ingredients_by_allergens(
    excluded_allergen_ids: list[int],
    include_may_contain: bool = True
) -> list[int]:
    """
    제외할 알레르기 기준으로 식재료 필터링

    1. 제외할 알레르기 목록 조회
    2. Ingredient Allergen 매핑 조회
    3. contamination_level 고려:
       - contains: 항상 제외
       - may_contain: include_may_contain 파라미터에 따라 결정
       - traces: 포함 (미량은 허용)
    4. 제외할 식재료 ID 목록 반환
    """
    pass
```

#### 2. 알레르기 위험도 계산
```python
def calculate_allergen_risk(
    meal_plan_id: int,
    excluded_allergen_ids: list[int]
) -> dict:
    """
    식단의 알레르기 위험도 계산

    1. 식단의 모든 식재료 조회
    2. 각 식재료의 알레르기 매핑 조회
    3. 제외 대상 알레르기와 비교
    4. 위험 항목 개수 및 심각도 계산
    5. 결과 반환:
       {
           "total_items": 100,
           "risk_items": 5,
           "high_risk": 2,
           "medium_risk": 3,
           "details": [...]
       }
    """
    pass
```

---

## 데이터 시드 (Seed Data)

### 1. 알레르기 마스터 데이터
식약처 21종 알레르기 유발 식품을 시드 데이터로 제공

### 2. 기본 식재료 데이터
자주 사용되는 식재료 50-100종을 시드 데이터로 제공:
- 곡물류: 쌀, 밀가루, 보리 등
- 채소류: 당근, 양파, 배추, 감자 등
- 육류: 쇠고기, 돼지고기, 닭고기
- 수산물: 고등어, 멸치, 오징어
- 조미료: 간장, 된장, 고추장, 소금

### 3. 영양 정보 데이터
식품의약품안전처 식품영양성분 DB 연동 또는 수동 입력

---

## 다음 단계

Epic 1-1 완료 후:
- **Epic 1-2**: ERD 설계 및 검토
- **Epic 1-3**: PostgreSQL 스키마 구현

---

## 참고 문서
- [PRD.md](./PRD.md) - 제품 요구사항 정의서
- [MVP_SCOPE.md](./MVP_SCOPE.md) - MVP 기능 범위
- [task.md](./task.md) - 개발 Task 관리
