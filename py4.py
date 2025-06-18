import pymongo
import random
import string
import bcrypt
from datetime import datetime, timedelta
from bson.objectid import ObjectId

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["EcommerTenants"]

TENANT_ID = ObjectId("6852dbf5c4a6f8d1a81074f6")

nombres_masculinos = [
    "Juan", "Carlos", "Roberto", "Miguel", "Pedro", "José", "David", "Daniel", "Alejandro",
    "Fernando", "Luis", "Jorge", "Andrés", "Rafael", "Francisco", "Gabriel", "Javier",
    "Antonio", "Sergio", "Manuel", "Oscar", "Enrique", "Martín", "Eduardo", "Ricardo",
    "Raúl", "Hugo", "Gonzalo", "Diego", "Arturo", "Mario", "Víctor", "Julio", "César",
    "Alfredo", "Alberto", "Ernesto", "Pablo", "Marcos", "Salvador", "Rubén", "Armando"
]

nombres_femeninos = [
    "María", "Ana", "Laura", "Sofía", "Carmen", "Patricia", "Isabel", "Luisa", "Gabriela",
    "Rosa", "Martha", "Daniela", "Claudia", "Mónica", "Silvia", "Elena", "Adriana", "Diana",
    "Julia", "Beatriz", "Valeria", "Natalia", "Teresa", "Susana", "Carolina", "Victoria",
    "Alicia", "Pilar", "Mariana", "Cristina", "Lucía", "Alejandra", "Verónica", "Leticia",
    "Juana", "Antonia", "Fernanda", "Guadalupe", "Cecilia", "Lourdes", "Catalina", "Camila"
]

apellidos = [
    "García", "Rodríguez", "González", "Fernández", "López", "Martínez", "Sánchez", "Pérez",
    "Gómez", "Martín", "Jiménez", "Ruiz", "Hernández", "Díaz", "Moreno", "Muñoz", "Álvarez",
    "Romero", "Alonso", "Gutiérrez", "Navarro", "Torres", "Domínguez", "Vázquez", "Ramos",
    "Gil", "Ramírez", "Serrano", "Blanco", "Molina", "Morales", "Suárez", "Ortega", "Delgado",
    "Castro", "Ortiz", "Rubio", "Marín", "Sanz", "Núñez", "Iglesias", "Medina", "Garrido",
    "Cortés", "Castillo", "Santos", "Lozano", "Guerrero", "Cano", "Prieto", "Méndez",
    "Cruz", "Calvo", "Gallego", "Vidal", "León", "Márquez", "Herrera", "Peña", "Flores",
    "Cabrera", "Campos", "Vega", "Fuentes", "Carrasco", "Díez", "Caballero", "Reyes",
    "Nieto", "Pascual", "Herrero", "Santana", "Lorenzo", "Montero", "Hidalgo", "Giménez",
    "Ibáñez", "Ferrer", "Duran", "Vicente", "Benítez", "Mora", "Santiago", "Arias",
    "Vargas", "Carmona", "Crespo", "Román", "Pastor", "Soto", "Sáez", "Velasco", "Soler",
    "Moya", "Esteban", "Parra", "Bravo", "Gallardo", "Rojas"
]

dominios = [
    "gmail.com", "hotmail.com", "outlook.com", "yahoo.com", "icloud.com", 
    "protonmail.com", "live.com", "aol.com", "zoho.com", "mail.com"
]

def generar_password_hash(longitud=5):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(caracteres) for _ in range(longitud))
    salt = bcrypt.gensalt(10)
    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password.decode('utf-8')

def generar_email(nombre, apellido):
    nombre = nombre.lower()
    apellido = apellido.lower()
    formato = random.randint(1, 8)
    dominio = random.choice(dominios)
    if formato == 1:
        return f"{nombre}.{apellido}@{dominio}"
    elif formato == 2:
        return f"{nombre}{random.randint(1, 999)}@{dominio}"
    elif formato == 3:
        return f"{nombre[0]}{apellido}@{dominio}"
    elif formato == 4:
        return f"{apellido}.{nombre}@{dominio}"
    elif formato == 5:
        return f"{apellido}{nombre[0]}@{dominio}"
    elif formato == 6:
        return f"{nombre}_{apellido}@{dominio}"
    elif formato == 7:
        año = random.randint(70, 99)
        return f"{nombre}{apellido}{año}@{dominio}"
    else:
        return f"{nombre}{apellido}{random.randint(1, 999)}@{dominio}"

def generar_fechas_rango(cantidad_total):
    fecha_inicio = datetime(2024, 6, 15)
    fecha_fin = datetime(2025, 6, 1)
    dias_totales = (fecha_fin - fecha_inicio).days + 1

    eventos_especiales = [
        (29, 11, 2024, "Black Friday", 0.40),
        (2, 12, 2024, "Cyber Monday", 0.20),
        (6, 1, 2025, "Día de Reyes", 0.10),
        (14, 2, 2025, "San Valentín", 0.10),
        (3, 3, 2025, "Lunes de Carnaval", 0.10),
        (4, 3, 2025, "Martes de Carnaval", 0.05),
    ]
    proporcion_eventos = sum(e[-1] for e in eventos_especiales)
    cantidad_eventos = int(cantidad_total * proporcion_eventos)
    cantidad_restante = cantidad_total - cantidad_eventos

    fechas_eventos = []
    for dia, mes, año, nombre, proporcion in eventos_especiales:
        n_evento = int(cantidad_total * proporcion)
        for _ in range(n_evento):
            hora_rand = random.random()
            if hora_rand < 0.05:
                hora = random.randint(0, 7)
            elif hora_rand < 0.25:
                hora = random.randint(8, 11)
            elif hora_rand < 0.55:
                hora = random.randint(12, 17)
            else:
                hora = random.randint(18, 23)
            minuto = random.randint(0, 59)
            segundo = random.randint(0, 59)
            fecha = datetime(año, mes, dia, hora, minuto, segundo)
            if fecha_inicio <= fecha <= fecha_fin:
                fechas_eventos.append(fecha)

    fechas_restantes = []
    for _ in range(cantidad_restante):
        dias_offset = random.randint(0, dias_totales - 1)
        fecha = fecha_inicio + timedelta(days=dias_offset)
        hora_rand = random.random()
        if hora_rand < 0.05:
            hora = random.randint(0, 7)
        elif hora_rand < 0.25:
            hora = random.randint(8, 11)
        elif hora_rand < 0.55:
            hora = random.randint(12, 17)
        else:
            hora = random.randint(18, 23)
        minuto = random.randint(0, 59)
        segundo = random.randint(0, 59)
        fecha_fin_hora = fecha.replace(hour=hora, minute=minuto, second=segundo)
        fechas_restantes.append(fecha_fin_hora)

    fechas_total = fechas_eventos + fechas_restantes
    fechas_total.sort()
    return fechas_total[:cantidad_total]

def generar_clientes(cantidad=50):
    clientes = []
    fechas_creacion = generar_fechas_rango(cantidad)
    for i in range(cantidad):
        genero = random.choice(["M", "F"])
        if genero == "M":
            num_nombres = min(random.randint(1, 2), len(nombres_masculinos))
            lista_nombres = random.sample(nombres_masculinos, num_nombres)
            nombres = " ".join(lista_nombres)
        else:
            num_nombres = min(random.randint(1, 2), len(nombres_femeninos))
            lista_nombres = random.sample(nombres_femeninos, num_nombres)
            nombres = " ".join(lista_nombres)
        num_apellidos = min(random.randint(1, 2), len(apellidos))
        lista_apellidos = random.sample(apellidos, num_apellidos)
        apellidos_cliente = " ".join(lista_apellidos)
        email = generar_email(lista_nombres[0], lista_apellidos[0])
        password_hash = generar_password_hash()
        fullname = f"{nombres} {apellidos_cliente}"
        fecha_creacion = fechas_creacion[i]
        email_validacion = random.choices([True, False], weights=[0.9, 0.1])[0]
        estado = random.choices([True, False], weights=[0.95, 0.05])[0]
        cliente = {
            "_id": ObjectId(),
            "nombres": nombres,
            "apellidos": apellidos_cliente,
            "email": email,
            "email_validacion": email_validacion,
            "password": password_hash,
            "estado": estado,
            "fullname": fullname,
            "createdAT": fecha_creacion,
            "tenant": TENANT_ID,
            "__v": 0
        }
        clientes.append(cliente)
    return clientes

def insertar_clientes(clientes):
    if not clientes:
        print("No hay clientes para insertar.")
        return
    try:
        resultado = db.clientes.insert_many(clientes)
        print(f"Se insertaron {len(resultado.inserted_ids)} clientes correctamente.")
    except Exception as e:
        print(f"Error al insertar clientes: {str(e)}")

def mostrar_estadisticas(clientes):
    total = len(clientes)
    validados = sum(1 for c in clientes if c["email_validacion"])
    activos = sum(1 for c in clientes if c["estado"])
    print("\n=== ESTADÍSTICAS DE CLIENTES GENERADOS ===")
    print(f"Total de clientes: {total}")
    print(f"Clientes con email validado: {validados} ({validados/total*100:.1f}%)")
    print(f"Clientes activos: {activos} ({activos/total*100:.1f}%)")
    meses = {}
    for cliente in clientes:
        mes = cliente["createdAT"].strftime("%Y-%m")
        if mes not in meses:
            meses[mes] = 0
        meses[mes] += 1
    print("\nDistribución por fecha de registro:")
    for mes, cantidad in sorted(meses.items()):
        print(f"  {mes}: {cantidad} clientes ({cantidad/total*100:.1f}%)")
    eventos = {
        "Black Friday (29/11/2024)": 0,
        "Cyber Monday (02/12/2024)": 0,
        "Día de Reyes (06/01/2025)": 0,
        "San Valentín (14/02/2025)": 0,
        "Carnaval (03-04/03/2025)": 0
    }
    for cliente in clientes:
        fecha = cliente["createdAT"]
        if fecha.day == 29 and fecha.month == 11 and fecha.year == 2024:
            eventos["Black Friday (29/11/2024)"] += 1
        elif fecha.day == 2 and fecha.month == 12 and fecha.year == 2024:
            eventos["Cyber Monday (02/12/2024)"] += 1
        elif fecha.day == 6 and fecha.month == 1 and fecha.year == 2025:
            eventos["Día de Reyes (06/01/2025)"] += 1
        elif fecha.day == 14 and fecha.month == 2 and fecha.year == 2025:
            eventos["San Valentín (14/02/2025)"] += 1
        elif (fecha.day in [3, 4]) and fecha.month == 3 and fecha.year == 2025:
            eventos["Carnaval (03-04/03/2025)"] += 1
    print("\nDistribución por eventos específicos:")
    for evento, cantidad in eventos.items():
        if cantidad > 0:
            print(f"  {evento}: {cantidad} clientes")

if __name__ == "__main__":
    try:
        cantidad = int(input("¿Cuántos clientes deseas generar? "))
    except ValueError:
        cantidad = 50
        print(f"Entrada inválida, se generarán {cantidad} clientes por defecto.")
    print(f"Generando {cantidad} clientes ficticios entre 15/06/2024 y 01/06/2025...")
    clientes = generar_clientes(cantidad)
    mostrar_estadisticas(clientes)
    respuesta = input("\n¿Deseas insertar estos clientes en la base de datos? (s/n): ").lower()
    if respuesta == 's' or respuesta == 'si':
        insertar_clientes(clientes)
        print("Operación completada.")
    else:
        print("Operación cancelada.")