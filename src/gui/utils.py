"""
Utilitários para a interface gráfica.
"""

from datetime import datetime
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
    Retorna o ano atual do sistema.
    
    Returns:
        Ano atual (ex: 2026)
    """
    return datetime.now().year


def extrair_mes_padrao() -> str:
    """
    Retorna o mês atual do sistema no formato abreviado (JAN, FEV, etc.).
    
    Returns:
        Mês abreviado (ex: "JAN", "DEZ")
    """
    from src.gerador.layout_constants import MESES_ALFANUMERICOS
    
    mes_atual = datetime.now().month
    return MESES_ALFANUMERICOS.get(mes_atual, "DEZ")
