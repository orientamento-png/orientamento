from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Orientamento Gruppo5")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("modello_rafinato.pkl")

# Modello per i dati reali del form
class FormData(BaseModel):
    eta: int
    punteggio_mat: int
    preferenza: int
    paura: int

@app.get("/")
def root():
    return {"status": "API attiva", "model": "rafinato"}

@app.post("/predict")
async def predict(request: Request):  # ← Usa Request invece di FormData fisso
    try:
        data = await request.json()  # prendi il JSON raw
        print("Dati ricevuti:", data)  # logga sempre (utile su Render)

        # Se è il test di Forminator → restituisci subito OK senza validare
        if not data or len(data) < 3:  # payload vuoto o molto piccolo → è il test
            return {"status": "test_ok", "message": "Webhook test ricevuto correttamente"}

        # Altrimenti prova a validare come FormData reale
        try:
            validated = FormData(**data)
        except Exception as e:
            raise HTTPException(422, f"Dati non validi: {str(e)}")

        df_input = pd.DataFrame([validated.dict()])
        pred = model.predict(df_input)[0]

        aree = {0: "scientifico", 1: "umanistico", 2: "tecnico"}
        area_text = aree.get(pred, "indefinita")

        livello = "alto" if validated.punteggio_mat >= 8 else "medio" if validated.punteggio_mat >= 5 else "da esplorare"

        consiglio = f"Ti consigliamo **{area_text.upper()}**! "
        if validated.paura == 1:
            consiglio += "Parla con un prof per chiarirti le idee."
        else:
            consiglio += "Hai già un buon orientamento!"

        return {
            "area": area_text,
            "livello_orientamento": livello,
            "consiglio": consiglio
        }

    except Exception as e:
        print("Errore:", str(e))  # logga l'errore
        raise HTTPException(500, str(e))
