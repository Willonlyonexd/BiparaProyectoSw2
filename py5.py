import pymongo
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import random
import calendar

# Colores para mensajes en consola
class Color:
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    BLUE = '\033[94m'

# Conexión a MongoDB
print(f"{Color.BLUE}Conectando a MongoDB...{Color.END}")
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["EcommerTenants"]

FECHA_FINAL = datetime(2025, 6, 18, 0, 18, 31)
FECHA_INICIAL = datetime(2024, 6, 1, 8, 0, 0)

USUARIO_ID = ObjectId("6852e2b9408bcbf69818d9ca")
PROVEEDOR_ID = ObjectId("6852dbf5c4a6f8d1a81074f9")
ALMACEN_ID = ObjectId("6852dbf5c4a6f8d1a81074f7")

PERIODOS_ESPECIALES = {
    (7, 2024): 1.0,
    (8, 2024): 1.5,
    (9, 2024): 1.2,
    (10, 2024): 1.0,
    (11, 2024): 1.8,
    (12, 2024): 2.0,
    (1, 2025): 1.0,
    (2, 2025): 2.0,
    (3, 2025): 1.5,
    (4, 2025): 1.2,
}

PRODUCTOS_ESPECIALES_POR_MES = {
    (8, 2024): ["Mochilas", "Maletas", "Escolar", "Lonchera", "Estuche", "Cartuchera"],
    (11, 2024): ["Premium", "Edición Limitada", "Kit", "Set"],
    (12, 2024): ["Premium", "Edición Limitada", "Kit", "Set"],
    (2, 2025): ["Mochilas", "Maletas", "Escolar", "Lonchera", "Estuche", "Cartuchera"],
}

def generar_codigo(prefijo):
    hex_part = ''.join(random.choices("0123456789ABCDEF", k=8))
    return f"{prefijo}68{hex_part}"

def calcular_dias_laborables(mes, anio):
    cal = calendar.monthcalendar(anio, mes)
    dias_laborables = []
    for semana in cal:
        for i, dia in enumerate(semana):
            if dia != 0 and i < 5:
                dias_laborables.append(dia)
    return dias_laborables

def obtener_ingresos_por_mes(productos):
    ingresos_por_mes = {}
    total_productos = len(productos)
    for (mes, anio), factor in PERIODOS_ESPECIALES.items():
        base_ingresos = int(total_productos * 0.35 * factor)
        variabilidad = random.randint(-10, 10)
        ingresos_por_mes[(mes, anio)] = max(15, base_ingresos + variabilidad)
    return ingresos_por_mes

def es_producto_especial(producto, mes, anio):
    if (mes, anio) not in PRODUCTOS_ESPECIALES_POR_MES:
        return False
    palabras_clave = PRODUCTOS_ESPECIALES_POR_MES[(mes, anio)]
    nombre_completo = producto.get("titulo", "").lower()
    subcategoria = producto.get("subcategorias", "").lower()
    for palabra in palabras_clave:
        if palabra.lower() in nombre_completo or palabra.lower() in subcategoria:
            return True
    return False

def obtener_fecha_ingreso(mes, anio):
    dias_laborables = calcular_dias_laborables(mes, anio)
    dia = random.choice(dias_laborables)
    hora = random.randint(8, 17)
    minuto = random.randint(0, 59)
    segundo = random.randint(0, 59)
    return datetime(anio, mes, dia, hora, minuto, segundo)

def obtener_precio_unitario(producto):
    nombre = producto.get("titulo", "").lower()
    if any(x in nombre for x in ["mochila", "maleta", "bolso"]):
        return random.randint(90, 180)
    elif any(x in nombre for x in ["chaqueta", "pantalón", "zapatilla", "tenis", "bota"]):
        return random.randint(70, 150)
    elif any(x in nombre for x in ["camiseta", "estuche", "lonchera"]):
        return random.randint(40, 90)
    elif any(x in nombre for x in ["audífono", "cargador", "gadget", "powerbank"]):
        return random.randint(30, 120)
    else:
        return random.randint(50, 100)

def obtener_cantidad_ingreso(producto, mes, anio):
    factor_temporada = PERIODOS_ESPECIALES.get((mes, anio), 1.0)
    es_especial = es_producto_especial(producto, mes, anio)
    if es_especial:
        base = random.randint(15, 30)
    else:
        base = random.randint(5, 15)
    return int(base * factor_temporada)

def crear_ingresos_por_temporada(productos):
    print(f"\n{Color.BLUE}{Color.BOLD}=== GENERANDO INGRESOS DE INVENTARIO - 1 AÑO ==={Color.END}")
    print(f"Periodo: {FECHA_INICIAL.strftime('%B %Y')} - {FECHA_FINAL.strftime('%B %Y')}")
    db.ingresos.delete_many({})
    db.ingresodetalles.delete_many({})
    print(f"{Color.GREEN}✅ Colecciones limpiadas{Color.END}")

    ingresos_por_mes = obtener_ingresos_por_mes(productos)
    codigo_ingreso = 1
    total_ingresos = 0
    total_detalles = 0
    resumen_por_mes = {}

    for (mes, anio), num_ingresos in ingresos_por_mes.items():
        print(f"\n{Color.BOLD}Procesando {calendar.month_name[mes]} {anio} - {num_ingresos} ingresos{Color.END}")
        ingresos_mes_actual = 0
        detalles_mes_actual = 0

        # Separar productos especiales y regulares por mes
        productos_especiales = []
        productos_regulares = []
        for p in productos:
            if es_producto_especial(p, mes, anio):
                productos_especiales.append(p)
            else:
                productos_regulares.append(p)
        random.shuffle(productos_especiales)
        random.shuffle(productos_regulares)
        productos_ordenados = productos_especiales + productos_regulares
        productos_para_usar = productos_ordenados[:num_ingresos]

        for producto in productos_para_usar:
            fecha_ingreso = obtener_fecha_ingreso(mes, anio)
            variantes = list(db.producto_variedads.find({"producto": producto["_id"]}))
            if not variantes:
                print(f"{Color.WARNING}⚠️ No se encontraron variantes para {producto.get('titulo','[sin nombre]')}{Color.END}")
                continue
            num_variantes = min(random.randint(1, 3), len(variantes))
            variantes_seleccionadas = random.sample(variantes, num_variantes)
            total_ingreso = 0
            ingreso_id = ObjectId()
            ingreso = {
                "_id": ingreso_id,
                "usuario": USUARIO_ID,
                "proveedor": PROVEEDOR_ID,
                "almacen": ALMACEN_ID,
                "total": 0,
                "tipo": "Compra",
                "codigo": codigo_ingreso,
                "estado": "Confirmado",
                "createdAT": fecha_ingreso,
                "__v": 0
            }
            detalles_ingreso = 0
            for variante in variantes_seleccionadas:
                precio_unitario = obtener_precio_unitario(producto)
                cantidad = obtener_cantidad_ingreso(producto, mes, anio)
                palabras = producto.get("titulo", "").split()
                prefijo = ''.join(p[0:2] for p in palabras[:2] if p)
                if len(prefijo) < 2:
                    prefijo = producto.get("titulo", "")[:2]
                for j in range(cantidad):
                    codigo = generar_codigo(prefijo)
                    detalle = {
                        "_id": ObjectId(),
                        "ingreso": ingreso_id,
                        "producto": producto["_id"],
                        "producto_variedad": variante["_id"],
                        "almacen": ALMACEN_ID,
                        "precioUnidad": precio_unitario,
                        "codigo": codigo,
                        "estado": True,
                        "estado_": "Confirmado",
                        "createdAT": fecha_ingreso + timedelta(milliseconds=j+1),
                        "__v": 0
                    }
                    db.ingresodetalles.insert_one(detalle)
                    detalles_ingreso += 1
                    detalles_mes_actual += 1
                    total_detalles += 1
                    total_ingreso += precio_unitario
                # ACUMULAR STOCK (suma, no sobreescribe)
                db.producto_variedads.update_one(
                    {"_id": variante["_id"]},
                    {
                        "$inc": {"cantidad": cantidad},
                        "$set": {"precio": round(precio_unitario * 1.4)}
                    }
                )
            ingreso["total"] = total_ingreso
            if detalles_ingreso > 0:
                db.ingresos.insert_one(ingreso)
                ingresos_mes_actual += 1
                total_ingresos += 1
                codigo_ingreso += 1
        resumen_por_mes[f"{calendar.month_name[mes]} {anio}"] = {
            "ingresos": ingresos_mes_actual,
            "detalles": detalles_mes_actual,
        }

    print(f"\n{Color.BLUE}{Color.BOLD}=== RESUMEN DE INGRESOS GENERADOS ==={Color.END}")
    print(f"{Color.GREEN}✅ Total ingresos creados: {total_ingresos}{Color.END}")
    print(f"{Color.GREEN}✅ Total detalles creados: {total_detalles}{Color.END}")
    print(f"\n{Color.BOLD}Distribución por mes:{Color.END}")
    for mes, datos in resumen_por_mes.items():
        print(f"  • {mes}: {datos['ingresos']} ingresos, {datos['detalles']} unidades")
    return total_ingresos, total_detalles

if __name__ == "__main__":
    try:
        print(f"{Color.BLUE}Cargando productos de la base de datos...{Color.END}")
        productos_db = list(db.productos.find({"estado": True}))
        if not productos_db:
            raise Exception("No se encontraron productos activos en la base de datos")
        print(f"{Color.GREEN}Se procesarán {len(productos_db)} productos{Color.END}")
        ingresos, detalles = crear_ingresos_por_temporada(productos_db)
        print(f"\n{Color.GREEN}{Color.BOLD}✅ Proceso completado con éxito{Color.END}")
        print(f"Se generaron {ingresos} ingresos con un total de {detalles} unidades")
        print(f"Fecha actual: {FECHA_FINAL.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Usuario: muimui69")
    except Exception as e:
        print(f"{Color.FAIL}❌ Error: {str(e)}{Color.END}")