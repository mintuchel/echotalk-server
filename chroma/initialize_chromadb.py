import chromadb
from sentence_transformers import SentenceTransformer

# ChromaDB 클라이언트 생성 (로컬 DB 사용)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# 기존 컬렉션 삭제
chroma_client.delete_collection(name="menu_collection")

# 컬렉션 생성 (존재하지 않으면 새로 생성)
collection = chroma_client.create_collection(name="menu_collection")

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-V2")

if collection.count() == 0 :
    # 데이터 삽입 (예제)
    documents = [
        {"question": "3월 24일(월요일)에 나오는 점심 메뉴는 뭐야?", "answer": "흰밥/잡곡밥, 냉이된장국, 순살찜닭, 비빔만두, 맛살, 그린빈볶음, 콩나물무침, 샐러드"},
        {"question": "3월 25일(화요일)에 나오는 점심 메뉴는 뭐야?", "answer": "흰밥/잡곡밥, 부대찌개개, 함박스테이크, 떡볶이, 무나물, 실곤약야채무침, 샐러드"},
        {"question": "3월 26일(수요일)에 나오는 점심 메뉴는 뭐야?", "answer": "흰밥/잡곡밥, 오징어무국, 돈육파불고기, 다코야끼, 감자채볶음, 미나리나물, 샐러드"},
        {"question": "3월 27일(목요일)에 나오는 점심 메뉴는 뭐야?", "answer": "흰밥/잡곡밥, 미소장국, 치킨까스유린기, 로제스파게티, 미역줄기볶음, 오이무침, 샐러드"},
        {"question": "3월 28일(금요일)에 나오는 점심 메뉴는 뭐야?", "answer": "흰밥/잡곡밥, 된장찌개, 보쌈, 해물까스, 무말랭이무침, 깻잎김치, 샐러드"},
        {"question": "3월 31일(월요일)에 나오는 점심 메뉴는 뭐야?", "answer": "흰밥/잡곡밥, 소고기무국, 목살김치찜, 고추튀김, 돈나물, 건파래무침, 샐러드"},
    ]

    # ChromaDB에 데이터 추가
    for i, doc in enumerate(documents):
        # 임베딩 변환
        question_embedding = embedding_model.encode(doc["question"]).tolist()

        collection.add(
            ids=[str(i)],  # 각 문서의 고유 ID
            documents=[doc["question"]],
            metadatas=[{"answer": doc["answer"]}],
            embeddings=[question_embedding]
        )
    
    print("현재 저장된 데이터 개수:", collection.count())

    all_docs = collection.get()  # 모든 데이터 가져오기
    print(all_docs)

    print("ChromaDB 학습 완료")
else:
    print("ChromaDB 이미 학습 완료됨")