import pymongo
from datetime import datetime

# Detalles de conexión
uri = "mongodb://localhost:27017/EcommerTenants?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client["EcommerTenants"]

# Obtener la colección
coleccion = db["producto_variedads"]

# Encontrar todos los documentos con cantidad negativa y actualizarlos
resultado = coleccion.update_many(
    {"cantidad": {"$lt": 0}},  # Filtro para cantidades negativas
    {"$set": {"cantidad": 0}}  # Establecer cantidad a 0
)

# Imprimir los resultados
print(f"Se encontraron {resultado.matched_count} documentos con cantidades negativas")
print(f"Se actualizaron {resultado.modified_count} documentos")

# Registrar la operación con fecha y usuario
print(f"Operación realizada el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Usuario: Willonlyonexd")

# Cerrar la conexión
client.close()