# 🚀 完全セットアップガイド

このガイドでは、インストーラーの作成からGitHubへのプッシュまで、すべての手順を説明します。

---

## 📋 目次

1. [実行可能ファイル（インストーラー）の作成](#1-実行可能ファイルインストーラーの作成)
2. [GitHubへのプッシュ](#2-githubへのプッシュ)
3. [リリースの作成と公開](#3-リリースの作成と公開)
4. [別のPCでの使用](#4-別のpcでの使用)

---

## 1. 実行可能ファイル（インストーラー）の作成

### ステップ1.1: ビルドの実行

プロジェクトフォルダで以下を実行：

```powershell
cd C:\temp\kindle-pdf

# 実行可能ファイルをビルド
.\build_exe.bat
```

**処理内容:**
- PyInstallerのインストール
- Python環境のパッケージング
- 実行可能ファイルの生成

**完了後の確認:**
- `dist\AKAutoScanner\AKAutoScanner.exe` が作成されているか確認
- フォルダサイズ: 約150-200MB

### ステップ1.2: テスト実行

```powershell
# ビルドした実行可能ファイルをテスト
cd dist\AKAutoScanner
.\AKAutoScanner.exe
```

動作確認：
- ✅ GUIが正常に起動する
- ✅ Kindleウィンドウが検出される
- ✅ スキャンが正常に実行できる

### ステップ1.3: リリースパッケージの作成

```powershell
# プロジェクトルートに戻る
cd C:\temp\kindle-pdf

# リリースパッケージ（ZIP）を作成
.\create_release.bat
```

**生成されるファイル:**
- `AKAutoScanner-v1.0.0.zip` (配布用)

**ZIPの内容:**
```
AKAutoScanner-v1.0.0/
├── AKAutoScanner/
│   ├── AKAutoScanner.exe  ← メイン実行ファイル
│   └── (その他の依存ファイル)
├── output/                     ← PDF保存フォルダ
├── README.md
├── START_HERE.md
├── INSTALLATION.md
├── LICENSE
└── README.txt                  ← 簡単な説明
```

---

## 2. GitHubへのプッシュ

### ステップ2.1: Gitの確認とインストール

```powershell
# Gitのバージョン確認
git --version
```

インストールされていない場合:
- [Git for Windows](https://git-scm.com/download/win)をダウンロード

### ステップ2.2: 自動セットアップスクリプトを実行

```powershell
cd C:\temp\kindle-pdf

# 自動セットアップスクリプトを実行
.\setup_github.bat
```

**スクリプトが実行すること:**
1. Gitリポジトリの初期化
2. ファイルのステージング
3. 初回コミットの作成
4. リモートリポジトリの設定

**入力が必要な情報:**
- GitHubユーザー名
- リポジトリ名（デフォルト: ak-auto-scanner）

### ステップ2.3: GitHubでリポジトリを作成

ブラウザで以下を実行：

1. [GitHub](https://github.com)にログイン
2. 右上の「+」→「New repository」
3. 設定：
   ```
   Repository name: ak-auto-scanner
   Description: Automated Kindle page scanner and PDF generator
   Visibility: Public または Private

   ⚠️ 重要: "Initialize this repository with:" のチェックを外す
   ```
4. 「Create repository」をクリック

### ステップ2.4: プッシュ

```powershell
# GitHubにプッシュ
git push -u origin main
```

**認証方法:**

#### 方法A: Personal Access Token（推奨）

1. GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. 「Generate new token」
4. スコープ: `repo` にチェック
5. トークンをコピー
6. パスワードとして貼り付け

#### 方法B: GitHub Desktop

[GitHub Desktop](https://desktop.github.com/)を使用すると簡単です。

### ステップ2.5: 確認

ブラウザで確認：
```
https://github.com/YOUR_USERNAME/ak-auto-scanner
```

すべてのファイルが表示されていればOK！

---

## 3. リリースの作成と公開

### ステップ3.1: GitHubでリリースページを開く

```
https://github.com/YOUR_USERNAME/ak-auto-scanner/releases/new
```

### ステップ3.2: リリース情報を入力

**Tag version:**
```
v1.0.0
```

**Release title:**
```
AK Auto-Scanner v1.0.0 - Initial Release
```

**Description:** (例)
```markdown
## 🎉 初回リリース

AK Auto-Scanner の最初の安定版リリースです！

### ✨ 主な機能

- 📖 Kindle for PC から自動でページをキャプチャ
- 📄 PDFファイルに変換
- 🎯 スマート重複検出（本の終わりを自動検出）
- ⏱️ 5秒カウントダウン機能
- 📏 キャプチャマージン調整
- 🔄 日本語・英語書籍対応

### 📥 ダウンロード

下記の `AKAutoScanner-v1.0.0.zip` をダウンロードして解凍し、
`AKAutoScanner.exe` を実行してください。

### 📚 ドキュメント

- [インストールガイド](INSTALLATION.md)
- [使い方ガイド](START_HERE.md)
- [完全マニュアル](README.md)

### 💻 システム要件

- Windows 10 以降
- Kindle for PC アプリ

### 🐛 既知の問題

なし

---

詳細は [RELEASE_NOTES.md](RELEASE_NOTES.md) を参照してください。
```

### ステップ3.3: ZIPファイルをアップロード

「Attach binaries」セクションに以下をドラッグ＆ドロップ：
```
AKAutoScanner-v1.0.0.zip
```

### ステップ3.4: 公開

「Publish release」をクリック

---

## 4. 別のPCでの使用

### ステップ4.1: ダウンロード

別のPCで以下のURLにアクセス：
```
https://github.com/YOUR_USERNAME/ak-auto-scanner/releases
```

最新の `AKAutoScanner-v1.0.0.zip` をダウンロード

### ステップ4.2: 解凍と実行

1. ZIPファイルを解凍（右クリック→すべて展開）
2. `AKAutoScanner\AKAutoScanner.exe` をダブルクリック
3. 完了！Pythonのインストールは不要

### ステップ4.3: 使い方

1. Kindle for PC を開く
2. 本を開いて最初のページへ
3. `AKAutoScanner.exe` を起動
4. 設定を選択
5. 「Start Scanning」をクリック
6. 5秒後にスキャン開始

**PDF保存場所:**
```
AKAutoScanner\output\kindle_scan_YYYYMMDD_HHMMSS.pdf
```

---

## 🎯 完了チェックリスト

### ローカル環境
- [ ] `build_exe.bat` でビルド成功
- [ ] `AKAutoScanner.exe` が動作確認済み
- [ ] `create_release.bat` でZIP作成済み

### GitHub
- [ ] リポジトリ作成完了
- [ ] すべてのファイルをプッシュ済み
- [ ] リリース（v1.0.0）を作成済み
- [ ] ZIPファイルをアップロード済み

### テスト
- [ ] 別のPCでZIPをダウンロード・解凍
- [ ] 実行ファイルが正常に動作
- [ ] スキャン・PDF生成が成功

---

## 🆘 トラブルシューティング

### ビルドエラー

**エラー:** "PyInstaller not found"
```powershell
pip install pyinstaller
```

**エラー:** "Module not found"
```powershell
pip install -r requirements.txt
```

### Gitエラー

**エラー:** "Permission denied"
- Personal Access Token を使用してください

**エラー:** "Repository not found"
- GitHubでリポジトリを作成してください
- リモートURLが正しいか確認: `git remote -v`

### 実行ファイルエラー

**Windows Defender警告**
- 「詳細情報」→「実行」をクリック
- 署名されていない実行ファイルに対する標準警告です

**DLL not found**
- [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe) をインストール

---

## 📚 関連ドキュメント

- **[README.md](README.md)** - 完全マニュアル
- **[START_HERE.md](START_HERE.md)** - クイックスタート
- **[INSTALLATION.md](INSTALLATION.md)** - インストールガイド
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)** - GitHub詳細ガイド
- **[RELEASE_NOTES.md](RELEASE_NOTES.md)** - リリースノート

---

## 🎉 完了！

これで、AK Auto-Scanner を別のPCで使用できるようになりました！

**リリースURL:**
```
https://github.com/YOUR_USERNAME/ak-auto-scanner/releases
```

他のユーザーも上記URLからダウンロードして使用できます。

---

**Version**: 1.0.0
**Last Updated**: 2026-02-04
