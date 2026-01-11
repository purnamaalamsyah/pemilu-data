from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_text(docs):
    """
    Splits documents into smaller chunks for vector storage.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    return splits
