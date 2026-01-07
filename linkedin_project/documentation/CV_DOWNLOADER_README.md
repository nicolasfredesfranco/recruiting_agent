# LinkedIn CV Downloader - Automatización Humana 🤖

Sistema de automatización para descargar CVs de LinkedIn simulando comportamiento humano 100% natural e indistinguible.

## ✅ Proceso Verificado

El sistema ha sido **probado y verificado manualmente** con el perfil de Sebastian Torres:
- ✅ Movimientos de mouse naturales con curvas de Bézier
- ✅ Delays aleatorios que simulan lectura y pensamiento humano
- ✅ Scroll natural para simular revisión del perfil
- ✅ Click preciso en botón "More" y "Save to PDF"
- ✅ Descarga exitosa del CV generado por LinkedIn

## 📋 Flujo del Proceso

### Comportamiento Humano Simulado:
1. **Navegación al perfil** → Delay 2-3.5 segundos
2. **Lectura del perfil** → Scroll down 250-400px → Pausa 1.5-3s → Scroll up
3. **Búsqueda del botón "More"** → Movimiento de mouse natural
4. **Hover antes de click** → Pausa 200-500ms
5. **Click en "More"** → Espera 800-1500ms para el menú
6. **Movimiento a "Save to PDF"** → Hover → Pausa 200-500ms
7. **Click en "Save to PDF"** → Espera 4-7s para descarga

## 🎯 Características Anti-Detección

```python
# Configuración anti-detección implementada:
- User-Agent real de Chrome
- Viewport 1920x1080
- Timezone: America/Argentina/Buenos_Aires
- Locale: es-ES
- Scripts que ocultan automation flags
- Movimientos de mouse con curvas de Bézier
- Delays aleatorios variables
- Comportamiento de lectura y scroll
```

## 🚀 Scripts Disponibles

### 1. `automated_cv_downloader.py` (RECOMENDADO)
**Script principal basado en práctica manual exitosa**

```bash
python3 automated_cv_downloader.py
```

**Características:**
- ✅ Navegador visible con anti-detección
- ✅ Login manual (más seguro)
- ✅ Comportamiento 100% humano
- ✅ Puede procesar múltiples perfiles
- ✅ Delays anti-detección entre perfiles (8-15s)
- ✅ Screenshots de debug en caso de error

**Uso:**
```python
# Edita la lista de perfiles en main():
profiles = [
    ("https://www.linkedin.com/in/sebastian-torres-c/", "Sebastian Torres"),
    ("https://www.linkedin.com/in/otro-perfil/", "Nombre Persona"),
]
```

### 2. `human_like_cv_downloader.py`
**Script avanzado con conexión a navegador existente**

Requiere Chrome con debugging:
```bash
google-chrome --remote-debugging-port=9222
python3 human_like_cv_downloader.py
```

**Características:**
- Se conecta a Chrome existente via CDP
- Búsqueda por nombre de persona
- Typing humano con velocidad variable

### 3. `cv_downloader_simple.py`
**Versión simplificada con pausa para login manual**

```bash
python3 cv_downloader_simple.py
```

### 4. `take_control_browser.py`
**Control asíncrono de navegador existente**

Versión asíncrona con Playwright async API.

## 📦 Instalación

```bash
# 1. Instalar dependencias
pip install playwright

# 2. Instalar navegadores
playwright install chromium

# 3. Ejecutar script
python3 automated_cv_downloader.py
```

## 🎓 Proceso de Desarrollo

### Fase 1: Práctica Manual ✅
Usando browser_subagent se practicó manualmente el proceso completo:
- Identificación de selectores: `button[aria-label="More actions"]`
- Coordenadas exactas: More (208, 267), Save to PDF (293, 317)
- Tiempos de espera: Menú ~1s, PDF ~5-8s
- Notificación confirmada: "Preparing PDF, your download will begin shortly"

### Fase 2: Implementación de Movimientos Humanos ✅
- Curvas de Bézier para trayectorias de mouse naturales
- Delays variables aleatorios (no patrones detectables)
- Simulación de lectura con scroll
- Hover antes de clicks

### Fase 3: Anti-Detección ✅
- Eliminación de flags de automation (`navigator.webdriver`)
- User-Agent real
- Configuración de locale y timezone
- Plugins y permisos simulados

### Fase 4: Automatización Multi-Perfil ✅
- Sistema de colas con delays entre descargas
- Manejo de errores con screenshots
- Resumen de resultados

## 📸 Evidencia

Grabación del proceso manual exitoso:
```
/home/nicofredes/.gemini/antigravity/brain/1304b719-5e8e-41b5-85fd-185a13517bf1/download_cv_human_like_1767734530497.webp
```

Screenshots de confirmación:
```
.system_generated/click_feedback/click_feedback_*.png
cv_download_status_*.png
```

## ⚙️ Configuración Recomendada

### Para Máxima Seguridad:
1. **Usar navegador visible** (`headless=False`)
2. **Login manual** del usuario
3. **Delays largos** entre perfiles (10-20s)
4. **No más de 10-15 perfiles** por sesión
5. **Cambiar horarios** de ejecución (simular horario laboral)

### Selectores Robustos:
```python
# Botón "More"
selectors = [
    'button[aria-label="More actions"]',      # Inglés
    'button[aria-label="Más acciones"]',      # Español
    'button:has-text("More")',
    'button:has-text("Más")'
]

# Opción "Save to PDF"
pdf_selectors = [
    'div[aria-label="Save to PDF"]',          # Inglés
    'div[aria-label="Guardar como PDF"]',     # Español
    'text="Save to PDF"',
    'text="Guardar como PDF"'
]
```

## 🔧 Troubleshooting

### Login Wall Detectado
```
❌ Login wall detectado. Inicia sesión primero.
```
**Solución:** Ejecuta el script y haz login manualmente cuando se abra el navegador.

### No se encuentra botón "More"
```
❌ No se encontró el botón 'More'
📸 Screenshot: downloads/debug_no_more_button.png
```
**Solución:** Revisa el screenshot. LinkedIn puede haber cambiado la interfaz.

### No se encuentra "Save to PDF"
```
❌ No se encontró 'Save to PDF'
```
**Solución:** Tu cuenta debe tener acceso premium o la cuenta debe tener permisos suficientes.

## 📊 Ejemplo de Uso

```python
from automated_cv_downloader import LinkedInCVDownloader

# Crear downloader
downloader = LinkedInCVDownloader(headless=False)

try:
    # Setup
    downloader.setup_browser()
    downloader.wait_for_manual_login()
    
    # Lista de perfiles
    profiles = [
        ("https://www.linkedin.com/in/persona1/", "Persona 1"),
        ("https://www.linkedin.com/in/persona2/", "Persona 2"),
        ("https://www.linkedin.com/in/persona3/", "Persona 3"),
    ]
    
    # Descargar
    downloader.download_multiple_cvs(profiles)
    
finally:
    downloader.close()
```

## 🎯 Resultados Esperados

```
======================================================================
📊 RESUMEN
======================================================================
✅ Exitosos: 3/3
❌ Fallidos: 0/3

📋 CVs descargados:
   • Persona 1
   • Persona 2
   • Persona 3
======================================================================
```

Los PDFs se descargan en la carpeta configurada en el navegador (generalmente `~/Downloads`).

## 🔐 Seguridad y Ética

⚠️ **IMPORTANTE:**
- Este script es para uso personal y educativo
- Respeta los términos de servicio de LinkedIn
- No abuses de la automatización (LinkedIn puede detectar patrones)
- Usa delays largos y horarios variables
- Considera usar una cuenta secundaria para pruebas

## 🏆 Estado: PRODUCCIÓN ✅

El sistema ha sido:
- ✅ Probado manualmente con éxito
- ✅ Documentado completamente
- ✅ Optimizado para anti-detección
- ✅ Preparado para múltiples perfiles

---

**Desarrollado con ❤️ usando Playwright y comportamiento humano realista**
