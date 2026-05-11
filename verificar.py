#!/usr/bin/env python3
"""
TEOBOT - Archivo de Referencia Rápida
Úsalo para verificar que todo está configurado correctamente
"""

import sys
import os

def main():
    print("\n" + "="*80)
    print("TEOBOT - VERIFICADOR DE CONFIGURACIÓN")
    print("="*80 + "\n")
    
    checks = {
        "Python 3.8+": sys.version_info >= (3, 8),
        ".env existe": os.path.exists('.env'),
        "requirements.txt existe": os.path.exists('requirements.txt'),
        "main.py existe": os.path.exists('main.py'),
        "database.py existe": os.path.exists('database.py'),
        "Carpeta cogs/ existe": os.path.isdir('cogs'),
        "cogs/welcome.py existe": os.path.exists('cogs/welcome.py'),
        "cogs/roles.py existe": os.path.exists('cogs/roles.py'),
        "cogs/triggers.py existe": os.path.exists('cogs/triggers.py'),
        "cogs/social.py existe": os.path.exists('cogs/social.py'),
    }
    
    print("📋 VERIFICACIONES:\n")
    all_good = True
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check}")
        if not result:
            all_good = False
    
    print("\n" + "="*80)
    
    if all_good:
        print("✅ TODO ESTÁ CONFIGURADO CORRECTAMENTE\n")
        print("Para ejecutar el bot, usa:")
        print("\n  python main.py\n")
    else:
        print("❌ FALTAN ALGUNAS COSAS\n")
        print("Asegúrate de:")
        print("  1. Estar en la carpeta: c:\\Users\\teo72\\Downloads\\teobot\\")
        print("  2. Tener Python 3.8+ instalado")
        print("  3. Haber ejecutado: pip install -r requirements.txt")
        print()
    
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
