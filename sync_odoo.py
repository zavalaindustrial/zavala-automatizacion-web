#!/usr/bin/env python3
"""
sync_odoo.py - Sincronizador de Inventario Odoo y Generador SEO B2B
Zavala Automatización y Control S.A. de C.V.
"""

import os
import sys
import json
import urllib.parse
import xmlrpc.client
from pathlib import Path
from datetime import datetime

# Importar configuración y metadatos SEO modulares
from seo_marcas_data import COMPANY, MARCAS_SEO_CONFIG

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR.parent / ".env"
if not ENV_FILE.exists():
    ENV_FILE = BASE_DIR / ".env"

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
MARCAS_DIR = BASE_DIR / "marcas"
MARCAS_DIR.mkdir(parents=True, exist_ok=True)

# Cargar .env
config = {}
if ENV_FILE.exists():
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            config[k.strip()] = v.strip()

ODOO_URL = config.get("ODOO_URL", "https://zavala-automatizacion-y-control.odoo.com")
ODOO_DB = config.get("ODOO_DB", "zavala-automatizacion-y-control")
ODOO_USER = config.get("ODOO_USER", "")
ODOO_PASSWORD = config.get("ODOO_PASSWORD", "")

def fetch_odoo_products():
    """Conecta a Odoo y descarga product.template activos"""
    print(f"[INFO] Conectando a Odoo ({ODOO_URL} - DB: {ODOO_DB})...")
    try:
        common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
        if not uid:
            print("[WARN] Autenticación Odoo fallida. Usando datos locales previos.")
            return load_fallback_products()
        
        models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
        fields = ['id', 'name', 'default_code', 'description_sale', 'categ_id']
        raw_products = models.execute_kw(
            ODOO_DB, uid, ODOO_PASSWORD,
            'product.template', 'search_read',
            [[['active', '=', True]]],
            {'fields': fields}
        )
        print(f"[OK] {len(raw_products)} productos descargados de Odoo.")
        return raw_products
    except Exception as e:
        print(f"[WARN] Error conectando a Odoo: {e}. Usando datos locales si existen.")
        return load_fallback_products()

def load_fallback_products():
    json_path = DATA_DIR / "productos.json"
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def classify_brand(name, desc):
    t = f"{name} {desc}".upper()
    if any(k in t for k in ["1746", "1756", "1769", "1734", "2080", "22B", "25B", "2711P", "ALLEN", "BRADLEY", "ROCKWELL", "CONTROLLOGIX", "COMPACTLOGIX", "POWERFLEX"]):
        return "Allen-Bradley"
    if any(k in t for k in ["SIEMENS", "SIMATIC", "SIRIUS", "SINAMICS", "3RT", "3RU", "3RV", "6ES7", "6AV", "6SL", "LOGO!", "SITOP"]):
        return "Siemens"
    if any(k in t for k in ["KEYENCE", "FS-N", "LR-Z", "IV2", "IV3", "SR-1000", "SR-2000", "GL-R", "FD-Q"]):
        return "Keyence"
    if any(k in t for k in ["FANUC", "A06B", "A05B", "R-30I", "A03B", "A16B", "ROBOT"]):
        return "Fanuc"
    if any(k in t for k in ["MITSUBISHI", "MELSEC", "FX3U", "FX5U", "FR-D700", "FR-E700", "GOT2000"]):
        return "Mitsubishi Electric"
    if any(k in t for k in ["SMC", "FRL", "VALVULA SELENOIDE", "CILINDRO", "CXSM", "AC20-"]):
        return "SMC"
    if any(k in t for k in ["ABB", "OT100", "OXS6", "OHBS"]):
        return "ABB"
    if any(k in t for k in ["FINDER", "55.34"]):
        return "Finder"
    if any(k in t for k in ["CELDUC", "SOB945"]):
        return "Celduc"
    if any(k in t for k in ["BANNER", "Q85VR"]):
        return "Banner Engineering"
    if any(k in t for k in ["AUTONICS", "PRW12"]):
        return "Autonics"
    if any(k in t for k in ["CARLO GAVAZZI", "CA30"]):
        return "Carlo Gavazzi"
    if any(k in t for k in ["HONEYWELL", "BZE6", "MICROSWITCH"]):
        return "Honeywell"
    if any(k in t for k in ["MICRO DETECTORS", "UK6A", "ST18C"]):
        return "Micro Detectors"
    if any(k in t for k in ["AUTOMATIONDIRECT", "CD12L"]):
        return "AutomationDirect"
    if any(k in t for k in ["MILWAUKEE", "RIDGID", "SURTEK", "MIKELS", "URREA", "HERMEX", "TRUPER", "STILLSON"]):
        return "Herramientas Industriales"
    if any(k in t for k in ["TORNILLO", "SOCKET", "TUERCA", "ARANDELA", "PIJA"]):
        return "Fijación y Tornillería Industrial"
    if any(k in t for k in ["CABLE", "CONDULET", "CONTRATUERCA", "COPLE", "FUSIBLE"]):
        return "Distribución Eléctrica"
    return "Control & Automatización"

def classify_category(name, desc):
    t = f"{name} {desc}".upper()
    if any(k in t for k in ["PLC", "CONTROLADOR", "MODULO", "1746", "1756", "1769", "SIMATIC"]):
        return "PLCs y Controladores"
    if any(k in t for k in ["FUENTE", "POWER SUPPLY", "24VCD", "120/240"]):
        return "Fuentes de Alimentación"
    if any(k in t for k in ["SENSOR", "PROXIMIDAD", "FOTOCELDA", "ULTRASONIC", "MAGNETICO", "FOTOELECTRICO", "VISION"]):
        return "Sensores e Instrumentación"
    if any(k in t for k in ["RELEVADOR", "RELE", "RELAY", "ESTADO SOLIDO", "CORTINA", "SEGURIDAD"]):
        return "Relevación y Seguridad"
    if any(k in t for k in ["VALVULA", "CILINDRO", "NEUMATICA", "FRL", "REGULADOR DE FLUJO", "SMC"]):
        return "Neumática y Válvulas"
    if any(k in t for k in ["VARIADOR", "ARRANCADOR", "DRIVE", "INVERSOR", "MOTOR"]):
        return "Drives y Arrancadores"
    if any(k in t for k in ["INTERRUPTOR", "CONTACTOR", "GUARDAMOTOR", "DESCONECTOR", "FUSIBLE"]):
        return "Maniobra y Protección Eléctrica"
    if any(k in t for k in ["HERRAMIENTA", "PINZA", "LLAVE", "ROTOMARTILLO"]):
        return "Herramientas de Mantenimiento"
    return "Componentes y Mantenimiento Industrial"

def process_and_save_products(raw_products):
    """Limpia productos, descarta pruebas y genera data/productos.json"""
    clean_list = []
    test_keywords = ["hambuerguesa", "hamburguesa", "jamon", "prueba 1 centenario"]

    for item in raw_products:
        name = (item.get("name") or "").strip()
        desc = (item.get("description_sale") or "").strip()
        code = (item.get("default_code") or "").strip()
        
        full_text = f"{name} {desc}".lower()
        if any(tk in full_text for tk in test_keywords) or not name:
            continue

        clean_desc = desc if desc else f"Suministro y reemplazo de refacción industrial {name}"
        clean_code = code if code else name
        brand = classify_brand(name, desc)
        category = classify_category(name, desc)

        wa_msg = f"Hola Zavala Automatización, me interesa cotizar el No. de Parte: {name} ({clean_desc}). ¿Tienen disponibilidad y tiempo de entrega?"
        wa_link = f"https://wa.me/5218132507130?text={urllib.parse.quote(wa_msg)}"

        clean_list.append({
            "id": item.get("id"),
            "part_number": name,
            "code": clean_code,
            "description": clean_desc,
            "brand": brand,
            "category": category,
            "availability": "Disponible para Cotización Express / Envío a todo México",
            "whatsapp_url": wa_link
        })

    out_file = DATA_DIR / "productos.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(clean_list, f, ensure_ascii=False, indent=2)

    print(f"[OK] {len(clean_list)} productos guardados en {out_file}.")
    return clean_list

def generate_brand_pages(products):
    """Genera las páginas HTML SEO de marcas en web-zavala/marcas/"""
    print("[INFO] Generando páginas de marcas SEO...")

    for key, cfg in MARCAS_SEO_CONFIG.items():
        if key == "siemens":
            b_prods = [p for p in products if p["brand"] == "Siemens"]
        elif key == "allen-bradley":
            b_prods = [p for p in products if p["brand"] == "Allen-Bradley"]
        elif key == "keyence":
            b_prods = [p for p in products if p["brand"] == "Keyence"]
        elif key == "fanuc":
            b_prods = [p for p in products if p["brand"] == "Fanuc"]
        elif key == "mitsubishi":
            b_prods = [p for p in products if p["brand"] == "Mitsubishi Electric"]
        else:
            b_prods = [p for p in products if p["brand"] not in ["Siemens", "Allen-Bradley", "Keyence", "Fanuc", "Mitsubishi Electric"]]

        html = f"""<!DOCTYPE html>
<html lang="es-MX">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{cfg['title']}</title>
  <meta name="description" content="{cfg['meta_desc']}">
  <link rel="canonical" href="{COMPANY['domain']}/marcas/{cfg['slug']}">
  <link rel="icon" type="image/png" href="../assets/img/favicon.png">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{cfg['title']}">
  <meta property="og:description" content="{cfg['meta_desc']}">
  <meta property="og:url" content="{COMPANY['domain']}/marcas/{cfg['slug']}">
  <meta property="og:image" content="{COMPANY['domain']}/assets/img/logo-zavala-horizontal.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/styles.css">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@graph":[{{"@type":"LocalBusiness","name":"{COMPANY['name']}","telephone":"{COMPANY['phone_office']}","url":"{COMPANY['domain']}","logo":"{COMPANY['domain']}/assets/img/logo-zavala-horizontal.png","address":{{"@type":"PostalAddress","streetAddress":"Hacienda San Ignacio 103","addressLocality":"San Nicolás de los Garza / Monterrey","addressRegion":"Nuevo León","postalCode":"66477","addressCountry":"MX"}}}},{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Inicio","item":"{COMPANY['domain']}/"}},{{"@type":"ListItem","position":2,"name":"Marcas","item":"{COMPANY['domain']}/#marcas"}},{{"@type":"ListItem","position":3,"name":"{cfg['brand_name']}","item":"{COMPANY['domain']}/marcas/{cfg['slug']}"}}]}}]}}
  </script>
</head>
<body class="page-brand">
  <div class="topbar">
    <div class="container topbar-content">
      <div class="topbar-left">
        <span class="badge-urgent">⚡ Paros de Planta Urgentes</span>
        <span class="divider">|</span>
        <span>🚚 Envíos Express a Todo México</span>
        <span class="divider">|</span>
        <span>🏢 Facturación CFDI 4.0 & Crédito</span>
      </div>
      <div class="topbar-right">
        <a href="tel:8124717534" class="topbar-link">📞 Oficina: {COMPANY['phone_office']}</a>
        <a href="{COMPANY['whatsapp_url']}" target="_blank" class="topbar-link topbar-wa">💬 WhatsApp: {COMPANY['whatsapp']}</a>
      </div>
    </div>
  </div>
  <header class="site-header">
    <div class="container header-container">
      <a href="../" class="brand-logo-link">
        <img src="../assets/img/logo-zavala-horizontal.png" alt="{COMPANY['name']}" class="brand-logo" width="220">
      </a>
      <nav class="main-nav">
        <a href="../#catalogo" class="nav-link">Catálogo en Vivo</a>
        <a href="../#marcas" class="nav-link active">Marcas</a>
        <a href="../#equipos" class="nav-link">Equipos</a>
        <a href="../#nosotros" class="nav-link">Nosotros</a>
        <a href="../#contacto" class="nav-link">Contacto</a>
      </nav>
      <div class="header-actions">
        <a href="{COMPANY['whatsapp_url']}?text=Hola%20Zavala%2C%20requiero%20cotizaci%C3%B3n%20urgente%20de%20equipo%20{urllib.parse.quote(cfg['brand_name'])}" target="_blank" class="btn btn-primary btn-sm">Cotizar {cfg['brand_name']}</a>
      </div>
    </div>
  </header>
  <div class="breadcrumb-bar">
    <div class="container">
      <ul class="breadcrumbs">
        <li><a href="../">Inicio</a></li>
        <li><a href="../#marcas">Marcas</a></li>
        <li class="active">{cfg['brand_name']}</li>
      </ul>
    </div>
  </div>
  <section class="brand-hero-section">
    <div class="container brand-hero-grid">
      <div class="brand-hero-text">
        <span class="sub-badge">Suministro de Refacciones & Equipos Originales</span>
        <h1>{cfg['h1']}</h1>
        <p class="lead-text">{cfg['hero_desc']}</p>
        <div class="hero-brand-cta">
          <a href="{COMPANY['whatsapp_url']}?text=Hola%20Zavala%2C%20tengo%20un%20paro%20de%20planta%20y%20necesito%20cotizar%20piezas%20de%20{urllib.parse.quote(cfg['brand_name'])}" target="_blank" class="btn btn-wa-large">💬 Cotizar {cfg['brand_name']} por WhatsApp</a>
          <a href="#buscador-marca" class="btn btn-secondary">Explorar Familias</a>
        </div>
        <div class="trust-pills">
          <span class="pill-item">✓ Piezas Nuevas y Reacondicionadas con Garantía</span>
          <span class="pill-item">✓ Reemplazo Directo de Series Obsoletas</span>
          <span class="pill-item">✓ Asesoría Técnica Especializada</span>
        </div>
      </div>
      <div class="brand-hero-card">
        <div class="brand-logo-frame">
          <img src="{cfg['brand_logo']}" alt="Logo {cfg['brand_name']}" class="brand-hero-logo">
        </div>
        <div class="quick-rfq-box">
          <h3>Cotización Inmediata {cfg['brand_name']}</h3>
          <p>Escribe tu número de parte o modelo y te respondemos en minutos:</p>
          <div class="quick-input-group">
            <input type="text" id="quick-part-input" placeholder="Ej. {cfg['families'][0]['prefixes'][0]}..." class="input-part">
            <button type="button" id="btn-quick-rfq" class="btn btn-accent">Cotizar Ya</button>
          </div>
          <small class="text-muted">Envíos a todo México por DHL / FedEx Express o entrega local inmediata.</small>
        </div>
      </div>
    </div>
  </section>
  <section class="section section-families" id="buscador-marca">
    <div class="container">
      <div class="section-header text-center">
        <span class="section-tag">Familias de Producto y Series Populares</span>
        <h2>Líneas de Equipo {cfg['brand_name']} con Suministro Activo</h2>
        <p>Localizamos refacciones tanto vigentes como descontinuadas para mantener tu línea funcionando.</p>
      </div>
      <div class="families-grid">"""

        for fam in cfg["families"]:
            prefixes_html = "".join([f'<a href="{COMPANY["whatsapp_url"]}?text=Hola%20Zavala%2C%20requiero%20cotizaci%C3%B3n%20urgente%20de%20la%20serie%20{urllib.parse.quote(p)}%20de%20{urllib.parse.quote(cfg["brand_name"])}" target="_blank" class="prefix-tag">{p}</a>' for p in fam["prefixes"]])
            html += f"""
        <div class="family-card">
          <div class="family-card-header"><h3>{fam['name']}</h3></div>
          <p class="family-desc">{fam['desc']}</p>
          <div class="family-prefixes">
            <span class="prefixes-label">Prefijos Frecuentes:</span>
            <div class="tag-cloud">{prefixes_html}</div>
          </div>
          <div class="family-card-footer">
            <a href="{COMPANY['whatsapp_url']}?text=Hola%20Zavala%2C%20busco%20informaci%C3%B3n%20y%20cotizaci%C3%B3n%20para%20la%20l%C3%ADnea%20{urllib.parse.quote(fam['name'])}%20de%20{urllib.parse.quote(cfg['brand_name'])}" target="_blank" class="btn btn-outline-sm">Cotizar esta Familia →</a>
          </div>
        </div>"""

        html += f"""
      </div>
    </div>
  </section>
  <section class="section section-catalog-filtered">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Inventario Sincronizado</span>
        <h2>Ejemplos de Productos {cfg['brand_name']} en Catálogo</h2>
      </div>
      <div class="table-responsive">
        <table class="table-industrial">
          <thead>
            <tr>
              <th>No. de Parte / Modelo</th>
              <th>Descripción Técnica</th>
              <th>Categoría</th>
              <th>Disponibilidad</th>
              <th>Acción</th>
            </tr>
          </thead>
          <tbody>"""

        if b_prods:
            for bp in b_prods[:15]:
                html += f"""
            <tr>
              <td><strong class="part-number-code">{bp['part_number']}</strong></td>
              <td>{bp['description']}</td>
              <td><span class="badge-cat">{bp['category']}</span></td>
              <td><span class="badge-stock">✓ Disponible</span></td>
              <td><a href="{bp['whatsapp_url']}" target="_blank" class="btn btn-table-wa">Cotizar WhatsApp</a></td>
            </tr>"""
        else:
            html += f"""
            <tr>
              <td colspan="5" class="text-center py-4">
                <p>Contamos con acceso a inventario de importación urgente y red de distribuidores autorizados para <strong>{cfg['brand_name']}</strong>.</p>
                <a href="{COMPANY['whatsapp_url']}?text=Hola%20Zavala%2C%20tengo%20un%20n%C3%BAmero%20de%20parte%20de%20{urllib.parse.quote(cfg['brand_name'])}%20para%20cotizar" target="_blank" class="btn btn-primary">Consultar Número de Parte de {cfg['brand_name']}</a>
              </td>
            </tr>"""

        html += f"""
          </tbody>
        </table>
      </div>
    </div>
  </section>
  <section class="section-urgent-banner">
    <div class="container urgent-banner-box">
      <div class="urgent-text">
        <h2>¿Tienes tu máquina detenida por una pieza {cfg['brand_name']}?</h2>
        <p>No pierdas miles de dólares por hora de paro. Localizamos números de parte difíciles y gestionamos envíos de emergencia.</p>
      </div>
      <div class="urgent-actions">
        <a href="{COMPANY['whatsapp_url']}?text=EMERGENCIA%3A%20Paro%20de%20planta%20por%20refacci%C3%B3n%20{urllib.parse.quote(cfg['brand_name'])}" target="_blank" class="btn btn-danger-pulse">🚨 Atención a Paro de Planta</a>
      </div>
    </div>
  </section>
  <footer class="site-footer">
    <div class="container footer-grid">
      <div class="footer-col footer-about">
        <img src="../assets/img/logo-zavala-horizontal.png" alt="{COMPANY['name']}" class="footer-logo" width="200">
        <p>Expertos en suministro, distribución y reemplazo de refacciones y equipos de automatización industrial.</p>
        <p class="company-legal"><strong>Razón Social:</strong> {COMPANY['name']}<br><strong>RFC:</strong> {COMPANY['rfc']}</p>
      </div>
      <div class="footer-col">
        <h4>Marcas Líderes</h4>
        <ul class="footer-links">
          <li><a href="allen-bradley.html">Allen-Bradley / Rockwell</a></li>
          <li><a href="siemens.html">Siemens SIMATIC / SIRIUS</a></li>
          <li><a href="keyence.html">Keyence Sensores & Visión</a></li>
          <li><a href="fanuc.html">Fanuc Robótica & CNC</a></li>
          <li><a href="mitsubishi.html">Mitsubishi Electric</a></li>
          <li><a href="control-y-sensores.html">Control & Sensores Multimarca</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Contacto y Almacén</h4>
        <p class="footer-contact-item"><strong>Ubicación:</strong><br>{COMPANY['address']}</p>
        <p class="footer-contact-item"><strong>Teléfono Oficina:</strong><br><a href="tel:8124717534">{COMPANY['phone_office']}</a></p>
        <p class="footer-contact-item"><strong>WhatsApp Ventas:</strong><br><a href="{COMPANY['whatsapp_url']}" target="_blank">{COMPANY['whatsapp']}</a></p>
        <p class="footer-contact-item"><strong>Correo:</strong><br><a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a></p>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="container footer-bottom-content">
        <p>© {datetime.now().year} {COMPANY['name']}. Todos los derechos reservados.</p>
        <p class="footer-disclaimer">Todas las marcas registradas pertenecen a sus respectivos fabricantes y se citan únicamente con fines de identificación y suministro.</p>
      </div>
    </div>
  </footer>
  <a href="{COMPANY['whatsapp_url']}?text=Hola%20Zavala%2C%20requiero%20cotizaci%C3%B3n%20de%20equipo%20{urllib.parse.quote(cfg['brand_name'])}" class="wa-floating-btn" target="_blank" aria-label="Contactar por WhatsApp">
    <span class="wa-icon">💬</span>
    <span class="wa-text">Cotizar {cfg['brand_name']}</span>
  </a>
  <script>
    document.getElementById('btn-quick-rfq')?.addEventListener('click', function() {{
      const input = document.getElementById('quick-part-input');
      const val = (input?.value || '').trim();
      if (!val) {{
        alert('Por favor escribe el modelo o número de parte que necesitas.');
        input?.focus();
        return;
      }}
      const msg = `Hola Zavala, requiero cotización inmediata para el número de parte de {cfg['brand_name']}: ${{val}}. ¿Tienen disponibilidad?`;
      window.open(`https://wa.me/5218132507130?text=${{encodeURIComponent(msg)}}`, '_blank');
    }});
  </script>
</body>
</html>"""

        dest = MARCAS_DIR / cfg["slug"]
        dest.write_text(html, encoding="utf-8")
        print(f"[OK] Página de marca generada: {dest.name}")

def generate_sitemap():
    print("[INFO] Generando sitemap.xml...")
    now_str = datetime.now().strftime("%Y-%m-%d")
    pages = [
        {"loc": f"{COMPANY['domain']}/", "priority": "1.0", "changefreq": "weekly"},
        {"loc": f"{COMPANY['domain']}/marcas/siemens.html", "priority": "0.9", "changefreq": "weekly"},
        {"loc": f"{COMPANY['domain']}/marcas/allen-bradley.html", "priority": "0.9", "changefreq": "weekly"},
        {"loc": f"{COMPANY['domain']}/marcas/keyence.html", "priority": "0.9", "changefreq": "weekly"},
        {"loc": f"{COMPANY['domain']}/marcas/fanuc.html", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{COMPANY['domain']}/marcas/mitsubishi.html", "priority": "0.8", "changefreq": "weekly"},
        {"loc": f"{COMPANY['domain']}/marcas/control-y-sensores.html", "priority": "0.8", "changefreq": "weekly"},
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        xml.append(f'  <url><loc>{p["loc"]}</loc><lastmod>{now_str}</lastmod><changefreq>{p["changefreq"]}</changefreq><priority>{p["priority"]}</priority></url>')
    xml.append('</urlset>')
    (BASE_DIR / "sitemap.xml").write_text("\n".join(xml), encoding="utf-8")
    print(f"[OK] sitemap.xml generado ({len(pages)} URLs).")

def generate_robots():
    print("[INFO] Generando robots.txt...")
    c = f"# Robots.txt para {COMPANY['name']}\nUser-agent: *\nAllow: /\n\nSitemap: {COMPANY['domain']}/sitemap.xml\n"
    (BASE_DIR / "robots.txt").write_text(c, encoding="utf-8")
    print("[OK] robots.txt generado.")

def generate_redirects():
    print("[INFO] Generando _redirects...")
    r = """/optimizamos-procesos-impulsamos-resultados/ /#nosotros 301
/marcas/ /#marcas 301
/contacto/ /#contacto 301
/nuestros-productos/ /#catalogo 301
/productos-para-automatizacion-industrial/ /#catalogo 301
/allen-bradley/ /marcas/allen-bradley.html 301
/2026/08/12/* /#nosotros 301
/product/contacto/ /#contacto 301
/product/marcas/ /#marcas 301
/product/productos/ /#catalogo 301
/product/* /#catalogo 301
"""
    (BASE_DIR / "_redirects").write_text(r, encoding="utf-8")
    print("[OK] _redirects generado.")

def main():
    print("=" * 60)
    print("SINCRONIZACIÓN ODOO & GENERADOR SEO INDUSTRIAL - ZAVALA")
    print("=" * 60)
    raw_products = fetch_odoo_products()
    clean_products = process_and_save_products(raw_products)
    generate_brand_pages(clean_products)
    generate_redirects()
    try:
        from geo_generator import main as geo_main
        geo_main()
    except Exception as e:
        print(f"[WARN] Error en generador GEO: {e}")
    print("=" * 60)
    print("¡Sincronización y generación completada exitosamente!")
    print("=" * 60)

if __name__ == "__main__":
    main()
