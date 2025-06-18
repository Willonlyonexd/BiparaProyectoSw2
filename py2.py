import pymongo
from bson import ObjectId
from datetime import datetime
import json

uri = "mongodb://localhost:27017/EcommerTenants?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client["EcommerTenants"]

# ID del tenant al que asociarás las categorías
TENANT_ID = ObjectId("6852dbf5c4a6f8d1a81074f6")

# Fecha actual actualizada
current_date = datetime(2025, 4, 17, 23, 12, 34)

print("Script de inserción de categorías ejecutándose...")
print(f"Usuario: muimui69")
print(f"Fecha: {current_date}")

# Eliminar las categorías existentes del tenant (solo para este tenant)
db.categorias.delete_many({"tenant": TENANT_ID})
print("Categorías anteriores eliminadas para tenant:", TENANT_ID)

# Helper para añadir tenant a cada categoría
def with_tenant(cat_list):
    for cat in cat_list:
        cat["tenant"] = TENANT_ID
    return cat_list

# Categorías de Maletas y Mochilas
categorias_maletas = with_tenant([
    {
        "titulo": "Maletas y Mochilas M",
        "slug": "maletas-y-mochilas-m",
        "genero": "Masculino",
        "subcategorias": [
            "Maletas de Viaje",
            "Mochilas Escolares",
            "Mochilas para Portátil",
            "Mochilas Urbanas",
            "Bolsos Deportivos",
            "Riñoneras"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Maletas y Mochilas F",
        "slug": "maletas-y-mochilas-f",
        "genero": "Femenino",
        "subcategorias": [
            "Maletas de Viaje",
            "Mochilas Escolares",
            "Mochilas para Portátil",
            "Mochilas Urbanas",
            "Bolsos Deportivos",
            "Riñoneras"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Maletas y Mochilas (niño)",
        "slug": "maletas-y-mochilas-nino",
        "genero": "Niños",
        "subcategorias": [
            "Mochilas Escolares",
            "Mochilas para Niños",
            "Loncheras"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Maletas y Mochilas (niña)",
        "slug": "maletas-y-mochilas-nina",
        "genero": "Niñas",
        "subcategorias": [
            "Mochilas Escolares",
            "Mochilas para Niños",
            "Loncheras"
        ],
        "estado": True,
        "createdAT": current_date
    }
])

db.categorias.insert_many(categorias_maletas)
print("Categorías de Maletas y Mochilas insertadas.")

# Categorías de Accesorios
categorias_accesorios = with_tenant([
    {
        "titulo": "Accesorios M",
        "slug": "accesorios-m",
        "genero": "Masculino",
        "subcategorias": [
            "Billeteras",
            "Estuches",
            "Portadocumentos",
            "Neceseres"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Accesorios F",
        "slug": "accesorios-f",
        "genero": "Femenino",
        "subcategorias": [
            "Billeteras",
            "Estuches",
            "Bolsos de Mano",
            "Neceseres"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Accesorios (niño)",
        "slug": "accesorios-nino",
        "genero": "Niños",
        "subcategorias": [
            "Estuches",
            "Loncheras",
            "Cartucheras"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Accesorios (niña)",
        "slug": "accesorios-nina",
        "genero": "Niñas",
        "subcategorias": [
            "Estuches",
            "Loncheras",
            "Cartucheras"
        ],
        "estado": True,
        "createdAT": current_date
    }
])

db.categorias.insert_many(categorias_accesorios)
print("Categorías de Accesorios insertadas.")

# Categorías de Ropa
categorias_ropa = with_tenant([
    {
        "titulo": "Ropa M",
        "slug": "ropa-m",
        "genero": "Masculino",
        "subcategorias": [
            "Camisetas", 
            "Pantalones", 
            "Chaquetas", 
            "Sudaderas", 
            "Gorras y Sombreros", 
            "Ropa Deportiva", 
            "Ropa Interior"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Ropa F",
        "slug": "ropa-f",
        "genero": "Femenino",
        "subcategorias": [
            "Camisetas", 
            "Pantalones", 
            "Chaquetas", 
            "Sudaderas", 
            "Gorras y Sombreros", 
            "Ropa Deportiva", 
            "Ropa Interior"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Ropa (niño)",
        "slug": "ropa-nino",
        "genero": "Niños",
        "subcategorias": [
            "Camisetas", 
            "Pantalones", 
            "Chaquetas", 
            "Sudaderas", 
            "Gorras y Sombreros"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Ropa (niña)",
        "slug": "ropa-nina",
        "genero": "Niñas",
        "subcategorias": [
            "Camisetas", 
            "Pantalones", 
            "Chaquetas", 
            "Sudaderas", 
            "Gorras y Sombreros"
        ],
        "estado": True,
        "createdAT": current_date
    }
])

db.categorias.insert_many(categorias_ropa)
print("Categorías de Ropa insertadas.")

# Categorías de Calzado
categorias_calzado = with_tenant([
    {
        "titulo": "Calzado M",
        "slug": "calzado-m",
        "genero": "Masculino",
        "subcategorias": [
            "Zapatillas Casual", 
            "Zapatillas Deportivas", 
            "Sandalias", 
            "Botas"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Calzado F",
        "slug": "calzado-f",
        "genero": "Femenino",
        "subcategorias": [
            "Zapatillas Casual", 
            "Zapatillas Deportivas", 
            "Sandalias", 
            "Botas"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Calzado (niño)",
        "slug": "calzado-nino",
        "genero": "Niños",
        "subcategorias": [
            "Zapatillas Casual", 
            "Zapatillas Deportivas", 
            "Sandalias", 
            "Botas"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Calzado (niña)",
        "slug": "calzado-nina",
        "genero": "Niñas",
        "subcategorias": [
            "Zapatillas Casual", 
            "Zapatillas Deportivas", 
            "Sandalias", 
            "Botas"
        ],
        "estado": True,
        "createdAT": current_date
    }
])

db.categorias.insert_many(categorias_calzado)
print("Categorías de Calzado insertadas.")

# Categorías de Tecnología
categorias_tecnologia = with_tenant([
    {
        "titulo": "Tecnología M",
        "slug": "tecnologia-m",
        "genero": "Masculino",
        "subcategorias": [
            "Audífonos", 
            "Cargadores", 
            "Powerbanks", 
            "Accesorios para Celular", 
            "Gadgets"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Tecnología F",
        "slug": "tecnologia-f",
        "genero": "Femenino",
        "subcategorias": [
            "Audífonos", 
            "Cargadores", 
            "Powerbanks", 
            "Accesorios para Celular", 
            "Gadgets"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Tecnología (niño)",
        "slug": "tecnologia-nino",
        "genero": "Niños",
        "subcategorias": [
            "Audífonos", 
            "Accesorios para Celular", 
            "Gadgets Infantiles"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Tecnología (niña)",
        "slug": "tecnologia-nina",
        "genero": "Niñas",
        "subcategorias": [
            "Audífonos", 
            "Accesorios para Celular", 
            "Gadgets Infantiles"
        ],
        "estado": True,
        "createdAT": current_date
    }
])

db.categorias.insert_many(categorias_tecnologia)
print("Categorías de Tecnología insertadas.")

# Categorías de Colecciones Especiales
categorias_especiales = with_tenant([
    {
        "titulo": "Colecciones Especiales M",
        "slug": "colecciones-especiales-m",
        "genero": "Masculino",
        "subcategorias": [
            "Eco-friendly", 
            "Colecciones Limitadas", 
            "Premium"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Colecciones Especiales F",
        "slug": "colecciones-especiales-f",
        "genero": "Femenino",
        "subcategorias": [
            "Eco-friendly", 
            "Colecciones Limitadas", 
            "Premium"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Colecciones Especiales (niño)",
        "slug": "colecciones-especiales-nino",
        "genero": "Niños",
        "subcategorias": [
            "Personajes", 
            "Colecciones Infantiles"
        ],
        "estado": True,
        "createdAT": current_date
    },
    {
        "titulo": "Colecciones Especiales (niña)",
        "slug": "colecciones-especiales-nina",
        "genero": "Niñas",
        "subcategorias": [
            "Personajes", 
            "Colecciones Infantiles"
        ],
        "estado": True,
        "createdAT": current_date
    }
])

db.categorias.insert_many(categorias_especiales)
print("Categorías de Colecciones Especiales insertadas.")

# Obtener y mostrar los IDs de las categorías creadas para el tenant
categorias = list(db.categorias.find({"tenant": TENANT_ID}))
categorias_ids = [str(cat["_id"]) for cat in categorias]

print("\nTodas las categorías han sido insertadas correctamente con subcategorías y tenant.")
print(f"Total de categorías creadas para el tenant: {len(categorias)}")

# Exportar IDs (opcional)
with open("categorias_ids.json", "w") as f:
    json.dump({"categorias_ids": categorias_ids}, f, indent=2)

print("\nIDs de categorías exportados a categorias_ids.json para uso posterior.")