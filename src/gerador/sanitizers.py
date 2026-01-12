"""
Módulo com funções de sanitização de dados.
Contém funções para limpar e formatar textos, números, etc.
"""

import re
import unidecode
from typing import Optional


def sanitizar_texto(texto: Optional[str], tamanho: int) -> str:
    """
    Remove acentos, converte para maiúscula e ajusta ao tamanho especificado.
    CRÍTICO: "Achata" o texto removendo TODAS as quebras de linha e espaços múltiplos.
    
    Esta função garante que nenhum campo contenha \n, \r, \t ou múltiplos espaços,
    evitando que o layout posicional seja quebrado.
    
    Args:
        texto: Texto a ser sanitizado (pode ser None)
        tamanho: Tamanho final do campo (preenche com espaços à direita)
    
    Returns:
        String sanitizada com tamanho fixo exato, SEM quebras de linha
    """
    if not texto:
        return " " * tamanho
    
    # 1. Converte para string primeiro (garante que é string)
    texto = str(texto)
    
    # 2. CRÍTICO: Remove quebras de linha ANTES de processar
    # Substitui explicitamente \n, \r, \t por espaço
    texto = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    # 3. Remove acentos e converte para maiúscula
    texto = unidecode.unidecode(texto).upper()
    
    # 4. O PULO DO GATO: Substitui QUALQUER sequência de espaços em branco
    # (múltiplos espaços) por um único espaço simples.
    # Isso "achata" o texto em uma linha só, eliminando quebras fantasma.
    texto_achatado = re.sub(r'\s+', ' ', texto)
    
    # 5. Remove espaços nas pontas
    texto_achatado = texto_achatado.strip()
    
    # 6. CRÍTICO: Corta PRIMEIRO, depois preenche (evita estouro)
    # Garantia final: remove qualquer caractere não imprimível que possa quebrar
    texto_final = ''.join(c for c in texto_achatado if c.isprintable() or c == ' ')
    texto_final = re.sub(r'\s+', ' ', texto_final).strip()
    
    return texto_final[:tamanho].ljust(tamanho)


def sanitizar_numerico(valor: Optional[str], tamanho: int) -> str:
    """
    Remove tudo que não for número e preenche com zeros à esquerda.
    
    Args:
        valor: Valor numérico a ser sanitizado (pode ser None)
        tamanho: Tamanho final do campo
    
    Returns:
        String numérica com tamanho fixo preenchida com zeros à esquerda
    """
    if not valor:
        return "0" * tamanho
    nums = ''.join(filter(str.isdigit, str(valor)))
    return nums.zfill(tamanho)


def sanitizar_alfanumerico(valor: Optional[str], tamanho: int) -> str:
    """
    Remove zeros à esquerda e ajusta ao tamanho (para campos alfanuméricos como NF).
    
    Args:
        valor: Valor alfanumérico a ser sanitizado
        tamanho: Tamanho final do campo
    
    Returns:
        String alfanumérica com tamanho fixo
    """
    if not valor:
        return " " * tamanho
    # Remove zeros à esquerda mas mantém o valor
    valor_str = str(valor).lstrip('0')
    if not valor_str:
        valor_str = "0"
    # Remove caracteres especiais e converte para maiúscula
    valor_limpo = re.sub(r'[^\w]', '', valor_str).upper()
    return valor_limpo[:tamanho].ljust(tamanho)
