
pdf_path = "JLPT-N2Used.pdf"
counter = 0

with open(pdf_path, 'rb') as file:
    for word in file:
        if '/Type/Annot/V/Yes' in str(word):
            counter +=1
print(counter)