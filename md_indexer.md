# Markdown Index Generator

Markdownファイルのインデックスを自動生成するシンプルなPythonスクリプトです。指定されたフォルダ内のすべての`.md`ファイルを探し出し、それらへのリンクを含む新しいMarkdownファイルを生成します。

## 機能

- フォルダ内のすべてのMarkdownファイル（`.md`）を検索
- ファイル名とリンクを含むインデックスMarkdownファイルを生成
- ファイルの作成日時を表示（オプション）
- ファイルの説明（Markdownファイルの最初の見出し）を抽出して表示（オプション）
- 出力するインデックスファイルはインデックス自体をリストに含めない

## 必要条件

- Python 3.6以上

## インストール

このリポジトリをクローンするか、スクリプトファイルをダウンロードしてください。

```bash
git clone https://github.com/yourusername/markdown-index-generator.git
cd markdown-index-generator
```

## 使い方

### 基本的な使い方

```bash
# スクリプトに実行権限を付与（Unix/Linux/Macの場合）
chmod +x md_indexer.py

# カレントディレクトリのMDファイルをインデックス化
python md_indexer.py

# または直接実行
./md_indexer.py
```

### コマンドラインオプション

```
usage: md_indexer.py [-h] [-d DIRECTORY] [-o OUTPUT] [-t TITLE] [--no-date] [--no-description]

Markdownファイルのインデックスを生成します。

options:
  -h, --help            ヘルプメッセージを表示して終了
  -d DIRECTORY, --directory DIRECTORY
                        Markdownファイルを検索するディレクトリ（デフォルト: カレントディレクトリ）
  -o OUTPUT, --output OUTPUT
                        出力するインデックスファイルの名前（デフォルト: index.md）
  -t TITLE, --title TITLE
                        インデックスファイルのタイトル（デフォルト: Markdown ファイル一覧）
  --no-date             ファイルの作成日時を含めない
  --no-description      ファイルの説明を含めない
```

### 使用例

```bash
# 特定のディレクトリを指定
python md_indexer.py -d /path/to/your/docs

# 出力ファイル名を指定
python md_indexer.py -o markdown_list.md

# インデックスのタイトルを指定
python md_indexer.py -t "プロジェクトドキュメント一覧"

# 日付と説明を含めない
python md_indexer.py --no-date --no-description
```

## 出力例

生成されるインデックスファイルの例：

```markdown
# Markdown ファイル一覧

*生成日時: 2025-04-30 15:30:45*
*このファイルは自動生成されました*

## [document1.md](document1.md)
*プロジェクト概要*
- 作成日: 2025-04-15

## [setup-guide.md](setup-guide.md)
*セットアップガイド*
- 作成日: 2025-04-20

## [troubleshooting.md](troubleshooting.md)
*よくある問題と解決策*
- 作成日: 2025-04-25
```

## カスタマイズ

スクリプト内の関数とオプションを変更することで、必要に応じてカスタマイズできます。例えば：

- インデックスのフォーマットを変更
- 追加のファイルメタデータを表示（ファイルサイズなど）
- ファイルをカテゴリごとにグループ化

## ライセンス

[MIT](LICENSE)

## 貢献

バグ報告や機能リクエストは、GitHubの課題トラッカーで受け付けています。プルリクエストも歓迎します。

## 作者

しろっちょ

---

*このプロジェクトは自分のワークフローを効率化するために作成されました。ご自由にカスタマイズしてお使いください。*
