import os
from flask import Flask, jsonify, render_template_string
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
    formatted_text = text.strip().replace('\n', '<br>')  # Usa <br> per andare a capo in HTML
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
        # Restituisci una pagina HTML
        html_content = f"""
        <!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Pagina {page_num}</title>
            <style>
                body {
                    text-align: center;
                    font-family: 'cursive', cursive;
                    margin: 20px;
                    line-height: 1.6;  
                    background-color: #663300;
                }
                .book-page {
                    border: 1px solid #ccc;
                    padding: 20px;
                    background-color: #FFE5CC;
                    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    text-align: center;
                }
                footer {
                    text-align: right;
                    font-size: 0.9em;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <div class="book-page">
                <h1>Pagina {page_num}</h1>
                <p>{formatted_text}</p>
                <footer>© Bibbia CEI 2008</footer>
            </div>
        </body>
        </html>
        """
        return render_template_string(html_content)
    else:
        return jsonify({"error": "Could not extract page"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
