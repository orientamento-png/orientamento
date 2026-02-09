from fastapi import FastAPI, HTTPException
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

class FormData(BaseModel):
    eta: int
    punteggio_mat: int
    preferenza: int
    paura: int

@app.get("/")
def root():
    return {"status": "API attiva", "model": "rafinato"}

@app.post("/predict")
def predict(data: FormData):
    try:
        df_input = pd.DataFrame([data.dict()])
        pred = model.predict(df_input)[0]
        
        aree = {0: "scientifico", 1: "umanistico", 2: "tecnico"}
        area_text = aree.get(pred, "indefinita")
        
        livello = "alto" if data.punteggio_mat >= 8 else "medio" if data.punteggio_mat >= 5 else "da esplorare"
        
        consiglio = f"Ti consigliamo **{area_text.upper()}**! "
        if data.paura == 1:
            consiglio += "Parla con un prof per chiarirti le idee."
        else:
            consiglio += "Hai già un buon orientamento!"

        return {
            "area": area_text,
            "livello_orientamento": livello,
            "consiglio": consiglio
        }
    except Exception as e:
        raise HTTPException(500, str(e))
