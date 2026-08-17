# Regras de negocio do projeto — Conversor SIPROQUIM

Este arquivo consolida regras observadas no codigo, nos testes e em
`docs/REGRAS_SIPROQUIM.md`. Ele serve como guia de manutencao: nao inventar,
completar ou trocar documentos fiscais sem evidencia da fonte.

## Fontes de verdade e precedencia

1. Layout e regras oficiais locais: `docs/REGRAS_SIPROQUIM.md`.
2. Implementacao executavel: `src/gerador/layout_constants.py`,
   `src/gerador/txt_generator.py` e `src/gerador/txt_validator.py`.
3. Regras de saneamento e checksum: `src/gerador/sanitizers.py` e
   `src/gerador/validators.py`.
4. Pipeline e regras de extracao/correcao: `main.py`, `src/extrator/` e
   `src/processador/`.
5. Testes em `tests/` definem comportamento regressivo esperado.

Quando uma regra geral de preenchimento numerico conflitar com a regra de
documento misto CPF/CNPJ em `TN`, `LR`, `LE` ou `LA`, prevalece a regra
especifica de documento: CPF valido ocupa 11 digitos e recebe espacos a
esquerda, nunca zeros.

## Regras globais do TXT

- Codificacao UTF-8 sem BOM.
- Uma linha fisica por registro; sem linha em branco.
- Layout posicional fixo; nao usar `;`, `,` ou `|` como delimitadores.
- Campos textuais em maiusculas, sem acentos ou outros caracteres nao ASCII;
  completar com espacos a direita.
- Campos numericos comuns completam com zeros a esquerda.
- Datas no formato `dd/mm/aaaa` e validas no calendario.
- O arquivo deve iniciar com exatamente uma linha `EM`.
- O arquivo e revalidado depois de gravado; erro estrutural impede sucesso.

## Documentos: regra critica

| Campo | Aceita | Validacao | Serializacao no campo de 14 posicoes |
|---|---|---|---|
| EM.CNPJ transportadora | somente CNPJ | 14 digitos no fluxo de formulario | 14 digitos, sem mascara |
| TN.CPF/CNPJ contratante | CPF ou CNPJ | CPF de 11 ou CNPJ de 14, ambos com Modulo 11 | CPF: 3 espacos + 11 digitos; CNPJ: 14 digitos |
| TN.CPF/CNPJ origem (emitente) | somente CNPJ | CNPJ de 14 digitos, Modulo 11 | 14 digitos |
| TN.CPF/CNPJ destino | CPF ou CNPJ | CPF de 11 ou CNPJ de 14, ambos com Modulo 11 | CPF: 3 espacos + 11 digitos; CNPJ: 14 digitos |
| LR/LE/LA.CPF/CNPJ empresa | CPF ou CNPJ quando aplicavel | mesmo criterio do campo misto | CPF: espacos a esquerda; CNPJ: 14 digitos |

- A entrada pode ter pontuacao; o programa remove tudo que nao for digito.
  A pontuacao nunca e exportada.
- Documento de 14 digitos e sempre testado como CNPJ; nao se deve tentar
  reinterpretar automaticamente parte dele como CPF.
- `zfill(14)`, tres zeros antes ou depois de um CPF produzem um pseudo-CNPJ e
  sao proibidos para campos mistos. O revalidador tem teste explicito para
  rejeitar CPF com zeros a esquerda.
- O emitente/origem nao pode ser pessoa fisica.
- Destino nacional vazio e bloqueante. Destino internacional sem CPF/CNPJ e
  tratado como transporte internacional, nao como `TN` incompleto.
- Um CNPJ matematicamente valido ainda pode nao estar cadastrado no SIPROQUIM;
  nesse caso o projeto emite aviso operacional, nao altera o documento.

## Registros e dependencias

| Registro | Tamanho e papel | Regras adicionais |
|---|---|---|
| `EM` | 31; cabecalho | mes `JAN`–`DEZ`, ano suportado, flags de atividade; o padrao atual ativa transporte |
| `TN` | 276; transporte nacional | locais de retirada e entrega: somente `P` ou `A` |
| `CC` | minimo 103; conhecimento de carga | obrigatorio quando pertinente; responsavel nao vazio; modal `RO`, `AQ`, `FE`, `AE` ou combinacao valida, padrao `RO` |
| `LR` | 86 | obrigatorio antes do proximo registro principal quando `TN.Local de Retirada = A` |
| `LE` | 86 | obrigatorio antes do proximo registro principal quando `TN.Local de Entrega = A` |
| `TI` | 109; transporte internacional | usa operacao e local de armazenamento validos (`P`/`A`) |
| `PI` | 145 | obrigatorio para `TI`; nome, endereco e identificador de pais com 3 digitos nao `000` |
| `LA` | 86 | obrigatorio para `TI` quando armazenamento e `A`; documento e nome da empresa obrigatorios |

## Regras do pipeline

1. Validar formulario (arquivo, CNPJ da transportadora e periodo).
2. Validar estrutura do PDF e extrair os blocos de NF/CT-e.
3. Deduplicar por NF, preservando o conjunto processado conforme a estrategia
   atual.
4. Validar NF, CT-e, datas, documentos, nomes e recebedor com severidade.
5. Aplicar somente correcao automatica suportada pela base de conhecimento;
   nao inventar documento. Registros nao sao descartados silenciosamente: erros
   criticos e ajustes manuais sao reportados.
6. Gerar `EM`, e para cada NF `TN`/`CC` ou `TI`/`PI` (e subsecoes exigidas).
7. Sanitizar, ajustar comprimento posicional apenas quando seguro e revalidar o
   arquivo gravado.

## Validacoes operacionais adicionais

- NF: numero no tamanho esperado e data valida.
- CT-e: numero e data validos; ausencia pode ser reportada como erro/pendencia
  operacional conforme o contexto, sem perda silenciosa do registro.
- Nomes obrigatorios precisam ter conteudo; texto e normalizado (maiuculas,
  sem acentos, tamanho fixo).
- Recebedor com menos de tres caracteres ou padrao de assinatura/carimbo gera
  alerta; o sistema pode aplicar fallback conhecido, mas o usuario deve revisar.
- Contratante igual ao destino gera aviso, pois pode causar rejeicao no
  SIPROQUIM.
- `TN` com local diferente de `P`/`A` e corrigido para `P` somente na camada de
  ajuste final; a origem do dado deve ser revisada.
- `CC` com modal deslocado por um espaco possui ajuste conhecido; modal ausente
  recebe o padrao rodoviario somente para preservar a estrutura.

## Regras para manutencao e suporte

- Preserve posicoes e tamanhos; uma mudanca em campo desloca todos os campos
  seguintes e invalida o lote.
- Inclua teste de unidade para cada nova excecao de extracao ou formato.
- Nao relaxe Modulo 11 para "fazer passar" um dado fiscal: registrar a
  pendencia e exigir a fonte correta e o comportamento seguro.
- Nao converta CPF em CNPJ adicionando zeros. Para CPF verdadeiro, mantenha os
  11 digitos e use o padding de espacos que o gerador ja implementa.
- Antes de enviar, use o validador local; ele verifica estrutura, dependencias,
  maiusculas/ASCII, comprimentos e documentos do layout.

## Caso de referencia: NF 27272

O documento de 17-08-2026 contem `38.927.505/8080-00` para a destinataria.
Normalizado, e `38927505808000`: tem 14 digitos, falha como CNPJ e nao deve ser
completado com zeros nem reclassificado por inferencia como CPF. A analise
detalhada e a decisao operacional estao em `states.md`.
