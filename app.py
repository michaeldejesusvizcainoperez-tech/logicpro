from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json

app = Flask(__name__)
app.secret_key = "techstore-secret-2024"

# ─── CATÁLOGO DE PRODUCTOS ───────────────────────────────────────────────────
PRODUCTS = [
    # LAPTOPS
    {
        "id": 1, "category": "Laptops",
        "name": "MacBook Pro 16\" M3 Max",
        "brand": "Apple",
        "price": 3499.99,
        "original_price": 3999.99,
        "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&q=80",
        "rating": 4.9, "reviews": 2341,
        "badge": "Bestseller",
        "stock": 15,
        "description": "El portátil más potente de Apple. Chip M3 Max con CPU de 16 núcleos y GPU de 40 núcleos. Pantalla Liquid Retina XDR de 16,2\" con ProMotion 120Hz. Hasta 128 GB de memoria unificada y 8 TB de SSD ultrarrápido.",
        "specs": {"Procesador": "Apple M3 Max", "RAM": "48 GB", "Almacenamiento": "1 TB SSD", "Pantalla": "16.2\" Liquid Retina XDR", "Batería": "22 horas", "Peso": "2.14 kg", "OS": "macOS Sonoma"},
        "colors": ["Plateado", "Negro espacial"]
    },
    {
        "id": 2, "category": "Laptops",
        "name": "Dell XPS 15 OLED",
        "brand": "Dell",
        "price": 1849.99,
        "original_price": 2199.99,
        "image": "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=600&q=80",
        "rating": 4.7, "reviews": 1120,
        "badge": "Oferta",
        "stock": 8,
        "description": "Diseño ultra delgado con pantalla OLED 3.5K de 15,6\". Intel Core i9-13900H con gráficos NVIDIA RTX 4070. El equilibrio perfecto entre rendimiento profesional y portabilidad.",
        "specs": {"Procesador": "Intel Core i9-13900H", "RAM": "32 GB DDR5", "Almacenamiento": "1 TB NVMe", "Pantalla": "15.6\" OLED 3.5K", "GPU": "NVIDIA RTX 4070 8GB", "Batería": "13 horas", "Peso": "1.86 kg"},
        "colors": ["Platinum Silver"]
    },
    {
        "id": 3, "category": "Laptops",
        "name": "ASUS ROG Zephyrus G16",
        "brand": "ASUS",
        "price": 2299.99,
        "original_price": 2499.99,
        "image": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=600&q=80",
        "rating": 4.8, "reviews": 876,
        "badge": "Gaming",
        "stock": 5,
        "description": "Laptop gaming de élite con pantalla ROG Nebula 2.5K 240Hz. AMD Ryzen 9 7945HX y NVIDIA RTX 4090. Refrigeración líquida MUX Switch para máximo rendimiento en juegos AAA.",
        "specs": {"Procesador": "AMD Ryzen 9 7945HX", "RAM": "32 GB DDR5", "Almacenamiento": "2 TB NVMe RAID", "Pantalla": "16\" ROG Nebula 2.5K 240Hz", "GPU": "NVIDIA RTX 4090 16GB", "Batería": "10 horas", "Peso": "1.95 kg"},
        "colors": ["Eclipse Gray", "Moonlight White"]
    },
    {
        "id": 4, "category": "Laptops",
        "name": "Lenovo ThinkPad X1 Carbon",
        "brand": "Lenovo",
        "price": 1649.99,
        "original_price": 1899.99,
        "image": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=600&q=80",
        "rating": 4.6, "reviews": 654,
        "badge": None,
        "stock": 12,
        "description": "El referente en laptops empresariales. Ultra ligero (1,12 kg), certificado MIL-SPEC, teclado legendario ThinkPad y batería de 15 horas. Ideal para profesionales en movimiento.",
        "specs": {"Procesador": "Intel Core Ultra 7 165U", "RAM": "32 GB LPDDR5", "Almacenamiento": "1 TB SSD", "Pantalla": "14\" IPS 2.8K OLED", "Batería": "15 horas", "Peso": "1.12 kg", "Certificaciones": "MIL-SPEC 810H"},
        "colors": ["Deep Black"]
    },

    # SMARTPHONES
    {
        "id": 5, "category": "Smartphones",
        "name": "iPhone 15 Pro Max",
        "brand": "Apple",
        "price": 1199.99,
        "original_price": 1299.99,
        "image": "https://images.unsplash.com/photo-1696446702183-cbd96701dea3?w=600&q=80",
        "rating": 4.9, "reviews": 8745,
        "badge": "Nuevo",
        "stock": 30,
        "description": "El iPhone más avanzado. Chip A17 Pro de titanio, cámara de 48 MP con zoom periscópico 5x, pantalla Super Retina XDR de 6.7\" con ProMotion 120Hz y Dynamic Island.",
        "specs": {"Procesador": "Apple A17 Pro", "RAM": "8 GB", "Almacenamiento": "256 GB", "Pantalla": "6.7\" Super Retina XDR", "Cámara": "48MP + 12MP + 12MP", "Batería": "4422 mAh", "Material": "Titanio"},
        "colors": ["Titanio Natural", "Titanio Negro", "Titanio Blanco", "Titanio Azul"]
    },
    {
        "id": 6, "category": "Smartphones",
        "name": "Samsung Galaxy S24 Ultra",
        "brand": "Samsung",
        "price": 1299.99,
        "original_price": 1399.99,
        "image": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=600&q=80",
        "rating": 4.8, "reviews": 5230,
        "badge": "S Pen",
        "stock": 20,
        "description": "El smartphone Android definitivo con S Pen integrado. Snapdragon 8 Gen 3, cámara de 200 MP con zoom 100x Space Zoom, pantalla Dynamic AMOLED 2X de 6.8\" y batería de 5000 mAh.",
        "specs": {"Procesador": "Snapdragon 8 Gen 3", "RAM": "12 GB", "Almacenamiento": "256 GB", "Pantalla": "6.8\" Dynamic AMOLED 2X 120Hz", "Cámara": "200MP + 12MP + 10MP + 10MP", "Batería": "5000 mAh", "Extra": "S Pen integrado"},
        "colors": ["Titanium Gray", "Titanium Black", "Titanium Violet", "Titanium Yellow"]
    },
    {
        "id": 7, "category": "Smartphones",
        "name": "Google Pixel 8 Pro",
        "brand": "Google",
        "price": 999.99,
        "original_price": 1099.99,
        "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&q=80",
        "rating": 4.7, "reviews": 2100,
        "badge": "IA",
        "stock": 18,
        "description": "La mejor experiencia de IA en un smartphone. Tensor G3 con funciones exclusivas de Google AI: Magic Eraser, Best Take, Audio Magic Eraser. Cámara Pro con sensor de temperatura.",
        "specs": {"Procesador": "Google Tensor G3", "RAM": "12 GB", "Almacenamiento": "128 GB", "Pantalla": "6.7\" LTPO OLED 120Hz", "Cámara": "50MP + 48MP + 48MP", "Batería": "5050 mAh", "Extra": "7 años de actualizaciones"},
        "colors":["Obsidian", "Porcelain", "Bay", "Mint"]
    },
    {
        "id": 8, "category": "Smartphones",
        "name": "OnePlus 12",
        "brand": "OnePlus",
        "price": 799.99,
        "original_price": 899.99,
        "image": "https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=600&q=80",
        "rating": 4.6, "reviews": 980,
        "badge": "Carga 100W",
        "stock": 25,
        "description": "Velocidad sin compromisos. Snapdragon 8 Gen 3, carga SUPERVOOC de 100W (0-100% en 26 min), cámara Hasselblad de triple lente y pantalla AMOLED 2K 120Hz.",
        "specs": {"Procesador": "Snapdragon 8 Gen 3", "RAM": "16 GB LPDDR5X", "Almacenamiento": "512 GB UFS 4.0", "Pantalla": "6.82\" 2K AMOLED 120Hz", "Cámara": "50MP Hasselblad + 64MP + 48MP", "Batería": "5400 mAh", "Carga": "100W SUPERVOOC"},
        "colors": ["Silky Black", "Flowy Emerald"]
    },

    # AUDÍFONOS
    {
        "id": 9, "category": "Audífonos",
        "name": "Sony WH-1000XM5",
        "brand": "Sony",
        "price": 349.99,
        "original_price": 399.99,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&q=80",
        "rating": 4.9, "reviews": 6700,
        "badge": "ANC #1",
        "stock": 40,
        "description": "El estándar de oro en cancelación de ruido. 8 micrófonos con dos procesadores de sonido, 30 horas de batería, plegable y compatible con Hi-Res Audio. La mejor experiencia de escucha inalámbrica.",
        "specs": {"Tipo": "Over-ear inalámbrico", "ANC": "8 micrófonos dual chip", "Batería": "30 horas (ANC on)", "Drivers": "30 mm", "Conectividad": "Bluetooth 5.2 / aptX HD / LDAC", "Peso": "250 g", "Micrófono": "4 micrófonos beamforming"},
        "colors": ["Negro", "Platino Plateado"]
    },
    {
        "id": 10, "category": "Audífonos",
        "name": "Apple AirPods Pro 2",
        "brand": "Apple",
        "price": 249.99,
        "original_price": 279.99,
        "image": "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=600&q=80",
        "rating": 4.8, "reviews": 12000,
        "badge": "Chip H2",
        "stock": 50,
        "description": "ANC adaptativa de próxima generación con chip H2. Audio espacial personalizado con seguimiento de cabeza, modo Transparencia adaptativa y carga MagSafe. Hasta 30h con el estuche.",
        "specs": {"Tipo": "In-ear TWS", "Chip": "Apple H2", "ANC": "Adaptativa de próxima gen", "Batería": "6h (30h con estuche)", "Audio": "Espacial personalizado", "Resistencia": "IP54", "Carga": "MagSafe / Lightning / Qi"},
        "colors": ["Blanco"]
    },
    {
        "id": 11, "category": "Audífonos",
        "name": "Bose QuietComfort Ultra",
        "brand": "Bose",
        "price": 429.99,
        "original_price": 449.99,
        "image": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=600&q=80",
        "rating": 4.7, "reviews": 3200,
        "badge": "Immersive Audio",
        "stock": 22,
        "description": "Bose Immersive Audio crea una experiencia de sonido envolvente revolucionaria. ANC líder de la industria, 24 horas de batería, diseño plegable ultra cómodo y sonido WorldClass.",
        "specs": {"Tipo": "Over-ear inalámbrico", "ANC": "CustomTune adaptativa", "Batería": "24 horas", "Audio": "Bose Immersive Audio", "Conectividad": "Bluetooth 5.3 / aptX Adaptive", "Peso": "254 g", "Carga": "USB-C (2.5h completa)"},
        "colors": ["Negro", "Moonstone Blue", "White Smoke"]
    },
    {
        "id": 12, "category": "Audífonos",
        "name": "Sennheiser Momentum 4",
        "brand": "Sennheiser",
        "price": 299.99,
        "original_price": 349.99,
        "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600&q=80",
        "rating": 4.6, "reviews": 1540,
        "badge": "60h batería",
        "stock": 17,
        "description": "60 horas de batería — la más larga del mercado. Sonido Hi-Fi con transductores de 42mm, ANC adaptativa, diseño minimalista premium y llamadas cristalinas con 6 micrófonos.",
        "specs": {"Tipo": "Over-ear inalámbrico", "Batería": "60 horas (ANC on)", "Drivers": "42 mm", "ANC": "Adaptativa 3 niveles", "Conectividad": "Bluetooth 5.2 / aptX / AAC", "Peso": "293 g", "Carga": "USB-C"},
        "colors": ["Black", "White", "Denim"]
    },

    # MONITORES
    {
        "id": 13, "category": "Monitores",
        "name": "LG UltraGear 27\" 4K OLED",
        "brand": "LG",
        "price": 799.99,
        "original_price": 999.99,
        "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&q=80",
        "rating": 4.9, "reviews": 2100,
        "badge": "OLED 240Hz",
        "stock": 10,
        "description": "El monitor gaming OLED definitivo. Panel WOLED 4K con 240Hz, tiempo de respuesta 0.03ms, AMD FreeSync Premium Pro y NVIDIA G-Sync Compatible. Negros absolutos y colores explosivos.",
        "specs": {"Panel": "27\" WOLED 4K", "Resolución": "3840 x 2160", "Tasa de refresco": "240 Hz", "Tiempo de respuesta": "0.03 ms GtG", "HDR": "DisplayHDR True Black 400", "Conectividad": "2x HDMI 2.1, 1x DP 1.4, USB-C 90W", "Soporte": "VESA 100x100"},
        "colors": ["Negro"]
    },
    {
        "id": 14, "category": "Monitores",
        "name": "Samsung Odyssey G9 49\"",
        "brand": "Samsung",
        "price": 1299.99,
        "original_price": 1499.99,
        "image": "https://images.unsplash.com/photo-1616763355548-1b606f439f86?w=600&q=80",
        "rating": 4.7, "reviews": 890,
        "badge": "Ultrawide",
        "stock": 6,
        "description": "Monitor curvo ultrawide 49\" con curvatura 1000R — el más inmersivo del mercado. Equivalente a dos monitores QHD uno al lado del otro. 240Hz, Mini LED con 2048 zonas de dimming.",
        "specs": {"Panel": "49\" VA Curved Mini LED", "Resolución": "5120 x 1440 DQHD", "Curvatura": "1000R", "Tasa de refresco": "240 Hz", "HDR": "DisplayHDR 2000 (2048 zonas)", "Conectividad": "2x HDMI 2.1, 1x DP 1.4, 4x USB", "Peso": "13.4 kg"},
        "colors": ["Negro / Blanco"]
    },
    {
        "id": 15, "category": "Monitores",
        "name": "Dell UltraSharp U2723QE",
        "brand": "Dell",
        "price": 649.99,
        "original_price": 749.99,
        "image": "https://images.unsplash.com/photo-1586210579191-33b45e38fa2c?w=600&q=80",
        "rating": 4.8, "reviews": 3400,
        "badge": "Profesional",
        "stock": 20,
        "description": "El monitor profesional por excelencia. Panel IPS Black con contraste 2000:1, cobertura DCI-P3 98%, calibración de fábrica Delta E < 2 y hub USB-C 90W. Para diseñadores y fotógrafos.",
        "specs": {"Panel": "27\" IPS Black 4K", "Resolución": "3840 x 2160", "Color": "DCI-P3 98%, sRGB 100%", "Calibración": "Delta E < 2 de fábrica", "Conectividad": "USB-C 90W, HDMI 2.0, DP 1.4, 4x USB-A, RJ45", "Ajuste": "Altura, giro, rotación, inclinación", "Garantía": "3 años Advanced Exchange"},
        "colors": ["Platinum Silver"]
    },

    # TABLETS
    {
        "id": 16, "category": "Tablets",
        "name": "iPad Pro 13\" M4",
        "brand": "Apple",
        "price": 1299.99,
        "original_price": 1399.99,
        "image": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&q=80",
        "rating": 4.9, "reviews": 4300,
        "badge": "M4 Ultra Thin",
        "stock": 14,
        "description": "El iPad Pro más delgado jamás fabricado (5.1 mm). Chip M4 con Neural Engine, pantalla Ultra Retina XDR OLED en tándem con 1000 nits (2000 pico), compatible con Apple Pencil Pro.",
        "specs": {"Procesador": "Apple M4", "RAM": "16 GB", "Almacenamiento": "256 GB", "Pantalla": "13\" Ultra Retina XDR OLED", "Cámara": "12MP gran angular + LiDAR", "Conectividad": "Wi-Fi 6E + Bluetooth 5.3 + 5G (opt.)", "Grosor": "5.1 mm"},
        "colors": ["Plata", "Negro espacial"]
    },
    {
        "id": 17, "category": "Tablets",
        "name": "Samsung Galaxy Tab S9 Ultra",
        "brand": "Samsung",
        "price": 1099.99,
        "original_price": 1199.99,
        "image": "https://images.unsplash.com/photo-1632516643720-287d0a0e9e34?w=600&q=80",
        "rating": 4.7, "reviews": 2100,
        "badge": "14.6\" AMOLED",
        "stock": 9,
        "description": "La tablet Android más grande y poderosa. Pantalla Dynamic AMOLED 2X de 14,6\", S Pen incluido, Snapdragon 8 Gen 2, IP68 y batería de 11200 mAh para un día completo de trabajo.",
        "specs": {"Procesador": "Snapdragon 8 Gen 2", "RAM": "12 GB", "Almacenamiento": "256 GB + microSD", "Pantalla": "14.6\" Dynamic AMOLED 2X 120Hz", "S Pen": "Incluido", "Batería": "11200 mAh", "Resistencia": "IP68"},
        "colors": ["Graphite", "Beige"]
    },

    # ACCESORIOS
    {
        "id": 18, "category": "Accesorios",
        "name": "Logitech MX Master 3S",
        "brand": "Logitech",
        "price": 99.99,
        "original_price": 119.99,
        "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&q=80",
        "rating": 4.8, "reviews": 9800,
        "badge": "Silencioso",
        "stock": 60,
        "description": "El ratón de trabajo definitivo. Sensor Darkfield 8000 DPI que funciona en cualquier superficie, rueda de desplazamiento electromagnética MagSpeed, clics 90% más silenciosos y conexión a 3 dispositivos.",
        "specs": {"Sensor": "Darkfield 8000 DPI", "Botones": "7 programables", "Batería": "70 días con carga completa", "Conectividad": "USB-C / Bluetooth / Logi Bolt", "Dispositivos": "Hasta 3 simultáneos", "Compatibilidad": "Windows, macOS, Linux", "Rueda": "MagSpeed electromagnética"},
        "colors": ["Grafito", "Rosa", "Blanco"]
    },
    {
        "id": 19, "category": "Accesorios",
        "name": "Keychron Q1 Pro",
        "brand": "Keychron",
        "price": 199.99,
        "original_price": 229.99,
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&q=80",
        "rating": 4.7, "reviews": 2300,
        "badge": "Mecánico",
        "stock": 25,
        "description": "Teclado mecánico premium 75% con cuerpo de aluminio CNC. Switches Gateron Jupiter intercambiables en caliente, retroiluminación RGB por tecla, inalámbrico Bluetooth 5.1 y batería de 4000 mAh.",
        "specs": {"Tipo": "Mecánico 75%", "Switches": "Gateron Jupiter (hot-swap)", "Cuerpo": "Aluminio CNC", "Retroiluminación": "RGB por tecla", "Conectividad": "Bluetooth 5.1 / USB-C", "Batería": "4000 mAh", "Compatibilidad": "Windows / macOS"},
        "colors": ["Carbon Black", "Carbon Grey"]
    },
    {
        "id": 20, "category": "Accesorios",
        "name": "Anker 737 GaNPrime 120W",
        "brand": "Anker",
        "price": 79.99,
        "original_price": 99.99,
        "image": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=600&q=80",
        "rating": 4.8, "reviews": 5600,
        "badge": "GaN 120W",
        "stock": 80,
        "description": "Cargador GaN de 3 puertos y 120W — carga un MacBook Pro + iPhone + AirPods simultáneamente. Tecnología ActiveShield 2.0 monitorea temperatura 3 millones de veces por hora. Compacto y potente.",
        "specs": {"Potencia total": "120W", "Puerto USB-C 1": "100W", "Puerto USB-C 2": "20W", "Puerto USB-A": "22.5W", "Tecnología": "GaN III", "Seguridad": "ActiveShield 2.0", "Tamaño": "69 x 69 x 32 mm"},
        "colors": ["Negro", "Blanco"]
    },
    {
        "id": 21, "category": "Accesorios",
        "name": "Samsung T7 Shield SSD 2TB",
        "brand": "Samsung",
        "price": 149.99,
        "original_price": 189.99,
        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&q=80",
        "rating": 4.7, "reviews": 3100,
        "badge": "IP65",
        "stock": 35,
        "description": "SSD portátil de 2TB con velocidades de 1050 MB/s. Resistente a agua, polvo (IP65) y caídas hasta 3m. Incluye cifrado AES de 256 bits y es compatible con PC, Mac y Android.",
        "specs": {"Capacidad": "2 TB", "Lectura": "1050 MB/s", "Escritura": "1000 MB/s", "Interfaz": "USB 3.2 Gen 2 (USB-C)", "Resistencia": "IP65, caídas hasta 3m", "Cifrado": "AES 256 bits", "Peso": "98 g"},
        "colors": ["Beige", "Azul", "Negro"]
    },

    # SMARTWATCHES
    {
        "id": 22, "category": "Smartwatches",
        "name": "Apple Watch Ultra 2",
        "brand": "Apple",
        "price": 799.99,
        "original_price": 849.99,
        "image": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=600&q=80",
        "rating": 4.9, "reviews": 4500,
        "badge": "Titanio",
        "stock": 20,
        "description": "El Apple Watch más extremo. Caja de titanio de 49mm, pantalla de 2000 nits (la más brillante), GPS de doble frecuencia, profundidad hasta 100m, altímetro barométrico y batería de 60 horas.",
        "specs": {"Caja": "Titanio 49mm", "Pantalla": "LTPO OLED 2000 nits", "GPS": "Doble frecuencia L1/L5", "Profundidad": "100m (EN 13319)", "Batería": "60 horas (modo bajo consumo)", "Sensores": "Temperatura, oxígeno, ECG, FC", "OS": "watchOS 10"},
        "colors": ["Titanio Natural", "Titanio Negro"]
    },
    {
        "id": 23, "category": "Smartwatches",
        "name": "Samsung Galaxy Watch 6 Classic",
        "brand": "Samsung",
        "price": 399.99,
        "original_price": 449.99,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&q=80",
        "rating": 4.7, "reviews": 2800,
        "badge": "Bisel giratorio",
        "stock": 28,
        "description": "El smartwatch Android más elegante con su icónico bisel giratorio físico. Exynos W930, análisis avanzado del sueño, composición corporal, monitor de presión arterial y ECG. Autonomía de 40 horas.",
        "specs": {"Caja": "Acero inox 47mm", "Pantalla": "AMOLED 1.5\" 480x480", "Bisel": "Giratorio físico", "Batería": "425 mAh / 40 horas", "Resistencia": "5 ATM + IP68", "Sensores": "BioActive (FC, SpO2, ECG, BIA)", "OS": "Wear OS 4 + One UI Watch 5"},
        "colors": ["Negro", "Plata", "Oro"]
    },
]

CATEGORIES = ["Todos", "Laptops", "Smartphones", "Audífonos", "Monitores", "Tablets", "Accesorios", "Smartwatches"]

def get_product_by_id(pid):
    return next((p for p in PRODUCTS if p["id"] == pid), None)

def get_cart_items():
    cart = session.get("cart", {})
    items = []
    total = 0
    for pid_str, qty in cart.items():
        p = get_product_by_id(int(pid_str))
        if p:
            subtotal = p["price"] * qty
            items.append({**p, "quantity": qty, "subtotal": subtotal})
            total += subtotal
    return items, round(total, 2)

# ─── RUTAS ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    featured = [p for p in PRODUCTS if p.get("badge") in ["Bestseller", "Nuevo", "ANC #1", "OLED 240Hz"]][:6]
    cart_count = sum(session.get("cart", {}).values())
    return render_template("index.html", featured=featured, categories=CATEGORIES, cart_count=cart_count)

@app.route("/catalog")
def catalog():
    category = request.args.get("category", "Todos")
    search = request.args.get("q", "").lower()
    products = PRODUCTS
    if category and category != "Todos":
        products = [p for p in products if p["category"] == category]
    if search:
        products = [p for p in products if search in p["name"].lower() or search in p["description"].lower() or search in p["brand"].lower()]
    cart_count = sum(session.get("cart", {}).values())
    return render_template("catalog.html", products=products, categories=CATEGORIES,
                           selected_category=category, search=search, cart_count=cart_count)

@app.route("/product/<int:pid>")
def product_detail(pid):
    product = get_product_by_id(pid)
    if not product:
        return redirect(url_for("catalog"))
    related = [p for p in PRODUCTS if p["category"] == product["category"] and p["id"] != pid][:4]
    cart_count = sum(session.get("cart", {}).values())
    return render_template("product.html", product=product, related=related, cart_count=cart_count)

@app.route("/cart")
def cart():
    items, total = get_cart_items()
    cart_count = sum(session.get("cart", {}).values())
    return render_template("cart.html", items=items, total=total, cart_count=cart_count)

@app.route("/cart/add/<int:pid>", methods=["POST"])
def add_to_cart(pid):
    product = get_product_by_id(pid)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    cart = session.get("cart", {})
    key = str(pid)
    qty = int(request.form.get("quantity", 1))
    cart[key] = cart.get(key, 0) + qty
    session["cart"] = cart
    session.modified = True
    total_count = sum(cart.values())
    return jsonify({"success": True, "cart_count": total_count, "message": f"{product['name']} añadido al carrito"})

@app.route("/cart/update/<int:pid>", methods=["POST"])
def update_cart(pid):
    cart = session.get("cart", {})
    key = str(pid)
    qty = int(request.form.get("quantity", 1))
    if qty <= 0:
        cart.pop(key, None)
    else:
        cart[key] = qty
    session["cart"] = cart
    session.modified = True
    items, total = get_cart_items()
    return jsonify({"success": True, "total": total, "cart_count": sum(cart.values())})

@app.route("/cart/remove/<int:pid>", methods=["POST"])
def remove_from_cart(pid):
    cart = session.get("cart", {})
    cart.pop(str(pid), None)
    session["cart"] = cart
    session.modified = True
    items, total = get_cart_items()
    return jsonify({"success": True, "total": total, "cart_count": sum(cart.values())})

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = get_cart_items()
    cart_count = sum(session.get("cart", {}).values())
    if request.method == "POST":
        name  = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        if not name or not email or not items:
            return render_template("checkout.html", items=items, total=total,
                                   cart_count=cart_count, error="Completa todos los campos.")
        order_id = f"TS-{abs(hash(name+email)) % 100000:05d}"
        session["cart"] = {}
        session.modified = True
        return render_template("order_success.html", order_id=order_id, name=name,
                               email=email, total=total, cart_count=0)
    return render_template("checkout.html", items=items, total=total, cart_count=cart_count)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
