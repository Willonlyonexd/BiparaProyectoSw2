from fastapi import FastAPI
from kpi import ventas

app = FastAPI(title="KPIs Ecommerce")
app.include_router(ventas.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)