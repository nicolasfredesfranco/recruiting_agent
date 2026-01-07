#!/usr/bin/env python3
"""
LinkedIn CV Downloader - Control Humano Realista
Toma control del navegador activo y simula comportamiento 100% humano
"""

import time
import random
import math
from playwright.sync_api import sync_playwright


class HumanBehaviorSimulator:
    """Simula comportamiento humano realista en el navegador"""
    
    def __init__(self, page):
        self.page = page
        
    def human_delay(self, min_ms=300, max_ms=800):
        """Delay aleatorio como una persona pensando"""
        delay = random.uniform(min_ms / 1000, max_ms / 1000)
        time.sleep(delay)
    
    def reading_delay(self, text_length):
        """Delay basado en leer texto (simula lectura humana)"""
        # ~250 palabras por minuto = ~4 palabras por segundo
        words = text_length / 5  # Aproximado de palabras
        reading_time = (words / 4) + random.uniform(0.3, 0.8)
        time.sleep(min(reading_time, 3))  # Max 3 segundos
    
    def bezier_curve_points(self, start_x, start_y, end_x, end_y, num_points=20):
        """
        Genera puntos siguiendo una curva de Bézier para movimiento natural del mouse
        """
        # Puntos de control para la curva
        ctrl1_x = start_x + random.uniform(-100, 100)
        ctrl1_y = start_y + random.uniform(-100, 100)
        ctrl2_x = end_x + random.uniform(-100, 100)
        ctrl2_y = end_y + random.uniform(-100, 100)
        
        points = []
        for i in range(num_points):
            t = i / (num_points - 1)
            
            # Curva de Bézier cúbica
            x = (1-t)**3 * start_x + \
                3 * (1-t)**2 * t * ctrl1_x + \
                3 * (1-t) * t**2 * ctrl2_x + \
                t**3 * end_x
            
            y = (1-t)**3 * start_y + \
                3 * (1-t)**2 * t * ctrl1_y + \
                3 * (1-t) * t**2 * ctrl2_y + \
                t**3 * end_y
            
            points.append((x, y))
        
        return points
    
    def move_mouse_like_human(self, target_x, target_y, current_x=None, current_y=None):
        """
        Mueve el mouse siguiendo una trayectoria natural con curva de Bézier
        y velocidad variable (más rápido en medio, más lento al inicio/final)
        """
        if current_x is None or current_y is None:
            # Posición aleatoria inicial
            current_x = random.randint(100, 500)
            current_y = random.randint(100, 500)
        
        # Generar curva de movimiento
        points = self.bezier_curve_points(current_x, current_y, target_x, target_y)
        
        # Mover el mouse punto por punto con velocidad variable
        for i, (x, y) in enumerate(points):
            # Velocidad más lenta al inicio y final
            if i < 3 or i > len(points) - 4:
                delay = random.uniform(0.015, 0.030)
            else:
                delay = random.uniform(0.005, 0.015)
            
            self.page.mouse.move(x, y)
            time.sleep(delay)
        
        # Pequeña pausa al llegar (como cuando una persona posiciona el mouse)
        time.sleep(random.uniform(0.05, 0.15))
    
    def human_click(self, x=None, y=None, element=None):
        """
        Click humano realista con movimiento previo del mouse
        """
        if element:
            # Obtener posición del elemento
            box = element.bounding_box()
            if box:
                # Variar ligeramente la posición dentro del elemento
                x = box['x'] + box['width'] * random.uniform(0.3, 0.7)
                y = box['y'] + box['height'] * random.uniform(0.3, 0.7)
        
        if x and y:
            # Mover mouse al objetivo
            self.move_mouse_like_human(x, y)
            
            # Pequeña pausa antes de hacer click (como persona dudando)
            time.sleep(random.uniform(0.1, 0.3))
            
            # Click con duración natural
            self.page.mouse.down()
            time.sleep(random.uniform(0.05, 0.12))  # Tiempo que tarda en hacer click
            self.page.mouse.up()
            
            # Pausa post-click
            time.sleep(random.uniform(0.2, 0.5))
    
    def human_type(self, text, typing_speed_wpm=60):
        """
        Escribe texto como humano con velocidad variable y errores ocasionales
        """
        # Convertir WPM a caracteres por segundo
        chars_per_second = (typing_speed_wpm * 5) / 60
        
        for i, char in enumerate(text):
            # Velocidad variable (algunos caracteres más rápidos, otros más lentos)
            base_delay = 1 / chars_per_second
            delay = base_delay * random.uniform(0.5, 1.5)
            
            # Ocasionalmente pausas más largas (como pensar)
            if random.random() < 0.05:
                time.sleep(random.uniform(0.3, 0.8))
            
            self.page.keyboard.press(char)
            time.sleep(delay)
        
        # Pausa después de escribir
        time.sleep(random.uniform(0.3, 0.7))
    
    def human_scroll(self, direction="down", amount=None):
        """
        Scroll natural con aceleración y desaceleración
        """
        if amount is None:
            amount = random.randint(300, 600)
        
        # Dividir el scroll en pasos más pequeños
        steps = random.randint(8, 15)
        step_amount = amount / steps
        
        for i in range(steps):
            # Scroll con variación
            scroll_delta = step_amount * random.uniform(0.8, 1.2)
            
            if direction == "down":
                self.page.mouse.wheel(0, scroll_delta)
            else:
                self.page.mouse.wheel(0, -scroll_delta)
            
            # Delay variable entre pasos
            time.sleep(random.uniform(0.02, 0.06))
        
        # Pausa después del scroll
        time.sleep(random.uniform(0.3, 0.7))


class LinkedInHumanCVDownloader:
    """Descarga CVs de LinkedIn con comportamiento humano perfecto"""
    
    def __init__(self):
        self.page = None
        self.human = None
        
    def connect_to_browser(self):
        """Se conecta al navegador que ya está abierto"""
        print("\n🔌 Conectándose al navegador activo...")
        
        # Nota: Necesitamos que Chrome esté corriendo con debugging habilitado
        # chrome --remote-debugging-port=9222
        
        try:
            self.playwright = sync_playwright().start()
            
            # Intentar conectar al navegador en el puerto de debugging
            browser = self.playwright.chromium.connect_over_cdp("http://localhost:9222")
            
            # Obtener el contexto y página actual
            contexts = browser.contexts
            if contexts:
                context = contexts[0]
                pages = context.pages
                if pages:
                    self.page = pages[0]
                    self.human = HumanBehaviorSimulator(self.page)
                    print("✅ Conectado al navegador existente\n")
                    return True
            
            print("❌ No se pudo encontrar una página abierta")
            return False
            
        except Exception as e:
            print(f"❌ Error conectando al navegador: {e}")
            print("\n💡 SOLUCIÓN: Cierra Chrome y vuelve a abrirlo con:")
            print("   google-chrome --remote-debugging-port=9222")
            return False
    
    def search_person_on_linkedin(self, person_name):
        """
        Busca a una persona en LinkedIn de forma natural
        """
        print(f"\n{'=' * 70}")
        print(f"🔍 Buscando: {person_name}")
        print(f"{'=' * 70}\n")
        
        try:
            # Paso 1: Ir a LinkedIn si no estamos ahí
            current_url = self.page.url
            if 'linkedin.com' not in current_url:
                print("1️⃣ Navegando a LinkedIn...")
                self.page.goto("https://www.linkedin.com/feed/")
                self.human.human_delay(2000, 3000)
            
            # Paso 2: Buscar el campo de búsqueda
            print("2️⃣ Buscando campo de búsqueda...")
            search_box = self.page.wait_for_selector('input[placeholder*="Search" i]', timeout=5000)
            
            # Scroll al campo si es necesario
            search_box.scroll_into_view_if_needed()
            self.human.human_delay(500, 1000)
            
            # Paso 3: Click en el campo de búsqueda como humano
            print("3️⃣ Haciendo click en búsqueda...")
            self.human.human_click(element=search_box)
            
            # Paso 4: Escribir el nombre como humano
            print(f"4️⃣ Escribiendo '{person_name}'...")
            self.human.human_type(person_name, typing_speed_wpm=random.randint(50, 80))
            
            # Paso 5: Presionar Enter
            print("5️⃣ Presionando Enter...")
            self.page.keyboard.press("Enter")
            self.human.human_delay(2000, 3500)
            
            # Paso 6: Esperar resultados
            print("6️⃣ Esperando resultados...")
            self.page.wait_for_load_state("networkidle")
            self.human.human_delay(1000, 2000)
            
            print("✅ Búsqueda completada\n")
            return True
            
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return False
    
    def click_first_people_result(self):
        """
        Hace click en el primer resultado de personas
        """
        print("7️⃣ Buscando primer resultado de persona...")
        
        try:
            # Buscar enlaces de perfiles en resultados
            selectors = [
                'a.app-aware-link[href*="/in/"]',
                'a[href*="/in/"].scale-down',
                '.entity-result__title-text a'
            ]
            
            for selector in selectors:
                try:
                    links = self.page.query_selector_all(selector)
                    if links:
                        first_link = links[0]
                        
                        # Scroll al link
                        first_link.scroll_into_view_if_needed()
                        self.human.human_delay(800, 1500)
                        
                        # Leer un poco (simular lectura)
                        self.human.reading_delay(20)
                        
                        # Click humano
                        print("8️⃣ Haciendo click en el perfil...")
                        self.human.human_click(element=first_link)
                        
                        # Esperar carga
                        self.human.human_delay(2000, 3500)
                        self.page.wait_for_load_state("networkidle")
                        
                        print("✅ Perfil abierto\n")
                        return True
                except:
                    continue
            
            print("❌ No se encontraron resultados de personas")
            return False
            
        except Exception as e:
            print(f"❌ Error abriendo perfil: {e}")
            return False
    
    def download_cv_from_current_profile(self):
        """
        Descarga el CV del perfil actual usando comportamiento humano
        """
        print(f"{'=' * 70}")
        print("📄 Descargando CV del perfil actual")
        print(f"{'=' * 70}\n")
        
        try:
            # Paso 1: Scroll un poco para ver mejor el perfil (comportamiento natural)
            print("1️⃣ Observando el perfil...")
            self.human.human_scroll("down", amount=random.randint(200, 400))
            self.human.human_delay(1000, 2000)
            
            # Volver arriba
            self.human.human_scroll("up", amount=random.randint(200, 400))
            self.human.human_delay(500, 1000)
            
            # Paso 2: Buscar botón "More"
            print("2️⃣ Buscando botón 'More'...")
            
            more_button = None
            selectors = [
                'button[aria-label="More actions"]',
                'button:has-text("More")',
                'button.pvs-profile-actions__action'
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
            
            # Scroll al botón
            more_button.scroll_into_view_if_needed()
            self.human.human_delay(800, 1500)
            
            # Paso 3: Click humano en "More"
            print("3️⃣ Haciendo click en 'More'...")
            self.human.human_click(element=more_button)
            self.human.human_delay(500, 1000)
            
            print("✅ Menú 'More' abierto\n")
            
            # Paso 4: Buscar "Save to PDF"
            print("4️⃣ Buscando 'Save to PDF'...")
            
            save_pdf = None
            pdf_selectors = [
                'div[aria-label="Save to PDF"]',
                'text="Save to PDF"',
                '.artdeco-dropdown__item:has-text("Save to PDF")'
            ]
            
            for selector in pdf_selectors:
                try:
                    save_pdf = self.page.wait_for_selector(selector, timeout=3000)
                    if save_pdf:
                        break
                except:
                    continue
            
            if not save_pdf:
                print("❌ No se encontró 'Save to PDF'")
                return False
            
            # Paso 5: Mover mouse sobre las opciones (leerlas)
            print("5️⃣ Leyendo opciones del menú...")
            self.human.reading_delay(15)
            
            # Click en "Save to PDF"
            print("6️⃣ Haciendo click en 'Save to PDF'...")
            self.human.human_click(element=save_pdf)
            
            # Esperar descarga
            print("7️⃣ Esperando generación del PDF...")
            self.human.human_delay(3000, 5000)
            
            print("✅ CV descargado exitosamente\n")
            return True
            
        except Exception as e:
            print(f"❌ Error descargando CV: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def download_cv_by_name(self, person_name):
        """
        Proceso completo: buscar persona y descargar CV
        """
        print("\n" + "=" * 70)
        print(f"🤖 DESCARGA AUTOMÁTICA DE CV - Modo Humano")
        print("=" * 70)
        print(f"Objetivo: {person_name}")
        print("=" * 70 + "\n")
        
        # Buscar persona
        if not self.search_person_on_linkedin(person_name):
            return False
        
        # Click en primer resultado
        if not self.click_first_people_result():
            return False
        
        # Descargar CV
        if not self.download_cv_from_current_profile():
            return False
        
        print("\n" + "=" * 70)
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 70 + "\n")
        
        return True
    
    def download_cv_from_url(self, profile_url):
        """
        Descarga CV desde una URL directa de perfil
        """
        print(f"\n{'=' * 70}")
        print("📄 Descargando CV desde URL")
        print(f"{'=' * 70}")
        print(f"URL: {profile_url}\n")
        
        # Navegar al perfil
        print("1️⃣ Navegando al perfil...")
        self.page.goto(profile_url)
        self.human.human_delay(2000, 4000)
        self.page.wait_for_load_state("networkidle")
        
        # Descargar CV
        return self.download_cv_from_current_profile()
    
    def close(self):
        """Desconecta del navegador (sin cerrarlo)"""
        if self.playwright:
            print("\n🔌 Desconectando del navegador...")
            self.playwright.stop()
            print("✅ Desconectado (navegador sigue abierto)\n")


def main():
    """Función principal"""
    
    print("\n" + "=" * 70)
    print("🤖 LINKEDIN CV DOWNLOADER - CONTROL HUMANO REALISTA")
    print("=" * 70)
    print("Simula comportamiento 100% humano para descargar CVs")
    print("=" * 70 + "\n")
    
    downloader = LinkedInHumanCVDownloader()
    
    try:
        # Conectar al navegador existente
        if not downloader.connect_to_browser():
            print("\n⚠️  No se pudo conectar al navegador")
            print("\n💡 PASOS PARA USAR ESTE SCRIPT:")
            print("   1. Cierra Chrome completamente")
            print("   2. Abre terminal y ejecuta:")
            print("      google-chrome --remote-debugging-port=9222")
            print("   3. Inicia sesión en LinkedIn manualmente")
            print("   4. Vuelve a ejecutar este script")
            return
        
        # Menú de opciones
        print("\n" + "=" * 70)
        print("OPCIONES:")
        print("=" * 70)
        print("1. Buscar persona por nombre y descargar CV")
        print("2. Descargar CV desde perfil actual")
        print("3. Descargar CV desde URL de perfil")
        print("=" * 70)
        
        choice = input("\nElige una opción (1-3): ").strip()
        
        if choice == "1":
            person_name = input("\n📝 Nombre de la persona a buscar: ").strip()
            downloader.download_cv_by_name(person_name)
            
        elif choice == "2":
            downloader.download_cv_from_current_profile()
            
        elif choice == "3":
            profile_url = input("\n🔗 URL del perfil: ").strip()
            downloader.download_cv_from_url(profile_url)
        
        else:
            print("❌ Opción inválida")
        
        print("\n✅ Script completado")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        downloader.close()


if __name__ == "__main__":
    main()
