import os
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from ckonlpy.tag import Twitter
from sqlalchemy import create_engine, text
import matplotlib.font_manager as fm
from PIL import Image
import numpy as np

# 마스크 이미지 로드 함수
def load_mask(mask_path):
    return np.array(Image.open(mask_path))

# 사용자 사전 로드 함수 (서울명소merge.txt)
def load_custom_dictionary(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='cp949') as f:
            lines = f.read().splitlines()
    words = set(line.strip() for line in lines if line.strip())
    return list(words)

# 여러 gsub 파일들을 불용어 집합으로 로드하는 함수
def load_stopwords(gsub_filepaths):
    stopwords = set()
    for filepath in gsub_filepaths:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.read().splitlines()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='cp949') as f:
                lines = f.read().splitlines()
        for line in lines:
            word = line.strip()
            if word:
                stopwords.add(word)
    return list(stopwords)

# SQLAlchemy를 이용한 MySQL 연결
def get_engine():
    host_name = 'localhost'
    user_name = 'root'
    password = 'Joshua0526!'
    db_name = 'wordcloud'
    engine = create_engine(f'mysql+pymysql://{user_name}:{password}@{host_name}/{db_name}')
    return engine

# MySQL에 사용자 사전 및 불용어 사전 테이블 생성
def create_tables(engine):
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS custom_dictionary (
                id INT AUTO_INCREMENT PRIMARY KEY,
                word VARCHAR(255) UNIQUE NOT NULL
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS stopwords (
                id INT AUTO_INCREMENT PRIMARY KEY,
                word VARCHAR(255) UNIQUE NOT NULL
            )
        """))
        conn.commit()

# MySQL 테이블에 단어 삽입 (중복 발생 시 건너뜀)
def insert_words(engine, table, words):
    with engine.connect() as conn:
        for word in words:
            try:
                conn.execute(text(f"INSERT INTO {table} (word) VALUES (:word)"), {"word": word})
            except Exception:
                pass
        conn.commit()

# Twitter 객체에 사용자 사전 추가하는 함수
def add_custom_dict_to_twitter(twitter, custom_words):
    for word in custom_words:
        twitter.add_dictionary(word, 'Noun')
    return twitter

# 간단한 텍스트 전처리 함수: 숫자 및 특수문자 제거
def preprocess_text(text):
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

# 사용자 정의 색상 함수: hsl 색상 모델을 이용하여 밝은 색상 랜덤 지정
def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    # hue: 0~360, saturation: 80%, lightness: 50%
    hue = np.random.randint(0, 360)
    return f"hsl({hue},80%,50%)"

# 단일 파일을 읽어 워드클라우드를 생성하는 함수 (체언만 추출)
def generate_wordcloud(title, file_path, twitter, stopwords, font_path, mask=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='cp949') as f:
            text = f.read()
    text = preprocess_text(text)
    tokens = twitter.nouns(text)
    filtered_tokens = [token for token in tokens if token not in stopwords and len(token) > 1]
    freq = Counter(filtered_tokens)
    print(f"[{file_path}] 상위 10개 단어:", freq.most_common(10))
    
    wc = WordCloud(font_path=font_path, background_color='white', width=800, height=600, mask=mask, max_words=200)
    wc.generate_from_frequencies(freq)
    # recolor를 적용하여 사용자 정의 색상 함수 사용
    wc = wc.recolor(color_func=custom_color_func)
    
    plt.figure(figsize=(10, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    font_prop = fm.FontProperties(fname=font_path, size=20)
    plt.title(title, fontproperties=font_prop, pad=20)
    plt.show()

# 여러 파일을 하나로 결합하여 워드클라우드를 생성하는 함수 (체언만 추출)
def generate_wordcloud_from_files(title, file_paths, twitter, stopwords, font_path, mask=None):
    full_text = ""
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                full_text += f.read() + "\n"
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='cp949') as f:
                full_text += f.read() + "\n"
    full_text = preprocess_text(full_text)
    tokens = twitter.nouns(full_text)
    filtered_tokens = [token for token in tokens if token not in stopwords and len(token) > 1]
    freq = Counter(filtered_tokens)
    print(f"[{', '.join(file_paths)}] 상위 10개 단어:", freq.most_common(10))
    
    wc = WordCloud(font_path=font_path, background_color='white', width=800, height=600, mask=mask, max_words=200)
    wc.generate_from_frequencies(freq)
    wc = wc.recolor(color_func=custom_color_func)
    
    plt.figure(figsize=(10, 8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    font_prop = fm.FontProperties(fname=font_path, size=20)
    plt.title(title, fontproperties=font_prop, pad=20)
    plt.show()

def main():
    font_path = "C:\\Windows\\Fonts\\malgun.ttf"
    
    # 사용자 사전 및 불용어 파일 경로 설정
    custom_dict_file = "./data_files/custom_dictionary/서울명소merge.txt"
    gsub_files = [
        "./data_files/stopwords/박근혜대통령gsub.txt",
        "./data_files/stopwords/서울명소gsub.txt",
        "./data_files/stopwords/성형gsub.txt",
        "./data_files/stopwords/성형부작용gsub.txt",
        "./data_files/stopwords/제주도여행코스gsub.txt"
    ]
    
    # 분석할 텍스트 파일들 (모두 ./data_files 안에 위치)
    tasks = [
        {"title": "서울시 응답소 페이지 키워드", "files": ["./data_files/서울시 응답소.txt"]},
        {"title": "여고생이 가장 고치고 싶은 성형부위", "files": ["./data_files/성형상담.txt"]},
        {"title": "성형 수술 부작용 관련 키워드", "files": ["./data_files/성형부작용.txt"]},
        {"title": "제주도 추천 여행코스", "files": ["./data_files/제주도여행지.txt"]},
        {"title": "블로거들이 추천하는 서울 명소", "files": ["./data_files/서울명소.txt"]},
        {"title": "연설문 분석", "files": ["./data_files/노무현대통령.txt"]},
        {"title": "대통령 신년 연설문", 
         "files": ["./data_files/대통령취임사_2013.txt",
                   "./data_files/대통령신년연설문_2014_01_06.txt",
                   "./data_files/대통령신년연설문_2015_01_12.txt"]}
    ]
    
    # data_files/masks 폴더에서 마스크 파일 경로 리스트 생성 (png, jpg, jpeg)
    mask_dir = "./data_files/masks"
    mask_files = sorted([os.path.join(mask_dir, f) for f in os.listdir(mask_dir) if f.lower().endswith(('.png','.jpg','.jpeg'))])
    mask_images = [load_mask(fp) for fp in mask_files]
    print("마스크 파일 목록:", mask_files)
    
    # 전체 워드클라우드 호출 횟수 카운터 (각 호출마다 mask_images에서 순서대로 적용)
    mask_idx = 0
    
    # 사용자 사전과 불용어 사전 로드
    custom_words = load_custom_dictionary(custom_dict_file)
    stopword_list = load_stopwords(gsub_files)
    
    print("사용자 사전 단어:", custom_words)
    print("불용어 단어:", stopword_list)
    
    # SQLAlchemy를 이용해 MySQL 연결 및 테이블 생성, 데이터 삽입
    engine = get_engine()
    create_tables(engine)
    insert_words(engine, "custom_dictionary", custom_words)
    insert_words(engine, "stopwords", stopword_list)
    print("사전 데이터가 MySQL에 저장되었습니다.")
    
    # Twitter 객체 생성 및 사용자 사전 추가
    twitter = Twitter()
    twitter = add_custom_dict_to_twitter(twitter, custom_words)
    print("Twitter 객체 생성 및 사용자 사전 추가 완료.")
    
    # 각 작업 수행
    for task in tasks:
        title = task['title']
        files = task['files']
        current_mask = mask_images[mask_idx % len(mask_images)]
        mask_idx += 1
        if title == "대통령 신년 연설문":
            for file_path in files:
                current_mask = mask_images[mask_idx % len(mask_images)]
                mask_idx += 1
                match = re.search(r'(\d{4})', file_path)
                if match:
                    year = match.group(1)
                else:
                    year = file_path.split('/')[-1]
                sub_title = f"{title} ({year}년)"
                print(f"처리 중: {sub_title}")
                generate_wordcloud(sub_title, file_path, twitter, stopword_list, font_path, mask=current_mask)
        else:
            print(f"처리 중: {title} - 파일: {', '.join(files)}")
            generate_wordcloud_from_files(title, files, twitter, stopword_list, font_path, mask=current_mask)

if __name__ == "__main__":
    main()
