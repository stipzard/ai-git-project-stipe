import os
from google import genai
from dotenv import load_dotenv

# --- VAŽNO: SPECIFICIRAMO TOČNO IME VAŠE DATOTEKE S KLJUČEM ---
# load_dotenv() obično traži samo .env, ali mi koristimo vaše ime
load_dotenv(dotenv_path='stipeai.env') 

# Čitamo ključ iz okruženja (morate biti sigurni da se ključ ispravno zove)
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("GREŠKA: Ključ nije pronađen ili varijabla nije dobro nazvana (GEMINI_API_KEY).")
else:
    try:
        # Inicijalizacija Gemini klijenta
        client = genai.Client(api_key=API_KEY)
        
        # Ovdje definirate što želite da AI napravi
        prompt = "Napiši mi 3 kratke, duhovite Git komande koje početnici stalno trebaju."
        
        print(f"Šaljem upit AI-u...")
        
        # Poziv AI modela
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt,
        )
        
        # Ispisivanje odgovora
        print("\n--- ODGOVOR OD GOOGLE AI-a ---")
        print(response.text)
        print("------------------------------\n")

    except Exception as e:
        print(f"Došlo je do greške prilikom pozivanja API-ja. Možda ključ nije valjan ili nema interneta: {e}")