# Setor de Infra

Area operacional para organizar demandas de infraestrutura da escola.

## Estrutura Organizativa

- Coordenacao de infra: enxerga todos os setores, acompanha a fila geral e administra o calendario comum.
- TI: gerencia rede Wi-Fi, suporte tecnico, computadores e maquinas usadas pelos operadores.
- Producao: planeja, acompanha e registra o ciclo de producao agricola da escola.
- Jardinagem: organiza o cuidado dos jardins, areas verdes e paisagismo.
- Manutencao: atende demandas hidraulicas, eletricas, estruturais e reparos gerais.

## Fluxo

1. Qualquer usuario autenticado abre uma solicitacao em `/infra/`.
2. O operador do setor responsavel acompanha a fila do seu setor.
3. Usuario e operador conversam dentro da solicitacao.
4. O operador agenda reparo, visita ou manutencao.
5. A coordenacao de infra acompanha todos os setores pelo calendario comum.

## Area de TI

A aba de TI dentro de `/infra/` possui quatro partes:

- Computadores: lista maquinas cadastradas no inventario, com local, usuario responsavel, patrimonio, sistema operacional, IP, MAC e status.
- Mapa de rede: registra links, roteadores, switches, pontos Wi-Fi, segmentos e servidores conectados.
- Chamados TI: canal direto para qualquer usuario autenticado abrir chamado de computador, maquina, Wi-Fi ou rede.
- Inventario: cadastro tecnico de equipamentos e pontos de rede, visivel para operadores de TI, coordenacao da infra e administradores.

Os chamados diretos de TI sao salvos como `InfraRequest` com setor `TI`, mantendo o mesmo dialogo e historico das demais demandas de infra.

Os dados de inventario sao salvos em `TiInventoryItem`.

Os dados de mapeamento de rede sao salvos em `TiNetworkNode`.

## Permissoes

As permissoes ficam no perfil do usuario:

- `is_infra_coordinator`
- `is_infra_ti_operator`
- `is_infra_production_operator`
- `is_infra_gardening_operator`
- `is_infra_maintenance_operator`

Administradores, fundadores e superusuarios tambem coordenam a infra.
