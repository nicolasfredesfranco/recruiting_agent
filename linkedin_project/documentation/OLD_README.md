# LinkedIn CV Scraper

Sistema automatizado para descargar perfiles de LinkedIn como CVs en formato PDF usando Playwright.

## ⚠️ Advertencia Legal

Este proyecto es solo para fines educacionales y de investigación. El web scraping de LinkedIn puede violar sus Términos de Servicio. Úsalo bajo tu propio riesgo y responsabilidad. Se recomienda:

- Usar solo para perfiles públicos
- Limitar el número de descargas
- Agregar delays entre requests
- Considerar usar la API oficial de LinkedIn para uso en producción

## 🚀 Instalación

### 1. Instalar dependencias de Python

```bash
cd /home/nicofredes/Desktop/code/jobsity/linkedin_project
pip install -r requirements.txt
```

### 2. Instalar navegadores de Playwright

```bash
playwright install chromium
```

## 📖 Uso

### Ejecución Básica

```bash
python main.py
```

### Flujo de Trabajo

1. **Inicio**: El script te dará la bienvenida y abrirá un navegador Chrome visible
2. **Login Manual**: Se abrirá LinkedIn en el navegador. Debes hacer login manualmente (tienes 120 segundos)
3. **Ingresar URLs**: Después del login, ingresa las URLs de perfiles de LinkedIn
   - Formato: `https://www.linkedin.com/in/nombre-usuario/`
   - Puedes ingresar múltiples URLs (una por línea)
   - Presiona Enter dos veces cuando termines
4. **Descarga**: El sistema descargará automáticamente los CVs
5. **Resultados**: Los PDFs se guardarán en la carpeta `downloads/`

### Ejemplo de URLs

```
Profile #1: https://www.linkedin.com/in/sebastian-torres-c/
Profile #2: https://www.linkedin.com/in/otro-perfil/
Profile #3: [presiona Enter para finalizar]
```

## 📁 Estructura del Proyecto

```
linkedin_project/
├── scraper/
│   ├── __init__.py              # Package initialization
│   ├── browser_manager.py       # Gestión del navegador Playwright
│   ├── linkedin_scraper.py      # Lógica principal de scraping
│   └── utils.py                 # Funciones auxiliares
├── downloads/                   # CVs descargados (se crea automáticamente)
├── requirements.txt             # Dependencias Python
├── main.py                      # Script principal
└── README.md                    # Esta documentación
```

## 🔧 Características

- ✅ **Navegador visible**: Ves todo lo que hace el scraper
- ✅ **Login manual seguro**: Evita detección de bots durante autenticación
- ✅ **Anti-detección**: User agents reales, delays aleatorios, movimientos naturales
- ✅ **Batch download**: Descarga múltiples CVs con delays entre cada uno
- ✅ **Manejo de errores**: Logging detallado y recuperación de errores
- ✅ **PDFs automáticos**: Convierte perfiles a PDF usando funcionalidad del navegador

## 🛠️ Configuración Avanzada

### Usar el scraper programáticamente

```python
from scraper import LinkedInScraper

with LinkedInScraper(download_path="downloads", headless=False) as scraper:
    # Login manual
    scraper.login_manual(wait_time=120)
    
    # Descargar un CV
    scraper.download_cv_as_pdf("https://www.linkedin.com/in/username/")
    
    # O descargar múltiples
    urls = [
        "https://www.linkedin.com/in/profile1/",
        "https://www.linkedin.com/in/profile2/"
    ]
    scraper.batch_download(urls, delay_range=(3, 7))
```

### Modo headless (sin interfaz gráfica)

```python
scraper = LinkedInScraper(headless=True)
```

**Nota**: Modo headless tiene mayor riesgo de detección.

## 🐛 Troubleshooting

### Error: "playwright not found"
```bash
pip install playwright
playwright install chromium
```

### Error: "Login timeout"
- Asegúrate de completar el login en 120 segundos
- Verifica tu conexión a internet
- Intenta de nuevo

### Los PDFs no se descargan
- Verifica que estés logueado correctamente
- Asegúrate de que la URL del perfil sea válida
- Revisa los logs para mensajes de error detallados

### Cuenta bloqueada
- Si LinkedIn bloquea tu cuenta, espera 24-48 horas
- Reduce la frecuencia de scraping
- Usa delays más largos entre descargas

## 📝 Mejores Prácticas

1. **Limita el uso**: No descargues cientos de CVs de una vez
2. **Usa delays**: El sistema ya incluye delays aleatorios (3-7 segundos)
3. **Respeta robots.txt**: Este scraper es para uso personal limitado
4. **Mantén tu sesión**: No hagas logout entre descargas para evitar logins repetidos
5. **Horarios**: Evita scraping en horas pico de LinkedIn

## 🔍 Logging

Los logs se muestran en la consola con el siguiente formato:
```
2026-01-06 17:30:00 - scraper.linkedin_scraper - INFO - Profile loaded successfully
```

## 📄 Licencia

Este proyecto es de código abierto para fines educacionales. Úsalo responsablemente.

## 🤝 Contribuciones

Si encuentras bugs o mejoras, siéntete libre de crear un issue o pull request.

---

**Desarrollado con ❤️ usando Playwright**
