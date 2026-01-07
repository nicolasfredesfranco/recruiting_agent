#!/usr/bin/env python3
"""
Demo sin login - Muestra las capacidades de automatización del navegador
"""

import time
import random
from playwright.sync_api import sync_playwright

def demo_browser_control():
    """Demuestra control del navegador y mouse sin necesitar login a LinkedIn"""
    
    print("\n" + "="*70)
    print("🎮 DEMO: CONTROL DE NAVEGADOR Y AUTOMATIZACIÓN")
    print("="*70)
    print("Esta demo te mostrará las capacidades de automatización:")
    print("  • Apertura de navegador visible")
    print("  • Control automático del mouse y clicks")
    print("  • Navegación automática")
    print("  • Scroll y movimientos naturales")
    print("  • Captura de elementos de la página")
    print("="*70 + "\n")
    
    input("Presiona ENTER para comenzar la demostración...")
    
    print("\n🚀 Iniciando navegador Chrome...\n")
    
    with sync_playwright() as p:
        # Abrir navegador en modo visible
        browser = p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        
        # Script anti-detección
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        page = context.new_page()
        
        print("✅ Navegador Chrome abierto (visible)")
        print("✅ Configuración anti-detección aplicada\n")
        
        # Demo 1: Navegar a un sitio público
        print("=" * 70)
        print("DEMO 1: Navegación Automatizada")
        print("=" * 70)
        print("🌐 Navegando a LinkedIn (página pública)...\n")
        
        page.goto("https://www.linkedin.com", wait_until="networkidle")
        print("✓ Navegación completada")
        print(f"✓ URL actual: {page.url}\n")
        time.sleep(2)
        
        # Demo 2: Scroll automático
        print("=" * 70)
        print("DEMO 2: Control de Scroll (Movimiento Natural)")
        print("=" * 70)
        print("📜 Haciendo scroll hacia abajo suavemente...\n")
        
        for i in range(3):
            scroll_amount = random.randint(300, 500)
            page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            print(f"  ↓ Scroll {i+1}: {scroll_amount}px")
            time.sleep(random.uniform(0.5, 1.0))
        
        print("\n📜 Volviendo al inicio...\n")
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(1)
        
        # Demo 3: Detectar elementos
        print("=" * 70)
        print("DEMO 3: Detección de Elementos en la Página")
        print("=" * 70)
        print("🔍 Buscando elementos en la página...\n")
        
        # Buscar links
        links = page.query_selector_all('a')
        print(f"✓ Encontrados {len(links)} enlaces en la página")
        
        # Buscar botones
        buttons = page.query_selector_all('button')
        print(f"✓ Encontrados {len(buttons)} botones en la página")
        
        # Buscar imágenes
        images = page.query_selector_all('img')
        print(f"✓ Encontradas {len(images)} imágenes en la página\n")
        
        time.sleep(2)
        
        # Demo 4: Hover y movimiento de mouse
        print("=" * 70)
        print("DEMO 4: Control del Mouse (Hover)")
        print("=" * 70)
        print("🖱️  Moviendo el mouse sobre elementos...\n")
        
        # Intentar hacer hover en algunos elementos
        if buttons:
            try:
                # Hover en el primer botón visible
                button = buttons[0]
                button.scroll_into_view_if_needed()
                button.hover()
                print("✓ Mouse posicionado sobre un botón")
                time.sleep(1)
            except:
                print("⚠️  Algunos elementos requieren autenticación")
        
        time.sleep(2)
        
        # Demo 5: Captura de screenshot
        print("\n=" * 70)
        print("DEMO 5: Captura de Pantalla")
        print("=" * 70)
        print("📸 Capturando screenshot de la página...\n")
        
        screenshot_path = "downloads/linkedin_demo_screenshot.png"
        page.screenshot(path=screenshot_path)
        print(f"✓ Screenshot guardado en: {screenshot_path}\n")
        
        # Demo 6: Navegación a perfil público
        print("=" * 70)
        print("DEMO 6: Navegación a Perfil Público")
        print("=" * 70)
        print("🔍 Navegando al perfil de Sebastian Torres...\n")
        
        profile_url = "https://www.linkedin.com/in/sebastian-torres-c/"
        page.goto(profile_url, wait_until="domcontentloaded")
        print(f"✓ Navegado a: {profile_url}")
        time.sleep(3)
        
        # Nota sobre el login wall
        current_url = page.url
        if 'authwall' in current_url or 'login' in current_url:
            print("\n⚠️  LinkedIn muestra un 'login wall' para perfiles")
            print("   Esto es normal y es por eso que el scraper requiere login manual")
            print("   Una vez logueado, el sistema puede:")
            print("     • Navegar libremente a cualquier perfil")
            print("     • Extraer información")
            print("     • Generar PDFs\n")
        else:
            print("✓ Perfil cargado (sin login wall)\n")
            
        time.sleep(2)
        
        # Demo 7: Generar PDF
        print("=" * 70)
        print("DEMO 7: Generación de PDF")
        print("=" * 70)
        print("📄 Generando PDF de la página actual...\n")
        
        pdf_path = "downloads/linkedin_demo_page.pdf"
        page.pdf(path=pdf_path, format='A4')
        print(f"✓ PDF generado: {pdf_path}\n")
        
        # Resumen final
        print("=" * 70)
        print("✅ DEMO COMPLETADA")
        print("=" * 70)
        print("\nLo que has visto:")
        print("  ✓ Navegador Chrome controlado automáticamente")
        print("  ✓ Navegación a páginas web")
        print("  ✓ Scroll automático con movimientos naturales")
        print("  ✓ Detección de elementos (links, botones, imágenes)")
        print("  ✓ Control del mouse (hover)")
        print("  ✓ Captura de screenshots")
        print("  ✓ Generación de PDFs")
        print("\nCON LOGIN A LINKEDIN, el sistema puede:")
        print("  🎯 Navegar a cualquier perfil")
        print("  🎯 Interactuar con botones y menús")
        print("  🎯 Descargar CVs completos como PDF")
        print("  🎯 Procesar múltiples perfiles con delays anti-detección")
        print("\n📁 Archivos generados en la carpeta 'downloads/'")
        print("="*70 + "\n")
        
        print("🎬 Manteniendo navegador abierto por 10 segundos más...")
        print("   Puedes interactuar manualmente con el navegador si quieres.\n")
        time.sleep(10)
        
        print("🔒 Cerrando navegador...\n")
        browser.close()
    
    print("Demo finalizada. ¡Gracias! 👋\n")


if __name__ == "__main__":
    try:
        demo_browser_control()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrumpida por usuario.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
