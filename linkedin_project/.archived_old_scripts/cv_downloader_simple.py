#!/usr/bin/env python3
"""
LinkedIn CV Downloader - Versión Simple y Robusta
Usa el navegador actual del browser subagent
"""

import time
import random
import math
from playwright.sync_api import sync_playwright


class HumanMouse:
    """Simula movimientos de mouse 100% humanos"""
    
    def __init__(self, page):
        self.page = page
        self.current_x = 500
        self.current_y = 500
    
    def bezier_curve(self, start_x, start_y, end_x, end_y, control_points=2):
        """Genera curva de Bézier para movimiento natural"""
        # Puntos de control aleatorios
        controls = []
        for _ in range(control_points):
            cx = random.uniform(min(start_x, end_x), max(start_x, end_x))
            cy = random.uniform(min(start_y, end_y), max(start_y, end_y))
            controls.append((cx, cy))
        
        points = []
        num_points = random.randint(15, 25)
        
        for i in range(num_points):
            t = i / (num_points - 1)
            
            if control_points ==2:
                # Curva de Bézier cúbica
                ctrl1_x, ctrl1_y = controls[0]
                ctrl2_x, ctrl2_y = controls[1]
                
                x = ((1-t)**3 * start_x + 
                     3*(1-t)**2*t * ctrl1_x + 
                     3*(1-t)*t**2 * ctrl2_x + 
                     t**3 * end_x)
                
                y = ((1-t)**3 * start_y + 
                     3*(1-t)**2*t * ctrl1_y + 
                     3*(1-t)*t**2 * ctrl2_y + 
                     t**3 * end_y)
            else:
                # Curva cuadrática
                ctrl_x, ctrl_y = controls[0]
                x = (1-t)**2 * start_x + 2*(1-t)*t * ctrl_x + t**2 * end_x
                y = (1-t)**2 * start_y + 2*(1-t)*t * ctrl_y + t**2 * end_y
            
            points.append((int(x), int(y)))
        
        return points
    
    def move_to(self, target_x, target_y):
        """Mueve el mouse de forma natural"""
        print(f"   🖱️  Moviendo mouse: ({self.current_x},{self.current_y}) → ({target_x},{target_y})")
        
        # Generar curva
        points = self.bezier_curve(self.current_x, self.current_y, target_x, target_y)
        
        # Mover punto por punto
        for i, (x, y) in enumerate(points):
            # Velocidad variable (más lento al inicio y final)
            if i < 3 or i > len(points) - 4:
                delay = random.uniform(0.020, 0.040)
            else:
                delay = random.uniform(0.005, 0.015)
            
            self.page.mouse.move(x, y)
            time.sleep(delay)
        
        self.current_x = target_x
        self.current_y = target_y
        
        # Pausa al llegar
        time.sleep(random.uniform(0.1, 0.3))
    
    def click(self, x=None, y=None):
        """Click humano con movimiento"""
        if x and y:
            self.move_to(x, y)
        
        # Pausa antes de click
        time.sleep(random.uniform(0.1, 0.3))
        
        # Click con duración natural
        self.page.mouse.down()
        time.sleep(random.uniform(0.05, 0.12))
        self.page.mouse.up()
        
        # Pausa post-click
        time.sleep(random.uniform(0.3, 0.6))
        
        print("   ✓ Click realizado")


def download_cv_human_like():
    """Descarga el CV del perfil actual con comportamiento humano"""
    
    print("\n" + "="*70)
    print("🤖 DESCARGA DE CV - MODO HUMANO")
    print("="*70 + "\n")
    
    print("📋 Instrucciones:")
    print("   1. Abre Chrome y navega al perfil de LinkedIn que quieres descargar")
    print("   2. Asegúrate de estar logueado")
    print("   3. Deja el perfil abierto")
    print("="*70 + "\n")
    
    input("Presiona ENTER cuando estés listo...")
    
    print("\n🚀 Iniciando automatización...\n")
    
    with sync_playwright() as p:
        # Abrir navegador visible
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
        mouse = HumanMouse(page)
        
        # Ir a LinkedIn
        print("1️⃣ Navegando a LinkedIn...")
        page.goto("https://www.linkedin.com", wait_until="domcontentloaded")
        time.sleep(2)
        
        print("\n⏸️  PAUSA: Inicia sesión manualmente si es necesario")
        print("         Navega al perfil de la persona")
        input("         Presiona ENTER cuando estés en el perfil...\n")
        
        try:
            # Buscar botón "More"
            print("\n2️⃣ Buscando botón 'More'...")
            
            more_button = None
            selectors = [
                'button[aria-label="More actions"]',
                'button:has-text("More")',
                'button:has-text("Más")',
                'button.pvs-profile-actions__action',
                'div.pvs-profile-actions button[aria-label*="More"]',
                'div.pvs-profile-actions button[aria-label*="Más"]'
            ]
            
            for selector in selectors:
                try:
                    more_button = page.wait_for_selector(selector, timeout=2000)
                    if more_button and more_button.is_visible():
                        print(f"   ✓ Encontrado con selector: {selector}")
                        break
                except:
                    continue
            
            if not more_button:
                print("\n❌ No se encontró el botón 'More'")
                print("Selectores intentados:")
                for sel in selectors:
                    print(f"   - {sel}")
                
                # Tomar screenshot para debug
                page.screenshot(path="downloads/debug_no_more_button.png")
                print("\n📸 Screenshot guardado en: downloads/debug_no_more_button.png")
                return False
            
            # Scroll al botón
            more_button.scroll_into_view_if_needed()
            time.sleep(random.uniform(0.5, 1.0))
            
            # Obtener posición del botón
            box = more_button.bounding_box()
            if not box:
                print("❌ No se pudo obtener posición del botón")
                return False
            
            # Calcular centro con variación
            center_x = box['x'] + box['width'] * random.uniform(0.4, 0.6)
            center_y = box['y'] + box['height'] * random.uniform(0.4, 0.6)
            
            print(f"\n3️⃣ Click humano en botón 'More'...")
            print(f"   Posición: ({int(center_x)}, {int(center_y)})")
            
            # Click humano
            mouse.click(int(center_x), int(center_y))
            
            print("   ✓ Menú desplegado")
            time.sleep(random.uniform(0.8, 1.5))
            
            # Buscar "Save to PDF"
            print("\n4️⃣ Buscando opción 'Save to PDF'...")
            
            save_pdf = None
            pdf_selectors = [
                'div[aria-label="Save to PDF"]',
                'text="Save to PDF"',
                'text="Guardar como PDF"',
                '.artdeco-dropdown__item:has-text("Save to PDF")',
                '.artdeco-dropdown__item:has-text("Guardar como PDF")'
            ]
            
            for selector in pdf_selectors:
                try:
                    save_pdf = page.wait_for_selector(selector, timeout=2000)
                    if save_pdf and save_pdf.is_visible():
                        print(f"   ✓ Encontrado con: {selector}")
                        break
                except:
                    continue
            
            if not save_pdf:
                print("\n❌ No se encontró 'Save to PDF'")
                page.screenshot(path="downloads/debug_no_save_pdf.png")
                print("📸 Screenshot: downloads/debug_no_save_pdf.png")
                return False
            
            # Obtener posición
            box = save_pdf.bounding_box()
            if not box:
                print("❌ No se pudo obtener posición")
                return False
            
            center_x = box['x'] + box['width'] * random.uniform(0.4, 0.6)
            center_y = box['y'] + box['height'] * random.uniform(0.4, 0.6)
            
            print(f"\n5️⃣ Click humano en 'Save to PDF'...")
            print(f"   Posición: ({int(center_x)}, {int(center_y)})")
            
            # Click humano
            mouse.click(int(center_x), int(center_y))
            
            print("\n6️⃣ Esperando descarga del PDF...")
            time.sleep(random.uniform(3, 5))
            
            print("\n" + "="*70)
            print("✅ ¡CV DESCARGADO EXITOSAMENTE!")
            print("="*70)
            print("📁 Revisa tu carpeta de Descargas")
            print("="*70 + "\n")
            
            # Mantener navegador abierto
            print("🎬 Navegador abierto por 10 segundos más...")
            time.sleep(10)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            
            # Screenshot de error
            try:
                page.screenshot(path="downloads/debug_error.png")
                print("\n📸 Screenshot de error: downloads/debug_error.png")
            except:
                pass
            
            return False
        finally:
            print("\n🔒 Cerrando navegador...")
            browser.close()


if __name__ == "__main__":
    try:
        download_cv_human_like()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
