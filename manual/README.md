# Manual Operacional

Esta pasta guarda os documentos praticos para abrir, atualizar e proteger a `Rede Raizes Socialista` em outro computador ou servidor.

## Documentos

- [Abrir o sistema em outro lugar](abrir-em-outro-lugar.md)
- [Acesso, dados retidos e responsabilidades](acesso-dados-e-retencao.md)

## Leitura rapida

Antes de mover ou atualizar o sistema, preserve sempre:

- `db.sqlite3`: banco de dados local;
- `media/`: fotos, anexos, comprovantes e arquivos enviados;
- `.env`: configuracoes e segredo do servidor;
- `backups/`: copias de seguranca;
- `logs/`: registros tecnicos e seguranca, quando forem necessarios para auditoria.

Para atualizar uma instalacao existente, o caminho seguro e:

```powershell
powershell -ExecutionPolicy Bypass -File .\backup.ps1
git pull origin main
py -3.14 manage.py migrate --settings=juventude_mst.settings.local
```

Nao apague a pasta inteira do servidor para substituir por outra sem antes fazer backup e separar os dados.
