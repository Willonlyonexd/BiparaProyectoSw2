import pymongo
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import random
import calendar
import csv
import math

# CONFIGURACIÓN
CSV_VARIANTES = "EcommerTenants.producto_variedads.csv"
DB_NAME = "EcommerTenants"
TENANT_ID = "6852dbf5c4a6f8d1a81074f6"
COL_VENTAS = "ventas"
COL_DETALLES = "ventadetalles"
META_VENTAS = 5000
FECHA_INICIO = datetime(2024, 6, 10)
FECHA_FIN = datetime(2025, 6, 17, 23, 59, 59)

DISTRIBUCION_MENSUAL = [
    (2024, 6, 0.03), (2024, 7, 0.03), (2024, 8, 0.04), (2024, 9, 0.06),
    (2024,10, 0.08), (2024,11, 0.10), (2024,12, 0.19), (2025, 1, 0.09),
    (2025, 2, 0.15), (2025, 3, 0.13), (2025, 4, 0.05), (2025, 5, 0.03),
    (2025, 6, 0.02)
]

def cargar_variantes_desde_csv(csv_path, tenant_id):
    variantes = []
    variantes_por_producto = {}
    with open(csv_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                if row["tenant"] != tenant_id:
                    continue
                cantidad = int(row["cantidad"])
                precio = float(row["precio"])
                if cantidad > 0 and precio > 0:
                    variante = {
                        "_id": row["_id"],
                        "hxd": row["hxd"],
                        "color": row["color"],
                        "talla": row["talla"],
                        "sku": row["sku"],
                        "cantidad": cantidad,
                        "precio": precio,
                        "producto": row["producto"],
                        "tenant": row["tenant"],
                        "createdAT": row["createdAT"]
                    }
                    variantes.append(variante)
                    if row["producto"] not in variantes_por_producto:
                        variantes_por_producto[row["producto"]] = []
                    variantes_por_producto[row["producto"]].append(variante)
            except Exception as e:
                print(f"Error en fila {row}: {e}")
    print(f"✓ {len(variantes)} variantes cargadas desde CSV para tenant {tenant_id}.")
    return variantes, variantes_por_producto

def distribuir_ventas_por_mes(meta_ventas, distribucion):
    ventas_por_mes = []
    asignadas = 0
    for (anio, mes, pct) in distribucion:
        cantidad = int(round(meta_ventas * pct))
        ventas_por_mes.append(((anio, mes), cantidad))
        asignadas += cantidad
    # Ajuste fino para cumplir la meta exacta
    diff = meta_ventas - sum(cnt for _, cnt in ventas_por_mes)
    for i in range(abs(diff)):
        idx = i % len(ventas_por_mes)
        ventas_por_mes[idx] = (
            ventas_por_mes[idx][0], ventas_por_mes[idx][1] + (1 if diff > 0 else -1)
        )
    return ventas_por_mes

def distribuir_ventas_por_dia(ventas_mes, fecha_inicio, fecha_fin):
    ventas_por_dia = {}
    for (anio, mes), cantidad in ventas_mes:
        dias_mes = [
            d for d in range(1, calendar.monthrange(anio, mes)[1] + 1)
            if datetime(anio, mes, d) >= fecha_inicio and datetime(anio, mes, d) <= fecha_fin
        ]
        if not dias_mes or cantidad == 0:
            continue
        base = cantidad // len(dias_mes)
        resto = cantidad % len(dias_mes)
        for i, dia in enumerate(dias_mes):
            ventas_por_dia[(anio, mes, dia)] = base + (1 if i < resto else 0)
    return ventas_por_dia

def obtener_clientes(db, tenant_id):
    clientes = list(db.clientes.find({"estado": True, "tenant": ObjectId(tenant_id)}))
    if not clientes:
        raise Exception("No hay clientes activos en la base de datos para este tenant.")
    print(f"✓ {len(clientes)} clientes activos cargados de la BD para tenant {tenant_id}.")
    return clientes

def seleccionar_cliente(clientes):
    return random.choice(clientes)

def seleccionar_variante(variantes_pool, stock_memoria):
    pool = [v for v in variantes_pool if stock_memoria.get(v["_id"], 0) > 0 and v["precio"] > 0]
    if not pool:
        return None
    pesos = [(stock_memoria[v["_id"]] * (1 + v["precio"]/100)) for v in pool]
    return random.choices(pool, weights=pesos, k=1)[0]

def main():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[DB_NAME]

    db[COL_VENTAS].delete_many({"tenant": ObjectId(TENANT_ID)})
    db[COL_DETALLES].delete_many({"tenant": ObjectId(TENANT_ID)})
    print("Colecciones 'ventas' y 'ventadetalles' limpiadas para el tenant.")

    variantes, variantes_por_producto = cargar_variantes_desde_csv(CSV_VARIANTES, TENANT_ID)
    stock_memoria = {v["_id"]: v["cantidad"] for v in variantes}

    clientes = obtener_clientes(db, TENANT_ID)

    ventas_por_mes = distribuir_ventas_por_mes(META_VENTAS, DISTRIBUCION_MENSUAL)
    ventas_por_dia = distribuir_ventas_por_dia(ventas_por_mes, FECHA_INICIO, FECHA_FIN)

    ventas = []
    venta_detalles = []
    total_ventas = 0

    print(f"\nSimulando {META_VENTAS} ventas de tenant {TENANT_ID} desde {FECHA_INICIO.date()} hasta {FECHA_FIN.date()}...")

    for (anio, mes, dia), cant_dia in sorted(ventas_por_dia.items()):
        for _ in range(cant_dia):
            cliente = seleccionar_cliente(clientes)
            n_items = random.choices([1,2,3], weights=[70,25,5])[0]
            variantes_elegidas = []
            intentos = 0
            while len(variantes_elegidas) < n_items and intentos < 20:
                prod_keys = list(variantes_por_producto.keys())
                pkey = random.choice(prod_keys)
                variante = seleccionar_variante(variantes_por_producto[pkey], stock_memoria)
                if variante and variante["_id"] not in [v["_id"] for v in variantes_elegidas] and stock_memoria[variante["_id"]] > 0:
                    variantes_elegidas.append(variante)
                intentos += 1
            if not variantes_elegidas:
                continue
            hora = random.randint(9, 20)
            minuto = random.randint(0,59)
            segundo = random.randint(0,59)
            fecha_venta = datetime(anio, mes, dia, hora, minuto, segundo)
            venta_id = ObjectId()
            total = 0
            detalles = []
            for variante in variantes_elegidas:
                max_cant = min(stock_memoria[variante["_id"]], random.choices([1,2], weights=[80,20])[0])
                if max_cant <= 0:
                    continue
                detalle = {
                    "_id": ObjectId(),
                    "venta": venta_id,
                    "producto_variedad": variante["_id"],
                    "color": variante["color"],
                    "talla": variante["talla"],
                    "sku": variante["sku"],
                    "cantidad": max_cant,
                    "precio": variante["precio"],
                    "createdAT": fecha_venta,
                    "tenant": ObjectId(TENANT_ID)
                }
                stock_memoria[variante["_id"]] -= max_cant
                total += variante["precio"] * max_cant
                detalles.append(detalle)
            if not detalles:
                continue
            venta = {
                "_id": venta_id,
                "cliente": cliente["_id"],
                "total": total,
                "estado": "Procesado",
                "createdAT": fecha_venta,
                "tenant": ObjectId(TENANT_ID)
            }
            ventas.append(venta)
            venta_detalles.extend(detalles)
            total_ventas += 1
            if total_ventas % 500 == 0:
                print(f"- {total_ventas} ventas simuladas...")

            if total_ventas >= META_VENTAS:
                break
        if total_ventas >= META_VENTAS:
            break

    print(f"\n{total_ventas} ventas simuladas. Insertando en la base de datos...")

    if ventas:
        db[COL_VENTAS].insert_many(ventas)
        db[COL_DETALLES].insert_many(venta_detalles)
        print(f"✓ {len(ventas)} ventas y {len(venta_detalles)} detalles insertados para el tenant.")
    else:
        print("No se generaron ventas.")

    ventas_por_mes_final = {}
    for venta in ventas:
        key = venta["createdAT"].strftime("%Y-%m")
        ventas_por_mes_final[key] = ventas_por_mes_final.get(key, 0) + 1
    print("\nVentas por mes:")
    for k, v in sorted(ventas_por_mes_final.items()):
        print(f"  {k}: {v} ventas")

    print("\n¡Simulación completada para el tenant seleccionado!")

if __name__ == "__main__":
    main()