# Referencia Visual OSSN

Referencia avaliada:

```text
https://github.com/opensource-socialnetwork/opensource-socialnetwork.git
```

## Conclusao

O OSSN e um sistema PHP completo. Nao vale importar o backend, templates PHP ou CSS inteiro para este projeto Django.
O melhor aproveitamento e usar a linguagem visual do tema `goblue` como referencia.

## Licenca

O reposititorio OSSN usa Open Source Social Network License / Cryptographic Autonomy License 1.0.
Por isso, nao copiamos arquivos de CSS, PHP, logo ou imagens proprietarias para dentro do nosso projeto.

Uso seguro feito aqui:

- estrutura visual inspirada no tema `goblue`;
- CSS proprio em `static/css/app.css`;
- nenhum logo ou arquivo de imagem do OSSN importado.

## Pontos Aproveitaveis

- Barra superior azul fixa, com navegacao direta.
- Fundo cinza claro para area autenticada.
- Cards brancos de feed com sombra leve.
- Feed central mais estreito e laterais de apoio.
- Comentarios em area cinza clara, parecida com bolhas.
- Perfil com area de capa visual e avatar mais destacado.
- Formularios com campos claros e bordas suaves.
- Mobile com menu horizontal rolavel.

## Direcao Invertida: GoBlue Com Nossos Modulos

A decisao atual e usar o modelo visual GoBlue como base social classica e colocar dentro dele os modulos que a Rede Raizes Socialista ja criou e que nao existem no fluxo padrao do OSSN.

Entraram como atalhos e cards proprios:

- Relatoria territorial com textos, multiplas fotos e arquivos.
- Comunidades e NBs com espaco publico ou privado e aprovacao de entrada.
- Saude popular.
- Almoxarifado e acervo.
- Protecao, gestao e auditoria.
- Midia protegida por rotas autenticadas.

Essa abordagem preserva a identidade e as regras do nosso Django, enquanto aproveita a organizacao visual de uma rede social de feed, laterais e cards.

## O Que Nao Importar Diretamente

- `themes/goblue/plugins/default/css/core/default.php`
- `components/OssnWall/plugins/default/css/wall.php`
- `components/OssnProfile/plugins/default/css/profile.php`
- logos em `themes/goblue/images/`
- templates PHP do OSSN
- componentes PHP de wall, chat, comentarios ou grupos

## Proximos Melhoramentos Possiveis

- Criar capa editavel para perfis e comunidades.
- Adicionar menu compacto com icones na barra superior.
- Melhorar editor de postagem com abas: texto, foto, privacidade.
- Criar modulo de albuns/fotos inspirado no fluxo do OSSN.
- Criar painel de notificacoes no topo.
