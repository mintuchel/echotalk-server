import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# ChromaDB 클라이언트 생성
chroma_client = chromadb.Client()  # 영구 저장

# 기존 컬렉션 삭제 후 재생성
collection = chroma_client.get_or_create_collection(name="menu_collection")

# Sentence Transformer 임베딩 모델 로드
# 한국어 지원 제대로 안해줌
# 토큰 필요한 api 모델 사용해보기
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-V2")

# 학습할 데이터
documents = [
    "3월 24일(월요일)에 나오는 점심 메뉴는 흰밥/잡곡밥, 냉이된장국, 순살찜닭, 비빔만두, 맛살, 그린빈볶음, 콩나물무침, 샐러드",
    "3월 25일(화요일)에 나오는 점심 메뉴는 흰밥/잡곡밥, 부대찌개개, 함박스테이크, 떡볶이, 무나물, 실곤약야채무침, 샐러드",
    "3월 26일(수요일)에 나오는 점심 메뉴는 흰밥/잡곡밥, 오징어무국, 돈육파불고기, 다코야끼, 감자채볶음, 미나리나물, 샐러드",
    "3월 27일(목요일)에 나오는 점심 메뉴는 흰밥/잡곡밥, 미소장국, 치킨까스유린기, 로제스파게티, 미역줄기볶음, 오이무침, 샐러드",
    "3월 28일(금요일)에 나오는 점심 메뉴는 흰밥/잡곡밥, 된장찌개, 보쌈, 해물까스, 무말랭이무침, 깻잎김치, 샐러드",
    "3월 31일(월요일)에 나오는 점심 메뉴는 흰밥/잡곡밥, 소고기무국, 목살김치찜, 고추튀김, 돈나물, 건파래무침, 샐러드"
]

# faiss 사용중

# vllm = llm model 서빙 툴
# VRAM 크기가 LLM 모델 돌릴때 중요함
# gpu 사양에 따라 vram이 달라짐
# 큰거를 양자화해서 작게 만들어서 올림


# ChromaDB에 추가할 데이터
ids = []
metadatas = []
embeddings = []

for index, doc in tqdm(enumerate(documents), desc="데이터 임베딩 중"):
    query = doc["question"]
    answer = doc["answer"]
    
    # 질문을 임베딩
    # 인코딩 X
    embedding = embedding_model.encode(query, normalize_embeddings=True)
    
    ids.append(str(index))
    metadatas.append({"question": query, "answer": answer})
    embeddings.append(embedding.tolist())

# 데이터를 Chunk 단위로 저장
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