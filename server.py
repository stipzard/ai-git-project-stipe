import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS # Potrebno za komunikaciju između različitih "portova"
from google import genai
from dotenv import load_dotenv

# --- UČITAVANJE API KLJUČA ---
# Učitava varijable okruženja iz vase datoteke s ključem
load_dotenv(dotenv_path='stpaai.env') 
API_KEY = os.getenv("GEMINI_API_KEY")

# --- FLASK INICIJALIZACIJA ---
app = Flask(__name__)
CORS(app) # Omogućava da web stranica šalje zahtjeve serveru

# Inicijalizacija Gemini klijenta (Ako je ključ pronađen)
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print(f"Greška kod inicijalizacije Gemini klijenta: {e}")
        client = None
else:
    client = None
    print("UPOZORENJE: GEMINI_API_KEY nije pronađen. AI funkcije neće raditi.")


# Ruta za prikaz vaše HTML stranice
@app.route('/')
def index():
    # Mora točno vratiti ime datoteke: 'index.html'
    return render_template('index.html')


# Ruta za obradu AI zahtjeva (Ovo će zvati JavaScript)
@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    if not client:
        return jsonify({"recommendation": "GREŠKA: AI ključ nije postavljen na serveru."}), 500

    # 1. Čitanje budžeta iz dolaznog POST zahtjeva
    data = request.json
    budzet = data.get('budzet')
    
    if not budzet or not budzet.isdigit():
        return jsonify({"recommendation": "Molimo unesite valjan budžet."}), 400

    # 2. Kreiranje upita za AI
    prompt = f"Daj detaljnu, optimiziranu preporuku za kupnju najboljeg desktop ili laptop računala za budžet od {budzet} Eura. Preporuka neka bude u obliku popisa sa specifikacijama (CPU, GPU, RAM, Pohrana) i kratkim objašnjenjem. Formatiraj tekst lijepo za prikaz na web stranici."

    try:
        # 3. Poziv Gemini API-ja
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        # 4. Vraćanje AI odgovora natrag web stranici
        return jsonify({"recommendation": response.text})

    except Exception as e:
        print(f"Greška kod Gemini API poziva: {e}")
        return jsonify({"recommendation": f"Došlo je do greške prilikom kontaktiranja AI servisa: {e}"}), 500


if __name__ == '__main__':
    # Flask će se pokrenuti na adresi http://127.0.0.1:5000/
    # Debug=True omogucava automatsko ponovno učitavanje koda
    app.run(debug=True)