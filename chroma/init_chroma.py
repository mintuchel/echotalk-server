import torch
from transformers import AutoTokenizer, AutoModel
import chromadb
from tqdm import tqdm
import numpy as np

# ChromaDB 클라이언트 생성
chroma_client = chromadb.Client()  # 영구 저장

# 기존 컬렉션 삭제 후 재생성
collection = chroma_client.get_or_create_collection(name="menu_collection")

# Hugging Face 임베딩 모델 로드
# 한국어에 특화된 SBERT 모델
model_name = "snunlp/KR-SBERT-V40K-klueNLI-augSTS"

# 자연어 텍스트를 모델이 처리할 수 있는 숫자 토큰 형태로 바꿔주는 역할
tokenizer = AutoTokenizer.from_pretrained(model_name)

# tokenize 된 입력을 받아 임베딩을 뱉어내는 Transformer 기반 모델
# 입력 문장 전체의 의미를 1개의 고정 벡터로 잘 압축해줌
model = AutoModel.from_pretrained(model_name)

# 임베딩 추출 함수 정의
def get_embedding(text):
    # 최종적으로 문장 하나를 벡터 하나로 바꿔주는 함수임
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state
        attention_mask = inputs["attention_mask"].unsqueeze(-1).expand(embeddings.size())
        masked_embeddings = embeddings * attention_mask
        summed = torch.sum(masked_embeddings, 1)
        counts = torch.clamp(attention_mask.sum(1), min=1e-9)
        mean_pooled = summed / counts
    return mean_pooled[0].cpu().numpy()

# 학습할 데이터 (예시 형식 맞추기)
documents = [
    {"question": "3월 24일(월요일)에 나오는 점심 메뉴는 무엇인가요?", 
     "answer": "흰밥/잡곡밥, 냉이된장국, 순살찜닭, 비빔만두, 맛살, 그린빈볶음, 콩나물무침, 샐러드"},
    {"question": "3월 25일(화요일)에 나오는 점심 메뉴는 무엇인가요?", 
     "answer": "흰밥/잡곡밥, 부대찌개개, 함박스테이크, 떡볶이, 무나물, 실곤약야채무침, 샐러드"},
    {"question": "3월 26일(수요일)에 나오는 점심 메뉴는 무엇인가요?", 
     "answer": "흰밥/잡곡밥, 오징어무국, 돈육파불고기, 다코야끼, 감자채볶음, 미나리나물, 샐러드"},
    {"question": "3월 27일(목요일)에 나오는 점심 메뉴는 무엇인가요?", 
     "answer": "흰밥/잡곡밥, 미소장국, 치킨까스유린기, 로제스파게티, 미역줄기볶음, 오이무침, 샐러드"},
    {"question": "3월 28일(금요일)에 나오는 점심 메뉴는 무엇인가요?", 
     "answer": "흰밥/잡곡밥, 된장찌개, 보쌈, 해물까스, 무말랭이무침, 깻잎김치, 샐러드"},
    {"question": "3월 31일(월요일)에 나오는 점심 메뉴는 무엇인가요?", 
     "answer": "흰밥/잡곡밥, 소고기무국, 목살김치찜, 고추튀김, 돈나물, 건파래무침, 샐러드"}
]

# 데이터 임베딩 및 저장
ids = []
metadatas = []
embeddings = []

for index, doc in tqdm(enumerate(documents), desc="데이터 임베딩 중"):
    query = doc["question"]
    answer = doc["answer"]
    
    embedding = get_embedding(query)
    
    ids.append(str(index))
    metadatas.append({"question": query, "answer": answer})
    embeddings.append(embedding.tolist())

# Chunk 단위로 저장
chunk_size = 2
total_chunks = len(embeddings) // chunk_size + 1

for chunk_idx in tqdm(range(total_chunks), desc="ChromaDB에 저장 중"):
    start_idx = chunk_idx * chunk_size
    end_idx = (chunk_idx + 1) * chunk_size
    
    chunk_embeddings = embeddings[start_idx:end_idx]
    chunk_ids = ids[start_idx:end_idx]
    chunk_metadatas = metadatas[start_idx:end_idx]

    if not chunk_embeddings:
        print(f"빈 데이터 발생 (chunk {chunk_idx})")
        continue
    
    collection.upsert(
        embeddings=chunk_embeddings,
        ids=chunk_ids,
        metadatas=chunk_metadatas
    )

print(f"ChromaDB 저장 완료! 총 데이터 개수: {collection.count()}")