#!/usr/bin/env python3
"""
Interactive Demo - Manual control with automation
"""

import time
from scraper import LinkedInScraper

def main():
    print("\n" + "="*60)
    print("🎯 LinkedIn CV Scraper - DEMO INTERACTIVO")
    print("="*60)
    print("Este demo abrirá un navegador donde TÚ tendrás el control.")
    print("Podrás ver cómo el sistema:")
    print("  • Abre Chrome con automatización")
    print("  • Te permite hacer login manualmente")
    print("  • Automatiza la navegación al perfil")
    print("  • Genera y descarga el CV")
    print("="*60 + "\n")
    
    print("INSTRUCCIONES:")
    print("1. El navegador se abrirá y navegará a LinkedIn")
    print("2. HAZ LOGIN con tus credenciales de LinkedIn")
    print("3. Después del login, el sistema continuará automáticamente")
    print("4. Observa cómo navega y descarga el CV\n")
    
    continuar = input("¿Estás listo para comenzar? (s/n): ").strip().lower()
    if continuar != 's':
        print("Demo cancelado.\n")
        return
    
    profile_url = "https://www.linkedin.com/in/sebastian-torres-c/"
    
    try:
        print("\n🚀 Iniciando scraper...\n")
        with LinkedInScraper(download_path="downloads", headless=False) as scraper:
            
            print("=" * 60)
            print("PASO 1: APERTURA DEL NAVEGADOR")
            print("=" * 60)
            print("✓ Navegador Chrome abierto en modo visible")
            print("✓ Configuración anti-detección aplicada\n")
            
            print("=" * 60)
            print("PASO 2: NAVEGACIÓN A LINKEDIN + LOGIN MANUAL")
            print("=" * 60)
            print(f"Por favor, haz login en el navegador que se abrió.")
            print(f"Tienes 3 minutos (180 segundos) para completar el login.\n")
            
            # Esperar login manual
            login_exitoso = scraper.login_manual(wait_time=180)
            
            if not login_exitoso:
                print("\n❌ Login no completado o timeout alcanzado.")
                print("   Tip: Asegúrate de completar el login en el tiempo dado.\n")
                return
            
            print("\n=" * 60)
            print("PASO 3: NAVEGACIÓN AUTOMATIZADA AL PERFIL")
            print("=" * 60)
            print(f"🔍 Navegando a: {profile_url}")
            print("⏳ Observa el navegador - verás la navegación automática...\n")
            
            if not scraper.navigate_to_profile(profile_url):
                print("❌ No se pudo navegar al perfil\n")
                return
            
            print("✓ Perfil de Sebastian Torres cargado correctamente")
            print("✓ Navegación completada\n")
            
            # Pausa para que veas el perfil
            print("📸 Mostrando perfil por 5 segundos...")
            time.sleep(5)
            
            print("\n=" * 60)
            print("PASO 4: GENERACIÓN Y DESCARGA DE CV")
            print("=" * 60)
            print("📄 Generando PDF del perfil...")
            print("⏳ Observa el navegador - verás el proceso de generación...\n")
            
            # Descargar CV
            filepath = scraper.download_cv_as_pdf(profile_url)
            
            if filepath:
                print("\n" + "=" * 60)
                print("✅ ¡ÉXITO! CV DESCARGADO")
                print("=" * 60)
                print(f"📁 Archivo guardado en: {filepath}")
                print("\n🔍 El CV está en formato PDF y contiene todo el perfil")
                print("   de Sebastian Torres tal como lo genera LinkedIn.\n")
                
                print("🎬 Manteniendo navegador abierto por 10 segundos")
                print("   para que veas el resultado final...\n")
                time.sleep(10)
            else:
                print("\n⚠️  No se pudo generar el CV")
                print("   (Puede requerir permisos o ajustes adicionales)\n")
                time.sleep(5)
            
            print("\n" + "=" * 60)
            print("DEMO COMPLETADO")
            print("=" * 60)
            print("Has visto cómo el sistema:")
            print("  ✓ Abre un navegador real y visible")
            print("  ✓ Permite login manual seguro")
            print("  ✓ Automatiza la navegación")
            print("  ✓ Genera y descarga CVs como PDF")
            print("=" * 60 + "\n")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrumpido por usuario (Ctrl+C).\n")
    except Exception as e:
        print(f"\n❌ Error durante la demo: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
