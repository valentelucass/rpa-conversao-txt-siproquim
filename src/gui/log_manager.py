"""
Gerenciador de logs da interface gráfica.
"""

import time
import customtkinter as ctk
from typing import Optional
from .constants import UIConstants


class LogManager:
    """Gerenciador de logs para a interface gráfica."""
    
    def __init__(self, textbox: ctk.CTkTextbox, frame_logs: ctk.CTkFrame):
        """
        Inicializa o gerenciador de logs.
        
        Args:
            textbox: Widget CTkTextbox para exibir logs
            frame_logs: Frame que contém o textbox (para mostrar/ocultar)
        """
        self.textbox = textbox
        self.frame_logs = frame_logs
        self.logs = []
        self._configurar_tags()
    
    def _configurar_tags(self):
        """Configura tags de cor para cada tipo de log."""
        for tipo, cor in UIConstants.LOG_TIPOS.items():
            tag_name = f"tag_{tipo}"
            self.textbox.tag_config(tag_name, foreground=cor)
    
    def adicionar(self, mensagem: str, tipo: str = "INFO"):
        """
        Adiciona uma mensagem de log.
        
        Args:
            mensagem: Mensagem a ser adicionada (pode conter quebras de linha \n)
            tipo: Tipo do log (ERRO, SUCESSO, INFO, DEBUG, AVISO)
        """
        timestamp = time.strftime("%H:%M:%S")
        
        # Se a mensagem contém quebras de linha, divide em múltiplas linhas de log
        # Cada linha terá o timestamp e tipo
        linhas_mensagem = mensagem.split('\n')
        
        self.textbox.configure(state="normal")
        
        for i, linha_msg in enumerate(linhas_mensagem):
            if linha_msg.strip():  # Ignora linhas vazias
                # Primeira linha tem timestamp e tipo, linhas seguintes são continuação
                if i == 0:
                    log_entry = f"[{timestamp}] [{tipo}] {linha_msg}\n"
                else:
                    # Linhas seguintes são continuação (sem timestamp duplicado)
                    log_entry = f"  → {linha_msg}\n"
                
                self.logs.append(log_entry)
                
                # Adiciona com tag para colorir
                pos_inicio = self.textbox.index("end-1c")
                self.textbox.insert("end", log_entry)
                pos_fim = self.textbox.index("end-1c")
                
                # Configura tag para colorir
                tag_name = f"tag_{tipo}"
                cor = UIConstants.LOG_TIPOS.get(tipo, "#FFFFFF")
                self.textbox.tag_config(tag_name, foreground=cor)
                self.textbox.tag_add(tag_name, pos_inicio, pos_fim)
        
        self.textbox.configure(state="disabled")
        self.textbox.see("end")  # Scroll to bottom
        # Frame de logs sempre visível no novo layout horizontal
    
    def limpar(self):
        """Limpa todos os logs."""
        self.logs = []
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")
        # Frame de logs sempre visível no novo layout horizontal
    
    def adicionar_erro(self, mensagem: str):
        """Adiciona mensagem de erro."""
        self.adicionar(mensagem, "ERRO")
    
    def adicionar_sucesso(self, mensagem: str):
        """Adiciona mensagem de sucesso."""
        self.adicionar(mensagem, "SUCESSO")
    
    def adicionar_info(self, mensagem: str):
        """Adiciona mensagem informativa."""
        self.adicionar(mensagem, "INFO")
    
    def adicionar_aviso(self, mensagem: str):
        """Adiciona mensagem de aviso."""
        self.adicionar(mensagem, "AVISO")
    
    def adicionar_debug(self, mensagem: str):
        """Adiciona mensagem de debug."""
        self.adicionar(mensagem, "DEBUG")
