# Cadastro Basico

Rota:

```text
/conta/cadastro/
```

O cadastro publico cria perfis comuns ou coletivos. A gestao libera permissoes especiais depois.

## Fluxo

1. Usuario acessa `/conta/cadastro/`.
2. Preenche nome, perfil, usuario interno, email e senha.
3. O sistema cria o perfil e faz login.
4. Perfis especiais sao editados no centro de gestao.

Senha minima: 6 caracteres.

## Perfis Especiais

- Relatoria: envia texto, varias fotos sem limite de tamanho no formulario e arquivos para comunidades/NBs.
- Saude: gerencia registros internos da unidade de saude.
- Almoxarifado: gerencia acervo, movimentacoes, acompanhamentos e estoque.

## Validacao Rapida

```powershell
py -3.14 manage.py test accounts core --settings=juventude_mst.settings.test
```
