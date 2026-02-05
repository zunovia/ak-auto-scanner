# 📖 AK Auto-Scanner - 簡単スタートガイド

## 🚀 PCを立ち上げてから起動するまでの手順

### ステップ1: PowerShellを開く

**方法1: スタートメニュー**
- `Windowsキー` を押す
- 「powershell」と入力
- 「Windows PowerShell」をクリック

**方法2: ショートカット**
- `Windows + X` を押す
- 「Windows PowerShell」または「ターミナル」を選択

---

### ステップ2: プロジェクトフォルダに移動

```powershell
cd C:\temp\kindle-pdf
```

---

### ステップ3: Kindle for PCを起動

1. Kindle for PCアプリを開く
2. スキャンしたい本を開く
3. **最初のページ**を表示する

---

### ステップ4: スキャナーを起動

```powershell
.\run_scanner.bat
```

または

```powershell
python src\main.py
```

---

### ステップ5: 設定を調整

GUIウィンドウが開いたら：

1. **Page Direction（ページ方向）**を選択
   - 洋書 → Western (Right arrow →)
   - 和書 → Japanese (Left arrow ←)

2. **Resolution（解像度）**を選択
   - Medium (High) - 推奨 ★

3. **Capture Speed（速度）**を選択
   - Standard (1.0s) - 推奨 ★

4. **Scan Mode（スキャンモード）**を選択
   - All pages (全ページ自動) ★ - 推奨

5. **Capture Margins（余白調整）**
   - 上下の文字が途切れる場合は調整
   - デフォルト: Top -20px, Bottom -20px
   - まだ途切れる場合は -30px や -40px に増やす

---

### ステップ6: スキャン開始

- 「**Start Scanning**」ボタンをクリック
- **5秒のカウントダウン**が始まります
- カウントダウン中にKindleウィンドウを確認できます
- 5秒後に自動でページキャプチャ開始
- ESCキーでいつでも停止できます

---

### ステップ7: 完成したPDFを確認

スキャン完了後、以下に保存されます：

```
C:\temp\kindle-pdf\output\kindle_scan_日付_時刻.pdf
```

PowerShellで開く：
```powershell
explorer output
```

---

## 💡 コピペ用コマンド一覧

```powershell
# 1. フォルダに移動
cd C:\temp\kindle-pdf

# 2. スキャナー起動
.\run_scanner.bat

# 3. 完了後、PDFを確認
explorer output
```

---

## ⚠️ 注意点

- Kindle for PCで**最初のページ**を表示しておく
- スキャン中はKindleウィンドウを**触らない**
- 途中でやめたい場合は**ESCキー**を押す
- 初回起動時は依存関係のインストールに数分かかります

---

## 🔧 トラブルシューティング

### 上下の文字が途切れる
→ GUIの「Capture Margins」で Top/Bottom を -30px や -40px に増やす

### ページがぼやける
→ Resolution を「High (Ultra)」に変更

### スキャンが止まらない
→ ESCキーを押すか、ウィンドウの「Stop」ボタンをクリック

---

## 📚 詳細マニュアル

- **完全マニュアル**: `README.md`
- **クイックスタート**: `QUICKSTART_SCANNER.md`

---

**Version**: 1.0.0
**Last Updated**: 2026-02-04
