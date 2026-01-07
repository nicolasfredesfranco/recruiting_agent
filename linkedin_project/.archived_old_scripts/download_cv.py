#!/usr/bin/env python3
"""
LinkedIn CV Downloader - VERSIÓN EJECUTABLE SIMPLE
Solo ejecuta: python3 download_cv.py
"""

import time
import random
from playwright.sync_api import sync_playwright


def download_linkedin_cv():
    """Función principal - descarga CV de LinkedIn con comportamiento humano"""
    
    print("\n" + "="*70)
    print("🤖 LINKEDIN CV DOWNLOADER")
    print("="*70)
    print("\nEste script descargará CVs de LinkedIn simulando comportamiento humano\n")
    print("="*70)
    
    # Pedir URLs
    print("\n📝 Ingresa las URLs de los perfiles que quieres descargar")
    print("   (Una por línea, línea vacía para terminar)\n")
    
    profiles = []
    while True:
        url = input(f"Perfil #{len(profiles)+1} (o ENTER para continuar): ").strip()
        if not url:
            break
        if 'linkedin.com/in/' in url:
            profiles.append(url)
            print(f"   ✓ Añadido: {url}")
        else:
            print("   ❌ URL inválida, debe contener 'linkedin.com/in/'")
    
    if not profiles:
        print("\n❌ No ingresaste ningún perfil. Saliendo...\n")
        return
    
    print(f"\n📦 Total de perfiles a procesar: {len(profiles)}\n")
    print("="*70)
    
    input("\n✋ Presiona ENTER para comenzar...\n")
    
    # Iniciar automatización
    print("🚀 Iniciando navegador...\n")
    
    with sync_playwright() as p:
        # Navegador visible con anti-detección
        browser = p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0',
            viewport={'width': 1920, 'height': 1080}
        )
        
        # Anti-detección
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = {runtime: {}};
        """)
        
        page = context.new_page()
        
        # Login
        print("🔐 Redirigiendo a LinkedIn...")
        page.goto("https://www.linkedin.com")
        time.sleep(2)
        
        print("\n" + "="*70)
        print("⏸️  PAUSA PARA LOGIN MANUAL")
        print("="*70)
        print("Por favor inicia sesión en LinkedIn")
        print("="*70)
        input("\n✋ Presiona ENTER cuando hayas iniciado sesión...\n")
        
        # Procesar perfiles
        successful = 0
        failed = 0
        
        for i, url in enumerate(profiles, 1):
            print(f"\n{'='*70}")
            print(f"[{i}/{len(profiles)}] Procesando perfil")
            print(f"{'='*70}")
            print(f"🔗 {url}\n")
            
            try:
                # Navegar
                print("1️⃣ Navegando al perfil...")
                page.goto(url, wait_until="domcontentloaded")
                time.sleep(random.uniform(2, 3.5))
                
                # Verificar login
                if 'authwall' in page.url or 'login' in page.url:
                    print("❌ Requiere login\n")
                    failed += 1
                    continue
                
                print("   ✓ Cargado\n")
                
                # Simular lectura
                print("2️⃣ Revisando perfil...")
                time.sleep(random.uniform(1.5, 2.5))
                page.mouse.wheel(0, random.randint(250, 400))
                time.sleep(random.uniform(1.5, 3))
                page.mouse.wheel(0, -random.randint(250, 400))
                time.sleep(random.uniform(0.5, 1))
                print("   ✓ Revisado\n")
                
                # Buscar "More"
                print("3️⃣ Buscando botón 'More'...")
                more = None
                for sel in ['button[aria-label="More actions"]', 'button:has-text("More")', 'button:has-text("Más")']:
                    try:
                        more = page.wait_for_selector(sel, timeout=3000)
                        if more and more.is_visible():
                            break
                    except:
                        pass
                
                if not more:
                    print("❌ No encontrado\n")
                    failed += 1
                    continue
                
                print("   ✓ Encontrado\n")
                
                # Click "More"
                print("4️⃣ Click en 'More'...")
                more.scroll_into_view_if_needed()
                time.sleep(random.uniform(0.5, 1))
                
                box = more.bounding_box()
                if box:
                    x = box['x'] + box['width'] * 0.5
                    y = box['y'] + box['height'] * 0.5
                    page.mouse.move(x, y)
                
                time.sleep(random.uniform(0.2, 0.5))
                more.click()
                print("   ✓ Menú abierto\n")
                time.sleep(random.uniform(0.8, 1.5))
                
                # Buscar "Save to PDF"
                print("5️⃣ Buscando 'Save to PDF'...")
                pdf = None
                for sel in ['div[aria-label="Save to PDF"]', 'text="Save to PDF"', 'text="Guardar como PDF"']:
                    try:
                        pdf = page.wait_for_selector(sel, timeout=3000)
                        if pdf and pdf.is_visible():
                            break
                    except:
                        pass
                
                if not pdf:
                    print("❌ No encontrado\n")
                    failed += 1
                    continue
                
                print("   ✓ Encontrado\n")
                
                # Click "Save to PDF"
                print("6️⃣ Click en 'Save to PDF'...")
                box = pdf.bounding_box()
                if box:
                    x = box['x'] + box['width'] * 0.5
                    y = box['y'] + box['height'] * 0.5
                    page.mouse.move(x, y)
                
                time.sleep(random.uniform(0.2, 0.5))
                pdf.click()
                print("   ✓ Descarga iniciada\n")
                
                # Esperar descarga
                print("7️⃣ Esperando PDF...")
                time.sleep(random.uniform(4, 7))
                
                print("✅ CV descargado\n")
                successful += 1
                
                # Delay entre perfiles
                if i < len(profiles):
                    delay = random.uniform(8, 15)
                    print(f"⏳ Esperando {delay:.1f}s antes del siguiente perfil...\n")
                    time.sleep(delay)
                
            except Exception as e:
                print(f"❌ Error: {e}\n")
                failed += 1
        
        # Resumen
        print("\n" + "="*70)
        print("📊 RESUMEN FINAL")
        print("="*70)
        print(f"✅ Exitosos: {successful}/{len(profiles)}")
        print(f"❌ Fallidos: {failed}/{len(profiles)}")
        print(f"📁 Revisa tu carpeta de Descargas")
        print("="*70 + "\n")
        
        input("Presiona ENTER para cerrar el navegador...\n")
        browser.close()
    
    print("✅ Proceso completado\n")


if __name__ == "__main__":
    try:
        download_linkedin_cv()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido por usuario\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
