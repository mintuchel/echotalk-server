from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 400,
    chunk_overlap = 20,
    length_function = len,
    separators=["\n\n", "\n", " ", ""],
)

def split_text(text: str) -> list[str] :
    return text_splitter.split_text(text)