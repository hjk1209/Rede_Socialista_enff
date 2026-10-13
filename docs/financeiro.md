# Financeiro

Modulo para controle financeiro de um movimento social, com foco em planejamento, transparencia interna, aprovacao e prestacao de contas.

## Objetivo

Centralizar:

- contas e caixas;
- orcamentos por periodo;
- linhas de orcamento por categoria;
- receitas, doacoes e contribuicoes;
- despesas e comprovantes;
- aprovacao de orcamento;
- aprovacao, rejeicao, pedido de ajuste e pagamento de despesas;
- exportacao CSV para prestacao de contas.

## Acesso

O painel fica em:

```text
/financeiro/
```

Somente usuarios com permissao financeira acessam:

```text
is_finance_operator
```

Administradores, fundadores e superusuarios tambem acessam.

## Perfil demo

```text
financeiro.mst
```

Senha:

```text
MstJuventude!2026
```

## Estrutura do modulo

### Contas e caixas

Modelo: `FinanceAccount`

Guarda:

- nome da conta/caixa;
- tipo: caixa fisico, conta bancaria, conta digital, fundo de projeto ou outro;
- titular/responsavel;
- referencia interna;
- saldo inicial;
- observacoes;
- usuario criador.

### Orcamentos

Modelo: `FinanceBudget`

Guarda:

- nome do orcamento;
- periodo inicial e final;
- descricao;
- valor planejado;
- status: rascunho, enviado, aprovado, recusado ou fechado;
- quem criou;
- quem revisou;
- data de envio e revisao.

### Linhas de orcamento

Modelo: `FinanceBudgetLine`

Categorias:

- alimentacao;
- transporte;
- formacao;
- comunicacao;
- infraestrutura;
- saude;
- producao;
- solidariedade;
- administrativo;
- outro.

### Parecer de orcamento

Modelo: `FinanceBudgetReview`

Permite:

- aprovar;
- recusar;
- pedir revisao.

Cada parecer fica salvo com:

- orcamento;
- pessoa revisora;
- decisao;
- nota/justificativa;
- data.

### Despesas

Modelo: `FinanceExpense`

Guarda:

- orcamento vinculado;
- conta/caixa;
- categoria;
- titulo da despesa;
- fornecedor/pessoa;
- documento/nota/recibo;
- valor;
- data da despesa;
- vencimento;
- data de pagamento;
- forma de pagamento;
- status;
- solicitante;
- aprovador;
- pagador;
- comprovante;
- justificativa.

Comprovantes ficam em:

```text
media/financeiro/comprovantes/%Y/%m/
```

### Decisoes de despesa

Modelo: `FinanceExpenseDecision`

Permite registrar:

- aprovado;
- recusado;
- pedir ajuste;
- marcado como pago.

### Entradas financeiras

Modelo: `FinanceContribution`

Guarda:

- conta/caixa de entrada;
- tipo de origem;
- fonte/descricao;
- valor;
- data de recebimento;
- numero de documento/recibo;
- observacoes;
- quem registrou.

Tipos de origem:

- militante;
- doacao;
- evento;
- parceria/projeto;
- venda solidaria;
- outro.

## Fluxo recomendado

1. Cadastrar uma conta ou caixa.
2. Criar um orcamento por periodo ou projeto.
3. Adicionar linhas de orcamento por categoria.
4. Enviar o orcamento para aprovacao.
5. Registrar parecer de aprovacao, recusa ou revisao.
6. Registrar entradas financeiras.
7. Solicitar despesas com justificativa e comprovante.
8. Aprovar, recusar ou pedir ajuste da despesa.
9. Marcar despesa como paga quando o pagamento for realizado.
10. Exportar CSV para prestacao de contas.

## Dados salvos

Banco de dados:

- contas;
- orcamentos;
- linhas;
- pareceres;
- receitas;
- despesas;
- decisoes;
- responsaveis;
- datas;
- valores;
- status.

Arquivos:

- comprovantes de despesas em `media/financeiro/comprovantes/`.

Logs:

- downloads de comprovantes passam pela rota protegida e podem gerar evento de seguranca.

## Prestacao de contas

O botao `Exportar prestacao de contas` gera:

```text
financeiro-prestacao-contas.csv
```

O CSV junta entradas e saidas com:

- tipo;
- data;
- categoria;
- descricao;
- valor;
- status;
- conta;
- responsavel;
- documento.

## Boas praticas

- Nenhuma despesa deve ser paga sem justificativa.
- Toda despesa deve ter comprovante sempre que possivel.
- Orcamento deve ser aprovado antes de executar gastos.
- Quem aprova deve registrar parecer claro.
- Quem paga deve marcar a despesa como paga.
- Nao misturar caixa pessoal com caixa coletivo.
- Exportar CSV ao final de cada ciclo, projeto ou jornada.
- Guardar comprovantes originais fora do sistema quando exigido.
- Definir dupla conferencia para valores altos.

## Observacao juridica

Este modulo organiza controle interno e prestacao de contas. Ele nao substitui contabilidade formal nem assessoria juridica quando houver recurso publico, parceria formal, convenio, termo de fomento, termo de colaboracao, OSCIP ou outra obrigacao especifica.

Referencias uteis:

- Lei 13.019/2014, Marco Regulatorio das Organizacoes da Sociedade Civil: https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l13019.htm
- Lei 9.790/1999, OSCIP: https://www.planalto.gov.br/ccivil_03/leis/l9790.htm
