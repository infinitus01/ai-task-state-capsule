# Git 與 Capsule 對齊

如何讓 **程式碼狀態**（Git）與 **任務狀態**（capsule）停在同一條時間線上。

> Capsule 回滾重置的是 AI 該相信什麼；Git 回滾重置的是磁碟上有什麼。**兩者要一起用。**

---

## 為什麼要對齊

| 層 | 回答什麼 |
|----|---------|
| **Git** | 哪個 commit 改了哪些檔案 |
| **Capsule** | 任務進度、決策、下一步、邊界 |
| **兩者對齊** | AI 從正確的敘事接手，且 repo 與敘事一致 |

只還原 capsule、不還原 Git → AI 描述的進度與實際檔案對不上。  
只 `git checkout`、不更新膠囊 → AI 不知道當初的決策與禁止項。

---

## 建議目錄

```text
your-repo/
├── .capsule/
│   ├── TASK_STATUS_REPORT.md
│   ├── DECISION_LOG.md
│   ├── BRANCH_INFO.md
│   ├── RESUME_INSTRUCTIONS.md
│   ├── RECOVERY_CHECK.md
│   └── STATE_MANIFEST.json
├── src/
└── ...
```

與程式碼相關的任務，膠囊建議放在**同一個 repo** 並納入版本管理。純研究、無 repo 時，可用旁路資料夾 + ZIP。

---

## 命名對齊

膠囊分支名盡量與 Git 對應：

| Capsule `branch` | Git 對應 |
|------------------|----------|
| `main` | `main` / `master` |
| `experiment/<name>` | 同名 branch |
| `rollback/<version-hash>` | tag：`capsule/<version-hash>` |
| `review/<name>` | 可選 branch 或 tag |

里程碑打 tag 範例：

```bash
git tag -a capsule/v20260706-1200-a1b2 -m "Capsule rollback point before risky refactor"
```

同一 hash 寫入 `STATE_MANIFEST.json` 的 `version_hash` 與 `BRANCH_INFO.md`。

---

## _checkpoint 流程（正常路徑）

每個里程碑：

1. 完成這一輪工作（程式、文件、測試視需要）
2. **更新六個膠囊檔** — 尤其 `version_hash`、`branch`、Done / Todo
3. **程式與膠囊一起 commit**（建議）或連續 commit 並在訊息中連結 hash：

```bash
git add .capsule/ src/
git commit -m "feat: parser milestone — capsule v20260706-1200-a1b2"
```

4. **可選：** 封裝 ZIP 供審計或離線交接
5. **高風險改動前：** 在當前 HEAD 打 `capsule/<version-hash>` tag

---

## 回滾流程（AI 或工作跑偏時）

1. **停止**當前 AI session
2. 執行 [`RECOVERY_CHECK.md`](../templates/RECOVERY_CHECK.md)
3. 從 manifest 或 Git tag 找到最後已知好的 **`version_hash`**
4. **還原 Git：**

```bash
git checkout capsule/v20260706-1200-a1b2
# 或：git checkout main && git reset --hard <commit-sha>
```

5. **還原膠囊**（若該 commit 尚未包含正確膠囊）：

```bash
git checkout capsule/v20260706-1200-a1b2 -- .capsule/
```

6. 將 manifest 的 `branch` 設為 `main` 或 `rollback/<version-hash>`
7. 在 `DECISION_LOG.md` 記錄回滾（標記被取代的決策）
8. **新 AI session：** 只貼還原後膠囊的 `RESUME_INSTRUCTIONS.md`

---

## 實驗分支

```text
main ──► experiment/new-api
              │
              ├─ 成功 → merge 回 main，在 main 更新膠囊
              └─ 失敗 → checkout main，在 DECISION_LOG 標記放棄
```

```bash
git checkout -b experiment/new-api
# 工作並更新膠囊（manifest branch = experiment/new-api）
```

放棄時：

```bash
git checkout main
# 膠囊：標記實驗 rejected；manifest branch 改回 main
```

不要刪除 `rollback/<hash>` tag — 那是安全網。

---

## Commit 訊息慣例（可選）

讓 Git log 可搜尋對應的 capsule hash：

```text
feat: add export adapter (capsule v20260706-1430-b2c3)
docs: update TASK_STATUS_REPORT (capsule v20260706-1500-c4d5)
rollback: restore to capsule v20260706-1200-a1b2
```

---

## 復原時多核對這四項

- [ ] `git status` 乾淨，或髒污狀態已寫進 blockers
- [ ] `TASK_STATUS_REPORT.md` 的 **Done** 與當前 HEAD 上的檔案一致
- [ ] manifest 的 `version_hash` 與要恢復的 tag/commit 一致
- [ ] `RESUME_INSTRUCTIONS.md` 是該 hash 的版本，不是較新的草稿

---

## 這套做法不做什麼

- Git 不會自動更新膠囊 — 六個檔仍要人手或流程維護
- 膠囊不會自動執行 `git checkout` — 需人類或腳本觸發
- Tag 不能取代需要 SHA-256 證據鏈時的 sealed audit ZIP

---

## 延伸閱讀

- [`BRANCH_AND_ROLLBACK.md`](BRANCH_AND_ROLLBACK.md)
- [`AI_RESUME_PROTOCOL.md`](AI_RESUME_PROTOCOL.md)
- [`GIT_CAPSULE_ALIGNMENT.md`](GIT_CAPSULE_ALIGNMENT.md)（英文版）