import MeCab
import pandas as pd

stop_word_list = ['게임', '로아', '유저', '사람', '생각', '내용', '업데이트', '시간', '시작', '이번', '느낌', '얘기', '금강선', '강선', '이상', '영상', '로스트', '정도', '재학', '처음', '다음', '바드', '필요', '이유', '방장', '미니', '편집', '소림', '가능', '자리', '자체', '리셋', '품질', '방송', '메이플', '부분', '카멘', '아바타']

def extract_noun(text):
    t = MeCab.Tagger()
    parsed = t.parse(text)
    nouns = []
    for line in parsed.split('\n'):
        if line == 'EOS' or line == '':
            break
        word, features = line.split('\t')
        pos = features.split(',')[0]
        if pos == 'NNG' or pos == 'NNP':
            if len(word) >= 2:
                if word not in stop_word_list:
                    nouns.append(word)
    return nouns

data_path = 'ratings_result.xlsx'

dataset = pd.read_excel(data_path).dropna(axis=0)

pos_text = list(dataset[dataset['label'] == 1]['Comment'].values)
neg_text = list(dataset[dataset['label'] == 0]['Comment'].values)



processed_texts = [extract_noun(doc) for doc in neg_text]

print(processed_texts[:3])

from gensim import corpora
from gensim.models import LdaModel

dictionary = corpora.Dictionary(processed_texts)
print('전체 명사의 수 : ', len(dictionary))
# no_above는 0.5~0.7 조정 가능
# 지나치게 일반적인 단어가 있을 경우에는 차후에 불용어
dictionary.filter_extremes(no_below=5, no_above=0.5) # no_below = 너무 적은 단어 삭제 no_above = 너무 많은 단어 삭제
print('전체 명사의 수에서 필터한 개수 : ', len(dictionary))

# with open('dict_neg_text.txt', 'w', encoding='utf-8') as f:
#     for token, id in dictionary.token2id.items():
#         f.write(f'{token}\t{id}\n')

corpus = [dictionary.doc2bow(text) for text in processed_texts]
print(corpus[:3])

num_topics = 3

lda_model = LdaModel(
    corpus=corpus,
    id2word=dictionary,
    num_topics=num_topics,
    random_state=2024
)

for idx, topic in lda_model.print_topics(num_words=5):
    print(f'토픽 #{idx+1} : {topic}')
