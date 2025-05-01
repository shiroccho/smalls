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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
        :root {
            --primary-color: #4a6da7;
            --accent-color: #f0f4f8;
            --text-color: #333;
            --hover-color: #5d82c1;
            --border-radius: 8px;
            --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            --transition: all 0.3s ease;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: #f8f9fa;
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px;
        }

        h1 {
            color: var(--primary-color);
            margin-bottom: 25px;
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 10px;
            font-size: 2.2rem;
        }

        h2 {
            color: var(--primary-color);
            margin: 25px 0 15px;
            font-size: 1.6rem;
        }

        .container {
            background-color: white;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 20px;
            margin-bottom: 30px;
        }

        .accordion {
            background-color: var(--accent-color);
            color: var(--primary-color);
            cursor: pointer;
            padding: 15px 20px;
            width: 100%;
            text-align: left;
            border: none;
            outline: none;
            transition: var(--transition);
            margin-bottom: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: var(--border-radius);
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .accordion:after {
            content: '\\f107';
            font-family: 'Font Awesome 5 Free';
            font-weight: 900;
            float: right;
            transition: var(--transition);
        }

        .active:after {
            content: '\\f106';
        }

        .active, .accordion:hover {
            background-color: var(--hover-color);
            color: white;
        }

        .panel {
            padding: 0;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s ease-out;
            background-color: white;
            border-radius: 0 0 var(--border-radius) var(--border-radius);
            margin-bottom: 10px;
        }

        .panel-content {
            padding: 20px;
        }

        .file-item {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
            display: flex;
            align-items: center;
            transition: var(--transition);
        }

        .file-item:hover {
            background-color: var(--accent-color);
        }

        .file-item:last-child {
            border-bottom: none;
        }

        .file-icon {
            margin-right: 15px;
            color: var(--primary-color);
            font-size: 1.2rem;
        }

        .file-name {
            flex-grow: 1;
        }

        a {
            color: var(--primary-color);
            text-decoration: none;
            transition: var(--transition);
        }

        a:hover {
            color: var(--hover-color);
            text-decoration: underline;
        }

        .image-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            padding: 15px 0;
        }

        .image-item {
            position: relative;
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: var(--box-shadow);
            transition: var(--transition);
            height: 200px;
        }

        .image-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
        }

        .image-container {
            width: 100%;
            height: 100%;
            overflow: hidden;
            position: relative;
        }

        .thumbnail {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }

        .image-item:hover .thumbnail {
            transform: scale(1.05);
        }

        .image-name {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 8px;
            font-size: 0.85rem;
            text-align: center;
            word-break: break-all;
            opacity: 0;
            transform: translateY(100%);
            transition: var(--transition);
        }

        .image-item:hover .image-name {
            opacity: 1;
            transform: translateY(0);
        }

        @media (max-width: 768px) {
            body {
                padding: 15px;
            }
            
            .image-gallery {
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            }
            
            .image-item {
                height: 150px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ディレクトリ一覧: """ + os.path.basename(directory_path) + """</h1>
"""

    # ディレクトリ内のすべてのファイルとフォルダを取得
    items = sorted(os.listdir(directory_path))
    
    # 最初にフォルダを処理
    folders = [item for item in items if os.path.isdir(os.path.join(directory_path, item))]
    
    # フォルダごとにアコーディオンを作成
    for folder in folders:
        folder_path = os.path.join(directory_path, folder)
        
        html += f'        <button class="accordion">{folder}</button>\n'
        html += '        <div class="panel">\n'
        html += '            <div class="panel-content">\n'
        
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
                
                html += f'                    <div class="image-item">\n'
                html += f'                        <a href="{image_path}" target="_blank">\n'
                html += f'                            <div class="image-container">\n'
                html += f'                                <img src="{image_path}" class="thumbnail" alt="{image}" />\n'
                html += f'                                <div class="image-name">{image}</div>\n'
                html += f'                            </div>\n'
                html += f'                        </a>\n'
                html += f'                    </div>\n'
            
            html += '                </div>\n'
        
        # その他のファイルを表示
        for file in other_files:
            file_path = os.path.join(folder, file).replace('\\', '/')
            file_ext = os.path.splitext(file.lower())[1]
            
            # ファイル拡張子に応じたアイコンを設定
            icon_class = get_file_icon(file_ext)
            
            html += f'                <div class="file-item">\n'
            html += f'                    <div class="file-icon"><i class="{icon_class}"></i></div>\n'
            html += f'                    <div class="file-name"><a href="{file_path}" target="_blank">{file}</a></div>\n'
            html += f'                </div>\n'
        
        html += '            </div>\n'
        html += '        </div>\n\n'
    
    # ルートディレクトリのファイルを処理
    root_files = [item for item in items if os.path.isfile(os.path.join(directory_path, item))]
    
    if root_files:
        html += '        <h2>ファイル</h2>\n'
        
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
                html += f'            <div class="image-item">\n'
                html += f'                <a href="{image}" target="_blank">\n'
                html += f'                    <div class="image-container">\n'
                html += f'                        <img src="{image}" class="thumbnail" alt="{image}" />\n'
                html += f'                        <div class="image-name">{image}</div>\n'
                html += f'                    </div>\n'
                html += f'                </a>\n'
                html += f'            </div>\n'
            
            html += '        </div>\n'
        
        # その他のファイルを表示
        for file in other_files:
            file_ext = os.path.splitext(file.lower())[1]
            
            # ファイル拡張子に応じたアイコンを設定
            icon_class = get_file_icon(file_ext)
            
            html += f'        <div class="file-item">\n'
            html += f'            <div class="file-icon"><i class="{icon_class}"></i></div>\n'
            html += f'            <div class="file-name"><a href="{file}" target="_blank">{file}</a></div>\n'
            html += f'        </div>\n'

    html += '    </div>\n'  # container終了

    # HTMLの終了部分とJavaScript
    html += """
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            var acc = document.getElementsByClassName("accordion");
            for (var i = 0; i < acc.length; i++) {
                acc[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    var panel = this.nextElementSibling;
                    
                    if (panel.style.maxHeight) {
                        panel.style.maxHeight = null;
                    } else {
                        panel.style.maxHeight = panel.scrollHeight + "px";
                    }
                });
            }
        });
    </script>
</body>
</html>"""

    return html

def get_file_icon(extension):
    """ファイル拡張子に応じたFont Awesomeのアイコンクラスを返す"""
    icons = {
        '.pdf': 'fas fa-file-pdf',
        '.doc': 'fas fa-file-word',
        '.docx': 'fas fa-file-word',
        '.xls': 'fas fa-file-excel',
        '.xlsx': 'fas fa-file-excel',
        '.ppt': 'fas fa-file-powerpoint',
        '.pptx': 'fas fa-file-powerpoint',
        '.txt': 'fas fa-file-alt',
        '.zip': 'fas fa-file-archive',
        '.rar': 'fas fa-file-archive',
        '.7z': 'fas fa-file-archive',
        '.mp3': 'fas fa-file-audio',
        '.wav': 'fas fa-file-audio',
        '.mp4': 'fas fa-file-video',
        '.avi': 'fas fa-file-video',
        '.mov': 'fas fa-file-video',
        '.html': 'fas fa-file-code',
        '.css': 'fas fa-file-code',
        '.js': 'fas fa-file-code',
        '.py': 'fas fa-file-code',
        '.json': 'fas fa-file-code',
        '.xml': 'fas fa-file-code',
    }
    
    return icons.get(extension, 'fas fa-file')

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
