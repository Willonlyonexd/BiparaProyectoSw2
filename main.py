from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from kpi import ventas, productos, clientes

app = FastAPI(title="KPIs Ecommerce")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origins en desarrollo
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

app.include_router(ventas.router)
app.include_router(productos.router)
app.include_router(clientes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)