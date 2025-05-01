# Google風ディレクトリ一覧ジェネレーター

Google Drive風のUIで、ディレクトリとファイルを視覚的に表示するHTMLページを生成するPythonスクリプトです。CDNを利用してGoogle風のデザインを実現し、シンプルかつ使いやすいインターフェースを提供します。

![Google風ディレクトリ一覧](https://api.placeholder/800/400)

## 特徴

- **Google Drive風UI**: Googleのデザイン言語に準拠したモダンなインターフェース
- **検索機能**: リアルタイムでファイルを検索可能
- **レスポンシブデザイン**: スマートフォン、タブレット、PC向けに最適化
- **画像ギャラリー**: 画像ファイルをきれいなグリッドレイアウトで表示
- **Google風カラーコード**: Googleのブランドカラーでアイコンをカテゴリごとにカラーリング
- **フォルダのアコーディオン表示**: 直感的な折りたたみ機能
- **CDN利用**: jQuery、Font Awesome、Google Fontsを利用して高品質なUIを実現

## 使用技術

- **jQuery**: 動的なUI操作
- **Google Fonts**: Robotoフォント
- **Font Awesome**: ファイルタイプアイコン
- **CSS変数**: Googleカラーパレットの効率的な適用

## 対応ファイル形式

### 画像ファイル (グリッドギャラリー表示)
- JPG/JPEG
- PNG
- WebP
- GIF

### ドキュメントファイル (Google風アイコン表示)-機能停止予定（コードは停止してる）
- PDF (赤色アイコン)
- Word文書 (青色アイコン)
- Excelスプレッドシート (緑色アイコン)
- PowerPointプレゼンテーション (黄色アイコン)
- その他多数のファイル形式

## インストール

外部依存関係はなく、Python 3.6以上が必要です。

```bash
# リポジトリのクローン
git clone https://github.com/yourusername/google-directory-listing.git
cd google-directory-listing
```

## 使い方

基本的な使用方法:

```bash
python generate_folder_html.py [ディレクトリパス]
```

ディレクトリパスを省略すると、現在のディレクトリが使用されます。

### 例

現在のディレクトリの一覧を生成:

```bash
python generate_folder_html.py
```

指定したディレクトリの一覧を生成:

```bash
python generate_folder_html.py /path/to/your/directory
```

## 出力

実行すると、以下の名前でHTMLファイルが生成されます:

```
directory_listing_[ディレクトリ名].html
```

このファイルをウェブブラウザで開くと、Google Drive風のインターフェースでディレクトリ内容が表示されます。

## 検索機能の使用方法

ページ上部の検索バーにキーワードを入力すると、ファイル名がリアルタイムでフィルタリングされます。
検索にマッチしたファイルが含まれるフォルダは自動的に開かれます。

## カスタマイズ

### Googleカラーの変更

`:root`セクション内のCSS変数を編集することで、カラースキームを変更できます:

```css
:root {
    --google-blue: #4285F4;
    --google-red: #EA4335;
    --google-yellow: #FBBC05;
    --google-green: #34A853;
    ...
}
```

### アイコン設定の変更

`get_file_icon`関数で、特定のファイル拡張子に対するアイコンとカラーを変更できます:

```python
def get_file_icon(extension):
    icons = {
        '.pdf': {'icon': 'fas fa-file-pdf', 'css_class': 'file-icon-pdf'},
        ...
    }
```

## 技術的詳細

- **フォルダ展開**: jQueryを使用した滑らかなアニメーション
- **検索機能**: キー入力ごとにリアルタイムで結果を更新
- **レスポンシブグリッド**: CSSグリッドレイアウトによる柔軟な画像表示
- **CDN利用**: 高速読み込みと安定性のためにCDNを使用

## 注意事項

- このスクリプトはローカル環境での使用を想定しています
- 大量のファイルがある場合は、ブラウザのパフォーマンスに影響する可能性があります
- CDNを使用しているため、オフライン環境では一部の機能が制限される場合があります

## ライセンス

[MIT License](LICENSE)

## 貢献

バグ報告や機能追加のリクエストは、Issueまたはプルリクエストでお願いします。
