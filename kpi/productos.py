from fastapi import APIRouter, Query
from etl.transformproductos import *

router = APIRouter(prefix="/kpi/productos", tags=["Productos"])

@router.get("/inventario_actual")
def endpoint_inventario_actual():
    """Inventario actual por producto y variedad."""
    return inventario_actual()

@router.get("/sin_stock")
def endpoint_productos_sin_stock():
    """Productos sin stock."""
    return productos_sin_stock()

@router.get("/valor_inventario")
def endpoint_valor_inventario():
    """Valor total del inventario."""
    return {"valor_inventario": valor_total_inventario()}

@router.get("/variedades_por_producto")
def endpoint_variedades_por_producto():
    """Cantidad de variedades por producto."""
    return variedades_por_producto()

@router.get("/activos_inactivos")
def endpoint_productos_activos_inactivos():
    """Cantidad de productos activos/inactivos."""
    return productos_activos_inactivos()

@router.get("/recien_agregados")
def endpoint_productos_recien_agregados(limit: int = 10):
    """Últimos productos agregados."""
    return productos_recien_agregados(limit)

@router.get("/proximos_a_agotarse")
def endpoint_productos_proximos_a_agotarse(umbral: int = 5):
    """Productos próximos a agotarse (stock bajo)."""
    return productos_proximos_a_agotarse(umbral)

@router.get("/por_categoria")
def endpoint_productos_por_categoria():
    """Cantidad de productos por categoría."""
    return productos_por_categoria()