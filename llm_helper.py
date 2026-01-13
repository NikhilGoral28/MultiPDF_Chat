from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter


def get_pdf_text(pdf_docs):
    text = ""

    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)  # pdf is an UploadedFile object

        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text

def get_text_chunks(raw_text):

    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len

    )

    chunks = text_splitter.split_text(raw_text)

    return chunks
