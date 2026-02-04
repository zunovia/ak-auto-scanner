# ⚡ クイックリファレンス

## 🏗️ インストーラーを作成する

```powershell
cd C:\temp\kindle-pdf
.\build_exe.bat
.\create_release.bat
```

**生成されるファイル:** `AKAutoScanner-v1.0.0.zip`

---

## 🚀 GitHubにプッシュする

### 自動セットアップ（推奨）

```powershell
cd C:\temp\kindle-pdf
.\setup_github.bat
```

入力事項：
- GitHubユーザー名
- リポジトリ名

その後：
1. [GitHub](https://github.com/new)でリポジトリ作成
2. `git push -u origin main`

### 手動セットアップ

```powershell
# 初期化
git init
git add .
git commit -m "Initial commit: AK Auto-Scanner v1.0.0"

# リモート追加
git remote add origin https://github.com/YOUR_USERNAME/ak-auto-scanner.git
git branch -M main

# プッシュ
git push -u origin main
```

---

## 📦 リリースを作成する

1. [リリースページ](https://github.com/YOUR_USERNAME/ak-auto-scanner/releases/new)を開く
2. タグ: `v1.0.0`
3. タイトル: `AK Auto-Scanner v1.0.0`
4. `AKAutoScanner-v1.0.0.zip` をアップロード
5. 「Publish release」をクリック

---

## 💾 別のPCで使う

1. [リリースページ](https://github.com/YOUR_USERNAME/ak-auto-scanner/releases)から `AKAutoScanner-v1.0.0.zip` をダウンロード
2. 解凍
3. `AKAutoScanner\AKAutoScanner.exe` を実行

---

## 🔄 コードを更新してプッシュ

```powershell
# 変更を確認
git status

# コミット
git add .
git commit -m "説明: 変更内容"

# プッシュ
git push
```

---

## 📁 プロジェクト構造

```
kindle-pdf/
├── src/                        # Python ソースコード
├── dist/                       # ビルドされた実行ファイル
├── build_exe.bat              # ビルドスクリプト
├── create_release.bat         # リリース作成
├── setup_github.bat           # GitHub自動セットアップ
├── run_scanner.bat            # 開発版起動
├── requirements.txt           # Python依存関係
└── README.md                  # ドキュメント
```

---

## 🆘 よくある問題

### ビルドエラー
```powershell
pip install pyinstaller
pip install -r requirements.txt
```

### Git認証エラー
- Personal Access Token を使用: [https://github.com/settings/tokens](https://github.com/settings/tokens)

### Windows Defender 警告
- 「詳細情報」→「実行」をクリック（安全です）

---

## 📚 詳細ドキュメント

| ファイル | 内容 |
|---------|------|
| [COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md) | 完全セットアップガイド |
| [GITHUB_SETUP.md](GITHUB_SETUP.md) | GitHub詳細ガイド |
| [INSTALLATION.md](INSTALLATION.md) | インストール方法 |
| [START_HERE.md](START_HERE.md) | 使い方ガイド |
| [README.md](README.md) | 完全マニュアル |

---

**すべてのコマンドは `C:\temp\kindle-pdf` で実行してください**
