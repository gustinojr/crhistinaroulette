import os
from flask import Flask, jsonify
import PyPDF2
import random

app = Flask(__name__)

# Funzione per estrarre una pagina casuale dal PDF
def extract_random_page(pdf_file):
    try:
        with open(pdf_file, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)

            if num_pages <= 2:
                return "Il PDF ha troppo poche pagine per escludere la prima e l'ultima.", None

            random_page_num = random.randint(1, num_pages - 2)
            page = reader.pages[random_page_num]
            return page.extract_text(), random_page_num + 1
    except Exception as e:
        return str(e), None

# Funzione per formattare il testo
def format_text(text):
    formatted_text = text.strip().replace('\n', '\n\n')
    return formatted_text

# Endpoint per la route radice
@app.route('/')
def home():
    return jsonify({"message": "API is running. Use /random-page to get a random page."})

# Endpoint per restituire una pagina casuale dal PDF
@app.route('/random-page', methods=['GET'])
def random_page():
    pdf_file = 'bibbia.pdf'
    page_text, page_num = extract_random_page(pdf_file)

    if page_text:
        formatted_text = format_text(page_text)
        return jsonify({
            "page_number": page_num,
            "content": formatted_text
        })
    else:
        return jsonify({"error": "Could not extract page"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
