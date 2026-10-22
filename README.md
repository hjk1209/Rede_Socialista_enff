# Rede Raizes Socialista

Sistema Django para rede social comunitaria com cadastro basico, feed, comunidades, relatoria, saude, almoxarifado, financeiro, infraestrutura, mensagens e seguranca operacional.

## Inicio Rapido

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

No Windows, o menu operacional tambem faz esse fluxo:

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

Comandos diretos do menu:

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action local -Port 8000
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action lan -Port 8000
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action check
powershell -ExecutionPolicy Bypass -File .\start.ps1 -Action validate
```

## Cadastro Basico

O cadastro publico fica em:

```text
http://127.0.0.1:8000/conta/cadastro/
```

Campos principais:

- nome
- nome de perfil
- usuario interno
- email
- tipo de perfil
- senha, com minimo de 6 caracteres

Usuarios logados podem trocar a propria senha em:

```text
/conta/perfil/senha/
```

Perfis especiais, como Relatoria, Saude e Almoxarifado, sao liberados pela gestao em `Protecao/Gestao`.

## Perfis Demo

Todos usam a senha:

```text
MstJuventude!2026
```

- `coord.juventude` - fundador/gestao
- `brigada.campo` - comunidade/coletivo
- `comunica.mst` - moderacao e relatoria
- `maria.raiz` - membro comum
- `saude.unidade` - operador de saude
- `almox.enff` - operador de almoxarifado
- `financeiro.mst` - operador financeiro
- `infra.coord` - coordenacao da infra
- `ti.infra` - operador de TI
- `producao.infra` - operador de producao
- `jardim.infra` - operador de jardinagem
- `manutencao.infra` - operador de manutencao

## Dependencias

Ambiente local minimo:

```powershell
py -3.14 -m pip install -r requirements.txt
```

Producao/Docker:

```powershell
py -3.14 -m pip install -r requirements-prod.txt
```

Detalhes ficam em [docs/dependencias.md](docs/dependencias.md).

## Validacao

```powershell
py -3.14 manage.py check --settings=juventude_mst.settings.local
py -3.14 manage.py makemigrations --check --dry-run --settings=juventude_mst.settings.local
py -3.14 manage.py test --settings=juventude_mst.settings.test
```

Ou:

```powershell
powershell -ExecutionPolicy Bypass -File .\validate.ps1
```

## Estrutura

```text
accounts/       usuarios, login, cadastro e permissoes
core/           home, seguranca, auditoria, midia protegida e comandos
health/         modulo de saude
messaging/      mensagens diretas
social/         feed, comunidades, stories e relatoria
warehouse/      almoxarifado, acervo, movimentacoes e estoque
finance/        orcamentos, entradas, despesas, aprovacao e prestacao de contas
infra/          solicitacoes, dialogo e calendario comum da infraestrutura
juventude_mst/  configuracao Django e rotas principais
templates/      HTML por modulo
static/         CSS e JavaScript
media/          arquivos enviados em ambiente local
logs/           logs locais
docs/           documentacao tecnica padronizada
manual/         guias praticos para abrir, mover e proteger o sistema
```

Detalhes ficam em [docs/estrutura.md](docs/estrutura.md).

## Documentos Padronizados

- [docs/estrutura.md](docs/estrutura.md)
- [docs/dependencias.md](docs/dependencias.md)
- [docs/cadastro-basico.md](docs/cadastro-basico.md)
- [docs/visual-ossn.md](docs/visual-ossn.md)
- [docs/infra.md](docs/infra.md)
- [docs/financeiro.md](docs/financeiro.md)
- [docs/manual-de-uso-termos-e-dados.md](docs/manual-de-uso-termos-e-dados.md)
- [manual/README.md](manual/README.md)
- [manual/abrir-em-outro-lugar.md](manual/abrir-em-outro-lugar.md)
- [manual/acesso-dados-e-retencao.md](manual/acesso-dados-e-retencao.md)

Os nomes foram mantidos em minusculo, sem espacos e em ASCII para evitar problemas no Windows, Docker e Git.

## Docker

```powershell
Copy-Item .env.prod.example .env
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py bootstrap_juventude_mst
```

## Rede Local

```powershell
powershell -ExecutionPolicy Bypass -File .\start_lan.ps1
```

## Backup Local

```powershell
powershell -ExecutionPolicy Bypass -File .\backup.ps1
```

Restaurar:

```powershell
powershell -ExecutionPolicy Bypass -File .\restore.ps1 -BackupDir .\backups\20260518-120000
```

## Variaveis Principais

O prefixo `RAIZ_` foi mantido por compatibilidade com scripts e ambientes antigos. O nome publico padrao agora e `Rede Raizes Socialista`.

- `RAIZ_SITE_NAME`
- `RAIZ_SITE_DESCRIPTION`
- `RAIZ_SECRET_KEY`
- `RAIZ_DEBUG`
- `RAIZ_ALLOWED_HOSTS`
- `RAIZ_CSRF_TRUSTED_ORIGINS`
- `RAIZ_ENABLE_REALTIME`
- `RAIZ_DB_ENGINE`
- `RAIZ_CACHE_BACKEND`
- `RAIZ_CACHE_LOCATION`
- `RAIZ_DEFAULT_FROM_EMAIL`


# Disponibilizar la aplicacion para la red local de la institucion

## Servidor DNS

La primer opcion más recomendable es agregar un servidor DNS que pueda ser a la vez de nomenclador de ip's de la red para acceder por ejemplo a la aplicacion en vez de por la ip 10.20.20.X:8000 podamos entrar cualquier persona conectado a la red desde cualquier navegador entrando a la url http://enff.rrs.com:8000

A su vez, el servidor DNS servirá como filtro de seguridad para controlar el acceso o no a ciertas aplicaciones que defina poíticamente la institucion como criterio de seguridad. Ejemplo, que el servidor DNS impida anuncios para evitar caer en estafa como phishing o otras técnicas de hacking, malware o ramswere.

**Sugerencia**: ***la app de código abierto y de facil uso puede ser en primer lugar Adguard, en segundo lugar PiHole. Son faciles de implementar y que necesita pocos recursos para correr.***

### Servidor DNS local para una única aplicacion

La alternativa sin servidor DNS implica que se debe modificar manualmente el archivo hosts en cada máquina cliente. Para personas propias de la institución esto no es mucho trabajo. Se realiza una vez asegurando que una persona que tenga el conocimiento técnico lo haga para cada área/sector/unidad de la institución.

* En Linux/Mac: /etc/hosts
* En Windows: C:\Windows\System32\drivers\etc\hosts

En ambos casos se añade la línea: [IP_DE_LA_VM] enff.rrs.com

## Servidor reverse-proxy

Un aspecto importante en la disponibilizacion de una aplicacion es orientar el flujo de entrada y de salida por distintos puertos que permita no abrir más puertos que el 80 para el servidor y que este programa pueda reorientar a comunicar todas las apps con la única salida del puerto 80.

Esto permitiría que además de acceder a la app por http://enff.rrs.com:8000 podamos omitir de colocar el puerto y que sea más directa la navegación, más profesional y como medida de seguridad no mostrar el puerto donde se esta ejecutando la aplicacion y no mostrar una "vulnerablidad" de peurta de ataque.

**Sugerencia**: ***la app de código abierto y de facil uso puede ser en primer lugar NGINX***

## Modificación en el archivo de variables de entorno

el archivo .env deberá modificarse de esta manera

```.env
    RAIZ_SECRET_KEY=tu_clave_secreta_super_segura_aqui
    RAIZ_ALLOWED_HOSTS=enff.rrs.com,localhost,127.0.0.1,[IP_DE_LA_VM]
    RAIZ_CSRF_TRUSTED_ORIGINS=http://enff.rrs.com,http://enff.rrs.com:8000,http://[IP_DE_LA_VM]:8000
```

## Requerimientos

1. Cuando se crea la invitación no tiene la opción de crear una nueva invitacion, tenes que refrescar la pantalla para que borre el formulario.
2. 

### Usuarios

1. En el formulario para registrarse Nome y Nome do perfil parecen la misma informacion. Dejar solo Nome
2. Data de nascimento y WhatsApp parecen datos irrelevantes para crear el perfil. Esa informacion se tiene por el documento cuando ingresan a la enff. La Bio y Local tambien parecen campos que se pueden sacar.
3. Tiene que aclarar cuales son los caracteres especiales que no permite cada cuadro de texto en el momento de crear usuarios

### Relatorías

1. Una vez que se sube la mística no se puede visualizar lo que esta subido pudiendo provocar que se cargue varias versiones de un mismo archivo. 
2. El archivo se sube con el nombre que le pone el usuario, debería convertirse a un hash para que sea imposible repetirse nombres de archivos y que si fuese una base de datos se pueda indexar. 

**ESTO TAMBIEN SE UTILIZARIA PARA LAS FOTOS JUNTO A LA COMPRESION O CAMBIO DE FORMA DE JPG/PNG A WEBP POR EJEMPLO** - ver informe en docs/requirimientos/2026-10-22-compresion-imagenes-y-hash-de-archivos.md


### Feed

1. Buscador de personas no anda - OK anda
2. Despues de hacer un comentario refresca la pagina
3. Al abrir la aplicacion de celular, las cajas de "buscar personas", "post", "comunidades" se ponen arriba y no dejan ver los posteos actuales. Es mejor que cuando hay resoluciones cortas estas opciones queden con un ícono. 
4. No tiene la opcion de eliminar posteos
5. En las historias tiene muchos perfiles para decidir los que pueden ver y leer. Hay que implementarlo de otra manera más sencilla. Cuando alla muchos perfiles, buscar en toda la lista demora mucho el proceso de cargar una historia.
6. En la historia poner la música tambien lleva tiempo, habría que ver de vincular con alguna api el buscador de youtube o otra app para buscar el tema directamente.
7. Las comunidades destacadas podría estar con un ícono abajo o arriba en un carrousel. Sino podría darse ese lugar a las historias subidas y dejar las comunidades con un submenú dentro de la opcion de menú principal de Comunidades.
8. La opcion "Abrir perfil" abajo a la derecha en el feed esta repetida con la opcion izquierda al inicio del feed que te lleva al perfil.

### Gestao

1. Usaría para toda la página la premisa de visualizar las acciones posibles a realizar y que cada formulario sea una página independiente en vez de tener todos los formularios y listas en una sola página.
    * Adicionar usuario
    * Convites unicos
    * Usuarios da plataforma
2. Para la pagina de Usuarios da plataforma usaría una lista con un buscador con las opciones en íconos de Editar, Borrar, Historial. Cada una de estas opciones te lleva a una página


### CHANGES.log

1. Se creo una skill llamada informe-requerimiento para poder hacer una nota en markdown para el baul de obsidian así podemos almacenar las planificaciones para los requerimientos a futuro a resolver y tener un historial
2. Desactivar la suspension de energía de Windows para que no se apague el wifi de la computadora y pueda accederse. Además configuramos el wifi para que se reconecte solo a la red por algun problema y que la app se inicie automaticamente si el equipo se reinicia en tal caso. 