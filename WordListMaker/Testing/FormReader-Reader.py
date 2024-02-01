import PyPDF2

def read_pdf_structure(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Get document information
        document_info = pdf_reader.metadata
        print(f"Title: {document_info.title}")
        print(f"Author: {document_info.author}")
        print(f"Number of Pages: {len(pdf_reader.pages)}")
        #print(document_info.)

        # Iterate through pages and extract text
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            
            print(f"\nPage {page_num + 1}:\n{text}")

if __name__ == "__main__":
    pdf_path = "overlay2.pdf"
    read_pdf_structure(pdf_path)
