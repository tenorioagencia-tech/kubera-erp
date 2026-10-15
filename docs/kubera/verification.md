# Verificação do Kubera ERP

Verificações locais executadas em 14/10/2026 com Frappe v16 e o fork `kubera-v16`.

## Testes de código e traduções

Na raiz do repositório:

```bash
python -m unittest discover -s erpnext/tests -p 'test_kubera_*.py'
python -m compileall -q erpnext/hooks.py erpnext/setup/install.py erpnext/patches/v16_0
git diff --check
```

Os **29 testes** passaram. Eles cobrem a marca, o idioma padrão do site e de usuários, traduções complementares, preservação de identificadores e links, e migrações idempotentes. O catálogo `pt_BR.po` foi parseado e compilado: 10.059 de 10.308 mensagens têm tradução; as 4.888 mensagens alteradas nesta etapa preservam os mesmos placeholders do texto de origem. Os JSON dos painéis foram parseados e os cartões continuaram ligados às respectivas seções.

## Site e navegador

Uma imagem local com Frappe v16 e este fork foi construída. No site Docker `frontend`, `bench --site frontend migrate` terminou sem erro e executou `kubera_workspace_ptbr_round2`, `kubera_user_language_ptbr` e `kubera_workspace_ptbr_round3`; `bench compile-po-to-mo --app erpnext --locale pt_BR --force` gerou o arquivo MO. A consulta ao banco confirmou `System Settings.language = pt-BR`, `User/Administrator.language = pt-BR`, `Workspace/Accounting.label = Contabilidade` e `Module Onboarding/Accounting Onboarding.title = Prepare sua contabilidade`.

Com o `agent-browser` da Vercel, foram conferidos login, Dock, assistentes de Contabilidade, Estoque, Produção e Vendas, relatórios e abertura de um relatório a partir do rótulo traduzido. “Entrar”, “Esqueceu a senha?”, “Opcional”, “Reproduzir vídeo”, títulos de relatórios e filtros apareceram em português. O navegador confirmou `frappe.boot.user.language = pt-BR` e o calendário mostrou “Outubro” e “Hoje”. Após a correção final, Estoque mostrou “Idade e valor do estoque por armazém e item”; Produção mostrou “Ordens de trabalho abertas”. O diff semântico dos JSON finais encontrou 22 mudanças, todas em valores de apresentação; `agent-browser errors` não retornou erros. Evidências visuais estão no relatório de entrega, fora do repositório.

## Limites

O catálogo do ERPNext ainda possui 249 mensagens sem tradução, em sua maioria unidades técnicas, HTML, modelos de mensagem ou texto longo. O framework Frappe mantém seu próprio catálogo, separado deste fork; telas não percorridas podem apresentar termos em inglês. Parte das novas traduções foi gerada com auxílio automático e validada estruturalmente, mas não passou por revisão linguística integral. Os testes foram locais, com dados fictícios; não houve auditoria de todas as telas, fluxos transacionais completos, carga ou implantação em produção.
