from bd.database import get_mongo_db
from bson import ObjectId
from datetime import datetime, timedelta
from calendar import month_name

db = get_mongo_db()

def fix_objectids(obj):
    """Recursively converts all ObjectId instances to strings for JSON serialization."""
    if isinstance(obj, list):
        return [fix_objectids(i) for i in obj]
    if isinstance(obj, dict):
        return {k: fix_objectids(v) for k, v in obj.items()}
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

def clientes_nuevos_por_mes(tenant=None):
    pipeline = []
    match = {}
    if tenant:
        try:
            match["tenant"] = ObjectId(tenant)
        except Exception:
            match["tenant"] = tenant
    if match:
        pipeline.append({"$match": match})
    pipeline.extend([
        {"$group": {
            "_id": {
                "year": {"$year": "$createdAT"},
                "month": {"$month": "$createdAT"}
            },
            "nuevos_clientes": {"$sum": 1}
        }},
        {"$sort": {"_id.year": 1, "_id.month": 1}}
    ])
    results = list(db.clientes.aggregate(pipeline))
    # Añadir nombre del mes en español
    meses_es = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    for obj in results:
        obj["mes_nombre"] = meses_es[obj["_id"]["month"]]
    return fix_objectids(results)

def top_clientes(limit=10, tenant=None):
    pipeline = []
    match = {}
    if tenant:
        try:
            match["tenant"] = ObjectId(tenant)
        except Exception:
            match["tenant"] = tenant
    if match:
        pipeline.append({"$match": match})
    pipeline.extend([
        {"$group": {
            "_id": "$cliente",
            "total_compras": {"$sum": "$total"},
            "num_compras": {"$sum": 1}
        }},
        {"$sort": {"total_compras": -1}},
        {"$limit": limit},
        {"$lookup": {
            "from": "clientes",
            "localField": "_id",
            "foreignField": "_id",
            "as": "cliente_info"
        }},
        {"$unwind": {"path": "$cliente_info", "preserveNullAndEmptyArrays": True}},
        {"$addFields": {
            "nombre": {"$concat": [
                {"$ifNull": ["$cliente_info.nombres", ""]},
                {"$cond": [{"$and": [
                    {"$ne": ["$cliente_info.nombres", None]},
                    {"$ne": ["$cliente_info.nombres", ""]},
                    {"$ne": ["$cliente_info.apellidos", None]},
                    {"$ne": ["$cliente_info.apellidos", ""]}
                ]}, " ", ""]},
                {"$ifNull": ["$cliente_info.apellidos", ""]}
            ]},
            "correo": {"$ifNull": ["$cliente_info.email", ""]}
        }},
        {"$project": {
            "cliente_info": 0
        }}
    ])
    return fix_objectids(list(db.ventas.aggregate(pipeline)))

def clientes_activos_inactivos_por_mes(tenant=None, meses=12):
    """Devuelve por cada mes el número de clientes activos e inactivos."""
    # Tomar los últimos `meses` meses
    ahora = datetime.utcnow()
    resultados = []
    match = {}
    if tenant:
        try:
            match["tenant"] = ObjectId(tenant)
        except Exception:
            match["tenant"] = tenant
    # Obtener todos los clientes del tenant
    clientes_todos = set(str(x["_id"]) for x in db.clientes.find(match, {"_id": 1}))
    for i in range(meses-1, -1, -1):
        inicio = datetime(ahora.year, ahora.month, 1) - timedelta(days=30*i)
        fin = datetime(inicio.year + (inicio.month // 12), ((inicio.month % 12) + 1), 1) if inicio.month < 12 else datetime(inicio.year + 1, 1, 1)
        ventas_match = dict(match)
        ventas_match["createdAT"] = {"$gte": inicio, "$lt": fin}
        pipeline = [
            {"$match": ventas_match},
            {"$group": {"_id": "$cliente"}}
        ]
        clientes_activos = set(str(x["_id"]) for x in db.ventas.aggregate(pipeline))
        clientes_inactivos = clientes_todos - clientes_activos
        resultados.append({
            "anio": inicio.year,
            "mes": inicio.month,
            "mes_nombre": ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][inicio.month],
            "activos": len(clientes_activos),
            "inactivos": len(clientes_inactivos)
        })
    return resultados

def frecuencia_compra_por_cliente(tenant=None, limit=100):
    pipeline = []
    match = {}
    if tenant:
        try:
            match["tenant"] = ObjectId(tenant)
        except Exception:
            match["tenant"] = tenant
    if match:
        pipeline.append({"$match": match})
    pipeline.extend([
        {"$group": {
            "_id": "$cliente",
            "num_compras": {"$sum": 1},
            "primera_compra": {"$min": "$createdAT"},
            "ultima_compra": {"$max": "$createdAT"}
        }},
        {"$lookup": {
            "from": "clientes",
            "localField": "_id",
            "foreignField": "_id",
            "as": "cliente_info"
        }},
        {"$unwind": {"path": "$cliente_info", "preserveNullAndEmptyArrays": True}},
        {"$addFields": {
            "nombre": {"$concat": [
                {"$ifNull": ["$cliente_info.nombres", ""]},
                {"$cond": [{"$and": [
                    {"$ne": ["$cliente_info.nombres", None]},
                    {"$ne": ["$cliente_info.nombres", ""]},
                    {"$ne": ["$cliente_info.apellidos", None]},
                    {"$ne": ["$cliente_info.apellidos", ""]}
                ]}, " ", ""]},
                {"$ifNull": ["$cliente_info.apellidos", ""]}
            ]}
        }},
        {"$project": {
            "_id": 1,
            "num_compras": 1,
            "primera_compra": 1,
            "ultima_compra": 1,
            "nombre": 1
        }},
        {"$sort": {"num_compras": -1}},
        {"$limit": limit}
    ])
    return fix_objectids(list(db.ventas.aggregate(pipeline)))

def tasa_retencion_clientes(tenant=None, dias=30):
    now = datetime.utcnow()
    hace_x_dias = now - timedelta(days=dias)
    pipeline = []
    match = {}
    if tenant:
        try:
            match["tenant"] = ObjectId(tenant)
        except Exception:
            match["tenant"] = tenant
    if match:
        pipeline.append({"$match": match})
    # Clientes que compraron antes del periodo
    pipeline_anteriores = list(pipeline)
    pipeline_anteriores.append({"$match": {"createdAT": {"$lt": hace_x_dias}}})
    pipeline_anteriores.append({"$group": {"_id": "$cliente"}})
    anteriores = set(str(x["_id"]) for x in db.ventas.aggregate(pipeline_anteriores))
    # Clientes que volvieron a comprar en el periodo
    pipeline_recurrentes = list(pipeline)
    pipeline_recurrentes.append({"$match": {"createdAT": {"$gte": hace_x_dias}}})
    pipeline_recurrentes.append({"$group": {"_id": "$cliente"}})
    recurrentes = set(str(x["_id"]) for x in db.ventas.aggregate(pipeline_recurrentes))
    retuvieron = anteriores & recurrentes
    tasa = (len(retuvieron) / len(anteriores)) * 100 if anteriores else 0
    return {
        "clientes_previos": len(anteriores),
        "clientes_recurrentes": len(retuvieron),
        "tasa_retencion": tasa
    }

def clientes_inactivos_tiempo(tenant=None, dias=30, limit=100):
    now = datetime.utcnow()
    hace_x_dias = now - timedelta(days=dias)
    pipeline = []
    match = {}
    if tenant:
        try:
            match["tenant"] = ObjectId(tenant)
        except Exception:
            match["tenant"] = tenant
    if match:
        pipeline.append({"$match": match})
    pipeline.extend([
        {"$group": {
            "_id": "$cliente",
            "ultima_compra": {"$max": "$createdAT"}
        }},
        {"$match": {"ultima_compra": {"$lt": hace_x_dias}}},
        {"$lookup": {
            "from": "clientes",
            "localField": "_id",
            "foreignField": "_id",
            "as": "cliente_info"
        }},
        {"$unwind": {"path": "$cliente_info", "preserveNullAndEmptyArrays": True}},
        {"$addFields": {
            "nombre": {"$concat": [
                {"$ifNull": ["$cliente_info.nombres", ""]},
                {"$cond": [{"$and": [
                    {"$ne": ["$cliente_info.nombres", None]},
                    {"$ne": ["$cliente_info.nombres", ""]},
                    {"$ne": ["$cliente_info.apellidos", None]},
                    {"$ne": ["$cliente_info.apellidos", ""]}
                ]}, " ", ""]},
                {"$ifNull": ["$cliente_info.apellidos", ""]}
            ]}
        }},
        {"$project": {
            "_id": 1,
            "ultima_compra": 1,
            "nombre": 1
        }},
        {"$sort": {"ultima_compra": 1}},
        {"$limit": limit}
    ])
    return fix_objectids(list(db.ventas.aggregate(pipeline)))