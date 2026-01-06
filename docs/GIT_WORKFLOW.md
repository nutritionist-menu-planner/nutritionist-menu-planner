# Git Workflow & Branching Strategy

## 브랜치 전략

본 프로젝트는 **GitHub Flow** 기반의 단순화된 브랜치 전략을 사용합니다.

### 브랜치 종류

#### 1. `main` (프로덕션)
- **목적**: 프로덕션 배포 버전
- **보호 규칙**:
  - Direct push 금지
  - PR을 통한 병합만 허용
  - 최소 1명 이상의 리뷰 승인 필요
  - CI/CD 테스트 통과 필수
- **배포**: main 브랜치에 병합 시 자동 배포

#### 2. `develop` (개발)
- **목적**: 개발 중인 기능들의 통합 브랜치
- **보호 규칙**:
  - Direct push 금지
  - PR을 통한 병합만 허용
  - 코드 리뷰 권장 (필수 아님)
- **배포**: 개발 서버 자동 배포

#### 3. `feature/*` (기능 개발)
- **목적**: 새로운 기능 개발
- **네이밍**: `feature/epic-X-Y-description` 또는 `feature/task-description`
  - 예: `feature/epic-0-2-development-environment`
  - 예: `feature/meal-plan-generation`
- **생성 시점**: Epic 또는 Task 시작 시
- **병합 대상**: `develop` 브랜치
- **삭제**: develop 병합 후 삭제

#### 4. `bugfix/*` (버그 수정)
- **목적**: develop 브랜치의 버그 수정
- **네이밍**: `bugfix/issue-number-description` 또는 `bugfix/description`
  - 예: `bugfix/issue-123-login-error`
  - 예: `bugfix/meal-calculation-error`
- **병합 대상**: `develop` 브랜치
- **삭제**: develop 병합 후 삭제

#### 5. `hotfix/*` (긴급 수정)
- **목적**: 프로덕션 긴급 버그 수정
- **네이밍**: `hotfix/description`
  - 예: `hotfix/critical-security-patch`
- **병합 대상**: `main` 및 `develop` 브랜치 (양쪽 모두)
- **삭제**: 병합 후 삭제

---

## 브랜치 생성 및 병합 흐름

### Feature 개발 흐름

```bash
# 1. develop 브랜치에서 최신 코드 가져오기
git checkout develop
git pull origin develop

# 2. feature 브랜치 생성
git checkout -b feature/epic-X-Y-description

# 3. 작업 및 커밋
git add .
git commit -m "feat: Add feature description"

# 4. 원격 저장소에 푸시
git push -u origin feature/epic-X-Y-description

# 5. GitHub에서 PR 생성 (develop ← feature)

# 6. 코드 리뷰 및 승인 후 병합

# 7. 로컬 브랜치 정리
git checkout develop
git pull origin develop
git branch -d feature/epic-X-Y-description
```

### Hotfix 개발 흐름

```bash
# 1. main 브랜치에서 hotfix 생성
git checkout main
git pull origin main
git checkout -b hotfix/description

# 2. 작업 및 커밋
git add .
git commit -m "fix: Critical bug fix"

# 3. main에 병합 (PR 또는 직접)
git checkout main
git merge --no-ff hotfix/description
git push origin main

# 4. develop에도 병합
git checkout develop
git merge --no-ff hotfix/description
git push origin develop

# 5. 브랜치 삭제
git branch -d hotfix/description
```

---

## 커밋 메시지 컨벤션

### Conventional Commits 사용

본 프로젝트는 [Conventional Commits](https://www.conventionalcommits.org/) 규칙을 따릅니다.

#### 기본 형식

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 종류

| Type | 설명 | 예시 |
|------|------|------|
| `feat` | 새로운 기능 추가 | `feat: Add meal plan generation API` |
| `fix` | 버그 수정 | `fix: Fix nutrition calculation error` |
| `docs` | 문서 수정 | `docs: Update README with setup instructions` |
| `style` | 코드 포맷팅 (기능 변경 없음) | `style: Format code with Black` |
| `refactor` | 코드 리팩토링 | `refactor: Simplify meal plan service logic` |
| `test` | 테스트 추가/수정 | `test: Add unit tests for meal item model` |
| `chore` | 빌드/설정 변경 | `chore: Update dependencies` |
| `perf` | 성능 개선 | `perf: Optimize database queries` |
| `ci` | CI/CD 설정 변경 | `ci: Add GitHub Actions workflow` |
| `build` | 빌드 시스템 변경 | `build: Update webpack config` |
| `revert` | 커밋 되돌리기 | `revert: Revert "feat: Add feature X"` |

#### Scope (선택사항)

프로젝트의 특정 영역을 나타냅니다:
- `auth`: 인증 관련
- `meal-plan`: 식단 관련
- `ingredient`: 식재료 관련
- `ui`: UI 컴포넌트
- `api`: API 엔드포인트
- `db`: 데이터베이스

예시:
```
feat(auth): Add JWT token refresh logic
fix(meal-plan): Fix nutrition calculation rounding error
docs(api): Add API endpoint documentation
```

#### Subject

- 50자 이내로 작성
- 명령형 현재 시제 사용 ("Add" not "Added" or "Adds")
- 첫 글자 대문자
- 마침표(.) 없음

#### Body (선택사항)

- 변경 이유 및 세부 내용 설명
- 72자마다 줄바꿈

#### Footer (선택사항)

- Breaking changes: `BREAKING CHANGE: <description>`
- Issue 참조: `Closes #123`, `Fixes #456`

#### 예시

```
feat(meal-plan): Add automatic meal plan generation

Implement the core meal plan generation algorithm based on
historical meal data analysis. The algorithm evaluates meal
combinations using nutrition score, budget efficiency, and
allergen filtering.

Closes #42
```

---

## Pull Request (PR) 규칙

### PR 생성 시

1. **브랜치 네이밍 확인**: `feature/`, `bugfix/`, `hotfix/` 접두사 사용
2. **최신 develop 브랜치와 동기화**: conflict 미리 해결
3. **Self-review**: 본인이 먼저 코드 리뷰
4. **테스트 실행**: 로컬에서 모든 테스트 통과 확인

### PR 제목

커밋 메시지와 동일한 형식:
```
feat(meal-plan): Add automatic meal plan generation
```

### PR 설명 템플릿

```markdown
## 변경 사항
- 무엇을 변경했는지 간단히 설명

## 변경 이유
- 왜 이 변경이 필요한지 설명

## 테스트 방법
1. 테스트 단계 1
2. 테스트 단계 2

## 스크린샷 (UI 변경 시)
![스크린샷](url)

## 체크리스트
- [ ] 코드 self-review 완료
- [ ] 테스트 추가/업데이트
- [ ] 문서 업데이트 (필요시)
- [ ] Linting 통과
- [ ] 로컬 테스트 통과

## 관련 이슈
Closes #123
```

### PR 리뷰 규칙

#### 리뷰어 역할
- 최소 1명 이상의 승인 필요 (main 브랜치 병합 시)
- 코드 품질, 로직, 보안 검토
- 건설적인 피드백 제공

#### 리뷰 코멘트 종류
- **💡 Suggestion**: 개선 제안 (선택사항)
- **❓ Question**: 질문 또는 명확화 필요
- **⚠️ Issue**: 반드시 수정 필요
- **✅ Approved**: 승인

#### 리뷰 응답 시간
- 24시간 이내 1차 리뷰
- 긴급한 경우 Slack으로 알림

---

## 브랜치 보호 규칙

### `main` 브랜치
- [x] Require pull request reviews before merging (1명 이상)
- [x] Require status checks to pass before merging
- [x] Require branches to be up to date before merging
- [x] Include administrators (관리자도 규칙 적용)
- [x] Restrict pushes (Direct push 금지)

### `develop` 브랜치
- [x] Require pull request reviews before merging (0명, PR만 강제)
- [x] Require status checks to pass before merging
- [ ] Require branches to be up to date before merging (권장)
- [ ] Include administrators

---

## .gitignore 설정

### Backend (Python)
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Database
*.db
*.sqlite3

# Logs
*.log
logs/

# Testing
.coverage
htmlcov/
.pytest_cache/
.tox/
```

### Frontend (React)
```gitignore
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Production
build/
dist/

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/

# Logs
*.log

# Testing
coverage/

# macOS
.DS_Store
```

### Common
```gitignore
# OS
.DS_Store
Thumbs.db

# Backup
*.bak
*.tmp
*.swp
```

---

## Git Hooks (선택사항)

### Pre-commit Hook

**목적**: 커밋 전 자동 검증

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Backend: Black formatting check
if git diff --cached --name-only | grep -q '\.py$'; then
    echo "Running Black formatter..."
    black --check .
    if [ $? -ne 0 ]; then
        echo "❌ Black formatting failed. Run 'black .' to fix."
        exit 1
    fi
fi

# Frontend: ESLint check
if git diff --cached --name-only | grep -q '\.[jt]sx\?$'; then
    echo "Running ESLint..."
    npm run lint
    if [ $? -ne 0 ]; then
        echo "❌ ESLint check failed. Fix linting errors."
        exit 1
    fi
fi

echo "✅ Pre-commit checks passed!"
exit 0
```

### Commit-msg Hook

**목적**: 커밋 메시지 형식 검증

```bash
#!/bin/sh
# .git/hooks/commit-msg

commit_msg=$(cat "$1")
pattern="^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\(.+\))?: .{1,50}"

if ! echo "$commit_msg" | grep -qE "$pattern"; then
    echo "❌ Invalid commit message format!"
    echo "Expected: <type>(<scope>): <subject>"
    echo "Example: feat(auth): Add JWT authentication"
    exit 1
fi

echo "✅ Commit message format valid!"
exit 0
```

---

## 협업 가이드라인

### 1. 브랜치 작업 전
- 항상 최신 develop 브랜치에서 시작
- `git pull origin develop` 실행

### 2. 작업 중
- 작은 단위로 자주 커밋
- 하나의 커밋은 하나의 논리적 변경만 포함
- 작업 중 develop 브랜치 변경 사항 주기적으로 병합 (`git merge develop`)

### 3. PR 생성 전
- Self-review: 본인이 먼저 변경 사항 검토
- 테스트 실행 및 통과 확인
- Conflict 해결

### 4. 코드 리뷰 중
- 리뷰 피드백에 신속히 대응
- 불명확한 피드백은 질문으로 명확화
- 모든 Issue 해결 후 병합

### 5. 병합 후
- 로컬 브랜치 삭제
- 원격 브랜치 삭제 (GitHub에서 자동 옵션 활성화 권장)

---

## 트러블슈팅

### Conflict 발생 시

```bash
# 1. develop 최신 변경 사항 가져오기
git checkout develop
git pull origin develop

# 2. feature 브랜치로 돌아가서 병합
git checkout feature/your-branch
git merge develop

# 3. Conflict 파일 수정
# (IDE에서 conflict marker 해결)

# 4. 해결 후 커밋
git add .
git commit -m "Resolve merge conflict with develop"

# 5. 푸시
git push origin feature/your-branch
```

### 실수로 잘못된 브랜치에 커밋한 경우

```bash
# 1. 올바른 브랜치로 변경 사항 이동
git stash
git checkout correct-branch
git stash pop

# 2. 잘못된 브랜치에서 커밋 되돌리기
git checkout wrong-branch
git reset --hard HEAD~1
```

### 커밋 메시지 수정

```bash
# 최근 커밋 메시지 수정 (push 전)
git commit --amend -m "New commit message"

# push 후 수정 (주의: force push)
git commit --amend -m "New commit message"
git push --force-with-lease origin branch-name
```

---

## 참고 자료
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Branching Model](https://nvie.com/posts/a-successful-git-branching-model/)
