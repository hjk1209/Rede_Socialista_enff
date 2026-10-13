# Manual de Uso, Termos, Consentimentos e Mapa de Dados

Documento operacional da `Rede Raizes Socialista`.

Versao: 2026-06-02

Guias praticos complementares:

- `manual/abrir-em-outro-lugar.md`;
- `manual/acesso-dados-e-retencao.md`.

Contato indicado para termos, consentimentos, duvidas e pedidos sobre dados:

```text
hjk1209@hotmal.com
```

> Observacao importante: este documento e uma minuta operacional para uso interno do sistema. Ele ajuda a organizar regras, consentimentos e explicacoes, mas nao substitui revisao juridica especializada antes de uso publico, institucional ou em producao.

## 1. Objetivo do Sistema

A `Rede Raizes Socialista` e um sistema Django para comunicacao comunitaria e gestao interna. Ele junta em um so ambiente:

- cadastro de usuarios e perfis;
- feed social com publicacoes, imagens, comentarios e curtidas;
- comunidades/coletivos;
- stories;
- mensagens diretas;
- relatoria de atividades;
- modulo de saude;
- almoxarifado, acervo, movimentacoes e estoque;
- financeiro, orcamentos, entradas, despesas, comprovantes e prestacao de contas;
- setor de infraestrutura;
- centro de protecao, gestao e auditoria.

O sistema foi pensado para uso em contexto comunitario, escolar, organizativo e operacional. Ele nao deve ser usado para expor dados sensiveis de pessoas sem necessidade, sem autorizacao ou sem definicao clara de quem pode acessar cada informacao.

## 2. Acesso Inicial

### 2.1 Endereco local

Em ambiente local, o sistema pode ser acessado por:

```text
http://127.0.0.1:8000/
```

Na rede local, quando o servidor estiver aberto para a rede:

```text
http://10.0.0.169:8000/
```

### 2.2 Comando para iniciar

```powershell
py -3.14 manage.py runserver 0.0.0.0:8000 --settings=juventude_mst.settings.local
```

Para usar apenas no proprio computador:

```powershell
py -3.14 manage.py runserver 127.0.0.1:8000 --settings=juventude_mst.settings.local
```

### 2.3 Perfis demo

Todos os perfis demo usam a senha:

```text
MstJuventude!2026
```

Principais perfis:

- `coord.juventude`: fundador/gestao;
- `brigada.campo`: comunidade/coletivo;
- `comunica.mst`: moderacao e relatoria;
- `maria.raiz`: membro comum;
- `saude.unidade`: operador de saude;
- `almox.enff`: operador de almoxarifado;
- `financeiro.mst`: operador financeiro;
- `infra.coord`: coordenacao da infra;
- `ti.infra`: operador de TI;
- `producao.infra`: operador de producao;
- `jardim.infra`: operador de jardinagem;
- `manutencao.infra`: operador de manutencao.

## 3. Papeis e Permissoes

### 3.1 Membro comum

Pode:

- acessar o feed;
- editar o proprio perfil;
- publicar conteudo conforme permissao da rede;
- comentar e curtir;
- enviar mensagens;
- seguir pessoas e comunidades;
- abrir solicitacoes de infraestrutura;
- acessar o proprio centro de protecao.

### 3.2 Coletivo/comunidade

Pode:

- representar uma comunidade, brigada, NB ou coletivo;
- receber pedidos de entrada;
- publicar conteudo comunitario;
- receber relatorias;
- organizar avisos e atividades de grupo.

### 3.3 Moderacao

Pode:

- acompanhar conteudos reportados;
- acessar ferramentas de protecao;
- atuar em casos de abuso, bloqueio e revisao.

### 3.4 Gestao, administrador e fundador

Pode:

- alterar permissoes;
- acessar paineis sensiveis;
- acompanhar auditoria;
- visualizar areas administrativas;
- operar modulos especiais quando necessario.

### 3.5 Operadores especiais

Permissoes especiais ficam no perfil do usuario:

- `is_rapporteur`: relatoria;
- `is_health_operator`: saude;
- `is_warehouse_operator`: almoxarifado;
- `is_finance_operator`: financeiro;
- `is_infra_coordinator`: coordenacao da infraestrutura;
- `is_infra_ti_operator`: TI;
- `is_infra_production_operator`: producao;
- `is_infra_gardening_operator`: jardinagem;
- `is_infra_maintenance_operator`: manutencao.

## 4. Cadastro e Perfil

### 4.1 Cadastro publico

O cadastro fica em:

```text
/conta/cadastro/
```

Campos principais:

- nome exibido;
- nome de perfil;
- usuario interno;
- email;
- data de nascimento, quando informada;
- telefone, quando informado;
- senha;
- tipo de perfil;
- avatar, quando enviado.

### 4.2 Login

O login fica em:

```text
/conta/entrar/
```

O sistema registra tentativas de login para seguranca. Tentativas repetidas podem gerar bloqueio temporario.

### 4.3 Perfil

No perfil, o usuario pode ajustar:

- nome exibido;
- bio;
- localidade;
- avatar;
- privacidade do perfil;
- tema visual;
- informacoes basicas de contato, quando habilitadas.

### 4.4 Troca de senha

Usuarios autenticados podem trocar a propria senha em:

```text
/conta/perfil/senha/
```

Para trocar a senha, o sistema pede:

- senha atual;
- nova senha;
- confirmacao da nova senha.

A senha nova passa pela politica de seguranca do Django. Depois da alteracao, a sessao atual continua aberta e tokens antigos de API sao revogados.

### 4.5 Privacidade do perfil

Se o perfil estiver privado:

- pessoas fora da lista de seguidores podem ter acesso limitado;
- a gestao pode ver conteudos em casos de moderacao, seguranca ou administracao;
- bloqueios entre usuarios interferem na visibilidade.

## 5. Feed Social

### 5.1 Publicacoes

O feed fica em:

```text
/feed/
```

O usuario pode publicar:

- texto;
- imagem;
- visibilidade;
- classificacao etaria;
- permissao de download;
- permissao de compartilhamento.

Visibilidades:

- publico;
- comunidade;
- amigos e seguidores;
- privado.

### 5.2 Comentarios e curtidas

Usuarios autenticados podem comentar e curtir publicacoes visiveis para eles.

Boas praticas:

- nao publicar dados pessoais de terceiros sem autorizacao;
- nao expor dados de saude, documentos, telefone ou endereco em publicacao aberta;
- usar visibilidade restrita quando o conteudo for interno.

### 5.3 Stories

Stories permitem publicacoes temporarias, com:

- texto curto;
- imagem;
- estilo visual;
- musica ou link musical;
- tempo de duracao;
- visibilidade;
- permissao de resposta;
- lista personalizada de visualizadores/respondedores.

O sistema tambem registra visualizacoes e reacoes de stories.

## 6. Comunidades e Coletivos

As comunidades ficam em:

```text
/feed/comunidades/
```

Uma comunidade pode ser:

- publica;
- privada com aprovacao;
- perfil coletivo com seguidores;
- destino de relatorias.

Pedidos de entrada em comunidades ficam registrados ate aprovacao ou recusa.

## 7. Mensagens Diretas

As mensagens ficam em:

```text
/mensagens/
```

O sistema permite:

- conversa direta entre duas pessoas;
- conversa em grupo, quando configurada;
- historico de mensagens;
- reporte de mensagem inadequada.

Regras de uso:

- mensagens diretas nao devem ser usadas para assedio, ameaca ou exposicao indevida;
- mensagens reportadas podem ser avaliadas pela moderacao/gestao;
- dados sensiveis devem ser enviados apenas quando houver necessidade real e permissao.

## 8. Relatoria

O modulo de relatoria permite registrar atividades de comunidades/NBs.

Pode conter:

- titulo;
- data da atividade;
- texto detalhado;
- comunidade destino;
- fotos;
- arquivo anexo;
- publicacao vinculada no feed.

Recomendacoes:

- registrar somente informacoes necessarias;
- evitar nomes de pessoas em situacoes sensiveis;
- revisar fotos antes de enviar;
- se houver menores de idade, registrar somente imagens e dados com autorizacao adequada.

## 9. Saude

O modulo de saude e sensivel. Deve ser usado apenas por operadores autorizados.

Ele permite:

- cadastrar unidades de saude;
- manter ficha de saude;
- registrar tipo sanguineo;
- registrar alergias;
- registrar condicoes cronicas;
- registrar medicamentos em uso;
- registrar contato de emergencia;
- criar agendamentos;
- registrar consultas, sintomas, avaliacao, procedimentos, orientacoes e encaminhamentos.

Regras obrigatorias de cuidado:

- acessar dados de saude somente quando necessario;
- nao copiar dados de saude para o feed, mensagens abertas ou relatorias comuns;
- limitar acesso a operadores autorizados;
- tratar dados de saude como dados sensiveis;
- corrigir ou remover informacoes incorretas quando solicitado e quando for tecnicamente possivel;
- registrar apenas o necessario para cuidado e acompanhamento.

## 10. Almoxarifado e Acervo

O almoxarifado permite controlar:

- quadros e obras;
- numero de inventario;
- autor;
- local de guarda;
- foto;
- estado de conservacao;
- saidas e devolucoes;
- responsavel pela retirada;
- telefone;
- turma/grupo;
- CPP responsavel;
- atividades com acervo;
- acompanhamentos;
- estoque de materiais.

Boas praticas:

- manter numero de inventario unico;
- registrar devolucao assim que ocorrer;
- nao expor telefone de responsavel fora do modulo;
- registrar condicao do item antes e depois de movimentacao;
- usar observacoes para contexto operacional, nao para dados pessoais desnecessarios.

## 11. Financeiro

O modulo financeiro fica em:

```text
/financeiro/
```

Ele permite organizar o controle financeiro interno de um movimento social, com:

- contas e caixas;
- orcamentos por periodo, projeto, jornada ou setor;
- linhas de orcamento por categoria;
- envio de orcamento para aprovacao;
- parecer de aprovacao, recusa ou revisao;
- entradas financeiras, contribuicoes, doacoes, vendas solidarias e parcerias;
- solicitacao de despesa com justificativa;
- aprovacao, recusa, pedido de ajuste e pagamento de despesas;
- comprovantes de gasto;
- exportacao de prestacao de contas em CSV.

### 11.1 Contas e caixas

Cada conta ou caixa representa um local de controle financeiro:

- caixa fisico;
- conta bancaria;
- conta digital;
- fundo de projeto;
- outro caixa interno.

Campos principais:

- nome;
- tipo;
- titular ou responsavel;
- referencia interna;
- saldo inicial;
- observacoes.

### 11.2 Orcamentos

O orcamento registra o planejamento financeiro antes do gasto.

Campos principais:

- titulo;
- periodo inicial e final;
- valor planejado;
- descricao;
- status;
- responsavel pela criacao;
- data de envio;
- responsavel pelo parecer.

Status possiveis:

- rascunho;
- enviado para aprovacao;
- aprovado;
- recusado;
- fechado.

### 11.3 Linhas de orcamento

As linhas detalham como o valor planejado sera usado.

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

### 11.4 Entradas financeiras

Entradas registram dinheiro recebido.

Exemplos:

- contribuicao de militante;
- doacao;
- evento;
- parceria ou projeto;
- venda solidaria;
- outra origem.

Campos principais:

- conta/caixa;
- origem;
- descricao da fonte;
- valor;
- data de recebimento;
- documento ou recibo;
- observacoes;
- operador que registrou.

### 11.5 Despesas

Despesas registram gastos solicitados, aprovados ou pagos.

Campos principais:

- orcamento vinculado;
- conta/caixa previsto;
- categoria;
- titulo;
- fornecedor ou pessoa;
- numero de nota, recibo ou documento;
- valor;
- data da despesa;
- vencimento;
- forma de pagamento;
- comprovante;
- justificativa;
- status;
- solicitante;
- aprovador;
- pagador.

Boas praticas:

- registrar justificativa clara;
- anexar comprovante sempre que possivel;
- aprovar antes de pagar;
- marcar como pago somente depois da execucao real;
- exportar CSV ao final de cada ciclo, projeto ou jornada.

### 11.6 Prestacao de contas

O botao de exportacao gera:

```text
financeiro-prestacao-contas.csv
```

O arquivo inclui entradas e saidas com:

- tipo;
- data;
- categoria;
- descricao;
- valor;
- status;
- conta;
- responsavel;
- documento.

## 12. Infraestrutura

O modulo de infra fica em:

```text
/infra/
```

Setores:

- TI;
- Producao;
- Jardinagem;
- Manutencao.

### 12.1 TI

Responsavel por:

- rede Wi-Fi;
- suporte de rede;
- computadores;
- maquinas usadas por operadores;
- inventario de equipamentos;
- mapeamento de rede;
- reparos e manutencao tecnica;
- dialogo direto com usuarios.

Na aba de TI, o usuario autenticado pode abrir chamado direto para computador, maquina, Wi-Fi ou rede. Operadores de TI e coordenacao da infra podem manter o inventario tecnico de equipamentos e o mapa de rede.

Dados registrados na TI:

- nome do equipamento ou ponto de rede;
- tipo;
- patrimonio;
- local;
- usuario responsavel;
- IP;
- MAC;
- sistema operacional;
- SSID;
- VLAN ou segmento;
- ponto ao qual esta ligado;
- status;
- observacoes tecnicas.

Esses dados devem ser acessados apenas por quem precisa operar, reparar, auditar ou planejar a infraestrutura tecnica. IP, MAC, patrimonio e localizacao de equipamentos nao devem ser publicados no feed ou em mensagens abertas.

### 12.2 Producao

Responsavel por:

- planejamento do ciclo de producao agricola;
- acompanhamento de atividades de campo;
- registros de cultivo;
- manejo e organizacao operacional da producao.

### 12.3 Jardinagem

Responsavel por:

- jardins;
- areas verdes;
- paisagismo;
- organizacao e cuidado dos espacos externos.

### 12.4 Manutencao

Responsavel por:

- hidraulica;
- eletrica;
- construcao;
- estruturas da escola;
- reparos gerais.

### 12.5 Coordenacao da Infra

Pode:

- ver todos os setores;
- acompanhar fila geral;
- gerenciar calendario comum;
- organizar agenda de manutencao;
- conectar atividades dos operadores.

## 13. Seguranca e Gestao

O centro de protecao/gestao fica em:

```text
/seguranca/
```

Ele pode mostrar:

- tentativas de login;
- eventos de seguranca;
- bloqueios;
- permissoes;
- sessoes e rastros de auditoria;
- reportes de mensagem;
- acoes administrativas.

Regras:

- somente pessoas autorizadas devem acessar;
- eventos de seguranca nao devem ser apagados sem motivo;
- mudancas de permissao devem ser registradas e justificadas;
- suspeitas de abuso devem ser analisadas com cuidado.

## 14. Onde Cada Dado Fica Salvo

### 14.1 Banco de dados

Em ambiente local, o banco padrao e SQLite:

```text
db.sqlite3
```

Em producao, o banco depende das variaveis:

```text
RAIZ_DB_ENGINE
RAIZ_DB_NAME
RAIZ_DB_USER
RAIZ_DB_PASSWORD
RAIZ_DB_HOST
RAIZ_DB_PORT
```

Por padrao, quando nao ha configuracao externa, o sistema usa SQLite local.

### 14.2 Arquivos enviados

Arquivos enviados ficam em:

```text
media/
```

Pastas usadas:

```text
media/avatars/
media/posts/
media/stories/
media/relatoria/fotos/
media/relatoria/arquivos/
media/almoxarifado/quadros/
media/financeiro/comprovantes/
```

### 14.3 Logs

Logs locais ficam em:

```text
logs/raiz.log
logs/security.log
```

### 14.4 Cookies e navegador

Cookies proprios:

- `raiz_sessionid`: sessao de login;
- `raiz_csrftoken`: protecao contra envio indevido de formulario.

Preferencias no navegador/localStorage:

- `redeRaizesSocialista.notificationSoundEnabled`;
- `redeRaizesSocialista.browserPopupEnabled`;
- `redeRaizesSocialista.storyDraft`;
- `redeRaizesSocialista.storyDraftSubmitted`.

Esses dados ficam no navegador do usuario, nao no banco, salvo quando o usuario envia oficialmente um formulario.

### 14.5 Mapa por area

| Area | Dados principais | Modelo Django | Onde salva |
| --- | --- | --- | --- |
| Usuarios | nome, usuario, email, perfil, telefone, data de nascimento, bio, tema, permissoes | `accounts.User` | banco de dados |
| Avatar | imagem do perfil | `accounts.User.avatar` | `media/avatars/%Y/%m/` |
| Recuperacao de senha | solicitante, email, hash da senha sugerida, status | `accounts.PasswordRequest` | banco de dados |
| Bloqueios | quem bloqueou, quem foi bloqueado, motivo | `accounts.UserBlock` | banco de dados |
| 2FA | hash do codigo, canal, destino, validade, tentativas | `accounts.TwoFactorChallenge` | banco de dados |
| Tokens API | hash do refresh token, IP, user agent, validade | `accounts.ApiRefreshToken` | banco de dados |
| Feed | legenda, visibilidade, download, compartilhamento, idade, autor | `social.Post` | banco de dados |
| Imagem do post | arquivo de imagem | `social.Post.media` | `media/posts/%Y/%m/` |
| Stories | legenda, visibilidade, respostas, estilo, duracao, musica, idade | `social.Story` | banco de dados |
| Midia de story | arquivo de imagem | `social.Story.media` | `media/stories/%Y/%m/` |
| Visualizacao de story | quem viu e quando | `social.StoryView` | banco de dados |
| Reacao de story | emoji, usuario, story | `social.StoryReaction` | banco de dados |
| Resposta de story | texto, autor, story | `social.StoryReply` | banco de dados |
| Comentarios | texto, autor, post | `social.Comment` | banco de dados |
| Curtidas | usuario e post curtido | `social.PostLike` | banco de dados |
| Seguidores | seguidor e seguido | `social.Follow` | banco de dados |
| Entrada em comunidade | solicitante, comunidade, status, decisor | `social.CommunityJoinRequest` | banco de dados |
| Relatoria | titulo, data, texto, comunidade, reporter | `social.ActivityReport` | banco de dados |
| Foto principal de relatoria | arquivo de foto | `social.ActivityReport.photo` | `media/relatoria/fotos/%Y/%m/` |
| Anexo de relatoria | arquivo/documento | `social.ActivityReport.attachment` | `media/relatoria/arquivos/%Y/%m/` |
| Galeria de relatoria | fotos adicionais | `social.ActivityReportPhoto` | `media/relatoria/fotos/%Y/%m/` |
| Avisos de comunidade | titulo, texto, fixado, autor | `social.CommunityNotice` | banco de dados |
| Atividades de grupo | titulo, descricao, data, hora, local | `social.GroupActivity` | banco de dados |
| Tarefas semanais | responsavel, prazo, status | `social.WeeklyTask` | banco de dados |
| Conversas | titulo, participantes, criador, tipo | `messaging.Conversation` | banco de dados |
| Participantes | usuario em conversa | `messaging.ConversationParticipant` | banco de dados |
| Mensagens | texto, autor, conversa, edicao | `messaging.Message` | banco de dados |
| Reporte de mensagem | motivo, status, reportante | `messaging.MessageReport` | banco de dados |
| Unidade de saude | nome, local, telefone, descricao | `health.HealthUnit` | banco de dados |
| Ficha de saude | alergias, condicoes, medicamentos, contato de emergencia, notas | `health.HealthRecord` | banco de dados |
| Agenda de saude | paciente, unidade, operador, data, status, motivo | `health.HealthAppointment` | banco de dados |
| Consulta de saude | sintomas, avaliacao, procedimentos, orientacoes, encaminhamento | `health.HealthConsultation` | banco de dados |
| Acervo/quadros | nome, inventario, autor, local, estado, notas | `warehouse.Artwork` | banco de dados |
| Foto do acervo | imagem do quadro/obra | `warehouse.Artwork.photo` | `media/almoxarifado/quadros/%Y/%m/` |
| Movimentacao de acervo | retirada, devolucao, responsavel, telefone, prazo | `warehouse.ArtworkMovement` | banco de dados |
| Atividade de acervo | data, tipo, responsavel, status, notas | `warehouse.WarehouseActivity` | banco de dados |
| Acompanhamento de acervo | motivo, acao, material, destino, status | `warehouse.WarehouseFollowUp` | banco de dados |
| Estoque | material, lote, unidade, quantidade, validade, local | `warehouse.WarehouseStockItem` | banco de dados |
| Contas financeiras | nome, tipo, titular, referencia, saldo inicial, observacoes | `finance.FinanceAccount` | banco de dados |
| Orcamentos financeiros | titulo, periodo, descricao, valor planejado, status, responsaveis | `finance.FinanceBudget` | banco de dados |
| Linhas de orcamento | categoria, descricao, valor previsto, observacoes | `finance.FinanceBudgetLine` | banco de dados |
| Parecer de orcamento | decisao, parecer, revisor, data | `finance.FinanceBudgetReview` | banco de dados |
| Entradas financeiras | origem, fonte, valor, data, documento, conta, operador | `finance.FinanceContribution` | banco de dados |
| Despesas | orcamento, conta, categoria, fornecedor, documento, valor, status, justificativa | `finance.FinanceExpense` | banco de dados |
| Comprovantes de despesa | arquivo de nota, recibo ou comprovante | `finance.FinanceExpense.receipt` | `media/financeiro/comprovantes/%Y/%m/` |
| Decisoes de despesa | aprovacao, recusa, pedido de ajuste, pagamento, parecer | `finance.FinanceExpenseDecision` | banco de dados |
| Solicitacao de infra | setor, categoria, titulo, local, maquina, descricao, prioridade, status | `infra.InfraRequest` | banco de dados |
| Dialogo de infra | atualizacao, autor, status, agenda | `infra.InfraRequestUpdate` | banco de dados |
| Calendario de infra | setor, titulo, data, local, responsavel, status | `infra.InfraCalendarEvent` | banco de dados |
| Inventario de TI | equipamento, tipo, patrimonio, local, usuario, IP, MAC, sistema, status | `infra.TiInventoryItem` | banco de dados |
| Mapa de rede de TI | ponto, tipo, local, IP, SSID, VLAN, ligado a, status | `infra.TiNetworkNode` | banco de dados |
| Tentativa de login | usuario, IP, user agent, resultado | `core.LoginAttempt` | banco de dados |
| Auditoria | tipo de evento, severidade, IP, rota, detalhes | `core.SecurityEvent` | banco de dados |
| Sessao local | sessao autenticada | `django_session` | banco de dados local |
| Sessao em producao | sessao autenticada | cache/sessao | cache configurado por `RAIZ_CACHE_*` |

## 15. Termos de Uso

Ao usar a `Rede Raizes Socialista`, o usuario declara que leu, entendeu e aceita estes termos.

### 15.1 Uso permitido

O sistema deve ser usado para:

- comunicacao comunitaria;
- organizacao de atividades;
- relatoria;
- acompanhamento de setores;
- gestao de infraestrutura;
- gestao financeira, orcamentos, gastos e prestacao de contas;
- gestao de saude autorizada;
- gestao de almoxarifado;
- protecao e auditoria operacional.

### 15.2 Uso proibido

E proibido:

- publicar conteudo discriminatorio, violento, ofensivo ou assediador;
- expor dados pessoais de terceiros sem autorizacao;
- divulgar dados de saude fora do modulo apropriado;
- tentar acessar conta de outra pessoa;
- compartilhar senha;
- burlar limite de acesso;
- baixar ou redistribuir midias sem permissao;
- usar o sistema para vigilancia indevida;
- alterar registros financeiros para esconder gasto, erro, desvio ou uso sem autorizacao;
- anexar comprovantes falsos ou de terceiros sem permissao;
- apagar ou alterar registros para esconder abuso;
- publicar imagens de pessoas, especialmente menores, sem autorizacao adequada.

### 15.3 Responsabilidade do usuario

Cada usuario e responsavel por:

- manter sua senha em sigilo;
- trocar a senha quando houver suspeita de acesso indevido;
- conferir dados antes de publicar;
- respeitar a privacidade de outros usuarios;
- avisar a gestao em caso de acesso indevido;
- solicitar correcao quando identificar dado errado;
- registrar valores, documentos e comprovantes financeiros com fidelidade;
- usar visibilidade restrita quando o conteudo for interno.

### 15.4 Moderacao

A gestao pode:

- remover ou ocultar conteudos inadequados;
- suspender acessos;
- revisar mensagens reportadas;
- ajustar permissoes;
- registrar eventos de seguranca;
- bloquear temporariamente tentativas abusivas de login.

### 15.5 Contato oficial

Pedidos, duvidas, revisoes de consentimento, solicitacoes de correcao ou remocao de dados devem ser enviados para:

```text
hjk1209@hotmal.com
```

## 16. Politica de Privacidade e Protecao de Dados

### 16.1 Dados coletados

O sistema pode coletar:

- dados de identificacao;
- dados de contato;
- dados de perfil;
- conteudo publicado;
- mensagens;
- registros de comunidades;
- dados de relatoria;
- dados de saude;
- dados de almoxarifado;
- dados financeiros internos;
- comprovantes, recibos, notas e documentos financeiros anexados;
- dados de infraestrutura;
- logs de seguranca;
- IP e user agent;
- preferencias de navegador.

### 16.2 Finalidade

Os dados sao usados para:

- autenticar usuarios;
- manter a rede social interna;
- controlar acesso;
- proteger contas;
- organizar setores;
- registrar atividades;
- acompanhar saude quando autorizado;
- controlar acervo e estoque;
- planejar orcamentos, registrar entradas, aprovar despesas e prestar contas;
- registrar demandas de infra;
- auditar seguranca.

### 16.3 Dados sensiveis

Dados de saude sao dados sensiveis. Eles devem ter acesso limitado, finalidade clara e cuidado reforcado.

Exemplos:

- alergias;
- condicoes cronicas;
- medicamentos;
- sintomas;
- avaliacao de consulta;
- procedimentos;
- encaminhamentos.

Dados financeiros podem envolver informacoes pessoais, documentos e dados de terceiros. Eles devem ser acessados somente por operadores autorizados e pela gestao responsavel.

### 16.4 Compartilhamento

O sistema nao deve compartilhar dados com terceiros sem necessidade, autorizacao ou base adequada.

Em ambiente local, os dados ficam no computador/servidor onde o projeto roda. Em producao, ficam no banco, armazenamento, logs e cache definidos pela infraestrutura.

### 16.5 Retencao

O sistema ainda nao possui rotina automatica completa de expiracao para todos os dados. Por isso, a gestao deve definir regras de retencao por area:

- logs de seguranca;
- mensagens antigas;
- relatorias;
- dados de saude;
- registros financeiros e comprovantes;
- arquivos enviados;
- registros de almoxarifado;
- solicitacoes de infra.

### 16.6 Direitos do titular

Usuarios podem solicitar:

- confirmacao de existencia de dados;
- acesso a dados;
- correcao;
- revisao;
- remocao quando aplicavel;
- revogacao de consentimento quando aplicavel;
- informacoes sobre uso e armazenamento.

Canal:

```text
hjk1209@hotmal.com
```

## 17. Consentimentos

### 17.1 Consentimento geral de cadastro

Texto sugerido:

```text
Declaro que autorizo o cadastro dos meus dados basicos na Rede Raizes Socialista para fins de identificacao, acesso, comunicacao interna, seguranca e organizacao comunitaria.
```

### 17.2 Consentimento para uso de imagem e midia

Texto sugerido:

```text
Declaro que tenho autorizacao para publicar as imagens e arquivos enviados por mim, e entendo que a visibilidade escolhida no sistema define quem podera acessar esse conteudo.
```

### 17.3 Consentimento para mensagens internas

Texto sugerido:

```text
Declaro estar ciente de que minhas mensagens ficam registradas no sistema e podem ser analisadas pela gestao ou moderacao em caso de denuncia, seguranca ou violacao dos termos.
```

### 17.4 Consentimento para dados de saude

Texto sugerido:

```text
Declaro que autorizo o registro de dados de saude necessarios para cuidado, acompanhamento e atendimento interno, sabendo que esses dados sao sensiveis e devem ser acessados apenas por operadores autorizados.
```

### 17.5 Consentimento para menores de idade

Texto sugerido:

```text
Quando o cadastro, imagem ou dado envolver menor de idade, declaro que ha autorizacao adequada de responsavel legal ou instancia responsavel definida pela organizacao.
```

### 17.6 Consentimento para auditoria e seguranca

Texto sugerido:

```text
Declaro estar ciente de que o sistema registra tentativas de login, IP, navegador, eventos de seguranca, downloads e acoes administrativas para proteger usuarios e a rede.
```

### 17.7 Consentimento para infraestrutura, almoxarifado e operacao

Texto sugerido:

```text
Declaro estar ciente de que solicitacoes, movimentacoes, agendamentos, responsaveis, telefones e registros operacionais podem ser salvos para organizar manutencao, estoque, acervo e atividades internas.
```

### 17.8 Consentimento para registros financeiros

Texto sugerido:

```text
Declaro estar ciente de que entradas financeiras, orcamentos, despesas, comprovantes, recibos, notas, pareceres e responsaveis podem ser registrados para controle interno, aprovacao, auditoria e prestacao de contas.
```

### 17.9 Revogacao

O usuario pode pedir revisao ou revogacao de consentimento pelo canal:

```text
hjk1209@hotmal.com
```

A revogacao pode nao apagar automaticamente registros necessarios para seguranca, auditoria, obrigacao operacional, historico de atendimento ou preservacao de direitos. A gestao deve avaliar caso a caso.

## 18. Operacao Segura

### 18.1 Senhas

- Nunca compartilhar senha.
- Trocar senha quando houver suspeita de vazamento.
- Usar senha diferente de outros servicos.
- Evitar senha demo em ambiente real.

### 18.2 Backups

Usar:

```powershell
powershell -ExecutionPolicy Bypass -File .\backup.ps1
```

Restaurar:

```powershell
powershell -ExecutionPolicy Bypass -File .\restore.ps1 -BackupDir .\backups\NOME-DO-BACKUP
```

O backup deve incluir:

- banco de dados;
- pasta `media/`;
- arquivos `.env`;
- logs, se forem necessarios para auditoria;
- documentacao.

### 18.3 Atualizacao e validacao

Antes de publicar mudancas:

```powershell
py -3.14 manage.py check --settings=juventude_mst.settings.local
py -3.14 manage.py test --settings=juventude_mst.settings.test
```

### 18.4 Rede local

Para acesso em rede local:

```powershell
py -3.14 manage.py runserver 0.0.0.0:8000 --settings=juventude_mst.settings.local
```

Configurar:

```text
RAIZ_ALLOWED_HOSTS
RAIZ_CSRF_TRUSTED_ORIGINS
```

Exemplo:

```text
RAIZ_ALLOWED_HOSTS=127.0.0.1,localhost,testserver,10.0.0.169
RAIZ_CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000,http://10.0.0.169:8000
```

## 19. Referencias Oficiais

Este documento foi orientado por principios gerais de protecao de dados e direitos digitais. Para uso publico ou institucional, revisar com assessoria juridica.

Referencias:

- Lei Geral de Protecao de Dados Pessoais, Lei 13.709/2018: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- Marco Civil da Internet, Lei 12.965/2014: https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm
- Marco Regulatorio das Organizacoes da Sociedade Civil, Lei 13.019/2014: https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l13019.htm
- OSCIP, Lei 9.790/1999: https://www.planalto.gov.br/ccivil_03/leis/l9790.htm
