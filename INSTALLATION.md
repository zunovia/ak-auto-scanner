# 📦 AK Auto-Scanner - インストールガイド

## 2つのインストール方法

### 方法1: 実行可能ファイル（.exe）を使用（推奨）

別のPCで使用する場合、最も簡単な方法です。

#### ダウンロード

1. [Releases](https://github.com/YOUR_USERNAME/ak-auto-scanner/releases)ページへ
2. 最新バージョンの`AKAutoScanner.zip`をダウンロード
3. ZIPファイルを解凍
4. フォルダ内の`AKAutoScanner.exe`をダブルクリック

#### システム要件
- Windows 10 以降
- Kindle for PC アプリ
- インターネット接続不要（実行時）

---

### 方法2: Pythonソースコードから実行

開発者向けまたはカスタマイズしたい場合

#### 必要なもの
- Python 3.8 以降
- Kindle for PC アプリ

#### インストール手順

1. **リポジトリをクローン**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ak-auto-scanner.git
   cd ak-auto-scanner
   ```

2. **仮想環境を作成（推奨）**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **依存関係をインストール**
   ```bash
   pip install -r requirements.txt
   ```

4. **アプリを起動**
   ```bash
   python src\main.py
   ```

   または

   ```bash
   .\run_scanner.bat
   ```

---

## 📖 使い方

詳細は以下のドキュメントを参照してください：

- **[START_HERE.md](START_HERE.md)** - 簡単スタートガイド
- **[README.md](README.md)** - 完全マニュアル
- **[QUICKSTART_SCANNER.md](QUICKSTART_SCANNER.md)** - クイックスタート

---

## 🏗️ 開発者向け：実行可能ファイルのビルド

自分で.exeファイルをビルドする場合：

1. **依存関係をインストール**
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **ビルドスクリプトを実行**
   ```bash
   .\build_exe.bat
   ```

3. **実行可能ファイルを確認**
   - 場所: `dist\AKAutoScanner\AKAutoScanner.exe`
   - フォルダごと別のPCにコピー可能

---

## ⚠️ トラブルシューティング

### Windows Defender の警告

初回実行時にWindows Defenderが警告を出す場合：
1. 「詳細情報」をクリック
2. 「実行」をクリック

これは署名されていない実行可能ファイルに対する標準的な警告です。

### "DLLが見つかりません" エラー

[Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)をインストールしてください。

### "Kindleウィンドウが見つかりません"

1. Kindle for PCが起動しているか確認
2. 本を開いているか確認（ライブラリビューではなく）

---

## 🆘 サポート

問題が発生した場合：
1. ログファイルを確認: `output\logs\`
2. [Issues](https://github.com/YOUR_USERNAME/ak-auto-scanner/issues)で報告
3. README.mdのトラブルシューティングセクションを参照

---

**Version**: 1.0.0
**Last Updated**: 2026-02-04
