"""
Gerenciador de progresso da interface gráfica.
"""

import time
from typing import Optional
from .constants import UIConstants


class ProgressManager:
    """Gerenciador de progresso para operações longas."""
    
    def __init__(self):
        """Inicializa o gerenciador de progresso."""
        self.inicio_processamento: Optional[float] = None
        self.total_paginas: int = 0
        self.pagina_atual: int = 0
    
    def iniciar(self):
        """Inicia o contador de tempo."""
        self.inicio_processamento = time.time()
        self.total_paginas = 0
        self.pagina_atual = 0
    
    def finalizar(self):
        """Finaliza o contador de tempo."""
        self.inicio_processamento = None
    
    def calcular_progresso_extracao(self, pagina_atual: int, total_paginas: int) -> float:
        """
        Calcula o progresso da etapa de extração.
        
        Args:
            pagina_atual: Página atual sendo processada
            total_paginas: Total de páginas do PDF
            
        Returns:
            Progresso entre 0.0 e PROGRESSO_EXTRAIR
        """
        self.pagina_atual = pagina_atual
        self.total_paginas = total_paginas
        
        if total_paginas > 0:
            return (pagina_atual / total_paginas) * UIConstants.PROGRESSO_EXTRAIR
        return 0.0
    
    def obter_tempo_decorrido(self) -> Optional[float]:
        """
        Obtém o tempo decorrido desde o início.
        
        Returns:
            Tempo em segundos ou None se não iniciado
        """
        if self.inicio_processamento:
            return time.time() - self.inicio_processamento
        return None
    
    def estimar_tempo_restante(self, pagina_atual: int, total_paginas: int) -> Optional[float]:
        """
        Estima o tempo restante baseado no progresso atual.
        
        Args:
            pagina_atual: Página atual
            total_paginas: Total de páginas
            
        Returns:
            Tempo estimado em segundos ou None se não iniciado
        """
        tempo_decorrido = self.obter_tempo_decorrido()
        if not tempo_decorrido or pagina_atual <= 0 or total_paginas <= 0:
            return None
        
        tempo_por_pagina = tempo_decorrido / pagina_atual
        tempo_restante = tempo_por_pagina * (total_paginas - pagina_atual)
        return tempo_restante
    
    def formatar_tempo(self, segundos: float) -> str:
        """
        Formata tempo em segundos para formato legível.
        
        Args:
            segundos: Tempo em segundos
            
        Returns:
            String formatada (ex: "2min 30s", "1h 15min")
        """
        if segundos < 60:
            return f"{int(segundos)}s"
        elif segundos < 3600:
            minutos = int(segundos // 60)
            segs = int(segundos % 60)
            return f"{minutos}min {segs}s"
        else:
            horas = int(segundos // 3600)
            minutos = int((segundos % 3600) // 60)
            return f"{horas}h {minutos}min"
    
    def deve_logar_pagina(self, pagina_atual: int, total_paginas: int) -> bool:
        """
        Determina se deve logar o progresso da página.
        
        Args:
            pagina_atual: Página atual
            total_paginas: Total de páginas
            
        Returns:
            True se deve logar
        """
        return (pagina_atual % UIConstants.INTERVALO_LOG_PAGINAS == 0 or 
                pagina_atual == total_paginas)
