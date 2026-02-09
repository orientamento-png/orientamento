# 🎓 UniChoice: Smart Career Orientation Platform

**UniChoice** è una soluzione tecnologica avanzata progettata per guidare gli studenti nel delicato passaggio verso l'istruzione post-scolastica. Attraverso l'uso del **Machine Learning**, la piattaforma analizza attitudini, competenze e stati emotivi per offrire un orientamento personalizzato, consapevole e basato sui dati.

---

## 🏗️ Architettura del Sistema

L'ecosistema UniChoice è strutturato su un'architettura modulare che garantisce scalabilità e manutenibilità. Di seguito i componenti core:

### 1. Data & Intelligence Layer

Il cuore decisionale del progetto risiede in un modello predittivo basato su **Random Forest**.

* **Dataset**: Generazione di dati sintetici che simulano i profili cognitivi ed emotivi degli studenti (età, performance STEM, interessi disciplinari).
* **Optimization**: Implementazione di `RandomizedSearchCV` per il tuning degli iperparametri, garantendo la selezione del miglior stimatore tra centinaia di combinazioni (profondità dell'albero, numero di stimatori, criteri di splitting).
* **Persistence**: Serializzazione tramite `joblib` per un caricamento istantaneo in ambiente di produzione.

### 2. Service Layer (API)

Il backend è alimentato da **FastAPI**, scelto per le sue prestazioni asincrone e la robustezza del data validation tramite **Pydantic**.

* **RESTful Endpoints**: Gestione delle richieste POST per l'elaborazione dei profili studente.
* **Business Logic**: Algoritmo integrato che trasforma la predizione numerica in consigli testuali dinamici e livelli di consapevolezza.
* **CORS Middleware**: Configurato per permettere l'integrazione sicura con dashboard e interfacce web esterne.

### 3. Knowledge Layer (Future Integration)

Il sistema è predisposto per accogliere un **Conversational AI Collector**.

* **RAG (Retrieval-Augmented Generation)**: Utilizzo di chatbot (es. Chatbase) per indicizzare documenti ministeriali e Open Data, offrendo risposte immediate basate su fonti ufficiali.

---

## 🛠️ Tecnologie Utilizzate

| Area | Stack Tecnologico |
| --- | --- |
| **Linguaggio** | Python 3.9+ |
| **Machine Learning** | Scikit-learn, Pandas, NumPy |
| **API Framework** | FastAPI, Uvicorn |
| **Data Validation** | Pydantic |
| **Deployment** | Joblib, Docker-ready |

---

## 🚀 Guida all'Installazione

1. **Clona il repository**
```bash
git clone https://github.com/orientamento-png/unichoice.git
cd unichoice

```


2. **Configura l'ambiente virtuale**
```bash
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate

```


3. **Installa le dipendenze**
```bash
pip install -r requirements.txt

```


4. **Esegui l'applicazione**
```bash
uvicorn main:app --reload

```


Accedi alla documentazione interattiva su: `http://127.0.0.1:8000/docs`

---

## ⚖️ Licenza

```text
MIT License

Copyright (c) 2026 orientamento-png

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
