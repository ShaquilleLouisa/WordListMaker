from reportlab.pdfgen import canvas
from reportlab.lib.colors import *
from PyPDF2 import PdfWriter, PdfReader

# Existing PDF and output PDF paths
existing_pdf_path = "output.pdf"
output_pdf_path = "N3NoKatakanaShuffleRemoved-interactive.pdf"


# Function to create an interactive checkbox
def create_checkbox(c, x, y, size, field_name):
    c.acroForm.checkbox(
        name=field_name,
        tooltip=field_name,
        x=x,
        y=y,
        checked=False,
        borderWidth=0,
        fillColor=transparent,
        textColor=transparent,
        buttonStyle="circle",
        size=size,
    )
    c.setFillColorRGB(1, 0, 0)


existing_pdf = PdfReader(open(existing_pdf_path, "rb"))
# Create an overlay PDF with interactive checkboxes
overlay_pdf_path = "overlay.pdf"
x = 37
y = 17.25
y_interval = 35.75
size = 35
c = canvas.Canvas(overlay_pdf_path)
for p in range(len(existing_pdf.pages)):
    for i in range(20):
        create_checkbox(
            c, x, y + i * y_interval, size, "checkbox" + str(i) + " - " + str(p)
        )
    c.showPage()
c.save()

# Merge the overlay with the existing PDF
output = PdfWriter()
overlay_pdf = PdfReader(overlay_pdf_path)
for i in range(len(existing_pdf.pages)):
    page = existing_pdf.pages[i]
    page.merge_page(overlay_pdf.pages[i])
    output.add_page(page)

# Save the final interactive PDF
with open(output_pdf_path, "wb") as out_pdf:
    output.write(out_pdf)

print("Interactive PDF saved to:", output_pdf_path)
