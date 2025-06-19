from fastapi import APIRouter, Query
from etl.transformclientes import *

router = APIRouter(prefix="/kpi/clientes", tags=["Clientes"])

@router.get("/nuevos-por-mes")
def kpi_clientes_nuevos_por_mes(tenant: str = Query(...)):
    return clientes_nuevos_por_mes(tenant)

@router.get("/top-clientes")
def kpi_top_clientes(limit: int = 10, tenant: str = Query(...)):
    return top_clientes(limit, tenant)

@router.get("/activos-inactivos-por-mes")
def kpi_activos_inactivos_por_mes(meses: int = 12, tenant: str = Query(...)):
    return clientes_activos_inactivos_por_mes(tenant, meses)

@router.get("/frecuencia-compra")
def kpi_frecuencia_compra(tenant: str = Query(...), limit: int = 100):
    return frecuencia_compra_por_cliente(tenant, limit)

@router.get("/tasa-retencion")
def kpi_tasa_retencion(dias: int = 30, tenant: str = Query(...)):
    return tasa_retencion_clientes(tenant, dias)

@router.get("/inactivos-por-tiempo")
def kpi_inactivos_tiempo(dias: int = 30, tenant: str = Query(...), limit: int = 100):
    return clientes_inactivos_tiempo(tenant, dias, limit)