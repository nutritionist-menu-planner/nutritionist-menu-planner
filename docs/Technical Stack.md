# Technical Stack Document

---

## 1. 기술 설계 원칙 (Technical Principles)

본 플랫폼의 기술 설계는 다음 원칙을 따른다.

1. **영양사 실무 중심**
    - 복잡한 AI보다 설명 가능한 로직 우선
2. **결과의 투명성**
    - 모든 계산·추천 결과는 근거 확인 가능
3. **점진적 확장성**
    - 향후 ML·B2C 확장 가능 구조
4. **파일 기반 업무 친화성**
    - 엑셀·PDF 중심 기존 업무 흐름 존중

---

## 2. 전체 아키텍처 개요 (High-Level Architecture)

- Frontend: Web 기반 영양사 UI
- Backend: API 서버 + 식단 분석 로직
- Database: 식단·식재료·영양 기준 저장
- File Processing: 문서 파싱 및 데이터 추출
- (확장) ML Layer: 조합 평가 고도화

---

## 3. Frontend Tech Stack

### 3.1 Framework

- **React.js**
    - 이유:
        - 컴포넌트 기반 UI로 식단 테이블 관리 용이
        - 드래그 앤 드롭 구현에 적합
        - B2B 웹 서비스에서 검증된 안정성

### 3.2 UI / UX Libraries

- **Material UI (MUI)** 또는 **Ant Design**
    - 표(Table)·폼(Form) 중심 UI 제공
    - 엑셀과 유사한 인터랙션 구현 가능
- **React DnD**
    - 식재료 드래그 앤 드롭 적용
    - 메뉴 교체 시 직관적 조작 지원

### 3.3 State Management

- **React Query**
    - 식단·식재료 데이터 비동기 처리
    - 실시간 수정 반영에 적합

---

## 4. Backend Tech Stack

### 4.1 Server Framework

- **Python + FastAPI**
    - 이유:
        - 데이터 처리·분석 로직에 강점
        - 문서 파싱 및 향후 ML 확장에 유리
        - API 응답 속도 및 문서화 우수

### 4.2 API Design

- RESTful API
- 주요 엔드포인트:
    - 식단 업로드 / 분석
    - 식단 자동 생성
    - 식재료 관리
    - 영양·예산 재계산

---

## 5. 식단 분석 및 로직 계층 (Core Logic Layer)

### 5.1 분석 방식

- **규칙 기반 + 통계 기반 분석**
    - 단순 빈도 분석 ❌
    - 조합의 질(Quality) 평가 중심

### 5.2 주요 평가 지표

- 영양 기준 충족도
- 열량 및 영양소 균형
- 예산 대비 효율성
- 알레르기 및 제한 식품 포함 여부
- 운영 안정성(조리·수급 부담)

※ 모든 점수는 가중치 기반으로 계산 가능하도록 설계

---

## 6. Database Tech Stack

### 6.1 RDBMS

- **PostgreSQL**
    - 이유:
        - 정형 데이터(식단, 영양소, 가격) 관리에 적합
        - 복잡한 조인 및 이력 관리 용이

### 6.2 주요 테이블 구조 (개요)

- meal_plan
- meal_item (밥/국/반찬)
- ingredient
- nutrition_info
- allergen
- supplier_item
- meal_plan_history

---

## 7. 파일 업로드 및 문서 파싱

### 7.1 지원 파일

- PDF
- HWP
- Excel

### 7.2 처리 기술

- **Excel**
    - pandas, openpyxl
- **PDF**
    - pdfplumber
    - (스캔 문서 시) Tesseract OCR
- **HWP**
    - pyhwp 또는 변환 기반 처리

### 7.3 처리 결과

- 표 구조 인식
- 식재료명 / 가격 / 수급 정보 DB 저장

---

## 8. 비기능 요소 (Non-Functional Tech)

### 8.1 인증·보안

- JWT 기반 인증
- 영양사 계정 단위 데이터 분리

### 8.2 로그 및 이력 관리

- 식단 생성 이력
- 수정 전·후 비교 가능 구조

---

## 9. 배포 및 인프라 (Deployment)

### 9.1 Backend

- Docker 기반 컨테이너화
- AWS EC2 / ECS

### 9.2 Database

- AWS RDS (PostgreSQL)

### 9.3 Frontend

- AWS S3 + CloudFront

---

## 10. 향후 확장 고려 기술 (Not in MVP)

- ML 모델(PyTorch / Scikit-learn)
- 개인 맞춤형 B2C 서비스 분리
- 외부 쇼핑몰 API 연동
- 자동 발주 시스템 연계

---

## 11. 기술 스택 요약

| 영역 | 기술 |
| --- | --- |
| Frontend | React, MUI, React DnD |
| Backend | Python, FastAPI |
| DB | PostgreSQL |
| File Processing | pandas, pdfplumber, OCR |
| Infra | AWS, Docker |

---

## 12. 기술 선택 한 줄 요약

> “설명 가능한 식단 자동화를 우선하고,
> 
> 
> 필요할 때 지능을 확장할 수 있는 구조를 선택했다.”
>