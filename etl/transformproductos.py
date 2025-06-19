from bd.database import get_mongo_db
from bson import ObjectId

db = get_mongo_db()

def inventario_actual():
    """Inventario actual por producto y variedad"""
    pipeline = [
        {
            "$group": {
                "_id": {"producto": "$producto", "nombre_variedad": "$nombre"},
                "stock": {"$sum": "$stock"}
            }
        }
    ]
    res = list(db.producto_variedads.aggregate(pipeline))
    # Enriquecer nombre producto
    ids = [ObjectId(r["_id"]["producto"]) for r in res]
    productos = {str(p["_id"]): p for p in db.productos.find({"_id": {"$in": ids}})}
    for r in res:
        prod = productos.get(str(r["_id"]["producto"]))
        r["producto_nombre"] = prod["titulo"] if prod else "Desconocido"
    return res

def productos_sin_stock():
    """Productos sin stock (todas sus variedades en 0)"""
    pipeline = [
        {
            "$group": {
                "_id": "$producto",
                "stock_total": {"$sum": "$stock"}
            }
        },
        {"$match": {"stock_total": {"$lte": 0}}},
    ]
    res = list(db.producto_variedads.aggregate(pipeline))
    ids = [ObjectId(r["_id"]) for r in res]
    productos = list(db.productos.find({"_id": {"$in": ids}}))
    return [{"producto_id": str(p["_id"]), "titulo": p["titulo"]} for p in productos]

def valor_total_inventario():
    """Valor total del inventario (precio_venta * stock, suma de todas las variedades)"""
    pipeline = [
        {
            "$project": {
                "valor": {"$multiply": ["$stock", "$precio_venta"]}
            }
        },
        {
            "$group": {
                "_id": None,
                "valor_inventario": {"$sum": "$valor"}
            }
        }
    ]
    res = list(db.producto_variedads.aggregate(pipeline))
    return res[0]["valor_inventario"] if res else 0

def variedades_por_producto():
    """Cantidad de variedades por producto"""
    pipeline = [
        {
            "$group": {
                "_id": "$producto",
                "variedades": {"$sum": 1}
            }
        }
    ]
    res = list(db.producto_variedads.aggregate(pipeline))
    ids = [ObjectId(r["_id"]) for r in res]
    productos = {str(p["_id"]): p for p in db.productos.find({"_id": {"$in": ids}})}
    for r in res:
        prod = productos.get(str(r["_id"]))
        r["producto_nombre"] = prod["titulo"] if prod else "Desconocido"
    return res

def productos_activos_inactivos():
    """Cantidad de productos activos/inactivos"""
    pipeline = [
        {
            "$group": {
                "_id": "$activo",
                "cantidad": {"$sum": 1}
            }
        }
    ]
    return list(db.productos.aggregate(pipeline))

def productos_recien_agregados(limit=10):
    """Últimos productos agregados"""
    res = list(db.productos.find({}).sort("createdAT", -1).limit(limit))
    return [{"producto_id": str(p["_id"]), "titulo": p["titulo"], "createdAT": p["createdAT"]} for p in res]

def productos_proximos_a_agotarse(umbral=5):
    """Productos con stock de alguna variedad por debajo del umbral"""
    pipeline = [
        {"$match": {"stock": {"$lt": umbral}}},
        {
            "$lookup": {
                "from": "productos",
                "localField": "producto",
                "foreignField": "_id",
                "as": "producto"
            }
        },
        {"$unwind": "$producto"},
        {
            "$project": {
                "producto_id": "$producto._id",
                "titulo": "$producto.titulo",
                "nombre_variedad": "$nombre",
                "stock": 1
            }
        }
    ]
    return list(db.producto_variedads.aggregate(pipeline))

def productos_por_categoria():
    """Cantidad de productos por categoría"""
    pipeline = [
        {
            "$group": {
                "_id": "$categoria",
                "cantidad": {"$sum": 1}
            }
        }
    ]
    return list(db.productos.aggregate(pipeline))