from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from app.core.config import configs
import tiktoken

embedder = OpenAIEmbeddings(openai_api_key=configs.openai_api_key)

tokenizer = tiktoken.get_encoding("cl100k_base")  # GPT-4, GPT-3.5용 토큰화기

# VectorDB에 데이터를 저장할때는 문단/문장 단위로 잘게 나누는 것이 좋음
# 질문과 더 잘 매칭되는 부분만 검색되어, 정확한 context 제공이 가능하기 때문.

# 1. seperators를 기준으로 텍스트를 재귀적으로 나눔 (우선 \n\n 기준으로 나누고, 너무 길면 ., 그다음 \n, 그 다음 " " 순서로 점점 더 세게 쪼갬)
#    그래도 chunk_size보다 길면 그냥 강제로 자름.
# 2. 그렇게 나눈 조각들을 붙여서 chunck_size 기준으로 chunck들을 생성함.
#    붙일때 최대 chunck_size 만큼 붙임. 붙이면서 chunck_overlap 만큼 겹치게 만들어줌
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 256, # 한 번에 나누는 텍스트 조각(chunk)의 최대 길이
    chunk_overlap = 20, # 인접한 chunk 사이에 겹치는 부분(중복되는 텍스트)의 크기
    length_function = lambda text: len(tokenizer.encode(text)),  # 토큰 수 계산
    separators=["\n\n", ".", "\n", " "],
)

def split_text(text: str) -> list[str] :
    return text_splitter.split_text(text)