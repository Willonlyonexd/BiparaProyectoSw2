from fastapi import APIRouter, Query
from etl.transformventas import *
from datetime import datetime

router = APIRouter(prefix="/kpi/ventas", tags=["Ventas"])

@router.get("/evolucion/dia")
def evolucion_dia(
    fecha_inicio: str = None,
    fecha_fin: str = None,
    tenant: str = Query(...)
):
    print(f"[API] /evolucion/dia tenant={tenant}, fecha_inicio={fecha_inicio}, fecha_fin={fecha_fin}")
    fi = fecha_inicio and datetime.fromisoformat(fecha_inicio)
    ff = fecha_fin and datetime.fromisoformat(fecha_fin)
    return ventas_evolucion("dia", fi, ff, tenant)

@router.get("/evolucion/mes")
def evolucion_mes(
    fecha_inicio: str = None,
    fecha_fin: str = None,
    tenant: str = Query(...)
):
    print(f"[API] /evolucion/mes tenant={tenant}, fecha_inicio={fecha_inicio}, fecha_fin={fecha_fin}")
    fi = fecha_inicio and datetime.fromisoformat(fecha_inicio)
    ff = fecha_fin and datetime.fromisoformat(fecha_fin)
    return ventas_evolucion("mes", fi, ff, tenant)

@router.get("/top_productos")
def top_productos(limit: int = 10, tenant: str = Query(...)):
    print(f"[API] /top_productos tenant={tenant}, limit={limit}")
    return ranking_productos_vendidos(limit, tenant)

@router.get("/top_categorias")
def top_categorias(limit: int = 10, tenant: str = Query(...)):
    print(f"[API] /top_categorias tenant={tenant}, limit={limit}")
    return top_categorias_vendidas(limit, tenant)

@router.get("/ventas_por_categoria")
def ventas_categoria(limit: int = 10, tenant: str = Query(...)):
    print(f"[API] /ventas_por_categoria tenant={tenant}, limit={limit}")
    return ventas_por_categoria(limit, tenant)