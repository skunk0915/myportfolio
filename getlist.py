import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

def get_title(url):
    """
    指定されたURLのウェブページからタイトルタグを適切に取得します。
    文字化けを防ぐため、エンコーディングを自動判別します。
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # requestsが自動でエンコーディングを判断するが、
        # もし誤っていた場合（文字化けする場合）、UTF-8として再デコードを試みる
        if 'charset' not in response.headers.get('content-type', '').lower():
            response.encoding = response.apparent_encoding
        
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tag = soup.find('title')

        if title_tag:
            return title_tag.get_text(strip=True)
        else:
            return 'タイトルが見つかりません'
    except requests.exceptions.RequestException as e:
        return f"エラー: {e}"
    except Exception as e:
        return f"予期せぬエラー: {e}"

def process_csv_and_add_titles(input_file, output_file):
    """
    CSVファイルを読み込み、各URLのタイトルを取得してB列に追記し、新しいCSVとして保存します。
    """
    if not os.path.exists(input_file):
        print(f"エラー: ファイル '{input_file}' が見つかりません。")
        return

    try:
        df = pd.read_csv(input_file, header=None, names=['URL'])
    except pd.errors.ParserError:
        print("エラー: CSVファイルの解析に失敗しました。ファイル形式を確認してください。")
        return

    print(f"'{input_file}' を読み込みました。")
    print(f"処理するURL数: {len(df)}")

    # URL列の各行に関数を適用
    df['B'] = df['URL'].apply(get_title)

    print("\n結果:")
    print(df)

    # UTF-8で新しいCSVファイルに保存
    df.to_csv(output_file, index=False, header=False, encoding='utf-8-sig')
    print(f"\n完了: 更新されたデータは '{output_file}' に保存されました。")

if __name__ == '__main__':
    # このファイル名を実際のCSVファイル名に合わせる
    input_csv = 'uranai-domain.csv'
    output_csv = 'uranai-domain-with-titles.csv'
    
    process_csv_and_add_titles(input_csv, output_csv)