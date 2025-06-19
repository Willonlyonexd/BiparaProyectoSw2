from fastapi import FastAPI
from kpi import ventas, productos, clientes

app = FastAPI(title="KPIs Ecommerce")
app.include_router(ventas.router)
app.include_router(productos.router)
app.include_router(clientes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)