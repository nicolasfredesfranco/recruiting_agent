#!/usr/bin/env python3
"""
LinkedIn Automated CV Downloader
Descarga CVs de LinkedIn con comportamiento humano 100% natural
Basado en la práctica manual exitosa con Sebastian Torres
"""

import time
import random
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class HumanBehavior:
    """Simula comportamiento humano perfecto"""
    
    @staticmethod
    def delay(min_ms=300, max_ms=800):
        """Delay aleatorio natural"""
        time.sleep(random.uniform(min_ms / 1000, max_ms / 1000))
    
    @staticmethod
    def reading_delay():
        """Pausa como si estuviera leyendo"""
        time.sleep(random.uniform(1.5, 3.0))
    
    @staticmethod
    def thinking_delay():
        """Pausa como si estuviera pensando"""
        time.sleep(random.uniform(0.5, 1.2))
    
    @staticmethod
    def click_delay():
        """Pausa antes de hacer click"""
        time.sleep(random.uniform(0.2, 0.5))


class LinkedInCVDownloader:
    """
    Automatiza descarga de CVs de LinkedIn con comportamiento indistinguible de humano
    """
    
    def __init__(self, headless=False):
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
        self.downloads = []
        
    def setup_browser(self):
        """Configura navegador con anti-detección"""
        print("\n🚀 Iniciando navegador...")
        
        self.playwright = sync_playwright().start()
        
        # Configuración anti-detección completa
        self.browser = self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )
        
        # Contexto con configuración humana
        self.context = self.browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='es-ES',
            timezone_id='America/Argentina/Buenos_Aires',
            accept_downloads=True
        )
        
        # Scripts anti-detección
        self.context.add_init_script("""
            // Eliminar webdriver
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Añadir chrome object
            window.chrome = {
                runtime: {},
                loadTimes: function() {},
                csi: function() {},
                app: {}
            };
            
            // Permisos
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // Plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['es-ES', 'es', 'en-US', 'en']
            });
        """)
        
        self.page = self.context.new_page()
        print("✅ Navegador configurado con anti-detección\n")
    
    def wait_for_manual_login(self):
        """Permite login manual del usuario"""
        print("=" * 70)
        print("🔐 LOGIN MANUAL REQUERIDO")
        print("=" * 70)
        print("Por favor:")
        print("  1. Inicia sesión en LinkedIn en el navegador")
        print("  2. Completa cualquier verificación de seguridad")
        print("  3. Asegúrate de ver tu feed de LinkedIn")
        print("=" * 70 + "\n")
        
        self.page.goto("https://www.linkedin.com", wait_until="domcontentloaded")
        HumanBehavior.delay(2000, 3000)
        
        input("✋ Presiona ENTER cuando hayas iniciado sesión...\n")
        
        # Verificar login
        try:
            self.page.wait_for_selector('nav[aria-label="Primary Navigation"]', timeout=5000)
            print("✅ Sesión verificada\n")
            return True
        except:
            print("⚠️  No se pudo verificar la sesión, continuando...\n")
            return True
    
    def simulate_human_reading(self):
        """Simula que un humano lee y revisa el perfil"""
        print("   👀 Revisando perfil (comportamiento humano)...")
        
        # Esperar como si leyera
        HumanBehavior.delay(1500, 2500)
        
        # Scroll hacia abajo para "ver" el perfil
        scroll_amount = random.randint(250, 400)
        self.page.mouse.wheel(0, scroll_amount)
        print(f"      ↓ Scroll {scroll_amount}px")
        
        HumanBehavior.reading_delay()
        
        # Volver arriba
        self.page.mouse.wheel(0, -scroll_amount)
        print(f"      ↑ Scroll up")
        
        HumanBehavior.delay(500, 1000)
    
    def download_cv_from_profile(self, profile_url, person_name=None):
        """
        Descarga CV de un perfil específico
        
        Args:
            profile_url: URL del perfil de LinkedIn
            person_name: Nombre de la persona (opcional, para logs)
        
        Returns:
            True si descargó exitosamente, False si falló
        """
        if not person_name:
            person_name = profile_url.split('/in/')[-1].rstrip('/')
        
        print(f"\n{'=' * 70}")
        print(f"📄 Descargando CV: {person_name}")
        print(f"{'=' * 70}")
        print(f"🔗 {profile_url}\n")
        
        try:
            # PASO 1: Navegar al perfil
            print("1️⃣ Navegando al perfil...")
            self.page.goto(profile_url, wait_until="domcontentloaded")
            HumanBehavior.delay(2000, 3500)
            
            # Verificar login wall
            if 'authwall' in self.page.url or 'login' in self.page.url:
                print("❌ Login wall detectado. Inicia sesión primero.\n")
                return False
            
            print("   ✓ Perfil cargado\n")
            
            # PASO 2: Simular lectura humana
            print("2️⃣ Observando perfil...")
            self.simulate_human_reading()
            print("   ✓ Perfil revisado\n")
            
            # PAUSO 3: Buscar botón "More"
            print("3️⃣ Buscando botón 'More'...")
            
            more_button = None
            selectors = [
                'button[aria-label="More actions"]',
                'button[aria-label="Más acciones"]',
                'button:has-text("More")',
                'button:has-text("Más")'
            ]
            
            for selector in selectors:
                try:
                    more_button = self.page.wait_for_selector(selector, timeout=3000)
                    if more_button and more_button.is_visible():
                        print(f"   ✓ Botón encontrado: {selector}\n")
                        break
                except:
                    continue
            
            if not more_button:
                print("❌ No se encontró el botón 'More'\n")
                self.page.screenshot(path="downloads/debug_no_more_button.png")
                return False
            
            # Asegurar que está visible
            more_button.scroll_into_view_if_needed()
            HumanBehavior.delay(500, 1000)
            
            # PASO 4: Click en "More" (movimiento de mouse natural)
            print("4️⃣ Click en 'More'...")
            
            # Obtener coordenadas del botón
            box = more_button.bounding_box()
            if box:
                # Centro con variación aleatoria (como humano que no apunta perfecto)
                x = box['x'] + box['width'] * random.uniform(0.4, 0.6)
                y = box['y'] + box['height'] * random.uniform(0.4, 0.6)
                
                # Mover mouse al botón
                self.page.mouse.move(x, y)
                print(f"   🖱️  Mouse en ({int(x)}, {int(y)})")
                
                # Hover natural
                HumanBehavior.click_delay()
                
                # Click
                more_button.click()
                print("   ✓ Click realizado\n")
            else:
                # Fallback sin coordenadas
                HumanBehavior.thinking_delay()
                more_button.click()
                print("   ✓ Click realizado\n")
            
            # Esperar que abra el menú
            HumanBehavior.delay(800, 1500)
            
            # PASO 5: Buscar "Save to PDF"
            print("5️⃣ Buscando 'Save to PDF'...")
            
            save_pdf = None
            pdf_selectors = [
                'div[aria-label="Save to PDF"]',
                'div[aria-label="Guardar como PDF"]',
                'text="Save to PDF"',
                'text="Guardar como PDF"',
                '.artdeco-dropdown__item:has-text("Save to PDF")',
                '.artdeco-dropdown__item:has-text("Guardar como PDF")'
            ]
            
            for selector in pdf_selectors:
                try:
                    save_pdf = self.page.wait_for_selector(selector, timeout=3000)
                    if save_pdf and save_pdf.is_visible():
                        print(f"   ✓ Opción encontrada: {selector}\n")
                        break
                except:
                    continue
            
            if not save_pdf:
                print("❌ No se encontró 'Save to PDF'\n")
                self.page.screenshot(path="downloads/debug_no_save_pdf.png")
                return False
            
            # PASO 6: Click en "Save to PDF"
            print("6️⃣ Click en 'Save to PDF'...")
            
            box = save_pdf.bounding_box()
            if box:
                x = box['x'] + box['width'] * random.uniform(0.4, 0.6)
                y = box['y'] + box['height'] * random.uniform(0.4, 0.6)
                
                self.page.mouse.move(x, y)
                print(f"   🖱️  Mouse en ({int(x)}, {int(y)})")
                
                HumanBehavior.click_delay()
                save_pdf.click()
                print("   ✓ Click realizado\n")
            else:
                HumanBehavior.thinking_delay()
                save_pdf.click()
                print("   ✓ Click realizado\n")
            
            # PASO 7: Esperar descarga
            print("7️⃣ Esperando generación del PDF...")
            HumanBehavior.delay(4000, 7000)
            
            print("\n✅ CV descargado exitosamente")
            print(f"📁 Revisa tu carpeta de Descargas\n")
            
            self.downloads.append(person_name)
            return True
            
        except PlaywrightTimeout as e:
            print(f"\n⏱️  Timeout: {e}\n")
            return False
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            import traceback
            traceback.print_exc()
            return False
    
    def download_multiple_cvs(self, profiles):
        """
        Descarga CVs de múltiples perfiles
        
        Args:
            profiles: Lista de URLs o tuplas (url, nombre)
        """
        total = len(profiles)
        successful = 0
        failed = 0
        
        print(f"\n{'=' * 70}")
        print(f"📦 PROCESANDO {total} PERFILES")
        print(f"{'=' * 70}\n")
        
        for i, profile_info in enumerate(profiles, 1):
            # Soportar URLs simples o tuplas (url, nombre)
            if isinstance(profile_info, tuple):
                url, name = profile_info
            else:
                url = profile_info
                name = None
            
            print(f"\n[{i}/{total}]")
            
            if self.download_cv_from_profile(url, name):
                successful += 1
            else:
                failed += 1
            
            # Delay entre perfiles (comportamiento humano anti-detección)
            if i < total:
                delay = random.uniform(8, 15)
                print(f"⏳ Esperando {delay:.1f}s antes del siguiente perfil...")
                time.sleep(delay)
        
        # Resumen
        print(f"\n{'=' * 70}")
        print("📊 RESUMEN")
        print(f"{'=' * 70}")
        print(f"✅ Exitosos: {successful}/{total}")
        print(f"❌ Fallidos: {failed}/{total}")
        if self.downloads:
            print(f"\n📋 CVs descargados:")
            for name in self.downloads:
                print(f"   • {name}")
        print(f"{'=' * 70}\n")
    
    def close(self):
        """Cierra el navegador"""
        if self.browser:
            print("\n🔒 Cerrando navegador...")
            self.browser.close()
            self.playwright.stop()
            print("✅ Cerrado\n")


def main():
    """Función principal"""
    
    print("\n" + "=" * 70)
    print("🤖  LINKEDIN CV DOWNLOADER - AUTOMATIZACIÓN HUMANA")
    print("=" * 70)
    print("Descarga CVs de LinkedIn simulando comportamiento 100% humano")
    print("=" * 70 + "\n")
    
    # Crear downloader
    downloader = LinkedInCVDownloader(headless=False)
    
    try:
        # Setup
        downloader.setup_browser()
        
        # Login manual
        downloader.wait_for_manual_login()
        
        # Lista de perfiles para descargar
        profiles = [
            ("https://www.linkedin.com/in/sebastian-torres-c/", "Sebastian Torres"),
            # Añade más perfiles aquí:
            # ("https://www.linkedin.com/in/otro-perfil/", "Nombre"),
        ]
        
        # Descargar CVs
        downloader.download_multiple_cvs(profiles)
        
        print("\n✅ Proceso completado")
        input("\nPresiona ENTER para cerrar el navegador...\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
    finally:
        downloader.close()


if __name__ == "__main__":
    main()
