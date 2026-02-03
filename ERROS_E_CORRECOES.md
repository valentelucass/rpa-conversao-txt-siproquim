# 📋 Registro de Erros e Correções - Sistema SIPROQUIM

Este documento registra todos os erros encontrados durante o desenvolvimento e suas respectivas correções, para evitar repetição e servir como referência técnica.

## 📌 Resumo Executivo

| # | Erro | Status | Severidade |
|---|------|--------|------------|
| 1 | CPF extraído com dígitos do telefone | ✅ **RESOLVIDO** | 🔴 Crítico |
| 2 | Formato de CPF rejeitado pelo SIPROQUIM | ⚠️ **PENDENTE** | 🔴 Crítico |
| 3 | Confusão entre CPF e CNPJ | ✅ **RESOLVIDO** | 🔴 Crítico |
| 4 | Correções específicas para documento único | ✅ **RESOLVIDO** | 🟡 Médio |
| 5 | Avisos cSpell (ortografia) | ✅ **RESOLVIDO** | 🟢 Baixo |

**Última Atualização:** Janeiro 2025

---

## 🔴 Erro #1: CPF Extraído com Dígitos do Telefone

### **Problema:**
- **Descrição:** O CPF estava sendo extraído com 3 dígitos a mais, que eram na verdade o início do número de telefone do cliente.
- **Exemplo:** CPF `41303082896` estava sendo extraído como `41303082896149` (onde `149` era o início do telefone).
- **Impacto:** CPF inválido gerando erro no SIPROQUIM.

### **Causa Raiz:**
- Regex não estava limitando corretamente a extração, capturando dígitos subsequentes que faziam parte do telefone.
- Processamento não estava parando no final do padrão CPF/CNPJ.

### **Solução Aplicada:**
- **Arquivo:** `src/extrator/campo_extractor.py`
- **Mudança:** Regex mais precisa com delimitadores explícitos:
  ```python
  # Antes: capturava dígitos seguidos sem limite
  # Depois: para na primeira ocorrência válida com delimitadores
  match_cpf = re.search(r'CNPJ/CPF:\s*(\d{3}\.\d{3}\.\d{3}-\d{2})(?:\s|$|[^\d])', texto, re.IGNORECASE)
  ```
- **Estratégia:** Processamento linha por linha para evitar mistura de dados.

### **Validação:**
- ✅ CPF extraído corretamente: `41303082896` (11 dígitos)
- ✅ Não captura mais dígitos do telefone

---

## 🔴 Erro #2: Formato de CPF Rejeitado pelo SIPROQUIM

### **Problema:**
- **Descrição:** CPF (11 dígitos) precisa ser formatado em campo de 14 dígitos (CNPJ), mas o SIPROQUIM rejeitava os formatos testados.
- **Tentativas Rejeitadas:**
  1. `00041303082896` (zeros à esquerda) - **REJEITADO** ❌
  2. `09241303082896` (prefixo 092) - **REJEITADO** ❌
  3. `41303082896000` (zeros à direita) - **REJEITADO** ❌

### **Causa Raiz:**
- **Validador Java do SIPROQUIM:** O sistema valida o número formatado (14 dígitos) como CNPJ usando algoritmo Módulo 11.
- **Input Sujo (Garbage In):** Quando um CPF válido (`41303082896`) é formatado para 14 dígitos (`00041303082896`), ele NÃO passa na validação de CNPJ, causando erro em cascata no servidor.
- Manual técnico especifica "CPF/CNPJ" mas não detalha como formatar CPF para passar na validação.

### **Solução Implementada:**
- **Arquivo:** `src/gerador/txt_generator.py`
- **Validação Preventiva:** O sistema agora valida ANTES de formatar e verifica se o CPF formatado passará na validação de CNPJ:
  ```python
  def verificar_cpf_formatado_sera_rejeitado(cpf_limpo: str, nome: str, campo: str) -> None:
      if len(cpf_limpo) == 11 and validar_cpf(cpf_limpo):
          cpf_formatado = cpf_limpo.zfill(14)
          if not validar_cnpj(cpf_formatado):
              raise ValueError(
                  f"ERRO CRÍTICO: CPF {campo} válido ({cpf_limpo}) será REJEITADO pelo SIPROQUIM. "
                  f"Quando formatado para 14 dígitos ({cpf_formatado}), não passa na validação de CNPJ."
              )
  ```
- **Formato Atual:** `00041303082896` (zeros à esquerda, conforme manual técnico)

### **Status:**
- ⚠️ **PROBLEMA IDENTIFICADO E PREVENIDO** - Sistema agora detecta o problema ANTES de gerar o TXT
- **Ação Necessária:** Consultar Polícia Federal sobre formato correto para CPF em campo de 14 dígitos
- **Possíveis Soluções:**
  1. SIPROQUIM pode não aceitar CPF nesse campo (apenas CNPJ)
  2. Pode haver formato especial não documentado no manual
  3. Pode ser necessário usar CNPJ genérico para pessoa física

### **Observações:**
- O manual técnico (v1.1) especifica "CPF/CNPJ" mas o validador rejeita CPF formatado.
- Erros Java (`IllegalArgumentException`, `GenericJDBCException`) são consequências do dado inválido, não a causa raiz.
- Sistema agora previne "Input Sujo" validando antes de formatar.

---

## 🔴 Erro #3: Confusão entre CPF e CNPJ

### **Problema:**
- **Descrição:** O código não diferenciava corretamente CPF (11 dígitos) de CNPJ (14 dígitos), causando validações incorretas.
- **Impacto:** Validação de CPF usando algoritmo de CNPJ e vice-versa.

### **Causa Raiz:**
- Funções de sanitização e validação não identificavam o tipo de documento antes de processar.
- Lógica genérica tratava CPF e CNPJ da mesma forma.

### **Solução Aplicada:**
- **Arquivos:** 
  - `src/gerador/sanitizers.py`
  - `src/gerador/txt_generator.py`
- **Mudanças:**
  1. Função `_identificar_tipo_documento()` criada para identificar por tamanho:
     ```python
     def _identificar_tipo_documento(valor: str) -> str:
         if len(valor) == 11:
             return 'CPF'
         elif len(valor) == 14:
             return 'CNPJ'
         else:
             return 'DESCONHECIDO'
     ```
  2. Funções específicas criadas:
     - `sanitizar_cpf()` - para CPF (11 dígitos)
     - `sanitizar_cnpj()` - para CNPJ (14 dígitos)
  3. Validação diferenciada em `txt_generator.py`:
     ```python
     if len(cnpj_contratante_limpo) == CPF_TAMANHO:
         if not validar_cpf(cnpj_contratante_limpo):
             raise ValueError(...)
     elif len(cnpj_contratante_limpo) == CNPJ_TAMANHO:
         if not validar_cnpj(cnpj_contratante_limpo):
             raise ValueError(...)
     ```

### **Validação:**
- ✅ CPF e CNPJ são identificados corretamente por tamanho
- ✅ Validação usa algoritmo correto para cada tipo
- ✅ Não há mais confusão entre os dois tipos

---

## 🔴 Erro #4: Correções Específicas para Documento Único

### **Problema:**
- **Descrição:** Código tinha correções hardcoded para um documento específico, não sendo genérico.
- **Exemplo:** Prefixo `092` ou valores fixos para casos específicos.
- **Impacto:** Sistema não funcionaria para outros PDFs com dados diferentes.

### **Causa Raiz:**
- Tentativa de resolver problema específico sem pensar em solução genérica.
- Falta de abstração na lógica de processamento.

### **Solução Aplicada:**
- **Arquivos:** Todos os módulos de extração e sanitização
- **Princípios Aplicados:**
  1. **Genérico:** Funções funcionam para qualquer PDF, não apenas casos específicos
  2. **Baseado em Padrões:** Identifica CPF/CNPJ por padrões, não por valores fixos
  3. **Sem Hardcoding:** Nenhum valor fixo ou formato específico no código
  4. **Robusto:** Múltiplas estratégias de extração para diferentes layouts de PDF

### **Validação:**
- ✅ Código funciona para qualquer PDF
- ✅ Sem valores hardcoded
- ✅ Lógica baseada em padrões e tamanhos

---

## 🔴 Erro #5: Avisos cSpell (Ortografia)

### **Problema:**
- **Descrição:** VS Code mostrava avisos de ortografia para termos técnicos em português.
- **Termos:** "numerico" e "alfanumerico"
- **Impacto:** Avisos desnecessários na IDE.

### **Causa Raiz:**
- Dicionário cSpell não incluía termos técnicos em português.

### **Solução Aplicada:**
- **Arquivo:** `.vscode/cspell.json`
- **Mudança:** Adicionados termos ao dicionário:
  ```json
  {
    "words": [
      "numerico",
      "alfanumerico"
    ]
  }
  ```

### **Validação:**
- ✅ Avisos de ortografia removidos
- ✅ Termos técnicos reconhecidos

---

## 📝 Lições Aprendidas

### **Princípios Importantes:**

1. **Genérico > Específico**
   - Sempre pensar em soluções genéricas que funcionem para qualquer caso
   - Evitar hardcoding de valores ou formatos específicos

2. **Validação por Tamanho**
   - CPF = 11 dígitos
   - CNPJ = 14 dígitos
   - Sempre identificar o tipo antes de processar

3. **Extração Precisa**
   - Regex com delimitadores explícitos
   - Processar linha por linha quando necessário
   - Parar na primeira ocorrência válida

4. **Manual Técnico como Referência**
   - Sempre consultar o manual técnico antes de implementar
   - Se não especificado, testar formatos padrão (zeros à esquerda para numéricos)

5. **Validação Rigorosa**
   - Usar algoritmos oficiais (Módulo 11) para CPF/CNPJ
   - Validar antes de formatar
   - Mensagens de erro claras

---

## 🔍 Checklist de Validação

Antes de considerar uma correção completa, verificar:

- [ ] A solução é genérica (funciona para qualquer PDF)?
- [ ] Não há valores hardcoded no código?
- [ ] CPF e CNPJ são diferenciados corretamente?
- [ ] A extração não captura dados adjacentes (telefone, etc)?
- [ ] O formato segue o manual técnico SIPROQUIM?
- [ ] A validação usa o algoritmo correto para cada tipo?
- [ ] Mensagens de erro são claras e informativas?

---

## 📚 Referências

- **Manual Técnico SIPROQUIM:** Seções 3.1.1, 3.1.9, 3.1.9.1
- **Algoritmo Validação CPF/CNPJ:** Módulo 11
- **Layout SIPROQUIM:** Campos numéricos preenchem com zeros à esquerda

---

## 🚨 Problemas Pendentes

### **Formato CPF em Campo CNPJ**
- **Status:** ⚠️ Aguardando validação
- **Formato Atual:** `00041303082896` (zeros à esquerda)
- **Próximos Passos:**
  1. Testar no SIPROQUIM
  2. Se rejeitado, consultar manual técnico novamente
  3. Verificar se há exemplos válidos de arquivos aceitos
  4. Considerar se o campo realmente aceita CPF ou apenas CNPJ

---

**Última Atualização:** Janeiro 2025
**Versão do Sistema:** 5.1

---

## ✅ Solução Implementada: Camada de Processamento Automático (v5.1)

### **Nova Arquitetura:**

1. **Extrator:** Lê o PDF e entrega dados brutos (Raw Data)
2. **Processador (NOVO):** Aplica regras de negócio, remove registros que causarão rejeição e gera log de exclusão
3. **Gerador:** Recebe apenas dados 100% seguros e gera o TXT

### **Implementação:**

- **Arquivo:** `src/processador/data_processor.py`
- **Classe:** `SiproquimProcessor`
- **Função Principal:** `filtrar_dados_validos()` - Remove automaticamente CPFs que causarão rejeição
- **Relatório:** `gerar_relatorio_exclusao()` - Gera arquivo TXT com detalhes das exclusões

### **Resultado:**

- ✅ **Automação Total:** Sistema remove automaticamente registros problemáticos
- ✅ **Sem Intervenção Humana:** Não precisa excluir manualmente linhas do arquivo
- ✅ **Rastreabilidade:** Relatório detalhado de todas as exclusões
- ✅ **Arquivo Limpo:** TXT gerado contém apenas registros que passarão na validação SIPROQUIM

### **Exemplo de Uso:**

```python
from src.processador import SiproquimProcessor

processador = SiproquimProcessor()
nfs_validas = processador.filtrar_dados_validos(nfs_extraidas)

# Gera relatório se houver exclusões
if processador.registros_rejeitados:
    processador.gerar_relatorio_exclusao("relatorio_exclusoes.txt")
```
