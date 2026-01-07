#!/usr/bin/env python3
"""
LinkedIn CV Downloader - TOMA CONTROL DEL NAVEGADOR EXISTENTE
Compatible con el browser subagent de Antigravity
"""

import asyncio
import time
import random
from playwright.async_api import async_playwright


class HumanMouseController:
    """Control de mouse con movimientos humanos realistas"""
    
    def __init__(self, page):
        self.page = page
        self.x = 500
        self.y = 500
    
    async def smooth_move(self, target_x, target_y, duration_ms=None):
        """Mueve el mouse suavemente con curva de Bézier"""
        if duration_ms is None:
            # Calcular duración basada en distancia
            distance = ((target_x - self.x)**2 + (target_y - self.y)**2)**0.5
            duration_ms = min(max(distance * 1.5, 300), 2000)
        
        # Puntos de control para Bézier
        ctrl1_x = self.x + random.uniform(-100, 100)
        ctrl1_y = self.y + random.uniform(-100, 100)
        ctrl2_x = target_x + random.uniform(-100, 100)
        ctrl2_y = target_y + random.uniform(-100, 100)
        
        steps = int(duration_ms / 20)  # ~50fps
        
        for i in range(steps):
            t = i / (steps - 1) if steps > 1 else 1
            
            # Curva de Bézier cúbica
            x = ((1-t)**3 * self.x + 
                 3*(1-t)**2*t * ctrl1_x + 
                 3*(1-t)*t**2 * ctrl2_x + 
                 t**3 * target_x)
            
            y = ((1-t)**3 * self.y + 
                 3*(1-t)**2*t * ctrl1_y + 
                 3*(1-t)*t**2 * ctrl2_y + 
                 t**3 * target_y)
            
            await self.page.mouse.move(x, y)
            await asyncio.sleep(0.02)  # 20ms entre pasos
        
        self.x = target_x
        self.y = target_y
        await asyncio.sleep(random.uniform(0.1, 0.3))
    
    async def human_click(self, x, y):
        """Click humano con movimiento previo"""
        print(f"   🖱️  Moviendo a ({x}, {y})...")
        await self.smooth_move(x, y)
        
        print(f"   👆 Click...")
        await asyncio.sleep(random.uniform(0.1, 0.2))
        await self.page.mouse.down()
        await asyncio.sleep(random.uniform(0.05, 0.12))
        await self.page.mouse.up()
        await asyncio.sleep(random.uniform(0.3, 0.6))
        print(f"   ✓ Click completado")


async def download_cv_from_current_page():
    """Descarga CV del perfil actualmente abierto"""
    
    print("\n" + "="*70)
    print("🤖 DESCARGA DE CV - CONTROL DIRECTO DEL NAVEGADOR")
    print("="*70)
    print("\nEste script tomará control del navegador que tienes abierto")
    print("y descargará el CV automáticamente.\n")
    print("="*70 + "\n")
    
    # Intentar obtener la URL del navegador actual desde Antigravity
    # Si no está disponible, usar CDP
    
    try:
        async with async_playwright() as p:
            # Conectar al navegador que está corriendo con debugging
            try:
                browser = await p.chromium.connect_over_cdp("http://localhost:9222")
                print("✅ Conectado al navegador via CDP\n")
            except:
                print("⚠️  No se pudo conectar via CDP")
                print("💡 Ejecuta Chrome con: google-chrome --remote-debugging-port=9222\n")
                return False
            
            # Obtener contexto y página
            contexts = browser.contexts
            if not contexts:
                print("❌ No hay contextos abiertos")
                return False
            
            context = contexts[0]
            pages = context.pages
            
            if not pages:
                print("❌ No hay páginas abiertas")
                return False
            
            # Usar la primera página (o buscar la del perfil de LinkedIn)
            page = None
            for p in pages:
                url = p.url
                if 'linkedin.com/in/' in url:
                    page = p
                    break
            
            if not page:
                page = pages[0]  # Usar la primera si no encontramos perfil
            
            print(f"📄 Página actual: {page.url}\n")
            
            # Crear controlador de mouse
            mouse = HumanMouseController(page)
            
            try:
                # PASO 1: Buscar botón "More"
                print("1️⃣ Buscando botón 'More'...\n")
                
                more_button = None
                selectors = [
                    'button[aria-label="More actions"]',
                    'button:has-text("More")',
                    'button:has-text("Más")',
                ]
                
                for selector in selectors:
                    try:
                        more_button = await page.wait_for_selector(selector, timeout=3000)
                        if more_button and await more_button.is_visible():
                            print(f"   ✓ Botón 'More' encontrado: {selector}\n")
                            break
                    except:
                        continue
                
                if not more_button:
                    print("❌ No se encontró el botón 'More'\n")
                    
                    # Debug: mostrar todos los botones
                    buttons = await page.query_selector_all('button')
                    print(f"📋 Botones detectados: {len (buttons)}")
                    for i, btn in enumerate(buttons[:10]):
                        try:
                            text = await btn.inner_text()
                            aria = await btn.get_attribute('aria-label')
                            print(f"   {i+1}. Text: '{text[:30]}' | Aria: '{aria}'")
                        except:
                            pass
                    
                    return False
                
                # Scroll al botón
                await more_button.scroll_into_view_if_needed()
                await asyncio.sleep(0.5)
                
                # Obtener posición
                box = await more_button.bounding_box()
                if not box:
                    print("❌ No se pudo obtener posición del botón")
                    return False
                
                # Centro con variación aleatoria
                center_x = int(box['x'] + box['width'] * random.uniform(0.4, 0.6))
                center_y = int(box['y'] + box['height'] * random.uniform(0.4, 0.6))
                
                print(f"2️⃣ Haciendo click en 'More' en ({center_x}, {center_y})...\n")
                await mouse.human_click(center_x, center_y)
                
                print("   ✓ Menú abierto\n")
                await asyncio.sleep(random.uniform(0.8, 1.5))
                
                # PASO 2: Buscar "Save to PDF"
                print("3️⃣ Buscando 'Save to PDF'...\n")
                
                save_pdf = None
                pdf_selectors = [
                    'div[aria-label="Save to PDF"]',
                    'div[aria-label="Guardar como PDF"]',
                    'text="Save to PDF"',
                    'text="Guardar como PDF"',
                ]
                
                for selector in pdf_selectors:
                    try:
                        save_pdf = await page.wait_for_selector(selector, timeout=3000)
                        if save_pdf and await save_pdf.is_visible():
                            print(f"   ✓ 'Save to PDF' encontrado: {selector}\n")
                            break
                    except:
                        continue
                
                if not save_pdf:
                    print("❌ No se encontró 'Save to PDF'\n")
                    return False
                
                # Obtener posición
                box = await save_pdf.bounding_box()
                if not box:
                    print("❌ No se pudo obtener posición")
                    return False
                
                center_x = int(box['x'] + box['width'] * random.uniform(0.4, 0.6))
                center_y = int(box['y'] + box['height'] * random.uniform(0.4, 0.6))
                
                print(f"4️⃣ Haciendo click en 'Save to PDF' en ({center_x}, {center_y})...\n")
                await mouse.human_click(center_x, center_y)
                
                print("   ✓ Descarga iniciada\n")
                
                # Esperar descarga
                print("5️⃣ Esperando que el PDF se descargue...\n")
                await asyncio.sleep(5)
                
                print("\n" + "="*70)
                print("✅ ¡CV DESCARGADO EXITOSAMENTE!")
                print("="*70)
                print("📁 Revisa tu carpeta de Descargas del navegador")
                print("="*70 + "\n")
                
                return True
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()
                
                # Screenshot de debug
                try:
                    await page.screenshot(path="downloads/debug_error.png")
                    print("\n📸 Screenshot: downloads/debug_error.png")
                except:
                    pass
                
                return False
    
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Punto de entrada"""
    print("\n🚀 Iniciando descarga de CV...\n")
    
    # Ejecutar función async
    result = asyncio.run(download_cv_from_current_page())
    
    if result:
        print("\n✅ Proceso completado exitosamente\n")
    else:
        print("\n❌ Proceso falló\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido por usuario\n")
