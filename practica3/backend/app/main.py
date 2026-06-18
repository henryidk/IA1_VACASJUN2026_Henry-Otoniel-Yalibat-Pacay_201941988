from fastapi import FastAPI

app = FastAPI(title="SmartInvoice API")


@app.get("/health")
def health_check():
    return {"status": "ok"}
