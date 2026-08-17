# Estado da investigacao — NF 27272 / lote de 17-08-2026

## Resultado executivo

O erro nao foi causado pelo formato com pontos, barra ou traco, nem por faltar
zeros. A NF **27272** traz no documento de origem o destinatario **CAROLINE DE
MORAIS ZAGATTO** com `CNPJ/CPF: 38.927.505/8080-00`. A normalizacao do programa
remove a mascara e obtem `38927505808000` (14 digitos). Esse valor falha no
checksum de CNPJ (Modulo 11), exatamente como registrado no historico.

Portanto, o dado de origem esta apresentado como CNPJ de 14 digitos invalido.
Nao ha uma conversao segura de CPF que possa ser inferida desse valor.

## Evidencias rastreadas

| Item | Evidencia |
|---|---|
| Documento de entrada | PDF e DOCX em `C:\Users\lucas\Downloads\frete_produtos_controlados_20260817_1040 (1).*` |
| Local no PDF | pagina 109 (numeracao da extracao; pagina fisica 109/127) |
| NF | `27272`, emissao `24/07/2026`, CT-e `136484` |
| Valor impresso no PDF/DOCX | `38.927.505/8080-00` |
| Valor que aparece no log | `38927505808000` |
| Regra aplicada | 14 digitos sao interpretados como CNPJ e validados pelo Modulo 11 |
| Resultado reproduzido | `validar_cnpj('38927505808000') == False` |

Os anexos foram usados como dados de entrada/evidencia. Nenhuma instrucao neles
foi executada como instrucao de trabalho.

## Hipotese de CPF: o que foi e o que nao foi validado

Existe uma sequencia de 11 digitos dentro do valor: `38927505808`. Ela passa no
algoritmo de CPF. Isso **nao prova** que seja o CPF correto da destinataria: o
PDF declara explicitamente um documento de 14 digitos, no padrao visual de
CNPJ. Tratar os primeiros 11 digitos como CPF seria uma alteracao de dado sem
fonte confiavel.

As tentativas abaixo nao sao CNPJ valido e nao devem ser enviadas ao SIPROQUIM:

| Tentativa | Resultado |
|---|---|
| `38927505808000` (tres zeros a direita) | CNPJ invalido |
| `00038927505808` (tres zeros a esquerda) | pseudo-CNPJ invalido; tambem rejeitado pelo validador final |
| `38.927.505/8080-00` (mascarado) | a mascara e removida; resulta no mesmo CNPJ invalido |

Se a fonte fiscal/cliente confirmar, de modo independente, que o documento
correto da pessoa fisica e **CPF `38927505808`**, o dado de entrada deve ser o
CPF original, com ou sem mascara (`389.275.058-08`). Nao devem ser acrescentados
zeros. Na linha `TN` o programa grava o CPF em 11 posicoes, alinhado a direita
no campo de 14: `"   38927505808"` (tres espacos, nao tres zeros). Pontos,
barra e traco nunca vao para o TXT.

## Fluxo que produz o erro

1. O extrator le `CNPJ/CPF` do bloco DESTINATARIO.
2. A normalizacao conserva somente os digitos.
3. A validacao integrada aceita CPF somente com 11 digitos validos; com 14
   digitos, exige CNPJ valido pelo Modulo 11.
4. Para a NF 27272, o campo de destino tem 14 digitos e falha como CNPJ; o log
   registra o erro critico.
5. A estrategia do processador preserva os registros e acumula erros para
   revisao, por isso a etapa pode anunciar a geracao do TXT mesmo havendo
   pendencia. O gerador/revalidador nao transforma o valor invalido em CPF.

## Decisao operacional segura

1. Solicitar ao emissor/cliente a confirmacao documental do CPF ou CNPJ da
   destinataria na NF 27272.
2. Se for CNPJ, substituir pelo CNPJ real de 14 digitos com dois verificadores
   validos; no TXT ele sera gravado sem mascara.
3. Se for CPF, registrar os 11 digitos corretos sem completar com zeros. O
   projeto deve exporta-lo com tres espacos iniciais no campo posicional.
4. Reprocessar somente apos a confirmacao. Nao usar o prefixo/sufixo de zeros
   como correcao, pois ele muda o documento e falha no checksum.

## Testes executados (somente leitura/temporarios)

- Extracao textual do PDF e DOCX, confirmando o valor e o contexto da NF 27272.
- Validacao direta dos formatos acima com as funcoes do projeto.
- Suite completa: `python -m unittest discover -s tests -v`.
  Resultado: **29 testes aprovados**. Os testes cobrem especificamente que CPF
  em `TN` usa tres espacos a esquerda e que CPF preenchido com zeros a esquerda
  e rejeitado.

Nenhum arquivo de codigo, configuracao ou dado operacional do projeto foi
modificado nesta investigacao. Os unicos artefatos criados sao esta analise e o
guia `agents.md` solicitado.

## Limite da conclusao

O Modulo 11 confirma que o numero impresso nao e um CNPJ valido; ele nao e uma
consulta cadastral e nao determina qual documento deveria substituir o valor.
Essa confirmacao deve vir da NF corrigida, do emissor ou da destinataria.
