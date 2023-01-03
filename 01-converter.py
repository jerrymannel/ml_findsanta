from pdf2image import convert_from_path

pages = convert_from_path('SecretSantaWordSearch.pdf', 500)

counter = 1
for page in pages:
    print("Slide - " + str(counter))
    page.save("pages/slide_new_" + str(counter) + ".jpg", "JPEG")
    counter += 1
