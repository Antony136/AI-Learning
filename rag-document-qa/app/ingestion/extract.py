from pypdf import PdfReader

from chunker import chunk_text


pdf_path = "documents/genai-notes.pdf"


reader = PdfReader(pdf_path)

full_text = ""

for page in reader.pages:

    text = page.extract_text()

    if text:
        full_text += text + "\n"


chunks = chunk_text(
    full_text,
    chunk_size=1000,
    overlap=200
)


print("Total characters:", len(full_text))
print("Number of chunks:", len(chunks))


for index, chunk in enumerate(chunks, start=1):

    print("\n" + "=" * 60)
    print(f"CHUNK {index}")
    print("=" * 60)

    print(chunk)