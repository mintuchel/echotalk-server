import requests
import json

# Hugging Face API Key
API_TOKEN = "NTNv7j0TuYARvmNMmWXo6fKvM4o6nv/aUi9ryX38ZH+L1bkrnD1ObOQ8JAUmHCBq7Iy7otZcyAagBLHVKvvYaIpmMuxmARQ97jUVG16Jkpkp1wXOPsrF9zwew6TpczyHkHgX5EuLg2MeBuiT/qJACs1J0apruOOJCg/gOtkjB4c="  # ← 여기에 본인 토큰 입력

# 사용할 모델
model_id = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# Hugginf Face API 사용
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# 문장 → 벡터
def get_embedding(text):
    payload = {"inputs": text}
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        raise Exception(f"API 호출 실패: {response.status_code}, {response.text}")

    embedding = response.json()

    # 결과가 [[...]] 형식으로 들어오기 때문에 벡터만 추출
    return embedding[0]
