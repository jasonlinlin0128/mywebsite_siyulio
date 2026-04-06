` ```markdown `

`# 專案：{專案名稱}`

`> 建立日期：{{date}}`

`> 專案狀態：🚀 進行中`

`---`

`## 專案概述`

`### 專案目標`

`{簡短描述這個專案要解決什麼問題、達成什麼目標}`

`### 專案類型`

`- [ ] 手機 APP`

`- [ ] 網頁應用`

`- [ ] 企業內網平台`

`- [ ] API 服務`

`- [ ] 第三方整合`

`---`

`## 專案資訊`

`| 項目 | 內容 |`

`|------|------|`

`| **專案名稱** | {專案名稱} |`

`| **專案代號** | {project-code} |`

`| **開始日期** | {YYYY-MM-DD} |`

`| **預計完成** | {YYYY-MM-DD} |`

`| **專案狀態** | 規劃中 / 開發中 / 測試中 / 已上線 |`

`| **優先順序** | 🔴 高 / 🟡 中 / 🟢 低 |`

`---`

`## 技術架構`

`### 前端（Gemini 負責）`

`- **框架**: React / Vue.js / Flutter / React Native`

`- **UI 庫**: Material-UI / Ant Design / Tailwind CSS`

`- **狀態管理**: Redux / Zustand / Pinia`

`- **其他工具**: {列出其他工具}`

`### 後端（Claude 負責）`

`- **語言**: Node.js / Python / Go / Java`

`- **框架**: Express / FastAPI / Gin / Spring Boot`

`- **資料庫**: PostgreSQL / MySQL / MongoDB`

`- **快取**: Redis`

`- **認證**: JWT / OAuth 2.0`

`### 基礎設施`

`- **部署環境**: AWS / GCP / Azure / 本地伺服器`

`- **容器化**: Docker / Kubernetes`

`- **CI/CD**: GitHub Actions / GitLab CI`

`- **監控**: Prometheus / Grafana / Sentry`

`---`

`## 核心功能`

`### 功能清單`

`#### 第一階段（MVP）`

`1. [ ] {功能 1} - [[API-功能1]]`

`2. [ ] {功能 2} - [[API-功能2]]`

`3. [ ] {功能 3} - [[API-功能3]]`

`#### 第二階段`

`1. [ ] {進階功能 1}`

`2. [ ] {進階功能 2}`

`#### 第三階段（未來規劃）`

`1. [ ] {功能擴充 1}`

`2. [ ] {功能擴充 2}`

`---`

`## 系統架構圖`

` ``` `

`[前端 APP/Web]`

`↓ HTTPS`

`[API Gateway]`

`↓`

`[後端服務] ←→ [資料庫]`

`↓`

`[第三方服務]`

` ``` `

`---`

`## 資料庫設計`

`### 核心資料表`

`- [[DB-users]] - 使用者表`

`- [[DB-{table_name}]] - {說明}`

`### 關聯圖`

`{可以用 Mermaid 或其他工具畫 ERD}`

`---`

`## API 端點總覽`

`### 認證相關`

``- `POST /api/v1/auth/register` - [[API-註冊]] 使用者註冊``

``- `POST /api/v1/auth/login` - [[API-登入]] 使用者登入``

``- `POST /api/v1/auth/logout` - [[API-登出]] 使用者登出``

`### 使用者相關`

``- `GET /api/v1/users` - [[API-使用者列表]] 取得使用者列表``

``- `GET /api/v1/users/:id` - [[API-使用者詳情]] 取得使用者詳情``

``- `PUT /api/v1/users/:id` - [[API-更新使用者]] 更新使用者資料``

`---`

`## 第三方整合`

`| 服務名稱 | 用途 | 文件連結 |`

`|----------|------|----------|`

`| Stripe | 金流服務 | [[Integration-Stripe]] |`

`| Firebase | 推播通知 | [[Integration-Firebase]] |`

`| AWS S3 | 檔案儲存 | [[Integration-S3]] |`

`---`

`## 環境配置`

`### 開發環境`

` ```bash `

`NODE_ENV=development`

`API_URL=http://localhost:3000`

`DB_URL=postgresql://localhost:5432/myapp_dev`

` ``` `

`### 測試環境`

` ```bash `

`NODE_ENV=staging`

`API_URL=https://api-staging.example.com`

`DB_URL=postgresql://staging-db:5432/myapp_staging`

` ``` `

`### 正式環境`

` ```bash `

`NODE_ENV=production`

`API_URL=https://api.example.com`

`DB_URL=postgresql://prod-db:5432/myapp_prod`

` ``` `

`---`

`## 開發規範`

`### 程式碼風格`

`- 遵循 [[CLAUDE.MD]] 中的規範`

`- ESLint + Prettier 自動格式化`

`- TypeScript 嚴格模式`

`### Git 流程`

`- 分支策略: Git Flow`

`- Commit 規範: Conventional Commits`

`- PR Review: 至少 1 人審查`

`### 測試要求`

`- 單元測試覆蓋率 > 80%`

`- E2E 測試覆蓋核心流程`

`- 每次 PR 必須通過所有測試`

`---`

`## 時程規劃`

`| 階段 | 開始日期 | 結束日期 | 狀態 |`

`|------|----------|----------|------|`

`| 需求分析 | - | - | ☐ |`

`| 系統設計 | - | - | ☐ |`

`| 前端開發 | - | - | ☐ |`

`| 後端開發 | - | - | ☐ |`

`| 整合測試 | - | - | ☐ |`

`| 上線部署 | - | - | ☐ |`

`---`

`## 風險與問題`

`### 技術風險`

`- [ ] {風險描述} - 應對方案：{方案}`

`### 專案風險`

`- [ ] {風險描述} - 應對方案：{方案}`

`### 已知問題`

`- {問題描述} - 狀態：{處理中/已解決}`

`---`

`## 文件索引`

`### 需求文件`

`- [[01-Requirements]] - 詳細需求規格`

`### API 文件`

`- [[02-API-Spec]] - API 規格總覽`

`### 資料庫文件`

`- [[03-Database-Schema]] - 資料庫設計`

`### 架構文件`

`- [[04-Architecture]] - 系統架構說明`

`### 整合文件`

`- [[05-Integrations]] - 第三方服務整合`

`---`

`## 團隊成員`

`| 角色 | 負責人 | 職責 |`

`|------|--------|------|`

`| 專案負責人 | - | 整體協調 |`

`| 前端開發 | Gemini | 前端實作 |`

`| 後端開發 | Claude | 後端實作 |`

`---`

`## 相關連結`

`- **Git Repository**: {GitHub/GitLab 連結}`

`- **API 文件**: {Swagger/Postman 連結}`

`- **測試環境**: {URL}`

`- **正式環境**: {URL}`

`- **專案管理**: {Jira/Trello 連結}`

`---`

`## 更新紀錄`

`| 日期 | 版本 | 變更內容 | 更新人 |`

`|------|------|----------|--------|`

`| 2025-11-27 | v1.0 | 建立專案 | - |`

` ``` `

`---`