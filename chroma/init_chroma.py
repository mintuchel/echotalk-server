from sentence_transformers import SentenceTransformer
import chromadb

# ChromaDB 클라이언트 생성 (로컬 DB 사용)
chroma_client = chromadb.Client()

# 컬렉션 생성 (존재하지 않으면 새로 생성)
collection = chroma_client.get_or_create_collection(name="menu_collection")

# Sentence Transformer 모델 로드
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-V2")

# 문서들을 임베딩한 후 upsert
documents = [
    "3월 24일(월요일)에 나오는 점심 메뉴는 흰밥/잡곡밥, 냉이된장국, 순살찜닭, 비빔만두, 맛살, 그린빈볶음, 콩나물무침, 샐러드",
    "3월 25일(화요일)에 나오는 점심 메뉴는 흰밥/잡곡밥, 부대찌개개, 함박스테이크, 떡볶이, 무나물, 실곤약야채무침, 샐러드",
    "3월 26일(수요일)에 나오는 점심 메뉴는 흰밥/잡곡밥, 오징어무국, 돈육파불고기, 다코야끼, 감자채볶음, 미나리나물, 샐러드",
    "3월 27일(목요일)에 나오는 점심 메뉴는 흰밥/잡곡밥, 미소장국, 치킨까스유린기, 로제스파게티, 미역줄기볶음, 오이무침, 샐러드",
    "3월 28일(금요일)에 나오는 점심 메뉴는 흰밥/잡곡밥, 된장찌개, 보쌈, 해물까스, 무말랭이무침, 깻잎김치, 샐러드",
    "3월 31일(월요일)에 나오는 점심 메뉴는 흰밥/잡곡밥, 소고기무국, 목살김치찜, 고추튀김, 돈나물, 건파래무침, 샐러드"
]

# 문서 임베딩 생성
embeddings = embedding_model.encode(documents)

# 임베딩과 문서 함께 upsert
collection.upsert(
    documents=documents,
    embeddings=embeddings,
    ids=["1", "2", "3", "4", "5", "6"]
)

print("현재 저장된 데이터 개수:", collection.count())