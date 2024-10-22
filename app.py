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

            # Estrae una pagina casuale escludendo la prima e l'ultima
            random_page_num = random.randint(1, num_pages - 2)
            page = reader.pages[random_page_num]
            return page.extract_text(), random_page_num + 1
    except Exception as e:
        return str(e), None

# Funzione per numerare automaticamente le righe di testo
def format_numbered_text(text):
    # Dividi il testo in righe, rimuovi eventuali spazi vuoti
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    formatted_lines = []
    
    # Aggiungi la numerazione a ogni riga
    for i, line in enumerate(lines, 1):  # Inizia la numerazione da 1
        formatted_lines.append(f'<p><span class="line-number">{i}</span>{line}</p>')
    
    # Unisci le righe in un unico blocco HTML
    return ''.join(formatted_lines)

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
        formatted_text = format_numbered_text(page_text)  # Usa la funzione aggiornata per numerare il testo
        # Restituisci una pagina HTML
        html_content = f"""
        <!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Pagina {page_num}</title>
            <style>
                /* CSS preesistente */
                body {{
                    text-align: center;
                    font-family: 'cursive', cursive;
                    margin: 20px;
                    line-height: 1.6;  
                    background-color: #663300;
                }}
                .book-page {{
                    border: 1px solid #ccc;
                    padding: 20px;
                    background-color: #FFE5CC;
                    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                }}
                h1 {{
                    text-align: center;
                }}
                footer {{
                    text-align: right;
                    font-size: 0.9em;
                    margin-top: 20px;
                }}
                
                /* Nuovo CSS per la numerazione delle righe */
                p {{
                    text-align: justify;
                    margin-bottom: 20px;
                }}
                .line-number {{
                    font-size: 0.9em;
                    color: #555;
                    display: inline-block;
                    width: 30px;
                    text-align: right;
                    margin-right: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="book-page">
                <h1>Pagina {page_num}</h1>
                {formatted_text}  <!-- Testo numerato -->
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
