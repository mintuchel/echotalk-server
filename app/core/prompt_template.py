def contextual_prompt(context_text: str, question: str) -> str:
    return f"""다음 정보를 참고하여 사용자의 질문에 답하세요.

### 문서 정보 ###
{context_text}

### 사용자 질문 ###
{question}

### 답변 ###
"""