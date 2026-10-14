# Verificação do Kubera ERP

Este arquivo registra somente verificações executadas. A validação completa requer um site Frappe v16 com o fork instalado, migração e build concluídos.

## Testes automatizados

Execute na raiz do repositório:

```bash
python erpnext/tests/test_kubera_branding.py
python erpnext/tests/test_kubera_app_name.py
python erpnext/tests/test_kubera_navigation.py
python -m compileall -q erpnext/hooks.py erpnext/setup/install.py erpnext/patches/v16_0/kubera_app_name.py
git diff --check
```

## Critérios de interface

Com um site local em execução, use o `agent-browser` da Vercel:

```bash
agent-browser --session kubera open http://localhost:8080/login
agent-browser --session kubera snapshot -i
agent-browser --session kubera screenshot kubera-login.png --full
agent-browser --session kubera errors
```

Após autenticar um usuário de teste, confira a marca **Kubera ERP**, o ícone e favicon, as cores, o Dock e o acesso a Contabilidade, Vendas, Estoque e Produção. Confira um usuário Desk não administrador e um usuário Website para validar que as permissões originais continuam aplicadas. Registre erros de console e screenshots.

## Estado desta entrega

Pendente da verificação final desta branch. Os resultados executados serão anotados aqui antes da publicação.
