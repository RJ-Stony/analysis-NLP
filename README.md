# 🧠 NLP Text Analysis Project

텍스트 데이터를 전처리하고, 시각화를 통해 의미를 탐색하는  
간단한 자연어처리(NLP) 기반 Python 프로젝트입니다.

---

## 📁 프로젝트 구조

```
analysis-NLP-main/
├── text_preprocessing.py     # ✅ 텍스트 정제, 불용어 제거, 형태소 분석 등
├── wordcloud_test.py         # ✅ 전처리된 텍스트로 워드클라우드 시각화
├── .gitignore
└── README.md
```

---

## 🔍 주요 기능

### 1. 텍스트 전처리 (`text_preprocessing.py`)
- 특수문자 제거, 소문자 변환 등 기본 클렌징
- 불용어(stopwords) 필터링
- 형태소 분석기(예: Okt 등) 기반 명사 추출 가능

### 2. 워드클라우드 시각화 (`wordcloud_test.py`)
- 전처리된 데이터를 바탕으로 WordCloud 생성
- 자주 등장하는 단어 시각적으로 강조

---

## 🛠 사용 기술

- Python 3.12+
- `re`, `collections`, `wordcloud`, `konlpy` 등

---

## 📌 참고 사항

- `wordcloud_test.py` 실행 전, 폰트 설정이 필요할 수 있습니다 (한글 출력 시)
- 분석할 텍스트 파일은 코드 내 `open()` 경로를 환경에 맞게 수정하세요
