from bd.database import get_mongo_db
from datetime import datetime
from bson import ObjectId

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

def ventas_evolucion(periodo="dia", fecha_inicio=None, fecha_fin=None, tenant=None):
    print(f"[ventas_evolucion] periodo={periodo}, fecha_inicio={fecha_inicio}, fecha_fin={fecha_fin}, tenant={tenant}")
    pipeline = []
    match = {}
    if tenant:
        try:
            match["tenant"] = ObjectId(tenant)
        except Exception:
            match["tenant"] = tenant
    if fecha_inicio:
        match["createdAT"] = {"$gte": fecha_inicio}
    if fecha_fin:
        match.setdefault("createdAT", {})
        match["createdAT"]["$lte"] = fecha_fin
    if match:
        print(f"[ventas_evolucion] match={match}")
        pipeline.append({"$match": match})

    if periodo == "dia":
        group_id = {
            "year": {"$year": "$createdAT"},
            "month": {"$month": "$createdAT"},
            "day": {"$dayOfMonth": "$createdAT"}
        }
    elif periodo == "mes":
        group_id = {
            "year": {"$year": "$createdAT"},
            "month": {"$month": "$createdAT"}
        }
    else:
        group_id = None

    pipeline.append({
        "$group": {
            "_id": group_id,
            "total_ventas": {"$sum": "$total"},
            "num_pedidos": {"$sum": 1},
            "ticket_promedio": {"$avg": "$total"}
        }
    })
    pipeline.append({"$sort": {"_id": 1}})
    print(f"[ventas_evolucion] pipeline={pipeline}")
    result = list(db.ventas.aggregate(pipeline))
    print(f"[ventas_evolucion] result={result}")
    return fix_objectids(result)

def ranking_productos_vendidos(limit=10, tenant=None):
    print(f"[ranking_productos_vendidos] limit={limit}, tenant={tenant}")
    pipeline = []
    match = {}
    if tenant:
        try:
            match["tenant"] = ObjectId(tenant)
        except Exception:
            match["tenant"] = tenant
    if match:
        print(f"[ranking_productos_vendidos] match={match}")
        pipeline.append({"$match": match})

    # Adaptación: Forzar producto_variedad a ObjectId
    pipeline.append({
        "$addFields": {
            "producto_variedad_oid": {
                "$cond": [
                    {"$eq": [{"$type": "$producto_variedad"}, "objectId"]},
                    "$producto_variedad",
                    {
                        "$cond": [
                            {"$eq": [{"$type": "$producto_variedad"}, "string"]},
                            {"$toObjectId": "$producto_variedad"},
                            "$producto_variedad"
                        ]
                    },
                ]
            }
        }
    })

    pipeline.extend([
        {"$group": {
            "_id": "$producto_variedad_oid",
            "unidades": {"$sum": "$cantidad"},
            "monto": {"$sum": {"$multiply": ["$cantidad", "$precio"]}}
        }},
        {"$sort": {"unidades": -1}},
        {"$limit": limit}
    ])
    print(f"[ranking_productos_vendidos] pipeline={pipeline}")
    detalles = list(db.ventadetalles.aggregate(pipeline))
    print(f"[ranking_productos_vendidos] detalles={detalles}")
    ids_variedad = [ObjectId(d["_id"]) for d in detalles if d["_id"]]
    variedades = {str(v["_id"]): v for v in db.producto_variedads.find({"_id": {"$in": ids_variedad}})}
    productos = {str(p["_id"]): p for p in db.productos.find({})}
    for d in detalles:
        variedad = variedades.get(str(d["_id"]))
        if variedad:
            prod = productos.get(str(variedad["producto"]))
            d["producto_nombre"] = prod["titulo"] if prod else "Desconocido"
    print(f"[ranking_productos_vendidos] detalles enriched={detalles}")
    return fix_objectids(detalles)

def top_categorias_vendidas(limit=10, tenant=None):
    print(f"[top_categorias_vendidas] limit={limit}, tenant={tenant}")
    pipeline = []
    match = {}
    if tenant:
        try:
            match["tenant"] = ObjectId(tenant)
        except Exception:
            match["tenant"] = tenant
    if match:
        print(f"[top_categorias_vendidas] match={match}")
        pipeline.append({"$match": match})

    # Adaptación: Forzar producto_variedad a ObjectId
    pipeline.append({
        "$addFields": {
            "producto_variedad_oid": {
                "$cond": [
                    {"$eq": [{"$type": "$producto_variedad"}, "objectId"]},
                    "$producto_variedad",
                    {
                        "$cond": [
                            {"$eq": [{"$type": "$producto_variedad"}, "string"]},
                            {"$toObjectId": "$producto_variedad"},
                            "$producto_variedad"
                        ]
                    },
                ]
            }
        }
    })

    pipeline.extend([
        {"$lookup": {
            "from": "producto_variedads",
            "localField": "producto_variedad_oid",
            "foreignField": "_id",
            "as": "variedad"
        }},
        {"$unwind": "$variedad"},
        {"$lookup": {
            "from": "productos",
            "localField": "variedad.producto",
            "foreignField": "_id",
            "as": "producto"
        }},
        {"$unwind": "$producto"},
        {"$group": {
            "_id": "$producto.categoria",
            "unidades": {"$sum": "$cantidad"},
            "monto": {"$sum": {"$multiply": ["$cantidad", "$precio"]}}
        }},
        {"$sort": {"unidades": -1}},
        {"$limit": limit},
        # Lookup para traer el nombre de la categoría
        {"$lookup": {
            "from": "categorias",
            "localField": "_id",
            "foreignField": "_id",
            "as": "categoria_info"
        }},
        {"$unwind": {"path": "$categoria_info", "preserveNullAndEmptyArrays": True}},
        {"$addFields": {
            "categoria_nombre": {"$ifNull": ["$categoria_info.titulo", "Sin categoría"]}
        }},
        {"$project": {
            "categoria_info": 0  # Oculta el objeto categoria_info
        }}
    ])
    print(f"[top_categorias_vendidas] pipeline={pipeline}")
    result = list(db.ventadetalles.aggregate(pipeline))
    print(f"[top_categorias_vendidas] result={result}")
    return fix_objectids(result)

def ventas_por_categoria(limit=10, tenant=None):
    print(f"[ventas_por_categoria] limit={limit}, tenant={tenant}")
    pipeline = []
    match = {}
    if tenant:
        try:
            match["tenant"] = ObjectId(tenant)
        except Exception:
            match["tenant"] = tenant
    if match:
        print(f"[ventas_por_categoria] match={match}")
        pipeline.append({"$match": match})

    # Adaptación: Forzar producto_variedad a ObjectId
    pipeline.append({
        "$addFields": {
            "producto_variedad_oid": {
                "$cond": [
                    {"$eq": [{"$type": "$producto_variedad"}, "objectId"]},
                    "$producto_variedad",
                    {
                        "$cond": [
                            {"$eq": [{"$type": "$producto_variedad"}, "string"]},
                            {"$toObjectId": "$producto_variedad"},
                            "$producto_variedad"
                        ]
                    },
                ]
            }
        }
    })

    pipeline.extend([
        {"$lookup": {
            "from": "producto_variedads",
            "localField": "producto_variedad_oid",
            "foreignField": "_id",
            "as": "variedad"
        }},
        {"$unwind": "$variedad"},
        {"$lookup": {
            "from": "productos",
            "localField": "variedad.producto",
            "foreignField": "_id",
            "as": "producto"
        }},
        {"$unwind": "$producto"},
        {"$group": {
            "_id": "$producto.categoria",
            "total_ventas": {"$sum": {"$multiply": ["$cantidad", "$precio"]}},
            "unidades": {"$sum": "$cantidad"}
        }},
        {"$sort": {"total_ventas": -1}},
        {"$limit": limit},
        # Lookup para traer el nombre de la categoría
        {"$lookup": {
            "from": "categorias",
            "localField": "_id",
            "foreignField": "_id",
            "as": "categoria_info"
        }},
        {"$unwind": {"path": "$categoria_info", "preserveNullAndEmptyArrays": True}},
        {"$addFields": {
            "categoria_nombre": {"$ifNull": ["$categoria_info.titulo", "Sin categoría"]}
        }},
        {"$project": {
            "categoria_info": 0  # Oculta el objeto categoria_info
        }}
    ])
    print(f"[ventas_por_categoria] pipeline={pipeline}")
    result = list(db.ventadetalles.aggregate(pipeline))
    print(f"[ventas_por_categoria] result={result}")
    return fix_objectids(result)