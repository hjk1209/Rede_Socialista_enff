# Abrir o Sistema em Outro Lugar

Este guia serve para abrir a `Rede Raizes Socialista` em outro computador, servidor local ou servidor de producao.

## 1. O que nunca deve ser perdido

Os dados reais do sistema ficam principalmente nestes locais:

- `db.sqlite3`: banco de dados local com usuarios, posts, mensagens, saude, almoxarifado, financeiro, infra, auditoria e configuracoes internas;
- `media/`: avatares, imagens de posts, stories, relatoria, fotos do acervo e comprovantes financeiros;
- `.env`: variaveis do ambiente, segredo do Django, hosts liberados e configuracoes sensiveis;
- `backups/`: copias de seguranca;
- `logs/`: logs tecnicos e de seguranca.

Ao atualizar ou mover o sistema, preserve esses itens.

## 2. Criar backup antes de mover

No computador ou servidor antigo, dentro da pasta do projeto:

```powershell
powershell -ExecutionPolicy Bypass -File .\backup.ps1
```

O backup fica em:

```text
backups/ANO MES DIA-HORA
```

Exemplo:

```text
backups/20260603-203000
```

Esse backup copia:

- `db.sqlite3`;
- `media/`, compactada como `media.zip`;
- logs disponiveis.

## 3. Abrir uma instalacao nova sem dados antigos

Use este caminho apenas quando for criar uma instalacao vazia ou demonstrativa.

```powershell
py -3.14 -m pip install -r requirements.txt
py -3.14 manage.py migrate --settings=juventude_mst.settings.local
py -3.14 manage.py bootstrap_juventude_mst --settings=juventude_mst.settings.local
py -3.14 manage.py runserver 127.0.0.1:8000 --settings=juventude_mst.settings.local
```

Abra:

```text
http://127.0.0.1:8000/
```

Atencao: `bootstrap_juventude_mst` cria dados demonstrativos. Nao use em cima de banco real sem necessidade.

## 4. Abrir em outro computador mantendo dados antigos

No computador novo:

1. Copie a pasta do projeto ou clone o repositorio.
2. Instale as dependencias.
3. Copie o backup criado no computador antigo para dentro da nova pasta.
4. Restaure o backup.
5. Aplique migrations.
6. Inicie o servidor.

Comandos:

```powershell
py -3.14 -m pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File .\restore.ps1 -BackupDir .\backups\NOME-DO-BACKUP
py -3.14 manage.py migrate --settings=juventude_mst.settings.local
py -3.14 manage.py runserver 127.0.0.1:8000 --settings=juventude_mst.settings.local
```

Para rede local:

```powershell
py -3.14 manage.py runserver 0.0.0.0:8000 --settings=juventude_mst.settings.local
```

Ou:

```powershell
powershell -ExecutionPolicy Bypass -File .\start_lan.ps1
```

## 5. Atualizar uma instalacao existente

Quando o servidor ja tem dados reais:

```powershell
powershell -ExecutionPolicy Bypass -File .\backup.ps1
git pull origin main
py -3.14 manage.py migrate --settings=juventude_mst.settings.local
py -3.14 manage.py check --settings=juventude_mst.settings.local
```

Depois reinicie o servidor.

Nao delete a pasta inteira para copiar outra por cima. Isso pode apagar `db.sqlite3`, `media/`, `.env`, logs e backups.

## 6. Validar depois de abrir

```powershell
py -3.14 manage.py check --settings=juventude_mst.settings.local
py -3.14 manage.py makemigrations --check --dry-run --settings=juventude_mst.settings.local
py -3.14 manage.py test --settings=juventude_mst.settings.test
```

Ou:

```powershell
powershell -ExecutionPolicy Bypass -File .\validate.ps1
```

## 7. Variaveis importantes

O arquivo `.env` deve ser protegido. Ele pode conter:

- `RAIZ_SECRET_KEY`;
- `RAIZ_DEBUG`;
- `RAIZ_ALLOWED_HOSTS`;
- `RAIZ_CSRF_TRUSTED_ORIGINS`;
- `RAIZ_DB_ENGINE`;
- `RAIZ_DB_NAME`;
- `RAIZ_CACHE_BACKEND`;
- `RAIZ_DEFAULT_FROM_EMAIL`.

Em producao:

- use `RAIZ_DEBUG=False`;
- use uma `RAIZ_SECRET_KEY` forte;
- configure `RAIZ_ALLOWED_HOSTS` com o dominio ou IP correto;
- nao use senha demo em contas reais.

## 8. Checklist antes de entregar para outra pessoa

- Backup criado e testado.
- `.env` protegido.
- Senhas demo trocadas.
- Admin/fundador definido.
- Operadores de saude, almoxarifado, financeiro e infra revisados.
- `db.sqlite3` e `media/` preservados.
- Firewall/rede liberado apenas para quem precisa.
- Comando de inicio documentado para o novo local.
