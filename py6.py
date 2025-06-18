import pymongo
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import random
import calendar
import math

# Colores para mensajes en consola
class Color:
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'

# Configuración: Tenant y BD
TENANT_ID = ObjectId("6852dbf5c4a6f8d1a81074f6")
BD_NAME = "EcommerTenants"
META_VENTAS = 5000
FECHA_INICIO = datetime(2024, 6, 10)
FECHA_FIN = datetime(2025, 6, 17, 23, 59, 59)

print(f"{Color.BLUE}Conectando a MongoDB...{Color.END}")
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client[BD_NAME]

# Segmentos y distribución (igual que tu script)
SEGMENTOS_CLIENTES = {
    "vip": {"porcentaje": 0.07, "frecuencia_mensual": 0.55, "pedidos_por_mes": [0, 1, 2], "pesos_pedidos": [35, 50, 15]},
    "fiel": {"porcentaje": 0.18, "frecuencia_mensual": 0.40, "pedidos_por_mes": [0, 1, 2], "pesos_pedidos": [55, 40, 5]},
    "ocasional": {"porcentaje": 0.55, "frecuencia_mensual": 0.20, "pedidos_por_mes": [0, 1], "pesos_pedidos": [85, 15]},
    "dormido": {"porcentaje": 0.20, "frecuencia_mensual": 0.05, "pedidos_por_mes": [0, 1], "pesos_pedidos": [98, 2]}
}

DISTRIBUCION_MENSUAL = {
    (2024, 6): 0.01,   # Junio 2024 (parcial)
    (2024, 7): 0.02,
    (2024, 8): 0.04,
    (2024, 9): 0.06,
    (2024, 10): 0.08,
    (2024, 11): 0.10,
    (2024, 12): 0.20,
    (2025, 1): 0.10,
    (2025, 2): 0.15,
    (2025, 3): 0.15,
    (2025, 4): 0.05,
    (2025, 5): 0.03,
    (2025, 6): 0.01  # hasta el 17
}

def cargar_datos_tenant():
    print(f"{Color.BLUE}Cargando datos del tenant...{Color.END}")
    productos = list(db.productos.find({"estado": True, "tenant": TENANT_ID}))
    variantes = list(db.producto_variedads.find({"cantidad": {"$gt": 0}, "tenant": TENANT_ID}))
    clientes = list(db.clientes.find({"estado": True, "tenant": TENANT_ID}))
    variantes_por_producto = {}
    for v in variantes:
        pid = str(v["producto"])
        if pid not in variantes_por_producto:
            variantes_por_producto[pid] = []
        variantes_por_producto[pid].append(v)
    print(f"{Color.GREEN}✓ Datos cargados: {len(productos)} productos, {len(variantes)} variantes, {len(clientes)} clientes{Color.END}")
    return productos, variantes, clientes, variantes_por_producto

def asignar_segmentos_cliente(clientes):
    print(f"{Color.BLUE}Asignando segmentos a clientes...{Color.END}")
    segmentos = {}
    info_cliente = {}
    clientes_shuffled = clientes.copy()
    random.shuffle(clientes_shuffled)
    total_clientes = len(clientes)
    n_vip = int(total_clientes * SEGMENTOS_CLIENTES["vip"]["porcentaje"])
    n_fieles = int(total_clientes * SEGMENTOS_CLIENTES["fiel"]["porcentaje"])
    n_ocasionales = int(total_clientes * SEGMENTOS_CLIENTES["ocasional"]["porcentaje"])
    n_dormidos = total_clientes - n_vip - n_fieles - n_ocasionales
    index = 0
    for i in range(n_vip):
        if index < len(clientes_shuffled):
            cid = str(clientes_shuffled[index]["_id"])
            segmentos[cid] = "vip"
            info_cliente[cid] = {"fecha_registro": clientes_shuffled[index].get("createdAT", FECHA_INICIO)}
            index += 1
    for i in range(n_fieles):
        if index < len(clientes_shuffled):
            cid = str(clientes_shuffled[index]["_id"])
            segmentos[cid] = "fiel"
            info_cliente[cid] = {"fecha_registro": clientes_shuffled[index].get("createdAT", FECHA_INICIO)}
            index += 1
    for i in range(n_ocasionales):
        if index < len(clientes_shuffled):
            cid = str(clientes_shuffled[index]["_id"])
            segmentos[cid] = "ocasional"
            info_cliente[cid] = {"fecha_registro": clientes_shuffled[index].get("createdAT", FECHA_INICIO)}
            index += 1
    while index < len(clientes_shuffled):
        cid = str(clientes_shuffled[index]["_id"])
        segmentos[cid] = "dormido"
        info_cliente[cid] = {"fecha_registro": clientes_shuffled[index].get("createdAT", FECHA_INICIO)}
        index += 1
    return segmentos, info_cliente

def seleccionar_productos_para_compra(productos, variantes_por_producto, cliente, segmento):
    # Peso por segmento (simplificado)
    weights_items = [10, 25, 35, 20, 7, 3] if segmento == "vip" else \
                    [20, 45, 25, 7, 2, 1] if segmento == "fiel" else \
                    [45, 40, 12, 3, 0, 0] if segmento == "ocasional" else \
                    [70, 25, 5, 0, 0, 0]
    num_items = random.choices([1, 2, 3, 4, 5, 6], weights=weights_items)[0]
    productos_disponibles = [p for p in productos if str(p["_id"]) in variantes_por_producto and variantes_por_producto[str(p["_id"])]]
    seleccion_productos = []
    intentos = 0
    while len(seleccion_productos) < num_items and intentos < 20:
        p = random.choice(productos_disponibles)
        pid = str(p["_id"])
        variante = random.choice(variantes_por_producto[pid])
        stock = variante.get("cantidad", 0)
        if stock <= 0: continue
        if any(ps["producto"]["_id"] == p["_id"] for ps in seleccion_productos): continue
        cantidad = min(1 if segmento in ["ocasional", "dormido"] else random.choices([1,2,3], [85,10,5])[0], stock)
        seleccion_productos.append({"producto": p, "variante": variante, "cantidad": cantidad})
        intentos += 1
    return seleccion_productos

def generar_ventas_controladas(productos, variantes, clientes, variantes_por_producto):
    print(f"{Color.BLUE}Generando ventas: {META_VENTAS} desde {FECHA_INICIO.strftime('%d/%m/%Y')} al {FECHA_FIN.strftime('%d/%m/%Y')}{Color.END}")
    segmentos_cliente, info_cliente = asignar_segmentos_cliente(clientes)
    # Distribuir ventas por mes
    meses = []
    d = FECHA_INICIO
    while d <= FECHA_FIN:
        meses.append((d.year, d.month))
        if d.month == 12:
            d = datetime(d.year+1, 1, 1)
        else:
            d = datetime(d.year, d.month+1, 1)
    ventas_por_mes = {}
    for ym, pct in DISTRIBUCION_MENSUAL.items():
        ventas_por_mes[ym] = int(META_VENTAS * pct)
    total_asignado = sum(ventas_por_mes.values())
    if total_asignado != META_VENTAS:
        diff = META_VENTAS - total_asignado
        ventas_por_mes[sorted(ventas_por_mes)[-1]] += diff
    # Generar ventas
    ventas = []
    venta_detalles = []
    for (anio, mes), num_ventas in ventas_por_mes.items():
        dias_mes = [d for d in range(1, calendar.monthrange(anio, mes)[1]+1)
                    if datetime(anio, mes, d) >= FECHA_INICIO and datetime(anio, mes, d) <= FECHA_FIN]
        for _ in range(num_ventas):
            dia = random.choice(dias_mes)
            hora = random.randint(9, 21)
            minuto = random.randint(0,59)
            segundo = random.randint(0,59)
            fecha_venta = datetime(anio, mes, dia, hora, minuto, segundo)
            # Solo clientes activos en ese momento
            posibles_clientes = [cli for cli in clientes if cli.get("createdAT", FECHA_INICIO) <= fecha_venta]
            if not posibles_clientes: continue
            cliente = random.choice(posibles_clientes)
            segmento = segmentos_cliente.get(str(cliente["_id"]), "ocasional")
            seleccion = seleccionar_productos_para_compra(productos, variantes_por_producto, cliente, segmento)
            if not seleccion: continue
            total = sum(s["variante"].get("precio", 0) * s["cantidad"] for s in seleccion)
            venta_id = ObjectId()
            venta = {
                "_id": venta_id,
                "cliente": cliente["_id"],
                "total": total,
                "envio": 0,
                "estado": "Procesado",
                "tenant": TENANT_ID,
                "createdAT": fecha_venta,
                "__v": 0
            }
            ventas.append(venta)
            for s in seleccion:
                detalle = {
                    "_id": ObjectId(),
                    "cliente": cliente["_id"],
                    "venta": venta_id,
                    "producto": s["producto"]["_id"],
                    "variedad": s["variante"]["_id"],
                    "cantidad": s["cantidad"],
                    "precio": s["variante"].get("precio", 0),
                    "tenant": TENANT_ID,
                    "createdAT": fecha_venta + timedelta(milliseconds=random.randint(1,99)),
                    "__v": 0
                }
                venta_detalles.append(detalle)
                # Descontar stock (en RAM, no en base)
                s["variante"]["cantidad"] = max(0, s["variante"]["cantidad"] - s["cantidad"])
                # Actualizar en base real si quieres: (descomenta si quieres tocar stock real)
                # db.producto_variedads.update_one({"_id": s["variante"]["_id"]}, {"$inc": {"cantidad": -s["cantidad"]}})
            if len(ventas) >= META_VENTAS: break
        if len(ventas) >= META_VENTAS: break
    print(f"{Color.GREEN}✓ Generadas {len(ventas)} ventas y {len(venta_detalles)} detalles{Color.END}")
    return ventas, venta_detalles

def insertar_datos_ventas(ventas, venta_detalles):
    print(f"{Color.BLUE}Insertando ventas en la base de datos...{Color.END}")
    db.ventas.delete_many({"tenant": TENANT_ID})
    db.ventadetalles.delete_many({"tenant": TENANT_ID})
    if ventas: db.ventas.insert_many(ventas)
    if venta_detalles: db.ventadetalles.insert_many(venta_detalles)
    print(f"{Color.GREEN}✓ Datos insertados para el tenant{Color.END}")

def main():
    productos, variantes, clientes, variantes_por_producto = cargar_datos_tenant()
    if not productos or not variantes or not clientes:
        print(f"{Color.FAIL}Faltan datos en la base de datos!{Color.END}")
        return
    ventas, venta_detalles = generar_ventas_controladas(productos, variantes, clientes, variantes_por_producto)
    print(f"\nSe generaron {len(ventas)} ventas para el tenant.")
    resp = input("¿Desea insertar estos datos en la base de datos? (s/n): ")
    if resp.lower() in ['s', 'si', 'y', 'yes']:
        insertar_datos_ventas(ventas, venta_detalles)
        print(f"{Color.GREEN}Proceso completado exitosamente.{Color.END}")
    else:
        print(f"{Color.WARNING}Operación cancelada. No se insertaron datos.{Color.END}")

if __name__ == "__main__":
    main()