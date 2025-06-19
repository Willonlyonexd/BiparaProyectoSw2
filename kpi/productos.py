from fastapi import APIRouter, Query
from etl.transformproductos import *

router = APIRouter(prefix="/kpi/productos", tags=["Productos"])

@router.get("/distribucion-por-categoria")
def kpi_distribucion_categoria(tenant: str = Query(...)):
    return distribucion_por_categoria(tenant)

@router.get("/stock-por-producto")
def kpi_stock_producto(tenant: str = Query(...)):
    return stock_actual_por_producto(tenant)

@router.get("/stock-por-categoria")
def kpi_stock_categoria(tenant: str = Query(...)):
    return stock_actual_por_categoria(tenant)

@router.get("/stock-por-almacen")
def kpi_stock_almacen(tenant: str = Query(...)):
    return stock_por_almacen(tenant)

@router.get("/productos-sin-stock")
def kpi_productos_sin_stock(tenant: str = Query(...)):
    return productos_sin_stock(tenant)

@router.get("/productos-recien-agregados")
def kpi_productos_recientes(limit: int = 10, tenant: str = Query(...)):
    return productos_recien_agregados(limit, tenant)

@router.get("/productos-sobre-stock")
def kpi_productos_sobre_stock(umbral: int = 100, tenant: str = Query(...)):
    return productos_sobre_stock(umbral, tenant)