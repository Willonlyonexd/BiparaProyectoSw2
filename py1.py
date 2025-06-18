import pymongo
from bson import ObjectId
from datetime import datetime

# Conexión a la base de datos
uri = "mongodb://localhost:27017/EcommerTenants?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client["EcommerTenants"]

# 1. Crear un tenant (ajustado a tu schema)
tenant_data = {
    "nombreTienda": "Tienda Arias",
    "suscripcion": "Premium",
    "estado": True,
    "subdominio": "TiendaArias",
    "createdAT": datetime.utcnow(),
}
tenant_result = db.tenants.insert_one(tenant_data)  # Colección: tenants (plural)
tenant_id = tenant_result.inserted_id

print(f"Tenant creado: {tenant_data['nombreTienda']} con _id: {tenant_id}")

# 2. Crear almacenes asociados al tenant
almacens = [
    {
        "nombre": "Almacén Central",
        "direccion": "Calle 1 #123, Lima",
        "tenant": tenant_id
    },
    {
        "nombre": "Almacén Secundario",
        "direccion": "Calle 2 #456, Lima",
        "tenant": tenant_id
    }
]
db.almacens.insert_many(almacens)  # Colección: almacens (plural)
print(f"Se insertaron {len(almacens)} almacenes para el tenant {tenant_id}")

# 3. Crear proveedores asociados al tenant
proveedors = [
    {
        "nombre": "Totto",
        "direccion": "Av. Proveedores 456, Lima",
        "tenant": tenant_id
    },
    {
        "nombre": "BR Calzados",
        "direccion": "Jr. Comerciantes 789, Lima",
        "tenant": tenant_id
    }
]
db.proveedors.insert_many(proveedors)  # Colección: proveedors (plural)
print(f"Se insertaron {len(proveedors)} proveedores para el tenant {tenant_id}")

print("¡Script finalizado correctamente!")