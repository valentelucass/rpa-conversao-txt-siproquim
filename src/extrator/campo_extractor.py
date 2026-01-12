"""
Módulo responsável pela extração de campos específicos de textos.
Contém funções utilitárias para extrair CNPJ, nomes, datas, etc.
"""

import re
from typing import Optional

# Importa constantes compartilhadas
try:
    from ..gerador.layout_constants import CNPJ_TAMANHO, CNPJ_VAZIO
except (ImportError, ValueError):
    # Fallback se importação circular - calcula dinamicamente
    CNPJ_TAMANHO = 14
    CNPJ_VAZIO = "0" * CNPJ_TAMANHO


def limpar_cnpj_cpf(texto: str) -> str:
    """
    Remove pontuação de CNPJ/CPF.
    
    Args:
        texto: Texto contendo CNPJ/CPF
    
    Returns:
        CNPJ/CPF apenas com números
    """
    if not texto:
        return ""
    return re.sub(r'[^\d]', '', str(texto))


def extrair_cnpj_do_texto(texto: str) -> Optional[str]:
    """
    Extrai CNPJ/CPF de um texto usando múltiplas estratégias (robustez).
    
    Estratégias (em ordem de prioridade):
    1. Busca padrão formatado: "CNPJ/CPF: XX.XXX.XXX/XXXX-XX"
    2. Busca padrão formatado solto: "XX.XXX.XXX/XXXX-XX"
    3. Busca sequência de CNPJ_TAMANHO dígitos (fallback para CNPJs mal formatados)
    
    Args:
        texto: Texto que pode conter CNPJ/CPF
    
    Returns:
        CNPJ/CPF limpo (apenas números) ou None
    """
    if not texto:
        return None
    
    # Estratégia 1: Busca padrão "CNPJ/CPF: XX.XXX.XXX/XXXX-XX"
    match = re.search(r'CNPJ/CPF:\s*([\d./-]+)', texto, re.IGNORECASE)
    if match:
        cnpj_limpo = limpar_cnpj_cpf(match.group(1))
        if len(cnpj_limpo) == CNPJ_TAMANHO:  # Valida tamanho
            return cnpj_limpo
    
    # Estratégia 2: Busca padrão formatado solto "XX.XXX.XXX/XXXX-XX"
    # Aceita variações: com/sem pontos, com/sem barra, com/sem hífen
    padroes_formatados = [
        r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}',  # 92.660.406/0076-36
        r'\d{2}\.\d{3}\.\d{3}/\d{4}',         # 92.660.406/0076
        r'\d{2}\.\d{3}\.\d{3}\.\d{4}-\d{2}', # Formato alternativo
    ]
    
    for padrao in padroes_formatados:
        match = re.search(padrao, texto)
        if match:
            cnpj_limpo = limpar_cnpj_cpf(match.group(0))
            if len(cnpj_limpo) == CNPJ_TAMANHO:
                return cnpj_limpo
    
    # Estratégia 3: Busca sequência de CNPJ_TAMANHO dígitos consecutivos (fallback agressivo)
    # Remove pontuação primeiro para facilitar busca
    texto_sem_pontuacao = re.sub(r'[^\d]', '', texto)
    
    # Busca sequências de CNPJ_TAMANHO dígitos
    match = re.search(rf'\d{{{CNPJ_TAMANHO}}}', texto_sem_pontuacao)
    if match:
        cnpj_candidato = match.group(0)
        # Validação básica: não pode ser tudo zeros ou começar com 00
        if cnpj_candidato != CNPJ_VAZIO and not cnpj_candidato.startswith('00'):
            return cnpj_candidato
    
    # Estratégia 4: Busca sequências de CNPJ_TAMANHO dígitos próximas a palavras-chave
    # Para casos extremos onde o CNPJ está quebrado
    # IMPORTANTE: Não converte CPFs (11 dígitos) para CNPJs adicionando zeros
    # CPFs devem ser tratados separadamente, não preenchidos com zeros
    contexto_cnpj = re.search(rf'(?:CNPJ|EMITENTE|DESTINAT[ÁA]RIO|CONTRANTE).*?(\d{{{CNPJ_TAMANHO}}})', 
                              texto, re.IGNORECASE | re.DOTALL)
    if contexto_cnpj:
        cnpj_candidato = limpar_cnpj_cpf(contexto_cnpj.group(1))
        if len(cnpj_candidato) == CNPJ_TAMANHO:
            # Validação básica: não pode ser tudo zeros ou começar com 000 (provavelmente CPF)
            if cnpj_candidato != CNPJ_VAZIO and not cnpj_candidato.startswith('000'):
                return cnpj_candidato
    
    return None


def extrair_nome_do_texto(texto: str) -> Optional[str]:
    """
    Extrai APENAS a Razão Social, descartando endereços, CNPJs e outras informações.
    CRÍTICO: Pega apenas a primeira linha válida após o rótulo, ignorando o resto.
    
    Estratégia:
    1. Divide o texto por linhas
    2. Pega a primeira linha que não contém CNPJ, endereço, telefone, etc.
    3. Remove qualquer "lixo" que possa ter vindo junto (CNPJ parcial, códigos)
    
    Args:
        texto: Texto que pode conter nome/razão social
    
    Returns:
        Apenas a razão social limpa (sem endereço, CNPJ, etc.) ou None
    """
    if not texto:
        return None
    
    # Divide por quebras de linha (mantém estrutura original antes de achatar)
    linhas = str(texto).split('\n')
    
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
        
        # Remove rótulos como "EMITENTE", "DESTINATÁRIO", etc.
        linha = re.sub(r'^(EMITENTE|DESTINATÁRIO|CONTRANTE|CONTRATANTE)\s*', '', linha, flags=re.IGNORECASE)
        linha = linha.strip()
        
        if not linha:
            continue
        
        # IGNORA linhas que claramente NÃO são o nome da empresa:
        # - Contém CNPJ/CPF
        # - Contém telefone (FONE)
        # - Contém endereço (END, ROD., RUA, AV., etc.)
        # - Contém CEP
        # - Contém cidade
        # - É uma data
        # - É só números
        
        if ('CNPJ/CPF' in linha.upper() or 
            'CPF:' in linha.upper() or
            'FONE' in linha.upper() or 
            'END' in linha.upper() or
            'ROD.' in linha.upper() or
            'RUA' in linha.upper() or
            'AV.' in linha.upper() or
            'AVENIDA' in linha.upper() or
            'CEP' in linha.upper() or
            'CIDADE' in linha.upper() or
            'CT-E' in linha.upper() or
            'CTE' in linha.upper() or
            'Nº CT' in linha.upper() or
            'DATA' in linha.upper() or
            'RECEBEDOR' in linha.upper() or
            re.match(r'^\d{1,2}/\d{1,2}/\d{4}', linha) or  # É data
            re.match(r'^\d+$', linha) or  # É só número
            re.search(r'\d{2}\.\d{3}\.\d{3}', linha)):  # Contém padrão de CNPJ
            continue
        
        # REMOVE "LIXO" que pode ter vindo junto:
        # 1. Remove CNPJ parcial se estiver no final (ex: "EMPRESA X 92.660.406/")
        nome_limpo = re.split(r'\d{2}\.\d{3}\.\d{3}', linha)[0]  # Corta antes de CNPJ
        nome_limpo = re.split(r'CNPJ', nome_limpo, flags=re.IGNORECASE)[0]  # Corta antes de "CNPJ"
        nome_limpo = re.split(r'CPF', nome_limpo, flags=re.IGNORECASE)[0]  # Corta antes de "CPF"
        
        # 2. Remove QUALQUER coisa após pipe (|), incluindo texto e números
        # Exemplos: "| SAO PAULO", "| CAJAMAR", "| 0076-36", "| 0042-97"
        nome_limpo = re.sub(r'\s*\|\s*.*$', '', nome_limpo)
        
        # 3. Remove códigos numéricos no final (ex: "0007-04" ou "0076-36")
        nome_limpo = re.sub(r'\s+\d{4}-\d{2}.*$', '', nome_limpo)
        
        # 4. Remove qualquer sequência de números no final
        nome_limpo = re.sub(r'\s+\d+$', '', nome_limpo)
        
        # 5. Remove espaços múltiplos
        nome_limpo = re.sub(r'\s+', ' ', nome_limpo).strip()
        
        # 6. Valida: deve ter pelo menos 3 caracteres e não ser só números/pontuação
        if nome_limpo and len(nome_limpo) >= 3 and not re.match(r'^[\d\s\.\-/]+$', nome_limpo):
            return nome_limpo
    
    return None


def extrair_numero_cte(texto: str) -> Optional[str]:
    """
    Extrai número do CTe de um texto.
    
    Args:
        texto: Texto que pode conter número do CTe
    
    Returns:
        Número do CTe ou None
    """
    if not texto:
        return None
    
    match = re.search(r'N[º°]?\s*CT-?E\s*:?\s*(\d+)', texto, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def extrair_data_cte(texto: str) -> Optional[str]:
    """
    Extrai data do CTe de um texto.
    
    Args:
        texto: Texto que pode conter data do CTe
    
    Returns:
        Data no formato dd/mm/aaaa ou None
    """
    if not texto:
        return None
    
    match = re.search(r'DATA\s*:?\s*(\d{1,2}/\d{1,2}/\d{4})', texto, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def extrair_data_entrega(texto: str) -> Optional[str]:
    """
    Extrai data de entrega de um texto.
    
    Args:
        texto: Texto que pode conter data de entrega
    
    Returns:
        Data no formato dd/mm/aaaa ou None
    """
    if not texto:
        return None
    
    # Procura padrão "DATA ENTREGA: dd/mm/aaaa"
    match = re.search(r'DATA\s*ENTREGA\s*:?\s*(\d{1,2}/\d{1,2}/\d{4})', texto, re.IGNORECASE)
    if match:
        return match.group(1)
    
    # Tenta buscar data com hora (ex: "05/01/2026 18:26")
    match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})\s+\d{1,2}:\d{2}', texto)
    if match:
        return match.group(1)
    
    return None


def extrair_recebedor(texto: str) -> Optional[str]:
    """
    Extrai nome do recebedor de um texto.
    Busca em múltiplos padrões para encontrar o recebedor.
    
    Args:
        texto: Texto que pode conter nome do recebedor
    
    Returns:
        Nome do recebedor limpo ou None
    """
    if not texto:
        return None
    
    # Padrão 1: "RECEBEDOR: Nome" ou "RECEBEDOR Nome"
    match = re.search(r'RECEBEDOR\s*:?\s*([^\n]+?)(?:\s*DATA\s*ENTREGA|$)', texto, re.IGNORECASE)
    if match:
        recebedor = match.group(1).strip()
        # Remove "DATA ENTREGA:" se aparecer
        recebedor = re.sub(r'\s*DATA\s*ENTREGA\s*:?\s*.*$', '', recebedor, flags=re.IGNORECASE)
        recebedor = recebedor.strip()
        
        if recebedor and recebedor.upper() not in ['', 'NONE', 'NULL', 'DATA ENTREGA:']:
            return recebedor
    
    # Padrão 2: Busca por "RESPONSAVEL" ou "RESPONSÁVEL" (variações)
    match = re.search(r'RESPONS[ÁA]VEL\s*(?:PELO\s*)?(?:RECEBIMENTO|RECEBEDOR)?\s*:?\s*([^\n]+)', texto, re.IGNORECASE)
    if match:
        recebedor = match.group(1).strip()
        if recebedor and recebedor.upper() not in ['', 'NONE', 'NULL']:
            return recebedor
    
    # Padrão 3: Busca por "RECEBIDO POR" ou "RECEBIDO EM"
    match = re.search(r'RECEBIDO\s*(?:POR|EM)\s*:?\s*([^\n]+)', texto, re.IGNORECASE)
    if match:
        recebedor = match.group(1).strip()
        if recebedor and recebedor.upper() not in ['', 'NONE', 'NULL']:
            return recebedor
    
    return None
