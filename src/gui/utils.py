"""
Utilitários para a interface gráfica.
"""

from pathlib import Path


def downloads_dir() -> Path:
    """
    Retorna o diretório de Downloads do usuário.
    
    Returns:
        Path do diretório Downloads ou home se não existir
    """
    home = Path.home()
    downloads = home / "Downloads"
    return downloads if downloads.exists() else home


def gerar_nome_arquivo_saida(ano: int, mes_abreviado: str, cnpj: str, nome_pdf: str = None) -> str:
    """
    Gera o nome do arquivo de saída conforme padrão SIPROQUIM.
    
    Args:
        ano: Ano de referência
        mes_abreviado: Mês abreviado (ex: "JAN", "DEZ")
        cnpj: CNPJ da filial (14 dígitos)
        nome_pdf: Nome do PDF de origem (opcional, para diferenciar arquivos)
        
    Returns:
        Nome do arquivo (ex: "M2026JAN60960473000243.txt" ou "M2026JAN60960473000243_nomepdf.txt")
    """
    import re
    from unidecode import unidecode
    
    # Formato base: M{ano}{mes}{cnpj}
    nome_base = f"M{ano}{mes_abreviado.upper()}{cnpj}"
    
    # Se houver nome do PDF, adiciona um sufixo único
    if nome_pdf:
        # Remove extensão .pdf
        nome_sem_ext = Path(nome_pdf).stem
        
        # Sanitiza o nome: remove acentos, converte para maiúscula, remove caracteres especiais
        nome_sanitizado = unidecode(nome_sem_ext).upper()
        nome_sanitizado = re.sub(r'[^A-Z0-9]', '_', nome_sanitizado)  # Substitui não-alfanuméricos por _
        nome_sanitizado = re.sub(r'_+', '_', nome_sanitizado)  # Remove underscores duplicados
        nome_sanitizado = nome_sanitizado.strip('_')  # Remove underscores nas extremidades
        
        # Limita o tamanho para não exceder limites do sistema de arquivos
        if len(nome_sanitizado) > 30:
            nome_sanitizado = nome_sanitizado[:30]
        
        # Adiciona o sufixo ao nome base
        return f"{nome_base}_{nome_sanitizado}.txt"
    
    return f"{nome_base}.txt"


def extrair_ano_padrao() -> int:
    """
    Extrai o ano padrão baseado na data atual.
    
    Se o mês atual for <= 6, retorna o ano anterior.
    Caso contrário, retorna o ano atual.
    
    Returns:
        Ano padrão
    """
    import time
    now = time.localtime()
    if now.tm_mon <= 6:
        return now.tm_year - 1
    return now.tm_year
