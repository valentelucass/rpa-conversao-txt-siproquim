"""
Módulo com funções de validação de dados.
Contém validação de CNPJ usando algoritmo oficial.
"""

from typing import Optional
from .layout_constants import CNPJ_TAMANHO, CPF_TAMANHO, CNPJ_VAZIO


def validar_cnpj(cnpj: str) -> bool:
    """
    Valida CNPJ usando o algoritmo oficial (Módulo 11).
    
    Args:
        cnpj: CNPJ a ser validado (pode ter ou não formatação)
    
    Returns:
        True se o CNPJ for válido, False caso contrário
    """
    # Remove tudo que não é dígito
    cnpj_limpo = ''.join(filter(str.isdigit, str(cnpj)))
    
    # Deve ter exatamente CNPJ_TAMANHO dígitos
    if len(cnpj_limpo) != CNPJ_TAMANHO:
        return False
    
    # Verifica se todos os dígitos são iguais (CNPJ inválido)
    if cnpj_limpo == CNPJ_VAZIO or cnpj_limpo == cnpj_limpo[0] * CNPJ_TAMANHO:
        return False
    
    # Calcula primeiro dígito verificador
    tamanho = len(cnpj_limpo) - 2
    numeros = cnpj_limpo[:tamanho]
    digitos = cnpj_limpo[tamanho:]
    soma = 0
    pos = tamanho - 7
    
    for i in range(tamanho):
        soma += int(numeros[i]) * pos
        pos -= 1
        if pos < 2:
            pos = 9
    
    resultado = soma % 11
    if resultado < 2:
        digito1 = 0
    else:
        digito1 = 11 - resultado
    
    if int(digitos[0]) != digito1:
        return False
    
    # Calcula segundo dígito verificador
    tamanho += 1
    numeros = cnpj_limpo[:tamanho]
    soma = 0
    pos = tamanho - 7
    
    for i in range(tamanho):
        soma += int(numeros[i]) * pos
        pos -= 1
        if pos < 2:
            pos = 9
    
    resultado = soma % 11
    if resultado < 2:
        digito2 = 0
    else:
        digito2 = 11 - resultado
    
    if int(digitos[1]) != digito2:
        return False
    
    return True


def validar_cpf(cpf: str) -> bool:
    """
    Valida CPF usando o algoritmo oficial (Módulo 11).
    
    Args:
        cpf: CPF a ser validado (pode ter ou não formatação)
    
    Returns:
        True se o CPF for válido, False caso contrário
    """
    # Remove tudo que não é dígito
    cpf_limpo = ''.join(filter(str.isdigit, str(cpf)))
    
    # Deve ter exatamente CPF_TAMANHO dígitos
    if len(cpf_limpo) != CPF_TAMANHO:
        return False
    
    # Verifica se todos os dígitos são iguais (CPF inválido)
    if cpf_limpo == cpf_limpo[0] * CPF_TAMANHO:
        return False
    
    # Calcula primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf_limpo[i]) * (10 - i)
    
    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto
    
    if int(cpf_limpo[9]) != digito1:
        return False
    
    # Calcula segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf_limpo[i]) * (11 - i)
    
    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto
    
    if int(cpf_limpo[10]) != digito2:
        return False
    
    return True


def is_cpf_convertido(cnpj: str) -> bool:
    """
    Verifica se um CNPJ é na verdade um CPF convertido (preenchido com zeros à esquerda).
    
    Estratégia: Verifica se os últimos 11 dígitos formam um CPF válido.
    Isso detecta CPFs convertidos independentemente do prefixo (000, 092, etc.).
    
    Args:
        cnpj: CNPJ a ser verificado (14 dígitos)
    
    Returns:
        True se for um CPF convertido, False caso contrário
    """
    cnpj_limpo = ''.join(filter(str.isdigit, str(cnpj)))
    
    # Deve ter exatamente 14 dígitos
    if len(cnpj_limpo) != CNPJ_TAMANHO:
        return False
    
    # Extrai os últimos 11 dígitos (o CPF original)
    cpf_candidato = cnpj_limpo[-11:]
    
    # Se os últimos 11 dígitos formam um CPF válido, então é um CPF convertido
    if validar_cpf(cpf_candidato):
        return True
    
    # Fallback: Se começa com 000 e os últimos 11 dígitos são numéricos
    # (mesmo que não passe na validação rigorosa, pode ser um CPF mal formatado)
    if cnpj_limpo.startswith('000') and len(cpf_candidato) == CPF_TAMANHO:
        # Aceita se não for tudo zeros
        if cpf_candidato != '0' * CPF_TAMANHO:
            return True
    
    return False


def extrair_cpf_de_cnpj_convertido(cnpj: str) -> Optional[str]:
    """
    Extrai o CPF original de um CNPJ que foi convertido de CPF.
    
    Args:
        cnpj: CNPJ que pode ser um CPF convertido (14 dígitos)
    
    Returns:
        CPF original (11 dígitos) ou None se não for um CPF convertido
    """
    if is_cpf_convertido(cnpj):
        cnpj_limpo = ''.join(filter(str.isdigit, str(cnpj)))
        return cnpj_limpo[-11:]
    return None


def parece_pessoa_fisica_pelo_nome(nome: str) -> bool:
    """
    Verifica se um nome parece ser de pessoa física (não tem indicadores de empresa).
    
    Esta função verifica se os indicadores de empresa aparecem como palavras completas,
    não apenas como substrings, evitando falsos positivos (ex: "ME" em "ALMEIDA").
    
    Args:
        nome: Nome a ser verificado
    
    Returns:
        True se parece ser pessoa física, False se parece ser empresa
    """
    if not nome:
        return True  # Se não tem nome, assume pessoa física por padrão
    
    nome_upper = nome.strip().upper()
    
    # Indicadores de empresa que devem aparecer como palavras completas
    # Removemos "ME" e "EPP" da lista geral pois são muito curtos e geram falsos positivos
    indicadores_empresa = ['LTDA', 'EIRELI', 'SA', 'S.A.', 'S/A', 'SOCIEDADE', 'EMPRESA', 'COMERCIO', 'COMÉRCIO']
    
    # Verifica se algum indicador aparece como palavra completa
    palavras = nome_upper.split()
    
    for ind in indicadores_empresa:
        # Verifica se o indicador aparece como palavra completa na lista de palavras
        if ind in palavras:
            return False
    
    # Para indicadores curtos como "ME" e "EPP", verifica separadamente
    # apenas se aparecem como palavras completas (não substring)
    indicadores_curtos = ['ME', 'EPP']
    for ind in indicadores_curtos:
        if ind in palavras:
            return False
    
    # Se nenhum indicador foi encontrado como palavra completa, assume pessoa física
    return True
