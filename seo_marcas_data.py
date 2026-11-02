"""
seo_marcas_data.py - Configuración Estática de SEO, Metadatos y Familias de Marcas
Zavala Automatización y Control S.A. de C.V.
"""

COMPANY = {
    "name": "Zavala Automatización y Control S.A. de C.V.",
    "short_name": "Zavala Automatización y Control",
    "phone_office": "81 2471 7534",
    "whatsapp": "81 3250 7130",
    "whatsapp_url": "https://wa.me/5218132507130",
    "email": "ventas1@zavalaindustrial.net",
    "address": "Monterrey, N.L. y Envíos a todo México",
    "city": "Monterrey",
    "state": "Nuevo León",
    "country": "México",
    "domain": "https://zavalaautomatizacionycontrol.com.mx"
}

MARCAS_SEO_CONFIG = {
    "siemens": {
        "slug": "siemens.html",
        "title": "Siemens Automatización y Control Industrial México | Suministro y Refacciones Urgentes Zavala",
        "h1": "Suministro y Refacciones Siemens en México: SIRIUS, SIMATIC, SINAMICS y LOGO!",
        "meta_desc": "Distribución y suministro express de refacciones industriales Siemens en México. Contactores 3RT, relevadores 3RU, 3RU2146-4KB0, PLCs S7-1200, S7-1500, variadores SINAMICS y módulos 6ES7. Catálogo con entrega inmediata y envíos express a todo México.",
        "brand_name": "Siemens",
        "brand_logo": "../assets/img/marca-siemens.png",
        "hero_desc": "Suministramos toda la gama industrial Siemens: desde contactores y relevadores térmicos SIRIUS (3RT, 3RU, 3RV) hasta controladores SIMATIC S7-1200 / S7-1500, variadores SINAMICS y micro-autómatas LOGO!. Catálogo con entrega inmediata en Monterrey y envíos express a todo México con suministro industrial inmediato.",
        "families": [
            {
                "name": "Maniobra y Protección SIRIUS",
                "prefixes": ["3RT20", "3RT10", "3RU21", "3RU2146-4KB0", "3RV20", "3RW30", "3RW40"],
                "desc": "Contactores tripolares SIRIUS (3RT2015, 3RT2026, 3RT2035), relevadores de sobrecarga bimetálicos (3RU2116, 3RU2146-4KB0), guardamotores compactos (3RV2011, 3RV2021) y arrancadores suaves 3RW."
            },
            {
                "name": "Controladores SIMATIC S7 y Módulos I/O",
                "prefixes": ["6ES7211", "6ES7212", "6ES7214", "6ES7215", "6ES7511", "6ES7513", "6ES7315", "6ES7134"],
                "desc": "CPUs SIMATIC S7-1200 (1211C, 1212C, 1214C, 1215C), SIMATIC S7-1500, módulos de entradas/salidas analógicas y digitales 6ES7, y refacciones para sistemas legacy S7-300 y S7-400."
            },
            {
                "name": "Variadores de Frecuencia SINAMICS",
                "prefixes": ["6SL3210", "6SL3224", "SINAMICS V20", "SINAMICS G120", "SINAMICS S120"],
                "desc": "Drives de propósito general SINAMICS V20 y G120 modulares (Unidades de Control CU240E-2 y Módulos de Potencia PM240-2), reactancias de línea y paneles de operador BOP-2 e IOP-2."
            },
            {
                "name": "Interfaces HMI y Micro-Automatización",
                "prefixes": ["6AV2123", "6AV2124", "LOGO! 24RCE", "LOGO! 230RCE", "SITOP Power 24V"],
                "desc": "Paneles de operador SIMATIC HMI Basic y Comfort (KTP400, KTP700, KTP900, TP1200), micro-controladores inteligentes LOGO! 8 y fuentes de alimentación conmutadas industriales SITOP PSU."
            }
        ]
    },
    "allen-bradley": {
        "slug": "allen-bradley.html",
        "title": "Allen-Bradley Rockwell Automation México | Refacciones, ControlLogix, CompactLogix, PowerFlex",
        "h1": "Refacciones y Equipo Allen-Bradley / Rockwell Automation en México",
        "meta_desc": "Suministro de equipo y refacciones Allen-Bradley en México. Fuentes 1746-P2, ControlLogix 1756, CompactLogix 1769, POINT I/O 1734, variadores PowerFlex 525 y PanelView Plus. Catálogo con entrega inmediata y envíos express a todo México.",
        "brand_name": "Allen-Bradley",
        "brand_logo": "../assets/img/marca-allen-bradley.png",
        "hero_desc": "Especialistas en suministro de refacciones críticas y sistemas completos de Rockwell Automation / Allen-Bradley en México. Contamos con stock de fuentes SLC 500 (1746-P2), módulos ControlLogix 1756, CompactLogix 1769, MicroLogix, variadores PowerFlex 525 y pantallas táctiles PanelView Plus. Solución inmediata ante fallas de maquinaria y piezas descontinuadas.",
        "families": [
            {
                "name": "Fuentes y Sistemas SLC 500 (Legacy y Críticos)",
                "prefixes": ["1746-P1", "1746-P2", "1746-P3", "1746-P4", "1746-IB16", "1746-OB16", "1746-NI8", "1746-NO4I"],
                "desc": "Fuentes de alimentación de chasis 120/240V 5A (1746-P2), módulos de entradas y salidas digitales de 16 y 32 puntos, módulos de termopar y comunicación para sistemas SLC 500 aún operativos."
            },
            {
                "name": "ControlLogix & GuardLogix Serie 1756",
                "prefixes": ["1756-L71", "1756-L72", "1756-L81E", "1756-IB16", "1756-OB16E", "1756-EN2T", "1756-PA72"],
                "desc": "Procesadores PAC de alto desempeño ControlLogix 5570 y 5580, módulos de comunicación Ethernet/IP 1756-EN2T / EN2TR, fuentes de alimentación redundantes y módulos de E/S seguras."
            },
            {
                "name": "CompactLogix & POINT I/O (1769 / 1734)",
                "prefixes": ["1769-L30ER", "1769-L33ER", "1769-L24ER", "1769-OB16", "1734-IB4", "1734-OB4E", "1734-AENT"],
                "desc": "Controladores modulares CompactLogix Serie 5370 y 5380, módulos compactos 1769 y estaciones remotas de distribución distribuida POINT I/O 1734 conectadas vía bus Ethernet/IP."
            },
            {
                "name": "Drives PowerFlex & Pantallas PanelView Plus",
                "prefixes": ["25B-D010N104", "25B-D4P0N104", "25B-D2P3N104", "22B-D4P0N104", "2711P-T7C22D9P", "2711P-T10C22D9P"],
                "desc": "Variadores de frecuencia PowerFlex 525 con puerto Ethernet/IP integrado, PowerFlex 4M/40/753 y pantallas táctiles gráficas industriales PanelView Plus 7 de 7 a 15 pulgadas."
            }
        ]
    },
    "keyence": {
        "slug": "keyence.html",
        "title": "Sensores Keyence México | Visión Artificial, Sensores Láser y Cortinas de Seguridad",
        "h1": "Sensores de Alta Precisión y Sistemas de Visión Keyence en México",
        "meta_desc": "Venta y suministro de sensores Keyence en México: amplificadores de fibra FS-N41N, sensores láser CMOS LR-ZB250CB, cámaras de visión inteligente IV2 / IV3, lectores de código SR-1000 y cortinas GL-R. Cotización express.",
        "brand_name": "Keyence",
        "brand_logo": "../assets/img/marca-keyence.png",
        "hero_desc": "Proveemos tecnología de detección y calidad Keyence para plantas automotrices, metalmecánicas y farmacéuticas en México. Localizamos y suministramos sensores láser inteligentes, amplificadores de fibra óptica, cámaras de visión artificial integradas y barreras de seguridad con entrega inmediata.",
        "families": [
            {
                "name": "Amplificadores de Fibra Óptica Serie FS-N",
                "prefixes": ["FS-N41N", "FS-N41P", "FS-N11N", "FS-N11P", "FU-77", "FU-35FA"],
                "desc": "Amplificadores digitales ultrarrápidos con calibración con un solo botón, alta penetración lumínica y cabezales de fibra resistentes a altas temperaturas y químicos."
            },
            {
                "name": "Sensores Láser CMOS Autónomos Serie LR-Z / LR-T",
                "prefixes": ["LR-ZB250CB", "LR-ZB100N", "LR-ZH500CB", "LR-TB5000", "LR-TB2000"],
                "desc": "Sensores de distancia con tecnología CMOS y tiempo de vuelo (TOF), inmunes al color, brillo o ángulo de la pieza inspeccionada."
            },
            {
                "name": "Sensores de Visión e Identificación Serie IV / SR",
                "prefixes": ["IV2-G500MA", "IV3-G500MA", "IV-G150MA", "SR-1000", "SR-2000", "SR-750"],
                "desc": "Sistemas de visión compactos basados en Inteligencia Artificial para detección de presencia/ausencia y lectores industriales de códigos de barras 1D/2D DPM de lectura directa sobre metal."
            },
            {
                "name": "Seguridad Industrial y Medición de Fluidos",
                "prefixes": ["GL-R20H", "GL-R32H", "FD-Q20C", "FD-Q32C", "PZ-G41N", "KV-N14DT"],
                "desc": "Cortinas de seguridad ópticas de alta resistencia categoría 4, sensores de flujo tipo abrazadera no invasivos Clamp-on para tuberías de agua y aceites, y PLCs ultrarrápidos."
            }
        ]
    },
    "fanuc": {
        "slug": "fanuc.html",
        "title": "Refacciones Fanuc Robótica y CNC México | Servomotores, Teach Pendants, Drives",
        "h1": "Refacciones de Robótica Industrial y Control Numérico Fanuc en México",
        "meta_desc": "Suministro de refacciones Fanuc en México: servomotores A06B, teach pendants A05B, controladores R-30iA, R-30iB, fuentes A16B y tarjetas A03B. Catálogo con entrega inmediata y refacciones descontinuadas con envío a todo México.",
        "brand_name": "Fanuc",
        "brand_logo": "../assets/img/marca-fanuc.png",
        "hero_desc": "Apoyamos a las plantas de manufactura en México a mantener sus celdas robóticas Fanuc en operación continua. Suministramos refacciones mecánicas y electrónicas originales: servomotores Alpha i, tarjetas de control de ejes, teach pendants para controladores R-30iA y R-30iB, y fuentes conmutadas para mantener la continuidad operativa de tus procesos.",
        "families": [
            {
                "name": "Servomotores y Servodrives Alpha i",
                "prefixes": ["A06B-0235", "A06B-0143", "A06B-6114", "A06B-6117", "A06B-6134"],
                "desc": "Motores de corriente alterna de alta precisión con codificador Pulsecoder, módulos amplificadores de potencia SVM, SVM mono y multi-eje para robots y centros de maquinado CNC."
            },
            {
                "name": "Teach Pendants e Interfaces de Operador",
                "prefixes": ["A05B-2255-C101", "A05B-2256-C100", "A05B-2301", "A05B-2518"],
                "desc": "Consolas de programación táctil con display a color, pulsador de validación de 3 posiciones (deadman switch) y cables reforzados de conexión directa al gabinete del robot."
            },
            {
                "name": "Tarjetas Principales y Fuentes de Poder",
                "prefixes": ["A16B-1212", "A16B-2200", "A16B-3200", "A03B-0819", "A20B-2101"],
                "desc": "Placas base (Mainboards), fuentes de alimentación para chasis de control R-30iA y R-30iB, y módulos de comunicación DeviceNet, Profinet y Ethernet/IP."
            },
            {
                "name": "Consumibles Mecánicos y Cables Robóticos",
                "prefixes": ["Cables de Eje Fanuc", "Baterías de Respaldo Litio 3V", "Grasas Especiales VIGO", "Sellos de Muñeca"],
                "desc": "Baterías de memoria para encoder, arneses de cableado flexible para brazo articulado, sellos mecánicos y lubricantes sintéticos recomendados por fabricante para robots M-10i, M-20i y R-2000i."
            }
        ]
    },
    "mitsubishi": {
        "slug": "mitsubishi.html",
        "title": "Mitsubishi Electric Automatización México | PLCs MELSEC, Variadores FR, HMIs GOT",
        "h1": "Suministro de Automatización Industrial Mitsubishi Electric en México",
        "meta_desc": "Distribución y suministro de equipo Mitsubishi Electric en México: PLCs MELSEC Serie FX3U, FX5U, serie Q, variadores de frecuencia FR-D700, FR-E700, FR-A800 y pantallas GOT2000. Envío express.",
        "brand_name": "Mitsubishi Electric",
        "brand_logo": "../assets/img/marca-mitsubishi.png",
        "hero_desc": "Soluciones completas de control y movimiento industrial con tecnología Mitsubishi Electric. Mantenemos a disposición de la industria mexicana controladores lógicos programables compactos y modulares (MELSEC FX y Q), servomotores MelServo MR-J4 y variadores de frecuencia para bombas, transportadores y extrusoras.",
        "families": [
            {
                "name": "Controladores Programables MELSEC Serie FX & iQ-F",
                "prefixes": ["FX3U-32MT/ES", "FX3U-64MR/ES", "FX5U-32MR", "FX5U-64MT", "FX2N-16EX", "FX3G-24MT"],
                "desc": "PLCs compactos de alta velocidad con entradas de conteo rápido integradas, módulos de ampliación de relevador y transistor, y comunicación Ethernet nativa en serie FX5U."
            },
            {
                "name": "Sistemas Modulares MELSEC Serie Q & iQ-R",
                "prefixes": ["Q03UDECPU", "Q06UDEHCPU", "QX40", "QY10", "Q64AD", "QJ71E71-100"],
                "desc": "Controladores de alta capacidad para líneas de producción continuas, con módulos de bus multiprocesador, entradas analógicas aisladas y módulos de red CC-Link y Modbus."
            },
            {
                "name": "Variadores de Frecuencia Inverter FR",
                "prefixes": ["FR-D720-042-NA", "FR-D740-050-NA", "FR-E740-060-SC", "FR-A840-00126", "FR-F800"],
                "desc": "Drives de control de par vectorial sin sensor, diseño compacto con perilla de ajuste M-Dial, funciones de ahorro de energía y frenado dinámico regenerativo."
            },
            {
                "name": "Interfaces de Operador GOT & Servomotores MelServo",
                "prefixes": ["GT2710-VTBA", "GT2508-VTBD", "GT2104-RTBD", "MR-J4-40B", "MR-J4-100A", "HG-KR43"],
                "desc": "Pantallas táctiles industriales GOT2000 con retroiluminación LED de alta definición, y sistemas servoacoplados MR-J4 con encoders absolutos de 22 bits."
            }
        ]
    },
    "control-y-sensores": {
        "slug": "control-y-sensores.html",
        "title": "Control, Sensores e Instrumentación Multimarca México | Suministro Industrial Urgente",
        "h1": "Sensores, Neumática y Control Eléctrico Multimarca en México",
        "meta_desc": "Suministro multimarca de componentes industriales: SMC neumática, Finder relevadores, Autonics, Banner, Carlo Gavazzi, ABB interruptores, Celduc estado sólido y sensores de proximidad. Cotizaciones urgentes.",
        "brand_name": "Control y Sensores",
        "brand_logo": "../assets/img/equipo-sensores-proximidad.png",
        "hero_desc": "Centralizamos las necesidades de refaccionamiento eléctrico, neumático y de sensórica para plantas de manufactura en México. Trabajamos con fabricantes de clase mundial como SMC, ABB, Finder, Celduc, Autonics, Honeywell, Carlo Gavazzi, Banner y más. Catálogo con entrega inmediata, entregas consolidadas y facturación fiscal CFDI 4.0.",
        "families": [
            {
                "name": "Neumática y Válvulas Industriales (SMC y Festo)",
                "prefixes": ["SMC SY3A0R", "SMC AC20-N02G", "SMC cxsm25-100", "Reguladores de Flujo", "Manguera Poliuretano PU"],
                "desc": "Electroválvulas 5/2 y 5/3 mono y biestables, unidades de mantenimiento de aire comprimido (FRL), cilindros neumáticos guiados y conectores rápidos push-in."
            },
            {
                "name": "Relevación y Estado Sólido (Finder & Celduc)",
                "prefixes": ["Finder 55.34.9.024.0040", "Celduc SOB945360", "Celduc SOB945660", "Relevadores Tipo Clema"],
                "desc": "Relevadores electromecánicos industriales encapsulados con base octal o undecal, relevadores de estado sólido (SSR) de alta corriente para calentadores y resistencias industriales."
            },
            {
                "name": "Detección, Proximidad y Medición (Autonics, Banner, Carlo Gavazzi)",
                "prefixes": ["PRW12-4DP", "Q85VR3DL", "CA30CAN25NA", "UK6A-D2-0A", "BZE6-2RN"],
                "desc": "Sensores inductivos M12/M18 de alta inmunidad al ruido, fotoceldas multiajuste de largo alcance, sensores capacitivos para nivel de granos y líquidos, y microswitches mecánicos para uso rudo."
            },
            {
                "name": "Maniobra, Seccionamiento y Distribución (ABB y Gabinetes)",
                "prefixes": ["ABB OT100F3", "ABB OXS6X330", "ABB OHBS2AJ1", "Fusibles Cerámicos 10x38", "Gabinetes NEMA"],
                "desc": "Interruptores seccionadores bajo carga de 3 polos, varillas de mando y manijas con bloqueo por candado para cumplimiento de normativas de seguridad LOTO."
            }
        ]
    }
}
