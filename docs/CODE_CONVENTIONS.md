# Code Conventions & Collaboration Rules

## 목적
코드 품질을 유지하고 팀 협업을 원활하게 하기 위한 코딩 컨벤션 및 규칙을 정의합니다.

---

## Python (Backend) 코딩 컨벤션

### 기본 원칙
- **PEP 8** 준수
- **Black** 포매터 사용 (line-length: 88)
- **Ruff** 린터 사용
- **Type hints** 사용 권장

### 네이밍 컨벤션

#### 1. 변수 및 함수
- **snake_case** 사용

```python
# ✅ Good
user_name = "John"
meal_plan_id = 123

def calculate_nutrition_score(meal_plan):
    pass

# ❌ Bad
userName = "John"
MealPlanId = 123

def CalculateNutritionScore(meal_plan):
    pass
```

#### 2. 클래스
- **PascalCase** 사용

```python
# ✅ Good
class MealPlan:
    pass

class NutritionCalculator:
    pass

# ❌ Bad
class meal_plan:
    pass

class nutrition_calculator:
    pass
```

#### 3. 상수
- **UPPER_SNAKE_CASE** 사용

```python
# ✅ Good
MAX_UPLOAD_SIZE = 10485760
DEFAULT_PAGE_SIZE = 20

# ❌ Bad
maxUploadSize = 10485760
default_page_size = 20
```

#### 4. 비공개 변수/메서드
- 앞에 **언더스코어(_)** 사용

```python
# ✅ Good
class MealPlanService:
    def __init__(self):
        self._cache = {}

    def _calculate_score(self):
        pass

# ❌ Bad
class MealPlanService:
    def __init__(self):
        self.cache = {}

    def calculate_score(self):  # public으로 오인될 수 있음
        pass
```

### 파일 및 모듈 구조

#### 1. 임포트 순서
```python
# 1. 표준 라이브러리
import os
import sys
from typing import Optional

# 2. 서드파티 라이브러리
from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, Integer, String

# 3. 로컬 모듈
from app.models.user import User
from app.services.auth_service import AuthService
```

#### 2. 파일명
- **snake_case** 사용
- 의미 있는 이름 사용

```
✅ Good:
- meal_plan_service.py
- nutrition_calculator.py
- user_repository.py

❌ Bad:
- MealPlanService.py
- nutritionCalculator.py
- ur.py
```

### 함수 및 메서드

#### 1. 함수 길이
- 한 함수는 **50줄 이내** 권장
- 복잡한 로직은 여러 함수로 분리

#### 2. 매개변수
- 매개변수는 **5개 이하** 권장
- 많은 경우 데이터 클래스 또는 딕셔너리 사용

```python
# ✅ Good
from dataclasses import dataclass

@dataclass
class MealPlanConfig:
    year: int
    month: int
    budget: float
    allergens: list[str]

def generate_meal_plan(config: MealPlanConfig):
    pass

# ❌ Bad
def generate_meal_plan(year, month, budget, allergens, holidays, target_calories):
    pass
```

#### 3. Type Hints
- 모든 함수에 타입 힌트 사용 권장

```python
# ✅ Good
def calculate_nutrition_score(
    meal_plan: MealPlan,
    target_calories: int
) -> float:
    pass

# ❌ Bad (타입 힌트 없음)
def calculate_nutrition_score(meal_plan, target_calories):
    pass
```

### 주석 및 Docstring

#### 1. Docstring
- 모든 public 함수/클래스에 docstring 작성
- Google Style 또는 NumPy Style 사용

```python
# ✅ Good
def calculate_nutrition_score(meal_plan: MealPlan) -> float:
    """Calculate the nutrition score for a meal plan.

    Args:
        meal_plan: The meal plan to evaluate.

    Returns:
        A float score between 0 and 100.

    Raises:
        ValueError: If meal_plan is empty.
    """
    pass

# ❌ Bad (docstring 없음)
def calculate_nutrition_score(meal_plan: MealPlan) -> float:
    pass
```

#### 2. 인라인 주석
- 복잡한 로직에만 사용
- 코드가 자명한 경우 주석 불필요

```python
# ✅ Good
# 연속된 같은 메뉴 등장 방지를 위한 페널티
if previous_menu == current_menu:
    score -= REPETITION_PENALTY

# ❌ Bad (불필요한 주석)
# 사용자 이름 가져오기
user_name = user.name
```

### 에러 처리

#### 1. 구체적인 예외 사용
```python
# ✅ Good
try:
    meal_plan = db.query(MealPlan).filter_by(id=id).one()
except NoResultFound:
    raise HTTPException(status_code=404, detail="Meal plan not found")

# ❌ Bad
try:
    meal_plan = db.query(MealPlan).filter_by(id=id).one()
except Exception:
    raise HTTPException(status_code=500, detail="Error")
```

#### 2. 커스텀 예외
```python
# app/core/exceptions.py
class MealPlanNotFoundError(Exception):
    """Raised when meal plan is not found."""
    pass

class InsufficientBudgetError(Exception):
    """Raised when budget is insufficient."""
    pass
```

---

## TypeScript (Frontend) 코딩 컨벤션

### 기본 원칙
- **Airbnb JavaScript Style Guide** 기반
- **Prettier** 포매터 사용
- **ESLint** 린터 사용
- **Strict mode** 활성화

### 네이밍 컨벤션

#### 1. 변수 및 함수
- **camelCase** 사용

```typescript
// ✅ Good
const userName = 'John'
const mealPlanId = 123

function calculateNutritionScore(mealPlan: MealPlan): number {
  return 0
}

// ❌ Bad
const user_name = 'John'
const MealPlanId = 123

function calculate_nutrition_score(meal_plan: MealPlan): number {
  return 0
}
```

#### 2. 인터페이스 및 타입
- **PascalCase** 사용
- 인터페이스에 `I` 접두사 사용 안 함

```typescript
// ✅ Good
interface User {
  id: number
  name: string
}

type MealPlanStatus = 'draft' | 'confirmed' | 'published'

// ❌ Bad
interface IUser {  // I 접두사 불필요
  id: number
  name: string
}

type mealPlanStatus = 'draft' | 'confirmed' | 'published'
```

#### 3. React 컴포넌트
- **PascalCase** 사용
- 파일명도 **PascalCase** 사용

```typescript
// ✅ Good
// components/MealPlanCard.tsx
export const MealPlanCard = ({ mealPlan }: MealPlanCardProps) => {
  return <div>{mealPlan.name}</div>
}

// ❌ Bad
// components/meal-plan-card.tsx
export const mealPlanCard = ({ mealPlan }: MealPlanCardProps) => {
  return <div>{mealPlan.name}</div>
}
```

#### 4. 상수
- **UPPER_SNAKE_CASE** 사용

```typescript
// ✅ Good
const MAX_UPLOAD_SIZE = 10 * 1024 * 1024
const API_TIMEOUT = 10000

// ❌ Bad
const maxUploadSize = 10 * 1024 * 1024
const apiTimeout = 10000
```

### 파일 및 모듈 구조

#### 1. 임포트 순서
```typescript
// 1. React 관련
import React, { useState, useEffect } from 'react'

// 2. 서드파티 라이브러리
import { useQuery } from '@tanstack/react-query'
import { Box, Button } from '@mui/material'

// 3. 절대 경로 임포트 (프로젝트 내부)
import { useMealPlans } from '@hooks/useMealPlans'
import { MealPlanCard } from '@components/MealPlanCard'

// 4. 타입
import type { MealPlan } from '@types/mealPlan'

// 5. 스타일 (있는 경우)
import './styles.css'
```

#### 2. 파일명
- 컴포넌트: **PascalCase**
- 훅, 유틸, 서비스: **camelCase**

```
✅ Good:
- MealPlanCard.tsx
- useMealPlans.ts
- authService.ts
- formatDate.ts

❌ Bad:
- meal-plan-card.tsx
- UseMealPlans.ts
- AuthService.ts
- format-date.ts
```

### React 컴포넌트

#### 1. 함수형 컴포넌트 사용
```typescript
// ✅ Good
export const MyComponent = () => {
  return <div>Hello</div>
}

// ❌ Bad (클래스 컴포넌트 지양)
export class MyComponent extends React.Component {
  render() {
    return <div>Hello</div>
  }
}
```

#### 2. Props 타입 정의
```typescript
// ✅ Good
interface MealPlanCardProps {
  mealPlan: MealPlan
  onEdit?: (id: number) => void
}

export const MealPlanCard = ({ mealPlan, onEdit }: MealPlanCardProps) => {
  // ...
}

// ❌ Bad (타입 없음)
export const MealPlanCard = ({ mealPlan, onEdit }) => {
  // ...
}
```

#### 3. 컴포넌트 구조
```typescript
// ✅ Good
import React from 'react'
import type { MealPlan } from '@types/mealPlan'

interface MealPlanCardProps {
  mealPlan: MealPlan
}

export const MealPlanCard = ({ mealPlan }: MealPlanCardProps) => {
  // 1. State
  const [isExpanded, setIsExpanded] = React.useState(false)

  // 2. Hooks
  const { data } = useMealPlanDetails(mealPlan.id)

  // 3. Event handlers
  const handleClick = () => {
    setIsExpanded(!isExpanded)
  }

  // 4. Render
  return (
    <div onClick={handleClick}>
      {/* ... */}
    </div>
  )
}
```

### 타입 시스템

#### 1. any 사용 금지
```typescript
// ✅ Good
interface ApiResponse<T> {
  data: T
  status: number
}

// ❌ Bad
interface ApiResponse {
  data: any  // any 사용 금지
  status: number
}
```

#### 2. Union Types 활용
```typescript
// ✅ Good
type MealPlanStatus = 'draft' | 'confirmed' | 'published'

interface MealPlan {
  status: MealPlanStatus
}

// ❌ Bad
interface MealPlan {
  status: string  // 너무 광범위
}
```

#### 3. Optional vs Undefined
```typescript
// ✅ Good
interface User {
  name: string
  email?: string  // optional
}

// ❌ Bad
interface User {
  name: string
  email: string | undefined  // 명시적 undefined는 지양
}
```

### 주석 및 문서화

#### 1. JSDoc
```typescript
/**
 * Calculate the nutrition score for a meal plan.
 *
 * @param mealPlan - The meal plan to evaluate
 * @returns A score between 0 and 100
 */
export function calculateNutritionScore(mealPlan: MealPlan): number {
  // ...
}
```

#### 2. TODO 주석
```typescript
// TODO: Add pagination support
// FIXME: Handle edge case when budget is zero
// NOTE: This logic will be refactored in v2
```

---

## 데이터베이스 컨벤션

### 1. 테이블명
- **snake_case** 사용
- 복수형 사용

```sql
✅ Good:
- users
- meal_plans
- ingredients

❌ Bad:
- User
- MealPlan
- ingredient
```

### 2. 컬럼명
- **snake_case** 사용
- 의미 있는 이름 사용

```sql
✅ Good:
- user_id
- created_at
- is_active

❌ Bad:
- userId
- CreatedAt
- active
```

### 3. 기본 컬럼
모든 테이블에 다음 컬럼 포함 권장:
- `id` (Primary Key)
- `created_at` (생성 시각)
- `updated_at` (수정 시각)

```sql
CREATE TABLE meal_plans (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 코드 리뷰 가이드라인

### 리뷰어 체크리스트

#### 1. 기능 검증
- [ ] 요구사항을 충족하는가?
- [ ] 엣지 케이스를 고려했는가?
- [ ] 에러 처리가 적절한가?

#### 2. 코드 품질
- [ ] 네이밍이 명확한가?
- [ ] 중복 코드가 없는가?
- [ ] 함수가 단일 책임을 가지는가?
- [ ] 복잡도가 적절한가?

#### 3. 성능
- [ ] 불필요한 연산이 없는가?
- [ ] N+1 쿼리 문제가 없는가?
- [ ] 메모리 누수 가능성은 없는가?

#### 4. 보안
- [ ] SQL Injection 위험은 없는가?
- [ ] XSS 공격 가능성은 없는가?
- [ ] 민감 정보가 노출되지 않는가?

#### 5. 테스트
- [ ] 테스트가 추가되었는가?
- [ ] 테스트가 통과하는가?

### 리뷰 코멘트 예시

#### 1. 긍정적 피드백
```
✅ 좋은 점: 에러 핸들링이 명확하고 구체적입니다!
✅ LGTM (Looks Good To Me): 깔끔한 구현입니다.
```

#### 2. 개선 제안
```
💡 Suggestion: 이 로직을 별도 함수로 분리하면 재사용성이 높아질 것 같습니다.
```

#### 3. 질문
```
❓ Question: 이 예외 케이스는 어떻게 처리되나요?
```

#### 4. 수정 요청
```
⚠️ Issue: SQL Injection 위험이 있습니다. 파라미터 바인딩을 사용해주세요.
```

---

## 커밋 메시지 규칙

[GIT_WORKFLOW.md](./GIT_WORKFLOW.md)의 Conventional Commits 규칙 참조

---

## 협업 규칙

### 1. 코드 작성 전
- 작업 내용을 Issue나 Task로 등록
- 브랜치 생성 (feature/*, bugfix/*)
- 팀원과 커뮤니케이션

### 2. 코드 작성 중
- 작은 단위로 자주 커밋
- 의미 있는 커밋 메시지 작성
- 주기적으로 develop 브랜치 병합

### 3. PR 생성 전
- Self-review 수행
- 테스트 실행 및 통과 확인
- Linting 통과 확인

### 4. PR 생성 후
- 리뷰어 지정
- CI/CD 통과 확인
- 리뷰 피드백에 신속히 대응

### 5. 병합 후
- 로컬 브랜치 삭제
- 원격 브랜치 삭제
- 다음 작업 시작

---

## 자동화 도구

### Backend
```bash
# 포맷팅
poetry run black .

# 린팅
poetry run ruff check .
poetry run ruff check --fix .

# 타입 체크
poetry run mypy app/

# 테스트
poetry run pytest
```

### Frontend
```bash
# 포맷팅
npm run format

# 린팅
npm run lint
npm run lint:fix

# 타입 체크
npm run type-check

# 테스트 (추후 추가)
npm test
```

---

## 참고 자료
- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
- [Conventional Commits](https://www.conventionalcommits.org/)
