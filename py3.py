import pymongo
import random
import uuid
from datetime import datetime, timedelta
from slugify import slugify
from bson.objectid import ObjectId

uri = "mongodb://localhost:27017/EcommerTenants?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client["EcommerTenants"]

# ID del tenant
TENANT_ID = ObjectId("6852dbf5c4a6f8d1a81074f6")

# Fecha de referencia
fecha_base = datetime(2025, 4, 17, 1, 13, 17)

# Listas de datos para generación
titulos_por_categoria = {
    "Maletas y Mochilas M": ["Mochila Explorer", "Maleta Viajera", "Mochila Urbana", "Morral Universitario", "Riñonera Deportiva"],
    "Maletas y Mochilas F": ["Mochila Lifestyle", "Maleta Weekend", "Mochila Fashion", "Morral Elegance", "Riñonera Mini"],
    "Maletas y Mochilas (niño)": ["Mochila Escolar Hero", "Lonchera Space", "Mochila Junior"],
    "Maletas y Mochilas (niña)": ["Mochila Escolar Princess", "Lonchera Unicorn", "Mochila Junior Pink"],
    "Accesorios M": ["Billetera Classic", "Neceser Voyage", "Estuche Tech", "Portadocumentos Ejecutivo"],
    "Accesorios F": ["Billetera Slim", "Neceser Beauty", "Estuche Glam", "Bolso de Mano Evening"],
    "Accesorios (niño)": ["Cartuchera Adventure", "Estuche Triple", "Lonchera Hero"],
    "Accesorios (niña)": ["Cartuchera Dream", "Estuche Triple Stars", "Lonchera Princess"],
    "Ropa M": ["Camiseta Logo", "Pantalón Cargo", "Chaqueta Urban", "Sudadera College"],
    "Ropa F": ["Camiseta Fit", "Pantalón Slim", "Chaqueta City", "Sudadera Comfort"],
    "Ropa (niño)": ["Camiseta Fun", "Pantalón Play", "Chaqueta Junior"],
    "Ropa (niña)": ["Camiseta Princess", "Pantalón Sweet", "Chaqueta Junior Girl"],
    "Calzado M": ["Zapatillas City", "Tenis Runner", "Sandalias Beach", "Botas Explorer"],
    "Calzado F": ["Zapatillas City Fit", "Tenis Jogging", "Sandalias Summer", "Botas Urban"],
    "Calzado (niño)": ["Zapatillas Junior", "Tenis Sport Kid", "Sandalias Fun"],
    "Calzado (niña)": ["Zapatillas Sweet", "Tenis Sport Girl", "Sandalias Summer Kid"],
    "Tecnología M": ["Audífonos Pro", "Cargador Rápido", "Powerbank 10000", "Case Phone"],
    "Tecnología F": ["Audífonos Slim", "Cargador Color", "Powerbank Compact", "Case Phone Fashion"],
    "Tecnología (niño)": ["Audífonos Kid", "Case Phone Fun", "Gadget Junior"],
    "Tecnología (niña)": ["Audífonos Girl", "Case Phone Cute", "Gadget Sweet"],
    "Colecciones Especiales M": ["Mochila Premium", "Set Eco-friendly", "Kit Edición Limitada"],
    "Colecciones Especiales F": ["Mochila Premium Gold", "Set Eco-friendly Plus", "Kit Edición Limitada Fashion"],
    "Colecciones Especiales (niño)": ["Mochila Personajes", "Set Colección Infantil"],
    "Colecciones Especiales (niña)": ["Mochila Personajes Girl", "Set Colección Sweet"]
}

descripciones = [
    "Diseño ergonómico y resistente, ideal para uso diario. Con compartimentos organizados para satisfacer todas tus necesidades.",
    "Material duradero y tecnología avanzada. Combina funcionalidad y estilo para acompañarte en todas tus actividades.",
    "Fabricado con los mejores materiales, ofrece comodidad y espacio. Su diseño único refleja tu personalidad.",
    "Calidad premium y estilo contemporáneo. La combinación perfecta de practicidad y tendencia actual.",
    "Innovación y diseño de vanguardia. Un producto que destaca por su durabilidad y detalles cuidadosamente seleccionados.",
    "Funcionalidad excepcional con detalles prácticos. La opción ideal para quienes valoran la calidad y el diseño.",
    "Línea exclusiva con los más altos estándares de calidad. Un producto indispensable para tu día a día.",
    "Diseño minimalista pero funcional. Perfecto para quienes buscan simplicidad sin renunciar al estilo.",
    "Elaborado con tecnología de punta y materiales sostenibles. Un producto que cuida de ti y del medio ambiente."
]

etiquetas = ["Nuevo", "Oferta", "Destacado", "Edición Limitada", "Exclusivo"]

colores = {
    "Negro": "#000000",
    "Blanco": "#FFFFFF",
    "Azul": "#0000FF",
    "Rojo": "#FF0000",
    "Verde": "#008000",
    "Amarillo": "#FFFF00",
    "Rosado": "#FFC0CB",
    "Morado": "#800080",
    "Gris": "#808080",
    "Naranja": "#FFA500",
    "Café": "#A52A2A",
    "Azul Marino": "#000080"
}

tallas_ropa = ["XS", "S", "M", "L", "XL", "XXL"]
tallas_calzado = ["35", "36", "37", "38", "39", "40", "41", "42", "43", "44"]
tallas_accesorios = ["Único"]

abreviaturas_categorias = {
    "Maletas y Mochilas M": "MMM",
    "Maletas y Mochilas F": "MMF", 
    "Maletas y Mochilas (niño)": "MMN",
    "Maletas y Mochilas (niña)": "MMNI",
    "Accesorios M": "ACM",
    "Accesorios F": "ACF",
    "Accesorios (niño)": "ACN",
    "Accesorios (niña)": "ACNI",
    "Ropa M": "RPM",
    "Ropa F": "RPF",
    "Ropa (niño)": "RPN",
    "Ropa (niña)": "RPNI",
    "Calzado M": "CAM",
    "Calzado F": "CAF",
    "Calzado (niño)": "CAN",
    "Calzado (niña)": "CANI",
    "Tecnología M": "TEC",
    "Tecnología F": "TECF",
    "Tecnología (niño)": "TECN",
    "Tecnología (niña)": "TECNI",
    "Colecciones Especiales M": "CEM",
    "Colecciones Especiales F": "CEF",
    "Colecciones Especiales (niño)": "CEN",
    "Colecciones Especiales (niña)": "CENI"
}

abreviaturas_subcategorias = {
    "Maletas de Viaje": "MAL",
    "Mochilas Escolares": "MOE",
    "Mochilas para Portátil": "MOP",
    "Mochilas Urbanas": "MOU",
    "Bolsos Deportivos": "BOD",
    "Riñoneras": "RIN",
    "Mochilas para Niños": "MON",
    "Loncheras": "LON",
    "Billeteras": "BIL",
    "Estuches": "EST",
    "Portadocumentos": "POR",
    "Neceseres": "NEC",
    "Bolsos de Mano": "BOM",
    "Cartucheras": "CAR",
    "Camisetas": "CAM",
    "Pantalones": "PAN",
    "Chaquetas": "CHA",
    "Sudaderas": "SUD",
    "Gorras y Sombreros": "GOR",
    "Ropa Deportiva": "ROD",
    "Ropa Interior": "ROI",
    "Zapatillas Casual": "ZAC",
    "Zapatillas Deportivas": "ZAD",
    "Sandalias": "SAN",
    "Botas": "BOT",
    "Audífonos": "AUD",
    "Cargadores": "CAR",
    "Powerbanks": "POW",
    "Accesorios para Celular": "ACC",
    "Gadgets": "GAD",
    "Gadgets Infantiles": "GAI",
    "Eco-friendly": "ECO",
    "Colecciones Limitadas": "COL",
    "Premium": "PRE",
    "Personajes": "PER",
    "Colecciones Infantiles": "COI"
}

abreviaturas_colores = {
    "Negro": "NEG",
    "Blanco": "BLA",
    "Azul": "AZU",
    "Rojo": "ROJ",
    "Verde": "VER",
    "Amarillo": "AMA",
    "Rosado": "ROS",
    "Morado": "MOR",
    "Gris": "GRI",
    "Naranja": "NAR",
    "Café": "CAF",
    "Azul Marino": "AZM"
}

def obtener_tallas_por_categoria(categoria_titulo):
    if "Ropa" in categoria_titulo:
        return tallas_ropa
    elif "Calzado" in categoria_titulo:
        return tallas_calzado
    else:
        return tallas_accesorios

def generar_nombre_imagen():
    return f"{uuid.uuid4()}.jpg"

def obtener_genero_de_categoria(categoria_titulo):
    if "M" in categoria_titulo and not any(x in categoria_titulo for x in ["(niño)", "(niña)"]):
        return "Masculino"
    elif "F" in categoria_titulo and not any(x in categoria_titulo for x in ["(niño)", "(niña)"]):
        return "Femenino"
    elif "(niño)" in categoria_titulo:
        return "Niños"
    elif "(niña)" in categoria_titulo:
        return "Niñas"
    else:
        return random.choice(["Masculino", "Femenino", "Niños", "Niñas"])

def generar_sku(categoria_titulo, subcategoria, color, talla, indice):
    num_indice = str(indice).zfill(2)
    abr_cat = abreviaturas_categorias.get(categoria_titulo, "GEN")[:3]
    abr_subcat = abreviaturas_subcategorias.get(subcategoria, "SUB")[:3]
    abr_color = abreviaturas_colores.get(color, "GEN")[:3]
    letra_talla = talla[0] if len(talla) > 0 else "U"
    num_aleatorio = str(random.randint(0, 99)).zfill(2)
    return f"{num_indice}{abr_cat}{abr_subcat}{abr_color}{letra_talla}{num_aleatorio}"

def generar_productos_normalizados(cantidad=50):
    productos_docs = []
    variedades_docs = []
    galerias_docs = []
    categorias = list(db.categorias.find({"tenant": TENANT_ID}))
    if not categorias:
        print("¡Error! No se encontraron categorías en la base de datos para este tenant.")
        return [], [], []
    print(f"Se encontraron {len(categorias)} categorías en la base de datos para este tenant.")
    indice_producto = 1
    for _ in range(cantidad):
        categoria = random.choice(categorias)
        categoria_id = categoria["_id"]
        categoria_titulo = categoria["titulo"]
        if not categoria.get("subcategorias") or len(categoria["subcategorias"]) == 0:
            print(f"¡Advertencia! La categoría '{categoria_titulo}' no tiene subcategorías.")
            continue
        subcategoria = random.choice(categoria["subcategorias"])
        if categoria_titulo not in titulos_por_categoria:
            titulo_base = "Producto"
        else:
            posibles_titulos = titulos_por_categoria[categoria_titulo]
            titulo_base = random.choice(posibles_titulos)
        titulo = f"{titulo_base} {random.choice(['Pro', 'Plus', 'Max', 'Lite', 'Premium', '2.0'])} {random.randint(100, 999)}"
        slug = slugify(titulo)
        clasificacion = obtener_genero_de_categoria(categoria_titulo)
        descripcion = random.choice(descripciones)
        etiqueta = random.choice(etiquetas)
        num_labels = random.randint(1, 5)
        labels = [f"etiqueta_{i+1}" for i in range(num_labels)]
        portada = generar_nombre_imagen()
        minutos_variacion = random.randint(-120, 120)
        fecha_creacion = fecha_base + timedelta(minutes=minutos_variacion)
        estado = random.choices([True, False], weights=[0.7, 0.3])[0]
        producto_id = ObjectId()
        producto = {
            "_id": producto_id,
            "titulo": titulo,
            "portada": portada,
            "slug": slug,
            "descripcion": descripcion,
            "etiqueta": etiqueta,
            "clasificacion": clasificacion,
            "categoria": categoria_id,
            "subcategorias": subcategoria,
            "labels": labels,
            "estado": estado,
            "createdAT": fecha_creacion,
            "tenant": TENANT_ID,
            "__v": 0
        }
        productos_docs.append(producto)
        num_colores = random.randint(1, 5)
        colores_seleccionados = random.sample(list(colores.items()), num_colores)
        tallas_disponibles = obtener_tallas_por_categoria(categoria_titulo)
        for nombre_color, codigo_color in colores_seleccionados:
            num_tallas = random.randint(1, len(tallas_disponibles))
            tallas_color = random.sample(tallas_disponibles, num_tallas)
            for talla in tallas_color:
                sku = generar_sku(categoria_titulo, subcategoria, nombre_color, talla, indice_producto)
                variedad = {
                    "_id": ObjectId(),
                    "hxd": codigo_color,
                    "color": nombre_color,
                    "talla": talla,
                    "sku": sku,
                    "cantidad": 0,
                    "precio": 0,
                    "producto": producto_id,
                    "tenant": TENANT_ID,
                    "createdAT": fecha_creacion,
                    "__v": 0
                }
                variedades_docs.append(variedad)
        num_imagenes = random.randint(1, 5)
        for i in range(num_imagenes):
            imagen_nombre = generar_nombre_imagen()
            galeria = {
                "_id": ObjectId(),
                "titulo": f"Imagen {i+1} de {titulo}",
                "imagen": imagen_nombre,
                "producto": producto_id,
                "tenant": TENANT_ID,
                "createdAT": fecha_creacion,
                "__v": 0
            }
            galerias_docs.append(galeria)
        indice_producto += 1
    return productos_docs, variedades_docs, galerias_docs

def insertar_productos_normalizados(productos_docs, variedades_docs, galerias_docs):
    if not productos_docs:
        print("No hay productos para insertar.")
        return
    try:
        if productos_docs:
            resultado = db.productos.insert_many(productos_docs)
            print(f"Se insertaron {len(resultado.inserted_ids)} productos.")
        if variedades_docs:
            resultado = db.producto_variedads.insert_many(variedades_docs)
            print(f"Se insertaron {len(resultado.inserted_ids)} variedades.")
        if galerias_docs:
            resultado = db.producto_galerias.insert_many(galerias_docs)
            print(f"Se insertaron {len(resultado.inserted_ids)} imágenes de galería.")
    except Exception as e:
        print(f"¡Error al insertar datos! {str(e)}")

def mostrar_estadisticas(productos_docs, variedades_docs, galerias_docs):
    total_productos = len(productos_docs)
    productos_publicados = sum(1 for p in productos_docs if p["estado"])
    productos_borrador = total_productos - productos_publicados
    print(f"\n=== ESTADÍSTICAS DE GENERACIÓN ===")
    print(f"Total de productos: {total_productos}")
    print(f"- Productos publicados: {productos_publicados}")
    print(f"- Productos en borrador: {productos_borrador}")
    print(f"Total de variedades: {len(variedades_docs)}")
    print(f"Total de imágenes de galería: {len(galerias_docs)}")
    if total_productos > 0:
        print(f"Promedio de variedades por producto: {len(variedades_docs) / total_productos:.2f}")
        print(f"Promedio de imágenes por producto: {len(galerias_docs) / total_productos:.2f}")

if __name__ == "__main__":
    try:
        cantidad = int(input("¿Cuántos productos deseas generar? "))
    except ValueError:
        cantidad = 50
        print(f"Entrada inválida, se generarán {cantidad} productos por defecto.")
    print(f"Generando {cantidad} productos con sus variedades e imágenes...")
    productos_docs, variedades_docs, galerias_docs = generar_productos_normalizados(cantidad)
    if not productos_docs:
        print("No se pudieron generar productos. Verifica la configuración de la base de datos.")
        exit(1)
    mostrar_estadisticas(productos_docs, variedades_docs, galerias_docs)
    respuesta = input("¿Deseas insertar estos datos en la base de datos? (s/n): ").lower()
    if respuesta == 's' or respuesta == 'si':
        print("Insertando datos en la base de datos...")
        insertar_productos_normalizados(productos_docs, variedades_docs, galerias_docs)
        print("Operación completada.")
    else:
        print("Operación cancelada.")