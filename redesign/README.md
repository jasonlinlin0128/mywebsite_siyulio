# siyulio.com 像素風改版（草稿）

選定風格：18 一位元／像素風。純靜態檔，不經 Quartz build，不影響現行部署。

- `index.html`、`css/` 由 `tools/build.py` 產生，不要手改。
- 文字內容改 `tools/content.json`。
- 配色只住在 `css/palette.css`；換色：`py redesign/tools/build.py 18k`（可選 18a～18n，現用值記在 `tools/palette.txt`）。
- 配色定義在 `tools/palettes18.py`，build 前會跑對比檢查（文字 ≥4.5、focus ≥3），不過就不輸出。
- 本機預覽：`py -m http.server 8765 -d redesign`，開 http://localhost:8765/。

配色比較頁（14 組）：https://claude.ai/artifact/AnUUe8JASPZffyCdJf86Yc
