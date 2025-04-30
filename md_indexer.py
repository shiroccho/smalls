#!/usr/bin/env python3
"""
Markdown Index Generator
------------------------
このスクリプトは指定されたフォルダ内のすべてのMarkdownファイル(.md)を探し、
それらへのリンクを含む新しいインデックスMarkdownファイルを生成します。
"""

import os
import argparse
from datetime import datetime

def generate_md_index(directory='.', output_file='index.md', title='Markdown ファイル一覧', 
                     include_creation_date=True, include_description=True):
    """
    指定されたディレクトリ内のMarkdownファイルを見つけ、インデックスを生成します
    
    Args:
        directory (str): Markdownファイルを検索するディレクトリ
        output_file (str): 出力するインデックスファイルの名前
        title (str): インデックスファイルのタイトル
        include_creation_date (bool): ファイルの作成日時を含めるかどうか
        include_description (bool): ファイルの最初の行を説明として含めるかどうか
    """
    # 出力ファイル自身は除外するために、完全なパスを取得
    output_fullpath = os.path.abspath(os.path.join(directory, output_file))
    
    # ディレクトリ内のすべてのmdファイルを取得
    md_files = []
    for file in os.listdir(directory):
        if file.endswith('.md'):
            full_path = os.path.abspath(os.path.join(directory, file))
            # 出力ファイル自身は除外
            if full_path != output_fullpath:
                md_files.append(file)
    
    # 名前でソート
    md_files.sort()
    
    # インデックスファイルの内容を作成
    content = [f"# {title}\n"]
    content.append(f"*生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    content.append(f"*このファイルは自動生成されました*\n\n")
    
    if not md_files:
        content.append("*このディレクトリにMarkdownファイルはありません。*")
    else:
        for md_file in md_files:
            file_path = os.path.join(directory, md_file)
            
            # ファイル情報を取得
            file_info = []
            
            if include_creation_date:
                try:
                    creation_time = os.path.getctime(file_path)
                    creation_date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')
                    file_info.append(f"作成日: {creation_date}")
                except:
                    pass
            
            # ファイルの最初の行から説明を取得
            description = ""
            if include_description:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        if first_line.startswith('# '):
                            description = first_line[2:].strip()
                except:
                    pass
            
            # ファイル名とリンクを追加
            link_text = md_file
            content.append(f"## [{link_text}]({md_file})")
            
            if description:
                content.append(f"*{description}*")
            
            if file_info:
                content.append("- " + ", ".join(file_info))
            
            content.append("")  # 空行を追加
    
    # インデックスファイルを書き込み
    with open(os.path.join(directory, output_file), 'w', encoding='utf-8') as f:
        f.write("\n".join(content))
    
    print(f"インデックスファイル '{output_file}' を生成しました。")

def main():
    parser = argparse.ArgumentParser(description='Markdownファイルのインデックスを生成します。')
    parser.add_argument('-d', '--directory', default='.', help='Markdownファイルを検索するディレクトリ（デフォルト: カレントディレクトリ）')
    parser.add_argument('-o', '--output', default='index.md', help='出力するインデックスファイルの名前（デフォルト: index.md）')
    parser.add_argument('-t', '--title', default='Markdown ファイル一覧', help='インデックスファイルのタイトル')
    parser.add_argument('--no-date', action='store_false', dest='include_date', help='ファイルの作成日時を含めない')
    parser.add_argument('--no-description', action='store_false', dest='include_description', help='ファイルの説明を含めない')
    
    args = parser.parse_args()
    
    generate_md_index(
        directory=args.directory,
        output_file=args.output,
        title=args.title,
        include_creation_date=args.include_date,
        include_description=args.include_description
    )

if __name__ == "__main__":
    main()
