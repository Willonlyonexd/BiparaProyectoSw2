from bd.database import get_mongo_db
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

def distribucion_por_categoria(tenant=None):
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
        {"$group": {"_id": "$categoria", "cantidad": {"$sum": 1}}},
        {"$lookup": {
            "from": "categorias",
            "localField": "_id",
            "foreignField": "_id",
            "as": "categoria"
        }},
        {"$unwind": "$categoria"},
        {"$project": {
            "_id": 0,
            "categoria_id": "$_id",
            "categoria": "$categoria.titulo",
            "cantidad": 1
        }}
    ])
    return fix_objectids(list(db.productos.aggregate(pipeline)))

def stock_actual_por_producto(tenant=None):
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
        {"$group": {"_id": "$producto", "stock_total": {"$sum": "$cantidad"}}},
        {"$lookup": {
            "from": "productos",
            "localField": "_id",
            "foreignField": "_id",
            "as": "producto"
        }},
        {"$unwind": "$producto"},
        {"$project": {
            "_id": 0,
            "producto_id": "$_id",
            "producto": "$producto.titulo",
            "stock_total": 1
        }}
    ])
    return fix_objectids(list(db.producto_variedads.aggregate(pipeline)))

def stock_actual_por_categoria(tenant=None):
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
        {"$lookup": {
            "from": "productos",
            "localField": "producto",
            "foreignField": "_id",
            "as": "producto"
        }},
        {"$unwind": "$producto"},
        {"$group": {
            "_id": "$producto.categoria",
            "stock_total": {"$sum": "$cantidad"}
        }},
        {"$lookup": {
            "from": "categorias",
            "localField": "_id",
            "foreignField": "_id",
            "as": "categoria"
        }},
        {"$unwind": "$categoria"},
        {"$project": {
            "_id": 0,
            "categoria_id": "$_id",
            "categoria": "$categoria.titulo",
            "stock_total": 1
        }}
    ])
    return fix_objectids(list(db.producto_variedads.aggregate(pipeline)))

def stock_por_almacen(tenant=None):
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
        {"$group": {"_id": "$almacen", "stock_total": {"$sum": "$cantidad"}}},
        {"$lookup": {
            "from": "almacens",
            "localField": "_id",
            "foreignField": "_id",
            "as": "almacen"
        }},
        {"$unwind": "$almacen"},
        {"$project": {
            "_id": 0,
            "almacen_id": "$_id",
            "almacen": "$almacen.titulo",
            "stock_total": 1
        }}
    ])
    return fix_objectids(list(db.producto_variedads.aggregate(pipeline)))

def productos_sin_stock(tenant=None):
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
        {"$group": {"_id": "$producto", "stock_total": {"$sum": "$cantidad"}}},
        {"$match": {"stock_total": {"$lte": 0}}},
        {"$lookup": {
            "from": "productos",
            "localField": "_id",
            "foreignField": "_id",
            "as": "producto"
        }},
        {"$unwind": "$producto"},
        {"$project": {
            "_id": 0,
            "producto_id": "$_id",
            "producto": "$producto.titulo",
            "stock_total": 1
        }}
    ])
    return fix_objectids(list(db.producto_variedads.aggregate(pipeline)))

def productos_recien_agregados(limit=10, tenant=None):
    match = {}
    if tenant:
        try:
            match["tenant"] = ObjectId(tenant)
        except Exception:
            match["tenant"] = tenant
    cursor = db.productos.find(match).sort("createdAT", -1).limit(limit)
    return fix_objectids(list(cursor))

def productos_sobre_stock(umbral=100, tenant=None):
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
        {"$group": {"_id": "$producto", "stock_total": {"$sum": "$cantidad"}}},
        {"$match": {"stock_total": {"$gt": umbral}}},
        {"$lookup": {
            "from": "productos",
            "localField": "_id",
            "foreignField": "_id",
            "as": "producto"
        }},
        {"$unwind": "$producto"},
        {"$project": {
            "_id": 0,
            "producto_id": "$_id",
            "producto": "$producto.titulo",
            "stock_total": 1
        }}
    ])
    return fix_objectids(list(db.producto_variedads.aggregate(pipeline)))