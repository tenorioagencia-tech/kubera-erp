# Kubera ERP — design do white-label

## Intenção e escopo

Transformar um fork do ERPNext Community v16 em Kubera ERP para uso interno da Kubera Mobiliário Sob Medida. O produto deve manter os fluxos, documentos, relatórios, APIs e módulos originais. Nesta etapa só mudam a identidade apresentada, a navegação visual e os padrões de configuração de marca. Não serão criados módulos de negócio.

O pedido não define uma matriz própria de cargos. Por isso, os direitos de acesso de DocTypes e relatórios continuam iguais aos do ERPNext. O acesso do usuário de sistema ao app continua governado pelo `check_app_permission` existente; usuários de website continuam sem acesso ao Desk. A administração poderá ajustar papéis pelos mecanismos nativos do Frappe quando houver uma matriz aprovada pela Kubera.

## Alternativas consideradas

1. **Fork dirigido do app ERPNext (escolhido):** trocar somente metadados de apresentação, assets, rótulos visuais e configurações de marca. Preserva o pacote Python `erpnext`, nomes de documentos e rotas, além de facilitar atualização via upstream.
2. **Renomeação global de ERPNext para kubera:** quebra imports, patches, dependências e links persistidos; rejeitada.
3. **App adicional de branding:** evita parte do diff no fork, mas cria outro app e contraria a restrição de não criar módulos nesta fase; rejeitada.

## Base e identidade

- Base: `frappe/erpnext`, branch `version-16`, commit `7474d9e786277383de1242ab882f16856d17a9c9` na criação do fork; trabalho em `kubera-v16`.
- Repositório: `https://github.com/tenorioagencia-tech/kubera-erp`; o app instalável permanece `erpnext`.
- Nome público e no Desk: **Kubera ERP**.
- Marca da Kubera: fundo `#f2efe8`, texto `#171714`, superfícies escuras `#11110f`, texto claro `#ece6dc`, linhas `rgba(23,23,20,.18)`, família Poppins com fallback sans-serif.
- O logo branco publicado em `https://kuberamobiliariosobmedida.com.br/brand/kubera-logo-white.png` será incorporado ao fork para uso em superfícies escuras. Um ícone quadrado derivado da marca será criado para a tela de apps e favicon. O logo de terceiros do ERPNext não será usado como marca do produto.
- Avisos de licença, autoria de Frappe e links de código-fonte permanecem explícitos. O fork continua sob GPLv3.

## Arquitetura e fluxo

`erpnext/hooks.py` fornecerá `app_title`, logo, favicon e bundles de estilo de Kubera ERP. O instalador define o nome do produto em `System Settings`. Um patch idempotente corrige instâncias que ainda mostram o nome padrão do ERPNext, sem sobrescrever um nome personalizado existente. `Website Settings` e `Navbar Settings` poderão prevalecer conforme o comportamento normal do Frappe.

No Desk v16, o Dock e Desktop Icon receberão nomes e assets de apresentação. O Dock conserva todos os `link_to`, `link_type`, `hidden` e a ordem originais. As Sidebars conservam seus destinos. Não serão renomeados identificadores `name` dos registros padrão nem IDs de DocType, Workspace e Module Def.

O tema será aplicado no bundle CSS já carregado pelo ERPNext, com tokens limitados ao Desk e regras de contraste. A tipografia utilizará Poppins quando disponível, com fallback local. O tema não alterará layouts funcionais, campos, formulários ou transações.

## Comportamento de erro e atualização

Sem o logo local, o carregamento da interface continua, mas o app não deve apontar para marca do ERPNext como fallback explícito. O patch de nome só altera valores `ERPNext` ou vazios; valores específicos de um site são preservados. Links internos continuam iguais, de modo que favoritos, permissões e integrações sigam funcionando.

Atualizações futuras exigem rebase e revisão dos poucos arquivos de apresentação modificados. A marca não muda o nome do pacote instalado nem a versão do ERPNext. Mudanças de navegação upstream serão comparadas antes do merge.

## Validação e aceitação

1. Validação estática: JSON válido; `git diff` sem mudanças em `link_to`, `link_type`, papéis, DocTypes, migrações existentes ou módulos; imports Python compilam.
2. Testes automatizados: verificam metadados de marca, patch idempotente e conservação de destinos/visibilidade do Dock frente à base upstream.
3. Ambiente real: instalar o fork com Frappe v16 em Docker, executar migração/build e verificar login, tela de apps, Dock, navegação para Vendas/Estoque/Produção/Contabilidade e um usuário não administrador.
4. Frontend: usar o `agent-browser` da Vercel para snapshot, screenshot, console e erros no site em execução, com evidência da marca Kubera ERP.

Se o ambiente Docker não permitir completar a instalação, a entrega deve indicar precisamente quais verificações foram executadas e quais não foram, sem afirmar validação visual ou funcional não observada.
