# 接手測試協議

可重複執行的 pilot 測試，用於膠囊 + Git 對齊。在複製 `.capsule/` 到其他 repo 前先跑完。

---

## 前置

- 已有膠囊目錄（如 `.capsule/`）
- Git 上至少有一個 `capsule/<hash>` tag
- 本地驗證：

```bash
python scripts/verify_capsule.py --check-git-tag
```

---

## 測試矩陣（三項）

| 測試 | 目的 | 通過條件 |
|------|------|---------|
| **T1 冷接手** | 新 AI 不靠聊天紀錄恢復脈絡 | 見下方評分 |
| **T2 回滾演練** | 還原舊 checkpoint | Git + 膠囊一致；AI 引用舊 hash |
| **T3 里程碑滾動** | 小改動 → 新 hash + tag | verifier PASS；tag 已 push |

Pilot 完成：**T1 通過 2～3 次**（可換工具）+ **T3 至少做過一次**。

---

## T1 — 冷接手

### 你的步驟

1. 開**新** AI session（可換工具）。
2. 貼 `RESUME_INSTRUCTIONS.md` 區塊。
3. 附上：`TASK_STATUS_REPORT.md`、`DECISION_LOG.md`、`BRANCH_INFO.md`、`STATE_MANIFEST.json`。
4. **不要**貼舊對話紀錄。

### AI 首則回覆評分

| # | 項目 | PASS |
|---|------|------|
| 1 | 說出正確 `version_hash` | 與 manifest 一致 |
| 2 | 說出 `branch` | 與 manifest 一致 |
| 3 | 3～5 句階段摘要 | 與報告 §2 / §5 一致 |
| 4 | 引用 Priority Action 1 | 來自報告 §4 |
| 5 | 無範圍膨脹 | 未擅自做 Todo 外大項 |
| 6 | 等待指示 | 未自動開大型工程 |

**PASS：** 1～6 皆符合。  
記錄於 `TASK_STATUS_REPORT.md` → Experiments / Tests。

---

## T2 — 回滾演練

1. 記下當前 hash `A`、上一版 `B`。
2. `git checkout capsule/B`（或還原該 commit 的 `.capsule/`）。
3. 用 hash `B` 的 `RESUME_INSTRUCTIONS` 開新 session。
4. 確認 AI 引用的是 `B` 而非 `A`。

通過後：`git checkout main` 回到最新膠囊。

---

## T3 — 里程碑滾動

文檔/腳本變更或 T1 記錄後：

1. 更新六檔案；遞增 `version_hash`，填 `previous_version_hash`。
2. 執行：

```bash
python scripts/verify_capsule.py --capsule-dir .capsule
git add .capsule/
git commit -m "chore: ... (capsule vYYYYMMDD-HHMM-xxxx)"
git tag -a capsule/vYYYYMMDD-HHMM-xxxx -m "Capsule checkpoint"
python scripts/verify_capsule.py --check-git-tag
git push origin master
git push origin capsule/vYYYYMMDD-HHMM-xxxx
```

---

## 失敗處理

| 現象 | 做法 |
|------|------|
| hash 錯 | 重貼 resume + manifest |
| 重做 Done | 引用 Done；跑 `RECOVERY_CHECK.md` §1 |
| 膠囊與 Git 不一致 | `GIT_CAPSULE_ALIGNMENT.md` 回滾流程 |
| verifier FAIL | 先修 hash 再測接手 |

---

## Pilot 結束條件

- [ ] T1 PASS × 2～3
- [ ] T2 回滾 × 1
- [ ] T3 滾動 × 2+（hash 鏈 ≥ 3 層）
- [ ] 最新版 `verify_capsule.py --check-git-tag` PASS

再考慮複製到第二個 repo。

英文版：[`HANDOFF_TEST_PROTOCOL.md`](HANDOFF_TEST_PROTOCOL.md)