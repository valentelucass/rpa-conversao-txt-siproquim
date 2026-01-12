"""
Validações para formulários da interface gráfica.
"""

import os
from pathlib import Path
from typing import Tuple, Optional
from src.gerador.layout_constants import CNPJ_TAMANHO, ANO_MINIMO, ANO_MAXIMO
from .constants import UIConstants


def somente_digitos(valor: str) -> str:
    """Remove todos os caracteres não numéricos."""
    return "".join(ch for ch in (valor or "") if ch.isdigit())


class FormValidator:
    """Validador de formulários."""
    
    @staticmethod
    def validar_pdf(caminho: str) -> Tuple[bool, Optional[str]]:
        """
        Valida se o caminho do PDF é válido.
        
        Args:
            caminho: Caminho do arquivo PDF
            
        Returns:
            Tupla (válido, mensagem_erro)
        """
        if not caminho or not caminho.strip():
            return False, UIConstants.TEXT_ERRO_PDF_INVALIDO
        
        if not os.path.exists(caminho):
            return False, UIConstants.TEXT_ERRO_PDF_INVALIDO
        
        if not caminho.lower().endswith('.pdf'):
            return False, "O arquivo selecionado não é um PDF."
        
        return True, None
    
    @staticmethod
    def validar_cnpj(cnpj: str) -> Tuple[bool, Optional[str]]:
        """
        Valida se o CNPJ tem o tamanho correto.
        
        Args:
            cnpj: CNPJ a ser validado (apenas dígitos)
            
        Returns:
            Tupla (válido, mensagem_erro)
        """
        cnpj_limpo = somente_digitos(cnpj)
        from src.gerador.layout_constants import CNPJ_TAMANHO
        if len(cnpj_limpo) != CNPJ_TAMANHO:
            return False, UIConstants.TEXT_ERRO_CNPJ_INVALIDO.format(digitos=CNPJ_TAMANHO)
        return True, None
    
    @staticmethod
    def validar_mes(mes: str) -> Tuple[bool, Optional[str], Optional[int]]:
        """
        Valida e converte mês abreviado para número.
        
        Args:
            mes: Mês abreviado (ex: "JAN", "DEZ")
            
        Returns:
            Tupla (válido, mensagem_erro, mes_numero)
        """
        if not mes:
            return False, UIConstants.TEXT_ERRO_MES_NAO_SELECIONADO, None
        
        mes_numero = UIConstants.MAPA_MESES.get(mes.upper())
        if not mes_numero:
            return False, UIConstants.TEXT_ERRO_MES_INVALIDO.format(mes=mes), None
        
        return True, None, mes_numero
    
    @staticmethod
    def validar_ano(ano_str: str) -> Tuple[bool, Optional[str], Optional[int]]:
        """
        Valida e converte ano string para inteiro.
        
        Args:
            ano_str: Ano como string (ex: "2025")
            
        Returns:
            Tupla (válido, mensagem_erro, ano_numero)
        """
        ano_digitos = somente_digitos(ano_str)
        
        if len(ano_digitos) != 4:
            return False, UIConstants.TEXT_ERRO_ANO_INVALIDO, None
        
        try:
            ano = int(ano_digitos)
            if ano < ANO_MINIMO or ano > ANO_MAXIMO:
                return False, UIConstants.TEXT_ERRO_ANO_FORA_INTERVALO.format(
                    min=ANO_MINIMO, max=ANO_MAXIMO
                ), None
            return True, None, ano
        except ValueError:
            return False, UIConstants.TEXT_ERRO_ANO_INVALIDO_VALOR, None
    
    @staticmethod
    def validar_formulario_completo(
        pdf: str, 
        cnpj: str, 
        mes: str, 
        ano_str: str
    ) -> Tuple[bool, Optional[str], dict]:
        """
        Valida o formulário completo.
        
        Args:
            pdf: Caminho do PDF
            cnpj: CNPJ digitado
            mes: Mês selecionado
            ano_str: Ano digitado
            
        Returns:
            Tupla (válido, mensagem_erro, dados_validados)
            dados_validados contém: pdf, cnpj, mes_numero, ano_numero
        """
        # Valida PDF
        pdf_valido, erro_pdf = FormValidator.validar_pdf(pdf)
        if not pdf_valido:
            return False, erro_pdf, {}
        
        # Valida CNPJ
        cnpj_limpo = somente_digitos(cnpj)
        cnpj_valido, erro_cnpj = FormValidator.validar_cnpj(cnpj_limpo)
        if not cnpj_valido:
            return False, erro_cnpj, {}
        
        # Valida Mês
        mes_valido, erro_mes, mes_numero = FormValidator.validar_mes(mes)
        if not mes_valido:
            return False, erro_mes, {}
        
        # Valida Ano
        ano_valido, erro_ano, ano_numero = FormValidator.validar_ano(ano_str)
        if not ano_valido:
            return False, erro_ano, {}
        
        return True, None, {
            'pdf': pdf,
            'cnpj': cnpj_limpo,
            'mes_numero': mes_numero,
            'ano_numero': ano_numero,
            'mes_abreviado': mes.upper()
        }
