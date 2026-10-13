# Acesso, Dados Retidos e Responsabilidades

Este documento explica quem pode acessar informacoes dos usuarios e onde os dados ficam guardados.

## 1. Quem acessa dados dos usuarios

### Proprio usuario

Cada usuario pode acessar:

- seu perfil;
- seus dados basicos;
- suas publicacoes;
- suas conversas em que participa;
- seus dados de saude em `Minha saude`;
- suas preferencias de tema, popup e som;
- troca da propria senha em `/conta/perfil/senha/`.

### Outros usuarios

Outros usuarios podem ver apenas o que estiver liberado pela regra de visibilidade:

- perfil publico;
- posts visiveis para eles;
- comentarios e interacoes permitidas;
- comunidades abertas;
- comunidades privadas somente quando houver permissao ou aprovacao.

### Moderacao, administracao e fundadores

Perfis com gestao podem acessar areas sensiveis quando necessario para seguranca, moderacao e administracao:

- centro de protecao/gestao;
- usuarios e permissoes;
- auditoria e tentativas de login;
- denuncias e revisoes;
- conteudos que precisam de moderacao;
- solicitacoes de senha.

Esses acessos devem ser usados apenas quando houver finalidade real.

### Operadores de saude

Operadores de saude acessam:

- fichas de saude;
- consultas;
- agendamentos;
- unidades de saude sob sua responsabilidade.

Dados de saude sao dados sensiveis. Nao devem ser copiados para feed, mensagens abertas ou relatorias comuns.

### Operadores de almoxarifado

Operadores de almoxarifado acessam:

- acervo e fotos dos quadros;
- movimentacoes;
- retiradas e devolucoes;
- acompanhamentos;
- estoque.

### Operadores financeiros

Operadores financeiros acessam:

- contas;
- orcamentos;
- entradas;
- despesas;
- comprovantes;
- decisoes de aprovacao;
- prestacao de contas.

Dados financeiros podem envolver pessoas, documentos, fornecedores e comprovantes. O acesso deve ser restrito.

### Operadores de infra

Operadores de infra acessam:

- solicitacoes do seu setor;
- dialogos de atendimento;
- agenda de manutencao;
- dados de inventario e rede quando forem operadores de TI.

A coordenacao de infra pode acompanhar todos os setores de infra.

### Mensagens

Mensagens sao acessadas pelos participantes da conversa. A gestao pode ter acesso em situacoes de seguranca, denuncia ou auditoria, conforme regra administrativa do sistema.

## 2. Onde os dados ficam salvos

### Banco local

Por padrao, em ambiente local, o banco fica em:

```text
db.sqlite3
```

Ele guarda:

- usuarios;
- permissoes;
- posts;
- comentarios;
- curtidas;
- seguidores;
- comunidades;
- mensagens;
- dados de saude;
- dados financeiros;
- dados de infra;
- dados de almoxarifado;
- auditoria;
- sessoes.

### Arquivos enviados

Arquivos ficam em:

```text
media/
```

Principais subpastas:

- `media/avatars/`;
- `media/posts/`;
- `media/stories/`;
- `media/relatoria/fotos/`;
- `media/relatoria/arquivos/`;
- `media/almoxarifado/quadros/`;
- `media/financeiro/comprovantes/`.

### Logs

Logs ficam em:

```text
logs/
```

Eles podem conter informacoes tecnicas, caminhos acessados e eventos de seguranca.

### Navegador do usuario

Algumas preferencias ficam no navegador:

- som de notificacao;
- popup web;
- rascunho de story.

Esses dados ficam no navegador e nao substituem os registros enviados oficialmente por formulario.

## 3. Senhas e tokens

O sistema nao salva senha em texto puro.

Ele guarda:

- hash da senha;
- hash de codigo de verificacao;
- hash de refresh token de API;
- registros de auditoria de login e seguranca.

Mesmo assim, o banco deve ser protegido, porque ele contem muitos dados pessoais e operacionais.

## 4. Quem acessa por fora do sistema

Quem tem acesso direto ao servidor pode acessar arquivos por fora da interface se tiver permissao no sistema operacional.

Por isso, proteja:

- a pasta do projeto;
- `db.sqlite3`;
- `media/`;
- `.env`;
- `backups/`;
- `logs/`.

Nao compartilhe a pasta completa com pessoas que nao devem acessar dados internos.

## 5. Retencao e remocao

Antes de apagar dados, avalie:

- se existe obrigacao de prestacao de contas;
- se o dado pertence a saude, financeiro ou auditoria;
- se ha solicitacao de correcao ou remocao;
- se existe backup antigo contendo o mesmo dado.

Dados antigos em backup tambem precisam de cuidado.

## 6. Regras praticas

- Dar acesso somente a quem precisa.
- Revisar operadores periodicamente.
- Trocar senhas quando houver suspeita de acesso indevido.
- Remover permissao de quem saiu da funcao.
- Evitar dados sensiveis em campos publicos.
- Fazer backup antes de atualizar.
- Proteger backup com o mesmo cuidado do banco principal.
- Nao usar contas demo em ambiente real.
