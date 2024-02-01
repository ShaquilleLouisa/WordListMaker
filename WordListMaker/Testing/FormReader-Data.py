# "overlay2.pdf"
import PyPDF2

def extract_pdf_form_data(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_fields = pdf_reader.get_fields()

        form_data = {}
        for field_name in pdf_fields:
            field_value = pdf_fields[field_name].get('/V')
            form_data[field_name] = field_value

        return form_data

if __name__ == "__main__":
    pdf_path = "N3NoKatakanaShuffleRemoved-interactive.pdf"
    data = extract_pdf_form_data(pdf_path)

    for field_name, field_value in data.items():
        print(f"{field_name}: {field_value}")