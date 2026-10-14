# Verificação do Kubera ERP

Este arquivo registra somente verificações executadas em 14/10/2026 no Windows, com Frappe v16 e o fork `kubera-v16`.

## Testes automatizados

Execute na raiz do repositório:

```bash
python erpnext/tests/test_kubera_branding.py
python erpnext/tests/test_kubera_app_name.py
python erpnext/tests/test_kubera_navigation.py
python erpnext/tests/test_kubera_onboarding.py
python -m compileall -q erpnext/hooks.py erpnext/setup/install.py erpnext/patches/v16_0/kubera_app_name.py erpnext/patches/v16_0/kubera_onboarding_title.py
git diff --check
```

Os quatro arquivos de teste passaram: **12 testes** no total. Os arquivos Python alterados compilaram, os JSON alterados foram parseados e `git diff --check` terminou sem erros.

## Interface e instalação local

Com um site local em execução, use o `agent-browser` da Vercel:

```bash
agent-browser --session kubera open http://localhost:8080/login
agent-browser --session kubera snapshot -i
agent-browser --session kubera screenshot kubera-login.png --full
agent-browser --session kubera errors
```

Uma imagem Docker personalizada foi construída com Frappe v16 e este fork; o site `frontend` foi criado com `--install-app erpnext`. Após atualizações incrementais da imagem local, `bench --site frontend migrate` executou `kubera_onboarding_title` e terminou sem erro. No site instalado, `Website Settings.app_logo` apontou para `kubera-wordmark.svg`, e `Module Onboarding/Organization Onboarding.title` passou a `Get to know Kubera ERP`.

Com o `agent-browser` da Vercel, foram verificados:

- Login HTTP 200, wordmark **Kubera ERP** legível, sem erros retornados por `agent-browser errors`.
- Autenticação do administrador e Desk com Dock em português. Contabilidade abriu `/desk/accounts/accounting` com Chart of Accounts e Sales Invoice; Vendas abriu `/desk/selling` com Quotation e Sales Order; Estoque abriu `/desk/stock` com Item e Stock Entry; Produção abriu `/desk/manufacturing` com BOM e Work Order.
- Usuário de sistema com apenas `Accounts User` entrou no Desk e abriu Contabilidade. Usuário `Website User` recebeu `Not Permitted` ao abrir `/desk/home`.
- Tema claro e atributos de tema escuro no Desk exibiram texto e ações legíveis. Capturas locais estão no relatório de entrega, fora do repositório.

## Limites observados

Os testes cobrem instalação, migração, apresentação, navegação e dois perfis de acesso em um site local com dados fictícios. Não foram executados fluxos transacionais completos, teste de carga, implantação em produção ou auditoria exaustiva de todas as permissões de cada DocType. A imagem local final foi atualizada por camada incremental sobre o build completo anterior, após o Docker Desktop interromper uma segunda construção completa; o código final do fork, inclusive os dois patches, foi aplicado ao site e migrado.
