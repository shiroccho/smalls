# Crontab Generator

直感的なインターフェースでcrontab行を簡単に生成できるシンプルなWebアプリケーションです。

## 機能

- **視覚的なプルダウンインターフェース**: 分、時、日、月、曜日の設定が直感的に行えます
- **柔軟な時間設定**: 各時間要素に対して以下の設定が可能
  - 特定の値 (例: 5分)
  - 毎回 (*)
  - 範囲 (例: 1-5)
  - 間隔 (例: */15)
- **コマンド検証**: 入力されたコマンドが正しくフルパス（"/"で始まる）かどうか自動チェック
- **即時プレビュー**: 設定を変更すると即座にcrontab行が更新されます
- **コピー機能**: 生成されたcrontab行を簡単にクリップボードにコピー可能
- **リセット機能**: 全ての設定を初期状態に戻せます
- **参考情報**: crontabの書式説明と実例を含む

## 使い方

1. HTMLファイルをブラウザで開きます
2. 各時間要素（分、時、日、月、曜日）の設定方法を選択
   - 特定の値: 特定の数値を指定
   - 毎回: アスタリスク (*) を使用
   - 範囲: 開始値と終了値を指定
   - 間隔: 一定間隔で繰り返し
3. 実行するコマンドをフルパスで入力
4. 生成されたcrontab行が下部に表示されます
5. 「コピー」ボタンでクリップボードにコピー可能

## 技術仕様

- 純粋なHTML、CSS、JavaScriptで実装
- 外部ライブラリやフレームワークに依存しない
- 単一のHTMLファイルで完結
- ブラウザ上でのみ動作（サーバー不要）

## 例

以下のようなcrontab設定がすぐに生成できます：

- 毎日12:00に実行: `0 12 * * * /usr/bin/backup.sh`
- 15分ごとに実行: `*/15 * * * * /usr/bin/check-service.sh`
- 毎月1日の0:00に実行: `0 0 1 * * /usr/bin/monthly-report.sh`

## インストール

インストールは不要です。単一のHTMLファイルなので、ダウンロードしてブラウザで開くだけで使用できます。

## ライセンス

MIT

---

作成：2025年5月
