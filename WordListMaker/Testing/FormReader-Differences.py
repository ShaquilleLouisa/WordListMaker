import fitz  # PyMuPDF

def find_differences(pdf1_path, pdf2_path):
    # Open the PDF files
    pdf1 = fitz.open(pdf1_path)
    pdf2 = fitz.open(pdf2_path)

    # Get the number of pages in each PDF
    num_pages_pdf1 = pdf1.page_count
    num_pages_pdf2 = pdf2.page_count

    # Find differences in the number of pages
    if num_pages_pdf1 != num_pages_pdf2:
        print(f"Number of pages is different: {num_pages_pdf1} vs {num_pages_pdf2}")
        return

    # Iterate through pages and find text differences
    for page_num in range(num_pages_pdf1):
        page1 = pdf1[page_num]
        page2 = pdf2[page_num]

        text1 = page1.get_text()
        text2 = page2.get_text()

        # Compare text on the current page
        if text1 != text2:
            print(f"Differences found on page {page_num + 1}:")

            # Split text into lines and compare line by line
            lines1 = text1.split('\n')
            lines2 = text2.split('\n')

            for line_num, (line1, line2) in enumerate(zip(lines1, lines2)):
                if line1 != line2:
                    print(f"  Line {line_num + 1}:")
                    print(f"    PDF 1: {line1}")
                    print(f"    PDF 2: {line2}")

    # Close the PDF files
    pdf1.close()
    pdf2.close()

if __name__ == "__main__":
    pdf1_path = "output_images/N3NoKatakanaShuffleRemoved-interactive.pdf"
    pdf2_path = "output_images/N3NoKatakanaShuffleRemoved-interactive2.pdf"

    find_differences(pdf1_path, pdf2_path)