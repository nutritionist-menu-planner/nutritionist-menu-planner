# Nutritionist Menu Planner - Frontend

React + TypeScript + Vite 기반 영양사 식단 자동 생성 플랫폼 프론트엔드

## 기술 스택

- **Framework**: React 18
- **Language**: TypeScript 5
- **Build Tool**: Vite 6
- **UI Library**: Material-UI (MUI) 6
- **State Management**:
  - Server State: TanStack Query (React Query)
  - Client State: Zustand
- **Routing**: React Router 7
- **Form Handling**: React Hook Form
- **HTTP Client**: Axios
- **Date Utilities**: date-fns

## 요구사항

- Node.js 18 이상
- npm, yarn, 또는 pnpm

## 설치 방법

### 1. 의존성 설치

```bash
cd frontend

# npm 사용
npm install

# yarn 사용
yarn install

# pnpm 사용
pnpm install
```

### 2. 환경 변수 설정

```bash
# .env.example 파일을 .env로 복사
cp .env.example .env

# .env 파일을 편집하여 실제 값 입력
# VITE_API_BASE_URL은 백엔드 API 주소로 설정
```

## 실행 방법

### 개발 서버 실행

```bash
npm run dev
```

브라우저에서 http://localhost:3000 접속

### 프로덕션 빌드

```bash
npm run build
```

빌드 결과는 `dist/` 디렉토리에 생성됩니다.

### 빌드 미리보기

```bash
npm run preview
```

## 프로젝트 구조

```
frontend/
├── public/                  # 정적 파일
│   └── vite.svg
│
├── src/
│   ├── components/          # 재사용 가능한 컴포넌트
│   │   ├── common/          # 공통 컴포넌트 (Button, Input 등)
│   │   ├── layout/          # 레이아웃 컴포넌트 (Header, Sidebar 등)
│   │   └── ...
│   │
│   ├── pages/               # 페이지 컴포넌트
│   │   ├── Login/
│   │   ├── Register/
│   │   ├── MealPlans/
│   │   ├── MealPlanDetail/
│   │   └── ...
│   │
│   ├── hooks/               # 커스텀 훅
│   │   ├── useAuth.ts
│   │   ├── useMealPlans.ts
│   │   └── ...
│   │
│   ├── services/            # API 통신 서비스
│   │   ├── api.ts           # Axios 인스턴스
│   │   ├── authService.ts
│   │   ├── mealPlanService.ts
│   │   └── ...
│   │
│   ├── store/               # 전역 상태 관리
│   │   ├── authStore.ts
│   │   └── ...
│   │
│   ├── types/               # TypeScript 타입 정의
│   │   ├── auth.ts
│   │   ├── mealPlan.ts
│   │   └── ...
│   │
│   ├── utils/               # 유틸리티 함수
│   │   ├── formatters.ts
│   │   ├── validators.ts
│   │   └── ...
│   │
│   ├── App.tsx              # 루트 컴포넌트
│   ├── main.tsx             # 진입점
│   └── index.css            # 전역 스타일
│
├── .env.example             # 환경 변수 예시
├── .env                     # 환경 변수 (gitignore)
├── .prettierrc              # Prettier 설정
├── eslint.config.js         # ESLint 설정
├── tsconfig.json            # TypeScript 설정
├── vite.config.ts           # Vite 설정
├── package.json             # 의존성 관리
└── README.md                # 이 파일
```

## 개발 가이드

### 코드 포맷팅

```bash
# Prettier로 코드 포맷팅
npm run format

# 포맷팅 검사만 (CI용)
npm run format:check
```

### 린팅

```bash
# ESLint 검사
npm run lint

# ESLint 자동 수정
npm run lint:fix
```

### 타입 체크

```bash
npm run type-check
```

### 컴포넌트 작성 가이드

#### 1. 함수형 컴포넌트 사용

```tsx
// ✅ Good
export const MyComponent = () => {
  return <div>Hello</div>
}

// ❌ Avoid
export class MyComponent extends React.Component {
  render() {
    return <div>Hello</div>
  }
}
```

#### 2. Props 타입 정의

```tsx
interface MyComponentProps {
  title: string
  count?: number // optional
  onSubmit: (value: string) => void
}

export const MyComponent = ({ title, count = 0, onSubmit }: MyComponentProps) => {
  // ...
}
```

#### 3. 커스텀 훅 활용

```tsx
// hooks/useMealPlans.ts
export const useMealPlans = () => {
  return useQuery({
    queryKey: ['mealPlans'],
    queryFn: () => mealPlanService.getAll(),
  })
}

// pages/MealPlans/index.tsx
const MealPlansPage = () => {
  const { data, isLoading, error } = useMealPlans()
  // ...
}
```

### 상태 관리 가이드

#### 서버 상태 (TanStack Query)

API 데이터는 React Query로 관리:

```tsx
import { useQuery, useMutation } from '@tanstack/react-query'

// GET 요청
const { data, isLoading } = useQuery({
  queryKey: ['mealPlans', id],
  queryFn: () => mealPlanService.getById(id),
})

// POST/PUT/DELETE 요청
const mutation = useMutation({
  mutationFn: mealPlanService.create,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['mealPlans'] })
  },
})
```

#### 클라이언트 상태 (Zustand)

UI 상태, 전역 설정 등은 Zustand로 관리:

```tsx
// store/authStore.ts
import { create } from 'zustand'

interface AuthState {
  token: string | null
  setToken: (token: string) => void
  clearToken: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  setToken: (token) => set({ token }),
  clearToken: () => set({ token: null }),
}))

// 사용
const { token, setToken } = useAuthStore()
```

### 라우팅 가이드

```tsx
// App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/meal-plans" element={<MealPlansPage />} />
        <Route path="/meal-plans/:id" element={<MealPlanDetailPage />} />
      </Routes>
    </BrowserRouter>
  )
}
```

### API 통신 가이드

```tsx
// services/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: Number(import.meta.env.VITE_API_TIMEOUT),
})

// Request Interceptor (JWT 토큰 자동 첨부)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response Interceptor (에러 핸들링)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // 로그아웃 처리
    }
    return Promise.reject(error)
  }
)

export default api
```

## 환경 변수 설명

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `VITE_API_BASE_URL` | Backend API 베이스 URL | http://localhost:8000 |
| `VITE_API_TIMEOUT` | API 요청 타임아웃 (ms) | 10000 |
| `VITE_APP_ENV` | 환경 (development, production) | development |

## 스타일링 가이드

본 프로젝트는 Material-UI (MUI)를 사용합니다.

### 테마 커스터마이징

```tsx
// theme.ts
import { createTheme } from '@mui/material/styles'

export const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
  },
})

// App.tsx
import { ThemeProvider } from '@mui/material/styles'
import { theme } from './theme'

function App() {
  return (
    <ThemeProvider theme={theme}>
      {/* ... */}
    </ThemeProvider>
  )
}
```

## 트러블슈팅

### Vite 빌드 오류

```
Error: Cannot find module '@rollup/rollup-win32-x64-msvc'
```

**해결 방법**:
```bash
npm install --force
```

### ESLint 설정 오류

```
Error: Failed to load config
```

**해결 방법**:
1. `node_modules` 삭제
2. 의존성 재설치
   ```bash
   rm -rf node_modules
   npm install
   ```

### TypeScript 경로 별칭 오류

```
Cannot find module '@/components/...'
```

**해결 방법**:
1. `tsconfig.json`의 `paths` 설정 확인
2. `vite.config.ts`의 `resolve.alias` 설정 확인
3. VS Code 재시작

## 기여 가이드

1. 브랜치 전략은 [GIT_WORKFLOW.md](../docs/GIT_WORKFLOW.md) 참조
2. 코드 컨벤션은 [CODE_CONVENTIONS.md](../docs/CODE_CONVENTIONS.md) 참조
3. PR 생성 시 [PULL_REQUEST_TEMPLATE.md](../.github/PULL_REQUEST_TEMPLATE.md) 사용

## 라이센스

MIT License

## 문의

프로젝트 관련 문의는 이슈 트래커를 사용해주세요.
