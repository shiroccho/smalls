#!/usr/bin/env python3
import os
import sys
import base64
from pathlib import Path
import mimetypes

# 画像ファイルの拡張子
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.gif']

def generate_html(directory_path):
    """ディレクトリ内のフォルダとファイルを一覧表示するHTMLを生成"""
    
    # HTMLの開始部分
    html = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ディレクトリ一覧</title>
    <!-- Google Fonts -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.cdnjs.cloudflare.com/css2?family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">
    <!-- Material Icons -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/material-design-icons/4.0.0/font/MaterialIcons-Regular.min.css" rel="stylesheet">
    <style>
        :root {
            --google-blue: #4285F4;
            --google-red: #EA4335;
            --google-yellow: #FBBC05;
            --google-green: #34A853;
            --google-gray: #f1f1f1;
            --google-text: #5f6368;
            --google-text-dark: #202124;
            --google-border: #dadce0;
            --shadow: 0 1px 6px rgba(32, 33, 36, 0.28);
            --hover-shadow: 0 1px 8px rgba(32, 33, 36, 0.38);
            --border-radius: 8px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Roboto', Arial, sans-serif;
        }

        body {
            color: var(--google-text);
            background-color: #fff;
            line-height: 1.6;
            padding: 0;
            margin: 0;
        }

        .header {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            border-bottom: 1px solid var(--google-border);
            position: sticky;
            top: 0;
            background-color: white;
            z-index: 100;
        }

        .header-logo {
            display: flex;
            align-items: center;
            margin-right: 30px;
        }

        .header-logo img {
            height: 24px;
        }

        .header-title {
            font-size: 20px;
            color: var(--google-text-dark);
            font-weight: normal;
            margin-left: 15px;
        }

        .search-bar {
            flex-grow: 1;
            max-width: 700px;
            position: relative;
            margin: 0 20px;
        }

        .search-input {
            width: 100%;
            padding: 12px 20px;
            border: 1px solid var(--google-border);
            border-radius: 24px;
            font-size: 16px;
            color: var(--google-text-dark);
            outline: none;
            transition: all 0.2s;
        }

        .search-input:focus {
            box-shadow: var(--shadow);
        }

        .search-icon {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--google-blue);
        }

        .main-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .folder-container {
            margin-bottom: 25px;
        }

        .folder-header {
            display: flex;
            align-items: center;
            padding: 15px;
            background-color: white;
            border-radius: var(--border-radius);
            border: 1px solid var(--google-border);
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .folder-header:hover {
            box-shadow: var(--shadow);
        }

        .folder-header.active {
            box-shadow: var(--shadow);
            border-color: var(--google-blue);
        }

        .folder-icon {
            color: var(--google-blue);
            margin-right: 15px;
            font-size: 20px;
        }

        .folder-name {
            font-size: 16px;
            font-weight: 500;
            color: var(--google-text-dark);
            flex-grow: 1;
        }

        .folder-toggle {
            color: var(--google-text);
            transition: transform 0.3s;
        }

        .folder-header.active .folder-toggle {
            transform: rotate(180deg);
            color: var(--google-blue);
        }

        .folder-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
            background-color: white;
            border-radius: 0 0 var(--border-radius) var(--border-radius);
        }

        .folder-header.active + .folder-content {
            max-height: 5000px; /* 大きな値を設定して完全に開くようにする */
        }

        .image-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
            gap: 16px;
            padding: 16px;
        }

        .image-item {
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(32, 33, 36, 0.2);
            transition: all 0.2s;
            position: relative;
            background-color: white;
        }

        .image-item:hover {
            box-shadow: var(--hover-shadow);
            transform: translateY(-2px);
        }

        .image-container {
            width: 100%;
            height: 140px;
            overflow: hidden;
            position: relative;
        }

        .thumbnail {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s;
        }

        .image-item:hover .thumbnail {
            transform: scale(1.05);
        }

        .image-name {
            padding: 8px 10px;
            font-size: 13px;
            color: var(--google-text-dark);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            border-top: 1px solid var(--google-border);
        }

        .file-list {
            padding: 0 16px 16px;
        }

        .file-item {
            display: flex;
            align-items: center;
            padding: 10px 16px;
            border-radius: var(--border-radius);
            margin-bottom: 8px;
            transition: all 0.2s;
        }

        .file-item:hover {
            background-color: var(--google-gray);
        }

        .file-icon {
            margin-right: 15px;
            width: 24px;
            text-align: center;
        }

        .file-icon-pdf {
            color: var(--google-red);
        }

        .file-icon-doc {
            color: var(--google-blue);
        }

        .file-icon-sheet {
            color: var(--google-green);
        }

        .file-icon-slide {
            color: var(--google-yellow);
        }

        .file-icon-audio {
            color: var(--google-blue);
        }

        .file-icon-video {
            color: var(--google-red);
        }

        .file-icon-code {
            color: var(--google-blue);
        }

        .file-icon-archive {
            color: var(--google-yellow);
        }

        .file-name {
            font-size: 14px;
            color: var(--google-text-dark);
            flex-grow: 1;
        }

        .file-name a {
            color: var(--google-text-dark);
            text-decoration: none;
            transition: color 0.2s;
        }

        .file-name a:hover {
            color: var(--google-blue);
        }

        .section-title {
            font-size: 20px;
            color: var(--google-text-dark);
            font-weight: normal;
            margin: 30px 0 15px;
            padding-bottom: 5px;
            border-bottom: 1px solid var(--google-border);
        }

        /* レスポンシブデザイン */
        @media screen and (max-width: 768px) {
            .header {
                flex-direction: column;
                align-items: flex-start;
                padding: 10px;
            }

            .header-logo {
                margin-bottom: 10px;
                margin-right: 0;
            }

            .search-bar {
                width: 100%;
                max-width: none;
                margin: 10px 0;
            }

            .image-gallery {
                grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            }

            .image-container {
                height: 100px;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-logo">
            <svg width="24" height="24" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z" fill="#4285F4"/>
            </svg>
            <h1 class="header-title">ディレクトリ一覧: """ + os.path.basename(directory_path) + """</h1>
        </div>
        <div class="search-bar">
            <input type="text" class="search-input" id="search-input" placeholder="ファイルを検索...">
            <span class="search-icon">
                <i class="fas fa-search"></i>
            </span>
        </div>
    </header>
    <main class="main-content">
"""

    # ディレクトリ内のすべてのファイルとフォルダを取得
    items = sorted(os.listdir(directory_path))
    
    # 最初にフォルダを処理
    folders = [item for item in items if os.path.isdir(os.path.join(directory_path, item))]
    
    # フォルダごとにアコーディオンを作成
    for folder in folders:
        folder_path = os.path.join(directory_path, folder)
        
        html += f'''        <div class="folder-container">
            <div class="folder-header">
                <div class="folder-icon">
                    <i class="fas fa-folder"></i>
                </div>
                <div class="folder-name">{folder}</div>
                <div class="folder-toggle">
                    <i class="fas fa-chevron-down"></i>
                </div>
            </div>
            <div class="folder-content">
'''
        
        # フォルダ内のファイルを取得
        folder_items = sorted(os.listdir(folder_path))
        
        # 画像ファイルとその他のファイルを分ける
        image_files = []
        other_files = []
        
        for item in folder_items:
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                ext = os.path.splitext(item.lower())[1]
                if ext in IMAGE_EXTENSIONS:
                    image_files.append(item)
                else:
                    other_files.append(item)
        
        # 画像ファイルがあれば表示
        if image_files:
            html += '                <div class="image-gallery">\n'
            
            for image in image_files:
                image_path = os.path.join(folder, image).replace('\\', '/')
                
                html += f'''                    <div class="image-item">
                        <a href="{image_path}" target="_blank">
                            <div class="image-container">
                                <img src="{image_path}" class="thumbnail" alt="{image}">
                            </div>
                            <div class="image-name">{image}</div>
                        </a>
                    </div>
'''
            
            html += '                </div>\n'
        
        # その他のファイルを表示
        if other_files:
            html += '                <div class="file-list">\n'
            
            for file in other_files:
                file_path = os.path.join(folder, file).replace('\\', '/')
                file_ext = os.path.splitext(file.lower())[1]
                
                # ファイル拡張子に応じたアイコンとCSSクラスを設定
                icon_info = get_file_icon(file_ext)
                
                html += f'''                    <div class="file-item">
                        <div class="file-icon {icon_info['css_class']}">
                            <i class="{icon_info['icon']}"></i>
                        </div>
                        <div class="file-name">
                            <a href="{file_path}" target="_blank">{file}</a>
                        </div>
                    </div>
'''
            
            html += '                </div>\n'
        
        html += '            </div>\n'
        html += '        </div>\n\n'
    
    # ルートディレクトリのファイルを処理
    root_files = [item for item in items if os.path.isfile(os.path.join(directory_path, item))]
    
    if root_files:
        html += '        <div class="section-title">ファイル</div>\n'
        
        # 画像ファイルとその他のファイルを分ける
        image_files = []
        other_files = []
        
        for item in root_files:
            item_path = os.path.join(directory_path, item)
            ext = os.path.splitext(item.lower())[1]
            if ext in IMAGE_EXTENSIONS:
                image_files.append(item)
            else:
                other_files.append(item)
        
        # 画像ファイルがあれば表示
        if image_files:
            html += '        <div class="image-gallery">\n'
            
            for image in image_files:
                html += f'''            <div class="image-item">
                <a href="{image}" target="_blank">
                    <div class="image-container">
                        <img src="{image}" class="thumbnail" alt="{image}">
                    </div>
                    <div class="image-name">{image}</div>
                </a>
            </div>
'''
            
            html += '        </div>\n'
        
        # その他のファイルを表示
        if other_files:
            html += '        <div class="file-list">\n'
            
            for file in other_files:
                file_ext = os.path.splitext(file.lower())[1]
                
                # ファイル拡張子に応じたアイコンとCSSクラスを設定
                icon_info = get_file_icon(file_ext)
                
                html += f'''            <div class="file-item">
                <div class="file-icon {icon_info['css_class']}">
                    <i class="{icon_info['icon']}"></i>
                </div>
                <div class="file-name">
                    <a href="{file}" target="_blank">{file}</a>
                </div>
            </div>
'''
            
            html += '        </div>\n'

    # HTMLの終了部分とJavaScript
    html += """    </main>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script>
        $(document).ready(function() {
            // フォルダヘッダーのクリックイベント
            $('.folder-header').click(function() {
                $(this).toggleClass('active');
            });

            // 検索機能
            $('#search-input').on('keyup', function() {
                var searchText = $(this).val().toLowerCase();
                
                // ファイル項目を検索
                $('.file-item').each(function() {
                    var fileName = $(this).find('.file-name').text().toLowerCase();
                    if (fileName.indexOf(searchText) > -1) {
                        $(this).show();
                        // 親フォルダを開く
                        $(this).closest('.folder-content').prev('.folder-header').addClass('active');
                    } else {
                        $(this).hide();
                    }
                });
                
                // 画像項目を検索
                $('.image-item').each(function() {
                    var imageName = $(this).find('.image-name').text().toLowerCase();
                    if (imageName.indexOf(searchText) > -1) {
                        $(this).show();
                        // 親フォルダを開く
                        $(this).closest('.folder-content').prev('.folder-header').addClass('active');
                    } else {
                        $(this).hide();
                    }
                });
                
                // 検索テキストが空の場合はすべて表示
                if (searchText === '') {
                    $('.file-item, .image-item').show();
                    $('.folder-header').removeClass('active');
                }
            });
        });
    </script>
</body>
</html>"""

    return html

def get_file_icon(extension):
    """ファイル拡張子に応じたFont Awesomeのアイコンクラスとカスタムクラスを返す"""
    icons = {
        '.pdf': {'icon': 'fas fa-file-pdf', 'css_class': 'file-icon-pdf'},
        '.doc': {'icon': 'fas fa-file-word', 'css_class': 'file-icon-doc'},
        '.docx': {'icon': 'fas fa-file-word', 'css_class': 'file-icon-doc'},
        '.xls': {'icon': 'fas fa-file-excel', 'css_class': 'file-icon-sheet'},
        '.xlsx': {'icon': 'fas fa-file-excel', 'css_class': 'file-icon-sheet'},
        '.ppt': {'icon': 'fas fa-file-powerpoint', 'css_class': 'file-icon-slide'},
        '.pptx': {'icon': 'fas fa-file-powerpoint', 'css_class': 'file-icon-slide'},
        '.txt': {'icon': 'fas fa-file-alt', 'css_class': ''},
        '.zip': {'icon': 'fas fa-file-archive', 'css_class': 'file-icon-archive'},
        '.rar': {'icon': 'fas fa-file-archive', 'css_class': 'file-icon-archive'},
        '.7z': {'icon': 'fas fa-file-archive', 'css_class': 'file-icon-archive'},
        '.mp3': {'icon': 'fas fa-file-audio', 'css_class': 'file-icon-audio'},
        '.wav': {'icon': 'fas fa-file-audio', 'css_class': 'file-icon-audio'},
        '.mp4': {'icon': 'fas fa-file-video', 'css_class': 'file-icon-video'},
        '.avi': {'icon': 'fas fa-file-video', 'css_class': 'file-icon-video'},
        '.mov': {'icon': 'fas fa-file-video', 'css_class': 'file-icon-video'},
        '.html': {'icon': 'fas fa-file-code', 'css_class': 'file-icon-code'},
        '.css': {'icon': 'fas fa-file-code', 'css_class': 'file-icon-code'},
        '.js': {'icon': 'fas fa-file-code', 'css_class': 'file-icon-code'},
        '.py': {'icon': 'fas fa-file-code', 'css_class': 'file-icon-code'},
        '.json': {'icon': 'fas fa-file-code', 'css_class': 'file-icon-code'},
        '.xml': {'icon': 'fas fa-file-code', 'css_class': 'file-icon-code'},
    }
    
    return icons.get(extension, {'icon': 'fas fa-file', 'css_class': ''})

def main():
    # コマンドライン引数からディレクトリパスを取得するか、現在のディレクトリを使用
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
    else:
        directory_path = os.getcwd()
    
    # 指定されたパスが存在し、ディレクトリであることを確認
    if not os.path.exists(directory_path):
        print(f"エラー: パス '{directory_path}' は存在しません。")
        sys.exit(1)
    
    if not os.path.isdir(directory_path):
        print(f"エラー: パス '{directory_path}' はディレクトリではありません。")
        sys.exit(1)
    
    # HTMLを生成
    html_content = generate_html(directory_path)
    
    # 出力ファイル名を作成（ディレクトリ名をベースに）
    output_filename = f"directory_listing_{os.path.basename(directory_path)}.html"
    
    # HTMLをファイルに書き込む
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTMLファイルが生成されました: {output_filename}")

if __name__ == "__main__":
    main()
