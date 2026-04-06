---
title: MyFirstApp Overview
tags:
  - obsidian-notes
  - project
---

這是一份示範型專案筆記，先用來整理一個簡單的使用者管理系統結構，方便後續延伸成 API、資料庫與架構文件。

## API 端點

- 使用者註冊：`POST /api/v1/users/register`
- 使用者登入：`POST /api/v1/users/login`
- 取得使用者資料：`GET /api/v1/users/me`

## 資料庫

- 使用者表設計：`users`
- 訂單表設計：`orders`

## 這份筆記目前的角色

這份內容先作為 Obsidian 筆記區的示範頁，後續如果我要把它公開成完整專案文章，會再補上：

- 問題背景
- 功能需求
- API 規格
- 資料庫設計
- 架構說明
