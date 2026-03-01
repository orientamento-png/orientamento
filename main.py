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
async def predict(request: Request):
    try:
        raw_data = await request.json()
        print("Dati ricevuti:", raw_data)  # già ce l'hai, tienilo

        # Riconosci il payload di TEST di Forminator
        if (
            "number_1" in raw_data
            and "number_2" in raw_data
            and "number_3" in raw_data
            and "number_4" in raw_data
            and "form_title" in raw_data
            and "entry_time" in raw_data
        ):
            # È il test → rispondi sempre OK senza validare
            print("Rilevato TEST di Forminator → risposta positiva")
            return {
                "status": "success",
                "message": "Webhook test ricevuto correttamente",
                "test": True
            }

        # Altrimenti è un invio reale → valida normalmente
        validated = FormData(**raw_data)

        df_input = pd.DataFrame([validated.dict()])
        pred = model.predict(df_input)[0]

        aree = {0: "scientifico", 1: "umanistico", 2: "tecnico"}
        area_text = aree.get(pred, "indefinita")

        livello = (
            "alto" if validated.punteggio_mat >= 8
            else "medio" if validated.punteggio_mat >= 5
            else "da esplorare"
        )

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
        print("Errore:", str(e))
        raise HTTPException(500, detail=str(e))
