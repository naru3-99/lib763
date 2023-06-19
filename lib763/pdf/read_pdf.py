import PyPDF2


def read_pdf(file_path: str) -> str:
    """
    @param
        file_path : str = ファイルのパス
    @return
        str = pdfファイルの中身
    @todo
        pdfファイルの中身を取得する
    """
    pdf_file = open(file_path, "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in range(len(pdf_reader.pages)):
        page_obj = pdf_reader.pages[page]
        text += page_obj.extract_text()
    pdf_file.close()
    return text
