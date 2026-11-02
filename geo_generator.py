"""
geo_generator.py - Generador GEO (Generative Engine Optimization) para IA y Motores de Búsqueda
Zavala Automatización y Control S.A. de C.V.
Genera llms.txt, llms-full.txt, catalogo-completo.html (estático para crawlers de IA) y robots.txt extendido.
"""

import json
from pathlib import Path
from datetime import datetime
from seo_marcas_data import COMPANY

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "productos.json"

def load_products():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def generate_llms_txt(products):
    """Genera llms.txt estándar de llmstxt.org"""
    content = f"""# {COMPANY['name']}
> Suministro urgente de equipo y refacciones de automatización industrial, control eléctrico y neumática en México.

## Información de la Empresa
- Razón Social: {COMPANY['name']}
- RFC: {COMPANY['rfc']}
- Dirección: {COMPANY['address']}
- Teléfono Oficina: {COMPANY['phone_office']}
- WhatsApp de Ventas y Paros de Planta: {COMPANY['whatsapp']} (+52 81 3250 7130)
- Correo Electrónico: {COMPANY['email']}
- Cobertura: Envíos express a los 32 estados de México por DHL, FedEx y paquetería dedicada.
- Condiciones Comerciales: Facturación CFDI 4.0 y crédito directo a plantas industriales y maquiladoras.

## Especialidad y Diferenciadores
- Atención prioritaria 24/7 a paros de planta industriales.
- Localización de refacciones obsoletas, difíciles de conseguir o descontinuadas de fabricantes líderes.
- Más de 149 números de parte en inventario activo local y red de importación exprés de Estados Unidos, Europa y Japón.

## Marcas y Familias Principales
- **Siemens**: Contactores SIRIUS (3RT20, 3RT10), relevadores de sobrecarga (3RU21, 3RU2146-4KB0), guardamotores (3RV20), PLCs SIMATIC S7-1200 (6ES7211, 6ES7212, 6ES7214, 6ES7215), S7-1500, S7-300, variadores SINAMICS (V20, G120, 6SL) y LOGO! 24RCE.
- **Allen-Bradley / Rockwell Automation**: Fuentes SLC 500 (1746-P2, 1746-P1), módulos ControlLogix 1756, CompactLogix 1769, POINT I/O 1734, variadores PowerFlex 525 (25B), PowerFlex 40 (22B), y pantallas táctiles PanelView Plus 7.
- **Keyence**: Amplificadores de fibra óptica serie FS-N (FS-N41N), sensores láser CMOS LR-Z (LR-ZB250CB), cámaras de visión artificial IV2/IV3, lectores de códigos de barras SR-1000/SR-2000, y cortinas ópticas de seguridad GL-R.
- **Fanuc**: Servomotores de corriente alterna Alpha i A06B, consolas Teach Pendant A05B, fuentes de alimentación A16B, tarjetas I/O A03B y refacciones para controladores R-30iA y R-30iB.
- **Mitsubishi Electric**: PLCs MELSEC serie FX3U, FX5U, serie Q, variadores de frecuencia Inverter FR-D700 / FR-E700, y pantallas industriales GOT2000.
- **Control y Sensores Multimarca**: Válvulas y cilindros SMC, relevadores Finder 55.34, relevadores de estado sólido Celduc SOB945, sensores inductivos Autonics PRW12, sensores fotoeléctricos Banner Q85, interruptores ABB OT100F3 y gabinetes NEMA.

## Enlaces Principales del Sitio Web
- [Portal Principal]({COMPANY['domain']}/)
- [Catálogo Estático Completo]({COMPANY['domain']}/catalogo-completo.html)
- [Siemens Automatización]({COMPANY['domain']}/marcas/siemens.html)
- [Allen-Bradley Refacciones]({COMPANY['domain']}/marcas/allen-bradley.html)
- [Keyence Sensores & Visión]({COMPANY['domain']}/marcas/keyence.html)
- [Fanuc Robótica & CNC]({COMPANY['domain']}/marcas/fanuc.html)
- [Mitsubishi Electric]({COMPANY['domain']}/marcas/mitsubishi.html)
- [Control, Neumática & Sensores]({COMPANY['domain']}/marcas/control-y-sensores.html)
"""
    dest = BASE_DIR / "llms.txt"
    dest.write_text(content.strip(), encoding="utf-8")
    print(f"[OK] llms.txt generado ({len(content)} bytes)")

def generate_llms_full_txt(products):
    """Genera llms-full.txt con tabla completa de los 149 productos"""
    base_text = (BASE_DIR / "llms.txt").read_text(encoding="utf-8")
    table_lines = [
        "",
        "## Catálogo Completo de Productos Sincronizados",
        "| No. de Parte | Descripción del Producto | Marca / Fabricante | Categoría Técnica | Disponibilidad |",
        "|---|---|---|---|---|"
    ]
    for p in products:
        part = p.get("part_number", "").replace("|", "-")
        desc = p.get("description", "").replace("|", "-")
        brand = p.get("brand", "")
        cat = p.get("category", "")
        table_lines.append(f"| `{part}` | {desc} | {brand} | {cat} | Suministro Inmediato / Cotización Express |")
    
    full_content = base_text + "\n" + "\n".join(table_lines)
    dest = BASE_DIR / "llms-full.txt"
    dest.write_text(full_content.strip(), encoding="utf-8")
    print(f"[OK] llms-full.txt generado con {len(products)} productos.")

def generate_static_catalog_html(products):
    """Genera catalogo-completo.html estático sin JS para crawlers de IA y Google"""
    now_year = datetime.now().year
    
    # JSON-LD ItemList
    items_json = []
    for idx, p in enumerate(products, start=1):
        items_json.append({
            "@type": "ListItem",
            "position": idx,
            "item": {
                "@type": "Product",
                "name": f"{p['part_number']} - {p['description']}",
                "sku": p['part_number'],
                "brand": {"@type": "Brand", "name": p['brand']},
                "category": p['category'],
                "offers": {
                    "@type": "Offer",
                    "availability": "https://schema.org/InStock",
                    "priceCurrency": "MXN",
                    "seller": {"@type": "Organization", "name": COMPANY['name']}
                }
            }
        })
    json_ld = json.dumps({"@context": "https://schema.org", "@type": "ItemList", "itemListElement": items_json}, ensure_ascii=False)

    rows = []
    for p in products:
        wa_url = p.get("whatsapp_url", f"{COMPANY['whatsapp_url']}?text=Cotizar%20{p['part_number']}")
        rows.append(f"<tr><td><strong class=\"part-number-code\">{p['part_number']}</strong></td><td>{p['description']}</td><td><span class=\"badge-cat\">{p['brand']}</span></td><td><span class=\"badge-stock\">✓ Suministro Express</span></td><td><a href=\"{wa_url}\" target=\"_blank\" class=\"btn btn-table-wa\">Cotizar WhatsApp</a></td></tr>")
    tbody_html = "".join(rows)

    html = f"""<!DOCTYPE html>
<html lang="es-MX">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Catálogo Completo de Refacciones y Equipos Industriales | Zavala</title>
  <meta name="description" content="Inventario y catálogo completo de equipo de automatización industrial y refacciones en México. Allen-Bradley, Siemens, Keyence, Fanuc, SMC, ABB. Cotización express.">
  <link rel="canonical" href="{COMPANY['domain']}/catalogo-completo.html">
  <link rel="icon" type="image/png" href="assets/img/favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/css/styles.css">
  <script type="application/ld+json">{json_ld}</script>
</head>
<body class="page-catalog">
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
      <a href="./" class="brand-logo-link">
        <img src="assets/img/logo-zavala-horizontal.png" alt="{COMPANY['name']}" class="brand-logo" width="220">
      </a>
      <nav class="main-nav">
        <a href="./" class="nav-link">Inicio</a>
        <a href="./#catalogo" class="nav-link">Catálogo Interactivo</a>
        <a href="./#marcas" class="nav-link">Marcas</a>
        <a href="./#contacto" class="nav-link">Cotización</a>
      </nav>
      <div class="header-actions">
        <a href="{COMPANY['whatsapp_url']}" target="_blank" class="btn btn-primary btn-sm">Cotizar Express</a>
      </div>
    </div>
  </header>
  <main class="container" style="padding: 40px 20px;">
    <div class="section-header text-center">
      <span class="section-tag">Inventario Sincronizado</span>
      <h1>Catálogo Completo de Refacciones y Componentes Industriales</h1>
      <p>Listado completo de {len(products)} referencias en stock o suministro urgente con despacho express a todo México.</p>
    </div>
    <div class="table-responsive">
      <table class="table-industrial">
        <thead>
          <tr>
            <th>No. de Parte / Modelo</th>
            <th>Descripción Técnica</th>
            <th>Marca</th>
            <th>Disponibilidad</th>
            <th>Cotizar</th>
          </tr>
        </thead>
        <tbody>
          {tbody_html}
        </tbody>
      </table>
    </div>
  </main>
  <footer class="site-footer">
    <div class="container footer-grid">
      <div class="footer-col footer-about">
        <img src="assets/img/logo-zavala-horizontal.png" alt="{COMPANY['name']}" class="footer-logo" width="200">
        <p>Expertos en venta, suministro y distribución de refacciones de automatización industrial en México.</p>
        <p class="company-legal"><strong>RFC:</strong> {COMPANY['rfc']}</p>
      </div>
      <div class="footer-col">
        <h4>Enlaces de Interés</h4>
        <ul class="footer-links">
          <li><a href="./">Inicio</a></li>
          <li><a href="catalogo-completo.html">Catálogo Completo (HTML Estático)</a></li>
          <li><a href="llms.txt">Documento para Agentes de IA (llms.txt)</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Contacto</h4>
        <p class="footer-contact-item"><strong>Ubicación:</strong><br>{COMPANY['address']}</p>
        <p class="footer-contact-item"><strong>WhatsApp:</strong> <a href="{COMPANY['whatsapp_url']}">{COMPANY['whatsapp']}</a></p>
      </div>
    </div>
    <div class="footer-bottom"><div class="container footer-bottom-content"><p>© {now_year} {COMPANY['name']}. Todos los derechos reservados.</p></div></div>
  </footer>
  <a href="{COMPANY['whatsapp_url']}" class="wa-floating-btn" target="_blank" aria-label="WhatsApp"><span class="wa-icon">💬</span><span class="wa-text">Cotizar</span></a>
</body>
</html>"""
    dest = BASE_DIR / "catalogo-completo.html"
    dest.write_text(html, encoding="utf-8")
    print(f"[OK] catalogo-completo.html generado ({dest.stat().st_size} bytes).")

def generate_ai_robots_txt():
    """Genera robots.txt explícito para Google y Motores de IA"""
    ai_bots = [
        "Googlebot",
        "Bingbot",
        "OAI-SearchBot",
        "ChatGPT-User",
        "GPTBot",
        "PerplexityBot",
        "ClaudeBot",
        "Claude-SearchBot",
        "Google-Extended",
        "Applebot-Extended"
    ]
    lines = [
        f"# robots.txt para {COMPANY['name']}",
        "# Optimizado para Google y Motores Generativos de IA (GEO)",
        ""
    ]
    for bot in ai_bots:
        lines.append(f"User-agent: {bot}")
        lines.append("Allow: /")
        lines.append("")
    
    lines.extend([
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {COMPANY['domain']}/sitemap.xml",
        f"# AI Knowledge Document: {COMPANY['domain']}/llms.txt"
    ])
    dest = BASE_DIR / "robots.txt"
    dest.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] robots.txt generado con permisos explícitos para {len(ai_bots)} motores de búsqueda e IA.")

def main():
    prods = load_products()
    if prods:
        generate_llms_txt(prods)
        generate_llms_full_txt(prods)
        generate_static_catalog_html(prods)
        generate_ai_robots_txt()
        print("¡Módulo GEO ejecutado exitosamente!")
    else:
        print("[WARN] No se encontraron productos en productos.json.")

if __name__ == "__main__":
    main()
