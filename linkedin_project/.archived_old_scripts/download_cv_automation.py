#!/usr/bin/env python3
"""
LinkedIn CV Downloader - Automatización Natural
Simula movimientos humanos del mouse para descargar CVs de LinkedIn
"""

import time
import random
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class LinkedInCVDownloader:
    """Automatiza la descarga de CVs de LinkedIn con comportamiento humano natural"""
    
    def __init__(self, download_dir="downloads/cvs"):
        """
        Inicializa el downloader
        
        Args:
            download_dir: Directorio donde se guardarán los PDFs
        """
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.browser = None
        self.context = None
        self.page = None
        
    def human_delay(self, min_ms=500, max_ms=1500):
        """Simula delays humanos aleatorios"""
        delay = random.uniform(min_ms / 1000, max_ms / 1000)
        time.sleep(delay)
        
    def move_mouse_naturally(self, x, y):
        """
        Mueve el mouse de forma natural a una posición
        Simula movimiento humano con curva suave
        
        Args:
            x, y: Coordenadas de destino
        """
        # Playwright mueve el mouse automáticamente al hacer hover/click
        # pero podemos hacer el movimiento más natural con múltiples pasos
        steps = random.randint(10, 20)
        self.page.mouse.move(x, y, steps=steps)
        self.human_delay(100, 300)
    
    def setup_browser(self, headless=False):
        """
        Configura y abre el navegador con anti-detección
        
        Args:
            headless: Si True, ejecuta sin interfaz visual
        """
        print("\n🚀 Iniciando navegador...")
        
        self.playwright = sync_playwright().start()
        
        # Configuración anti-detección
        self.browser = self.playwright.chromium.launch(
            headless=headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-web-security'
            ]
        )
        
        # Configurar contexto con user agent real
        self.context = self.browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            accept_downloads=True,
            # Configurar directorio de descargas
            downloads_path=str(self.download_dir)
        )
        
        # Script anti-detección
        self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Otros parches anti-detección
            window.chrome = {
                runtime: {}
            };
        """)
        
        self.page = self.context.new_page()
        print("✅ Navegador configurado\n")
    
    def wait_for_login(self):
        """
        Espera a que el usuario haga login manualmente
        """
        print("=" * 70)
        print("🔐 INICIO DE SESIÓN MANUAL REQUERIDO")
        print("=" * 70)
        print("Por favor:")
        print("  1. Inicia sesión en LinkedIn en el navegador que se abrió")
        print("  2. Completa cualquier verificación de seguridad si es necesaria")
        print("  3. Espera a estar en tu feed principal de LinkedIn")
        print("=" * 70)
        
        self.page.goto("https://www.linkedin.com", wait_until="domcontentloaded")
        
        input("\n✋ Presiona ENTER cuando hayas iniciado sesión y estés listo...\n")
        
        # Verificar que estamos logueados
        try:
            # Si vemos el feed de LinkedIn, estamos logueados
            self.page.wait_for_selector('nav[aria-label="Primary Navigation"]', timeout=5000)
            print("✅ Sesión iniciada correctamente\n")
            return True
        except:
            print("⚠️  No se pudo verificar el login. Continuando de todas formas...\n")
            return True
    
    def download_cv_from_profile(self, profile_url, person_name=None):
        """
        Descarga el CV de un perfil de LinkedIn
        
        Args:
            profile_url: URL del perfil de LinkedIn
            person_name: Nombre de la persona (opcional, para logging)
            
        Returns:
            True si la descarga fue exitosa, False en caso contrario
        """
        if not person_name:
            # Extraer nombre del URL
            person_name = profile_url.split('/in/')[-1].rstrip('/')
        
        print(f"\n{'=' * 70}")
        print(f"📄 Descargando CV de: {person_name}")
        print(f"{'=' * 70}")
        print(f"🔗 URL: {profile_url}\n")
        
        try:
            # Paso 1: Navegar al perfil
            print("1️⃣ Navegando al perfil...")
            self.page.goto(profile_url, wait_until="domcontentloaded")
            self.human_delay(2000, 3000)  # Delay natural después de cargar
            
            # Verificar que no hay login wall
            if 'authwall' in self.page.url or 'login' in self.page.url:
                print("❌ Login wall detectado. Por favor inicia sesión.")
                return False
            
            print("✅ Perfil cargado\n")
            
            # Paso 2: Buscar y hacer hover en el botón "More"
            print("2️⃣ Buscando botón 'More'...")
            
            # Intentar múltiples selectores
            more_button = None
            selectors = [
                'button[aria-label="More actions"]',
                'button:has-text("More")',
                'button.artdeco-dropdown__trigger--placement-bottom'
            ]
            
            for selector in selectors:
                try:
                    more_button = self.page.wait_for_selector(selector, timeout=3000)
                    if more_button:
                        break
                except:
                    continue
            
            if not more_button:
                print("❌ No se encontró el botón 'More'")
                return False
            
            print("✅ Botón 'More' encontrado\n")
            
            # Scroll al botón si es necesario
            more_button.scroll_into_view_if_needed()
            self.human_delay(500, 1000)
            
            # Paso 3: Mover mouse al botón y hacer click
            print("3️⃣ Moviendo mouse al botón 'More'...")
            box = more_button.bounding_box()
            if box:
                # Calcular centro del botón con pequeña variación aleatoria
                x = box['x'] + box['width'] / 2 + random.uniform(-5, 5)
                y = box['y'] + box['height'] / 2 + random.uniform(-5, 5)
                self.move_mouse_naturally(x, y)
            
            print("4️⃣ Haciendo click en 'More'...")
            more_button.click()
            self.human_delay(500, 1000)
            print("✅ Menú 'More' abierto\n")
            
            # Paso 4: Buscar y hacer click en "Save to PDF"
            print("5️⃣ Buscando opción 'Save to PDF'...")
            
            save_to_pdf = None
            pdf_selectors = [
                'div[aria-label="Save to PDF"]',
                'text="Save to PDF"',
                '.artdeco-dropdown__item:has-text("Save to PDF")'
            ]
            
            for selector in pdf_selectors:
                try:
                    save_to_pdf = self.page.wait_for_selector(selector, timeout=3000)
                    if save_to_pdf:
                        break
                except:
                    continue
            
            if not save_to_pdf:
                print("❌ No se encontró la opción 'Save to PDF'")
                return False
            
            print("✅ Opción 'Save to PDF' encontrada\n")
            
            # Paso 5: Mover mouse a la opción y hacer click
            print("6️⃣ Moviendo mouse a 'Save to PDF'...")
            box = save_to_pdf.bounding_box()
            if box:
                x = box['x'] + box['width'] / 2 + random.uniform(-5, 5)
                y = box['y'] + box['height'] / 2 + random.uniform(-5, 5)
                self.move_mouse_naturally(x, y)
            
            print("7️⃣ Haciendo click en 'Save to PDF'...")
            
            # Esperar la descarga
            with self.page.expect_download(timeout=30000) as download_info:
                save_to_pdf.click()
            
            download = download_info.value
            
            # Guardar el archivo con nombre personalizado
            filename = f"{person_name.replace('/', '-')}_CV.pdf"
            filepath = self.download_dir / filename
            download.save_as(filepath)
            
            print(f"\n✅ CV descargado exitosamente")
            print(f"📁 Guardado en: {filepath}\n")
            
            # Delay post-descarga
            self.human_delay(2000, 4000)
            
            return True
            
        except PlaywrightTimeout as e:
            print(f"\n⏱️ Timeout: {e}")
            return False
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def download_multiple_cvs(self, profile_urls):
        """
        Descarga CVs de múltiples perfiles
        
        Args:
            profile_urls: Lista de URLs de perfiles o lista de tuplas (url, nombre)
        """
        total = len(profile_urls)
        successful = 0
        failed = 0
        
        print(f"\n{'=' * 70}")
        print(f"📦 Procesando {total} perfiles")
        print(f"{'=' * 70}\n")
        
        for i, profile_info in enumerate(profile_urls, 1):
            # Soportar tanto URLs simples como tuplas (url, nombre)
            if isinstance(profile_info, tuple):
                url, name = profile_info
            else:
                url = profile_info
                name = None
            
            print(f"\n[{i}/{total}] Procesando perfil...")
            
            if self.download_cv_from_profile(url, name):
                successful += 1
            else:
                failed += 1
            
            # Delay entre descargas para simular comportamiento humano
            if i < total:
                delay = random.uniform(5, 10)
                print(f"\n⏳ Esperando {delay:.1f}s antes del siguiente perfil...\n")
                time.sleep(delay)
        
        # Resumen final
        print(f"\n{'=' * 70}")
        print("📊 RESUMEN DE DESCARGAS")
        print(f"{'=' * 70}")
        print(f"✅ Exitosas: {successful}/{total}")
        print(f"❌ Fallidas: {failed}/{total}")
        print(f"📁 Archivos guardados en: {self.download_dir.absolute()}")
        print(f"{'=' * 70}\n")
    
    def close(self):
        """Cierra el navegador"""
        if self.browser:
            print("\n🔒 Cerrando navegador...")
            self.browser.close()
            self.playwright.stop()
            print("✅ Navegador cerrado\n")


def main():
    """Función principal de demostración"""
    
    print("\n" + "=" * 70)
    print("🤖 LINKEDIN CV DOWNLOADER - AUTOMATIZACIÓN NATURAL")
    print("=" * 70)
    print("Este script automatiza la descarga de CVs de LinkedIn")
    print("simulando movimientos naturales del mouse")
    print("=" * 70 + "\n")
    
    # Crear instancia del downloader
    downloader = LinkedInCVDownloader(download_dir="downloads/cvs")
    
    try:
        # Configurar navegador (visible para que el usuario pueda hacer login)
        downloader.setup_browser(headless=False)
        
        # Esperar login manual
        downloader.wait_for_login()
        
        # Lista de perfiles para descargar
        # Puedes añadir más perfiles aquí
        profiles = [
            ("https://www.linkedin.com/in/sebastian-torres-c/", "Sebastian Torres"),
            # Añade más perfiles aquí:
            # ("https://www.linkedin.com/in/otro-perfil/", "Nombre Persona"),
        ]
        
        # Descargar CVs
        downloader.download_multiple_cvs(profiles)
        
        print("\n✅ Proceso completado exitosamente")
        
        # Mantener navegador abierto por si quieres verificar
        input("\nPresiona ENTER para cerrar el navegador...\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
    finally:
        downloader.close()


if __name__ == "__main__":
    main()
