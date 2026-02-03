# 📘 Manual Técnico - Sistema SIPROQUIM Converter

**Este documento serve como referência técnica completa para desenvolvimento e manutenção do sistema.**

Contém:
- Mapeamento técnico completo (posições, tamanhos, tipos)
- Regras de higienização obrigatórias
- Arquitetura ETL implementada
- Validações e regras de negócio
- Problemas conhecidos e soluções

**Última Atualização:** Janeiro 2025  
**Versão do Sistema:** 5.1  
**Versão do Mapeamento:** Manual Técnico v1.1 + Informativo Técnico

---

## 📋 Regras Gerais de Higienização

| Regra | Status | Implementação |
|-------|--------|---------------|
| **Sem Acentos** (Ç→C, Á→A) | ✅ | `unidecode.unidecode()` em `sanitizar_texto()` |
| **Caixa Alta** (MAIÚSCULO) | ✅ | `.upper()` em `sanitizar_texto()` |
| **Numéricos:** Zeros à esquerda | ✅ | `.zfill(tamanho)` em `sanitizar_numerico()` |
| **Alfanuméricos:** Espaços à direita | ✅ | `.ljust(tamanho)` em `sanitizar_texto()` |

**Conclusão:** ✅ Todas as regras de higienização estão implementadas corretamente.

---

## 📋 Seção EM (3.1.1) - Identificação

| Campo | Mapeamento | Código Atual | Status |
|-------|------------|--------------|--------|
| **Tipo** | Pos 1-2, Tam 2, Fixo "EM" | `EM_TIPO = "EM"` | ✅ |
| **CNPJ** | Pos 3-16, Tam 14, Num | `EM_TAM_CNPJ = 14` | ✅ |
| **Mês** | Pos 17-19, Tam 3, Alfa (JAN, FEV) | `EM_TAM_MES = 3` | ✅ |
| **Ano** | Pos 20-23, Tam 4, Num | `EM_TAM_ANO = 4` | ✅ |
| **Comerc. Nacional** | Pos 24, Tam 1, Num (0/1) | `EM_POS_COM_NACIONAL = (24, 24)` | ✅ |
| **Comerc. Internacional** | Pos 25, Tam 1, Num (0/1) | `EM_POS_COM_INTERNACIONAL = (25, 25)` | ✅ |
| **Produção** | Pos 26, Tam 1, Num (0/1) | `EM_POS_PRODUCAO = (26, 26)` | ✅ |
| **Transformação** | Pos 27, Tam 1, Num (0/1) | `EM_POS_TRANSFORMACAO = (27, 27)` | ✅ |
| **Consumo** | Pos 28, Tam 1, Num (0/1) | `EM_POS_CONSUMO = (28, 28)` | ✅ |
| **Fabricação** | Pos 29, Tam 1, Num (0/1) | `EM_POS_FABRICACAO = (29, 29)` | ✅ |
| **Transporte** | Pos 30, Tam 1, Num (1) | `EM_POS_TRANSPORTE = (30, 30)` | ✅ |
| **Armazenamento** | Pos 31, Tam 1, Num (0/1) | `EM_POS_ARMAZENAMENTO = (31, 31)` | ✅ |

**Conclusão:** ✅ Seção EM está correta e completa.

---

## 📋 Seção TN (3.1.9) - Transporte Nacional

| Campo | Mapeamento | Código Atual | Status |
|-------|------------|--------------|--------|
| **Tipo** | Pos 1-2, Tam 2, Fixo "TN" | `TN_TIPO = "TN"` | ✅ |
| **CPF/CNPJ Contratante** | Pos 3-16, Tam 14, Num | `TN_POS_CNPJ_CONTRATANTE = (3, 16)` | ✅ |
| **Nome Contratante** | Pos 17-86, Tam 70, Alfa | `TN_POS_NOME_CONTRATANTE = (17, 86)` | ✅ |
| **Número NF** | Pos 87-96, Tam 10, Alfa | `TN_POS_NF_NUMERO = (87, 96)` | ✅ |
| **Data Emissão NF** | Pos 97-106, Tam 10, Data (dd/mm/aaaa) | `TN_POS_NF_DATA = (97, 106)` | ✅ |
| **CPF/CNPJ Origem** | Pos 107-120, Tam 14, Num | `TN_POS_CNPJ_ORIGEM = (107, 120)` | ✅ |
| **Razão Social Origem** | Pos 121-190, Tam 70, Alfa | `TN_POS_NOME_ORIGEM = (121, 190)` | ✅ |
| **CPF/CNPJ Destino** | Pos 191-204, Tam 14, Num | `TN_POS_CNPJ_DESTINO = (191, 204)` | ✅ |
| **Razão Social Destino** | Pos 205-274, Tam 70, Alfa | `TN_POS_NOME_DESTINO = (205, 274)` | ✅ |
| **Local de Retirada** | Pos 275, Tam 1, Alfa (P/A) | `TN_POS_LOCAL_RETIRADA = (275, 275)` | ✅ |
| **Local de Entrega** | Pos 276, Tam 1, Alfa (P/A) | `TN_POS_LOCAL_ENTREGA = (276, 276)` | ✅ |

**Conclusão:** ✅ Todas as posições estão corretas conforme mapeamento técnico.

**⚠️ PROBLEMA IDENTIFICADO:**
- Mapeamento especifica "CPF/CNPJ" mas validador SIPROQUIM rejeita CPF formatado para 14 dígitos
- Sistema agora detecta o problema ANTES de gerar o arquivo (validação preventiva)

---

## 📋 Seção CC (3.1.9.1) - Conhecimento de Carga

| Campo | Mapeamento | Código Atual | Status |
|-------|------------|--------------|--------|
| **Tipo** | Pos 1-2, Tam 2, Fixo "CC" | `CC_TIPO = "CC"` | ✅ |
| **Núm. Conhecimento** | Pos 3-11, Tam 9, Num | `CC_POS_CTE_NUMERO = (3, 11)` | ✅ |
| **Data Conhecimento** | Pos 12-21, Tam 10, Data (dd/mm/aaaa) | `CC_POS_CTE_DATA = (12, 21)` | ✅ |
| **Data Recebimento** | Pos 22-31, Tam 10, Data (dd/mm/aaaa) | `CC_POS_DATA_RECEBIMENTO = (22, 31)` | ✅ |
| **Responsável Recebim.** | Pos 32-101, Tam 70, Alfa | `CC_POS_RECEBEDOR = (32, 101)` | ✅ |
| **Modal de Transporte** | Pos 102-103, Tam 2, Alfa (RO/AQ/FE/AE) | `CC_POS_MODAL = (102, 103)` | ✅ |

**Conclusão:** ✅ Seção CC está correta e completa.

---

## 🔍 Validações Implementadas

### ✅ Validação no Processador (Camada TRANSFORM)
- **Localização:** `src/processador/data_processor.py`
- **Classe:** `SiproquimProcessor`
- **Comportamento:** Remove registros que causarão rejeição ANTES da geração
- **Vantagem:** Arquivo TXT sempre será aceito pelo SIPROQUIM

### ✅ Validação de CNPJ/CPF
- **Algoritmo:** Módulo 11 (oficial)
- **Localização:** `src/gerador/validators.py`
- **Funções:** `validar_cpf()`, `validar_cnpj()`
- **Uso:** Processador usa para identificar registros problemáticos

### ✅ Validação de Tamanho
- **Localização:** Todas as funções `gerar_linha_*()`
- **Comportamento:** Verifica se linha tem exatamente o tamanho esperado
- **Ação:** Lança `ValueError` se tamanho incorreto
- **Garantia:** Layout posicional sempre correto

---

## 🏗️ Arquitetura ETL (Extract, Transform, Load)

### **Estrutura de Módulos:**

```
src/
├── extrator/         # EXTRACT: Lê PDF, extrai dados brutos
│   ├── pdf_extractor.py
│   └── campo_extractor.py
├── processador/      # TRANSFORM: Aplica regras de negócio, filtra dados
│   └── data_processor.py  (SiproquimProcessor)
├── gerador/          # LOAD: Formata e gera TXT
│   ├── txt_generator.py
│   ├── sanitizers.py
│   └── validators.py
└── gui/              # Interface gráfica
```

### **Fluxo de Processamento:**

```
1. EXTRACT (ExtratorPDF)
   └─> Abre PDF
   └─> Extrai TODOS os dados (incluindo "lixo")
   └─> Deduplica por número de NF
   └─> Retorna lista de dicionários brutos

2. TRANSFORM (SiproquimProcessor) ← CAMADA CRÍTICA
   └─> Recebe dados brutos
   └─> Aplica regras de negócio:
       • Remove CPFs que causarão rejeição (ex: linha 152)
       • Valida CNPJ Origem (deve ter 14 dígitos válidos)
       • Remove registros com documentos inválidos
   └─> Gera relatório de exclusões (*_EXCLUSAO.txt)
   └─> Retorna apenas dados válidos

3. LOAD (GeradorTXT)
   └─> Recebe dados limpos (100% válidos)
   └─> Formata conforme layout SIPROQUIM
   └─> Gera arquivo TXT posicional
   └─> Valida tamanhos finais
```

### **Princípio da Responsabilidade Única:**

- **Extrator:** Apenas lê PDF. Não julga, não filtra, apenas entrega dados brutos.
- **Processador:** Aplica inteligência de negócio. Remove registros problemáticos automaticamente.
- **Gerador:** Apenas formata. Recebe dados limpos e confia que são válidos.

### **Classe SiproquimProcessor:**

**Localização:** `src/processador/data_processor.py`

**Métodos Principais:**
- `filtrar_dados_validos()`: Remove registros que causarão rejeição
- `_verificar_rejeicao_conhecida()`: Aplica regras de bloqueio
- `gerar_relatorio_exclusao()`: Gera relatório de exclusões

**Regras de Bloqueio Implementadas:**
1. **CPF em campo CNPJ:** Remove CPFs que, quando formatados com zeros à esquerda, não passam na validação matemática de CNPJ
2. **CNPJ Origem inválido:** Remove registros com CNPJ Origem inválido ou com tamanho incorreto

---

## ⚠️ Problemas Conhecidos e Soluções

### 1. CPF em Campo de 14 Dígitos
- **Status:** ✅ **RESOLVIDO** (v5.1)
- **Problema:** Validador SIPROQUIM rejeita CPF formatado (`00041303082896`)
- **Causa:** CPF formatado com zeros à esquerda não passa na validação matemática de CNPJ (Módulo 11)
- **Solução Implementada:** 
  - `SiproquimProcessor` remove automaticamente CPFs problemáticos
  - Gera relatório de exclusões para rastreabilidade
  - Arquivo TXT gerado contém apenas registros válidos

### 2. Formato de Data
- **Status:** ✅ Implementado
- **Formato:** `dd/mm/aaaa` (com barras)
- **Validação:** Verifica formato antes de usar

---

## 📝 Conclusão Geral

### ✅ Conformidade com Mapeamento Técnico
- **Posições:** 100% corretas
- **Tamanhos:** 100% corretos
- **Tipos de Campo:** 100% corretos
- **Regras de Higienização:** 100% implementadas

## 📋 Regras de Negócio Obrigatórias

### **Regra #1: Formatação Numérica**
- **Campos numéricos:** Sempre preencher com **zeros à esquerda** (`zfill()`)
- **Exemplo:** CPF `41303082896` → `00041303082896` (14 dígitos)
- **Manual Técnico:** "preencher os espaços não utilizados com zeros à esquerda"

### **Regra #2: Formatação Alfanumérica**
- **Campos alfanuméricos:** Sempre preencher com **espaços à direita** (`ljust()`)
- **Exemplo:** Nome "JOAO" → `"JOAO" + " " * 66` (70 caracteres)
- **Manual Técnico:** "preencher com brancos à direita"

### **Regra #3: Remoção de Acentos**
- **Obrigatório:** Remover todos os acentos (Ç→C, Á→A, etc.)
- **Implementação:** `unidecode.unidecode()` antes de `.upper()`

### **Regra #4: Caixa Alta**
- **Obrigatório:** Converter tudo para MAIÚSCULO
- **Implementação:** `.upper()` após remoção de acentos

### **Regra #5: Filtragem Automática**
- **Obrigatório:** Remover registros que causarão rejeição no SIPROQUIM
- **Implementação:** `SiproquimProcessor.filtrar_dados_validos()`
- **Registros removidos:**
  - CPFs que não passam na validação de CNPJ quando formatados
  - CNPJs Origem inválidos ou com tamanho incorreto

### **Regra #6: Rastreabilidade**
- **Obrigatório:** Gerar relatório de exclusões quando houver remoções
- **Formato:** `{nome_arquivo}_EXCLUSAO.txt`
- **Conteúdo:** NF, Cliente, Documento, Motivo da rejeição

---

## 🎯 Diretrizes de Desenvolvimento

### **Ao Adicionar Nova Regra de Bloqueio:**

1. **Localização:** `src/processador/data_processor.py`
2. **Método:** `_verificar_rejeicao_conhecida()`
3. **Formato:**
   ```python
   # Nova regra de bloqueio
   if condicao_que_causa_rejeicao:
       return f"BLOQUEIO AUTOMÁTICO: [Motivo claro e técnico]"
   ```
4. **Documentação:** Atualizar este manual com a nova regra

### **Ao Modificar Layout:**

1. **Atualizar:** `src/gerador/layout_constants.py`
2. **Validar:** Todas as posições e tamanhos
3. **Testar:** Gerar arquivo e verificar tamanho total
4. **Documentar:** Atualizar este manual

### **Ao Adicionar Nova Validação:**

1. **Processador:** Validações que removem registros → `SiproquimProcessor`
2. **Gerador:** Validações que formatam dados → `GeradorTXT`
3. **Validators:** Algoritmos de validação → `validators.py`

---

## 📊 Status de Conformidade

### ✅ Conformidade com Mapeamento Técnico
- **Posições:** 100% corretas
- **Tamanhos:** 100% corretos
- **Tipos de Campo:** 100% corretos
- **Regras de Higienização:** 100% implementadas
- **Arquitetura ETL:** 100% implementada

### ✅ Funcionalidades Implementadas
- ✅ Extração automática de PDF
- ✅ Deduplicação por número de NF
- ✅ Filtragem automática de registros problemáticos
- ✅ Geração de relatório de exclusões
- ✅ Validação matemática de CPF/CNPJ
- ✅ Formatação conforme Manual Técnico
- ✅ Interface gráfica completa

---

**Última Verificação:** Janeiro 2025
**Versão do Mapeamento:** Manual Técnico v1.1 + Informativo Técnico
