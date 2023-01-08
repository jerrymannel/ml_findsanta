from pdf2image import convert_from_path

pages = convert_from_path('SecretSantaWordSearch.pdf', 500)
print(len(pages))

slidesToSkip = [2, 23, 34]

for pageNumber, page in enumerate(pages):
    pageNumber = pageNumber + 1
    pageName = "pages/SLIDE-{:02d}.jpg".format(pageNumber)
    if (slidesToSkip.count(pageNumber) > 0):
        pageName = "pages/TEST-{:02d}.jpg".format(pageNumber)
    page.save(pageName, "JPEG")
    print("Exported slide {:02d} to {}".format(pageNumber, pageName))
