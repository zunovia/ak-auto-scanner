# 🚀 GitHub セットアップガイド

このガイドでは、AK Auto-ScannerをGitHubにプッシュする手順を説明します。

## 前提条件

- Gitがインストールされていること
- GitHubアカウントを持っていること
- コマンドラインの基本的な知識

---

## ステップ1: Gitのインストール確認

```bash
git --version
```

インストールされていない場合は、[Git for Windows](https://git-scm.com/download/win)をダウンロードしてインストールしてください。

---

## ステップ2: Gitの初期設定

初回のみ実行（既に設定済みの場合はスキップ）：

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## ステップ3: ローカルリポジトリの初期化

プロジェクトフォルダで実行：

```bash
cd C:\temp\kindle-pdf

# Gitリポジトリを初期化
git init

# .gitignoreを確認（既に存在します）
```

---

## ステップ4: ファイルをステージング

```bash
# すべてのファイルを追加
git add .

# 状態を確認
git status
```

---

## ステップ5: 最初のコミット

```bash
git commit -m "Initial commit: AK Auto-Scanner v1.0.0

- Python-based Kindle page scanner
- Automatic page capture and PDF generation
- GUI with configurable settings
- Smart duplicate detection using SSIM
- 5-second countdown before scan
- Capture margin adjustment feature
"
```

---

## ステップ6: GitHubでリポジトリを作成

### Webブラウザで：

1. [GitHub](https://github.com)にログイン
2. 右上の「+」→「New repository」をクリック
3. 以下を設定：
   - **Repository name**: `ak-auto-scanner`（または任意の名前）
   - **Description**: `Automated Kindle page scanner and PDF generator for personal book backups`
   - **Public** または **Private** を選択
   - ✅ **Do NOT** initialize with README（既にREADME.mdがあるため）
4. 「Create repository」をクリック

---

## ステップ7: リモートリポジトリを追加

GitHubページに表示されるコマンドを使用（YOUR_USERNAMEを実際のユーザー名に置き換え）：

```bash
git remote add origin https://github.com/YOUR_USERNAME/ak-auto-scanner.git

# mainブランチに名前を変更（推奨）
git branch -M main
```

---

## ステップ8: GitHubにプッシュ

```bash
# 初回プッシュ
git push -u origin main
```

### 認証が求められた場合：

#### 方法1: Personal Access Token（推奨）

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 「Generate new token」をクリック
3. スコープで「repo」を選択
4. トークンをコピー
5. パスワードの代わりにトークンを貼り付け

#### 方法2: GitHub Desktop

[GitHub Desktop](https://desktop.github.com/)を使用すると認証が簡単です。

---

## ステップ9: 確認

ブラウザでGitHubリポジトリを開き、すべてのファイルがプッシュされたことを確認します。

```
https://github.com/YOUR_USERNAME/ak-auto-scanner
```

---

## 📦 リリースの作成（オプション）

実行可能ファイルを配布する場合：

### 1. 実行可能ファイルをビルド

```bash
.\build_exe.bat
```

### 2. ZIPファイルを作成

```bash
# PowerShellで実行
Compress-Archive -Path "dist\AKAutoScanner" -DestinationPath "AKAutoScanner-v1.0.0.zip"
```

### 3. GitHubでリリースを作成

1. GitHubリポジトリページへ
2. 「Releases」→「Create a new release」
3. タグを作成: `v1.0.0`
4. タイトル: `AK Auto-Scanner v1.0.0`
5. 説明を追加（機能リスト、変更点など）
6. `AKAutoScanner-v1.0.0.zip`をアップロード
7. 「Publish release」をクリック

---

## 🔄 日常の使い方

### 変更をコミット

```bash
# 変更を確認
git status

# ファイルを追加
git add .

# コミット
git commit -m "説明: 変更内容を簡潔に記述"

# プッシュ
git push
```

### 新機能のブランチを作成

```bash
# 新しいブランチを作成
git checkout -b feature/new-feature-name

# 変更を加えてコミット
git add .
git commit -m "Add: 新機能の説明"

# ブランチをプッシュ
git push -u origin feature/new-feature-name
```

---

## 📝 コミットメッセージの例

```bash
git commit -m "Add: マージン調整機能を追加"
git commit -m "Fix: 上下の文字が途切れる問題を修正"
git commit -m "Update: README.mdのインストール手順を更新"
git commit -m "Refactor: スキャナーコードをリファクタリング"
```

---

## 🆘 トラブルシューティング

### "Permission denied (publickey)" エラー

SSHキーを設定するか、HTTPSを使用してください：

```bash
git remote set-url origin https://github.com/YOUR_USERNAME/ak-auto-scanner.git
```

### プッシュが拒否される

```bash
# リモートの変更を取得
git pull origin main --rebase

# 再度プッシュ
git push
```

### 間違ったファイルをコミットした

```bash
# 最後のコミットを取り消し（変更は保持）
git reset --soft HEAD~1

# または特定のファイルを除外
git reset HEAD <file>
```

---

## 📚 参考リンク

- [Git公式ドキュメント](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com/)
- [GitHub Desktop](https://desktop.github.com/)

---

**これでGitHubへのセットアップは完了です！**

次回からは、変更を加えたら以下のコマンドでプッシュできます：

```bash
git add .
git commit -m "変更内容"
git push
```
