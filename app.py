import os
from flask import Flask, jsonify
import PyPDF2
import random

app = Flask(__name__)

# Funzioni come definite prima...

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Prendi la porta dall'ambiente, default a 5000
    app.run(host='0.0.0.0', port=port, debug=True)

# Funzione per estrarre una pagina casuale dal PDF
def extract_random_page(pdf_file):
    try:
        # Apri il file PDF
        with open(pdf_file, 'rb') as file:
            # Leggi il PDF
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)

            if num_pages <= 2:
                return "Il PDF ha troppo poche pagine per escludere la prima e l'ultima.", None

            # Seleziona una pagina casuale escludendo la prima e l'ultima
            random_page_num = random.randint(1, num_pages - 2)

            # Estrai il contenuto della pagina casuale
            page = reader.pages[random_page_num]
            return page.extract_text(), random_page_num + 1  # Restituisce il testo e il numero della pagina
    except Exception as e:
        return str(e), None

# Funzione per formattare il testo
def format_text(text):
    # Semplice formattazione, rimuovi doppi spazi e sostituisci i ritorni a capo con paragrafi
    formatted_text = text.strip().replace('\n', '\n\n')  # Due nuove righe per ogni ritorno a capo
    return formatted_text

# Endpoint per restituire una pagina casuale dal PDF
@app.route('/random-page', methods=['GET'])
def random_page():
    pdf_file = 'bibbia.pdf'  # Percorso del file PDF
    page_text, page_num = extract_random_page(pdf_file)
    
    if page_text:
        # Applica la formattazione al testo
        formatted_text = format_text(page_text)
        return jsonify({
            "page_number": page_num,
            "content": formatted_text
        })
    else:
        return jsonify({"error": "Could not extract page"}), 500

# Avvio del server Flask
if __name__ == '__main__':
    app.run(debug=True)
