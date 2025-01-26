from langchain_community.document_loaders import DirectoryLoader, TextLoader


def load_documents(PROBLEM_PATH, EDITORIAL_PATH):

    class UTF8TextLoader(TextLoader):
        def __init__(self, file_path):
            super().__init__(file_path, encoding="utf-8")

    loader1 = DirectoryLoader(PROBLEM_PATH, glob="*.txt", loader_cls = UTF8TextLoader)
    documents1 = loader1.load()
    loader2 = DirectoryLoader(EDITORIAL_PATH, glob="*.txt", loader_cls = UTF8TextLoader)
    documents2 = loader2.load()

    documents = documents2 + documents1
    return documents

