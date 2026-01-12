"""
Configuração de filiais da Rodogarcia.
Mapeia CNPJs para nomes de filiais.
"""

from typing import Dict, List, Optional


# Dicionário de filiais: CNPJ -> Nome da Filial
FILIAIS: Dict[str, str] = {
    "60960473000677": "CWB - RODOGARCIA TRANSPORTES RODOVIARIOS LTDA",
    "60960473000758": "CPQ - RODOGARCIA TRANSPORTES RODOVIARIOS LTDA",
    "60960473001568": "NHB - RODOGARCIA TRANSPORTES RODOVIARIOS LTDA",
    "60960473000839": "REC - RODOGARCIA TRANSPORTES RODOVIARIOS LTDA",
    "60960473001304": "RJR - RODOGARCIA TRANSPORTES RODOVIARIOS LTDA",
    "60960473001134": "AGU - RODOGARCIA TRANSPORTES RODOVIARIOS LTDA",
    "60960473000243": "SPO - RODOGARCIA TRANSPORTES RODOVIARIOS LTDA",
    "60960473000596": "CAS - RODOGARCIA TRANSPORTES RODOVIARIOS LTDA",
    "51863654000694": "TR RODOGARCIA | CAS",
    "51863654000775": "TR RODOGARCIA | RJR",
    "51863654000341": "TR RODOGARCIA | CPQ",
    "51863654000856": "TR RODOGARCIA | CWB",
    "51863654000422": "TR RODOGARCIA | NHB",
    "51863654000180": "TR RODOGARCIA | SPO",
    "51863654000503": "TR RODOGARCIA | REC",
    "51863654000260": "TR RODOGARCIA | AGU",
    "04547874000386": "AGU - DALGA LOGISTICA",
    "04547874000203": "CAS - DALGA LOGISTICA E TRANSPORTES LTDA",
    "04547874000114": "SPO - DALGA LOGISTICA E TRANSPORTES LTDA",
}


class FiliaisManager:
    """Gerenciador de filiais para busca e seleção."""
    
    def __init__(self):
        self.filiais = FILIAIS.copy()
    
    def buscar_por_cnpj(self, cnpj: str) -> Optional[str]:
        """
        Busca nome da filial por CNPJ.
        
        Args:
            cnpj: CNPJ da filial (com ou sem formatação)
        
        Returns:
            Nome da filial ou None se não encontrado
        """
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
        return self.filiais.get(cnpj_limpo)
    
    def buscar_por_nome(self, termo: str) -> List[tuple]:
        """
        Busca filiais por termo no nome (case-insensitive).
        
        Args:
            termo: Termo de busca
        
        Returns:
            Lista de tuplas (CNPJ, Nome) que correspondem ao termo
        """
        termo_lower = termo.lower()
        resultados = []
        for cnpj, nome in self.filiais.items():
            if termo_lower in nome.lower():
                resultados.append((cnpj, nome))
        return resultados
    
    def listar_todas(self) -> List[tuple]:
        """
        Lista todas as filiais.
        
        Returns:
            Lista de tuplas (CNPJ, Nome) ordenadas por nome
        """
        return sorted(self.filiais.items(), key=lambda x: x[1])
    
    def validar_cnpj(self, cnpj: str) -> bool:
        """
        Verifica se o CNPJ existe no cadastro de filiais.
        
        Args:
            cnpj: CNPJ a ser validado
        
        Returns:
            True se o CNPJ existe, False caso contrário
        """
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
        return cnpj_limpo in self.filiais
    
    def obter_opcoes_combo(self) -> List[str]:
        """
        Retorna lista formatada para ComboBox: "NOME - CNPJ"
        
        Returns:
            Lista de strings formatadas
        """
        opcoes = []
        for cnpj, nome in sorted(self.filiais.items(), key=lambda x: x[1]):
            opcoes.append(f"{nome} - {cnpj}")
        return opcoes
