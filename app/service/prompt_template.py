def contextual_prompt(docs: str, question: str) -> str:
    contexts = "\n\n".join(docs[:3])

    return f"""다음 정보를 참고하여 사용자의 질문에 답하세요.

            ### 문서 정보 ###
            {contexts}

            ### 사용자 질문 ###
            {question}

            ### 답변 ###
            """