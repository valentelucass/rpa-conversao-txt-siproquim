"""
Script para gerar o executável (.exe) usando PyInstaller.

Uso:
    python build.py

O executável será gerado na pasta 'dist/'.
"""

import subprocess
import sys
import os
from pathlib import Path

# Configura encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def main():
    print("Iniciando build do executavel...\n")
    
    # Verifica se PyInstaller está instalado
    try:
        import PyInstaller
    except ImportError:
        print("[ERRO] PyInstaller nao esta instalado!")
        print("[INFO] Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[OK] PyInstaller instalado com sucesso!\n")
    
    # Configurações do build
    script = "gui.py"
    nome_app = "Conversor_SIPROQUIM"
    
    # Converte o PNG para ICO se necessário
    icon_png = Path("public/icon.png")
    icon_ico = Path("public/icon.ico")
    
    if icon_png.exists() and (not icon_ico.exists() or icon_png.stat().st_mtime > icon_ico.stat().st_mtime):
        try:
            from PIL import Image
            print("[INFO] Convertendo icon.png para icon.ico...")
            img = Image.open(icon_png)
            # Salva em múltiplos tamanhos para melhor compatibilidade
            img.save(icon_ico, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
            print("[OK] Icone convertido com sucesso!\n")
        except ImportError:
            print("[AVISO] PIL/Pillow nao encontrado. Tentando sem converter...")
        except Exception as e:
            print(f"[AVISO] Erro ao converter icone: {e}")
    
    # Procura por um ícone .ico na raiz do projeto
    icon_path = icon_ico if icon_ico.exists() else None
    
    # Comando PyInstaller
    # Usa 'python -m PyInstaller' para garantir que funciona mesmo se não estiver no PATH
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", nome_app,
        "--onefile",  # Gera um único arquivo .exe
        "--windowed",  # Sem console (GUI only) - abre direto a interface gráfica
        "--clean",  # Limpa cache antes de buildar
        "--noconfirm",  # Não pergunta antes de sobrescrever
        # Inclui os módulos necessários explicitamente
        "--hidden-import", "pdfplumber",
        "--hidden-import", "unidecode",
        "--hidden-import", "src.extrator",
        "--hidden-import", "src.gerador",
        "--hidden-import", "src.extrator.pdf_extractor",
        "--hidden-import", "src.extrator.tabela_parser",
        "--hidden-import", "src.extrator.campo_extractor",
        "--hidden-import", "src.gerador.txt_generator",
        "--hidden-import", "src.gerador.sanitizers",
        "--hidden-import", "main",
        # Coleta todos os arquivos do src
        "--collect-all", "src",
        script
    ]
    
    if icon_path:
        cmd.extend(["--icon", str(icon_path)])
        print(f"[INFO] Usando icone: {icon_path}")
    else:
        print("[INFO] Sem icone personalizado (usando padrao do Windows)")
    
    print("[INFO] Comando de build:")
    print("   " + " ".join(cmd[:3]) + " ... [modulos] ...")
    print("\n[INFO] Gerando executavel (isso pode levar alguns minutos)...\n")
    print("   [AVISO] O PyInstaller esta empacotando Python + todas as dependencias")
    print("   [INFO] O arquivo final tera aproximadamente 50-100 MB (isso e normal)\n")
    
    try:
        subprocess.check_call(cmd)
        exe_path = Path("dist") / f"{nome_app}.exe"
        
        if exe_path.exists():
            tamanho_mb = exe_path.stat().st_size / (1024 * 1024)
            print("\n" + "="*60)
            print("[OK] BUILD CONCLUIDO COM SUCESSO!")
            print("="*60)
            print(f"\n[INFO] Executavel gerado:")
            print(f"   {exe_path.absolute()}")
            print(f"   Tamanho: {tamanho_mb:.1f} MB\n")
            print("[INFO] PROXIMOS PASSOS:")
            print("   1. Va ate a pasta 'dist'")
            print(f"   2. Encontre o arquivo 'Conversor_SIPROQUIM.exe'")
            print("   3. DUPLO CLIQUE no arquivo .exe")
            print("   4. A interface grafica abrira automaticamente!\n")
            print("[INFO] IMPORTANTE:")
            print("   [OK] O .exe e standalone (nao precisa instalar Python)")
            print("   [OK] Pode ser copiado para qualquer computador Windows")
            print("   [OK] Pode ser compartilhado com outros usuarios")
            print("   [OK] Basta clicar no icone para abrir a tela\n")
        else:
            print("[AVISO] Executavel nao encontrado apos o build!")
            print("   Verifique se houve erros no processo acima.")
        
    except subprocess.CalledProcessError as e:
        print(f"\n[ERRO] Erro durante o build: {e}")
        print("\n[DICA] Troubleshooting:")
        print("   - Verifique se todas as dependencias estao instaladas")
        print("   - Tente executar: python -m pip install -r requirements.txt")
        print("   - Verifique se ha mensagens de erro acima")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[AVISO] Build cancelado pelo usuario.")
        sys.exit(1)


if __name__ == "__main__":
    main()
