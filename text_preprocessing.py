import urllib.request
from soynlp import DoublespaceLineCorpus
from soynlp.word import WordExtractor

# 데이터 다운로드
urllib.request.urlretrieve(
    "https://raw.githubusercontent.com/lovit/soynlp/master/tutorials/2016-10-20.txt", 
    filename="2016-10-20.txt"
)

# 문서를 코퍼스로 변환
corpus = DoublespaceLineCorpus("2016-10-20.txt")

# 전체 문서 수 확인
print(len(corpus))  # 30,091개의 문서

i = 0
for document in corpus:
    if len(document) > 0:
        print(document)
        i += 1
        if i == 3:
            break

word_extractor = WordExtractor()
word_extractor.train(corpus)  # 학습 진행
word_score_table = word_extractor.extract()  # 단어 점수표 생성

word_score_table

word_score_table["디"].right_branching_entropy
word_score_table["디스"].right_branching_entropy
word_score_table["디스플"].right_branching_entropy
word_score_table["디스플레"].right_branching_entropy
word_score_table["디스플레이"].right_branching_entropy

from soynlp.normalizer import emoticon_normalize

print(emoticon_normalize('앜ㅋㅋㅋㅋ이영화존잼쓰ㅠㅠㅠㅠㅠ', num_repeats=2))
print(emoticon_normalize('앜ㅋㅋㅋㅋㅋㅋㅋㅋㅋ이영화존잼쓰ㅠㅠㅠㅠ', num_repeats=2))

from soynlp.normalizer import repeat_normalize

print(repeat_normalize('하하하하하하핫', num_repeats=2))
print(repeat_normalize('하하하하핫', num_repeats=2))
