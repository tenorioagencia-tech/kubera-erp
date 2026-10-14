# Implantação do Kubera ERP

## Pré-requisitos

- Frappe Framework `version-16` e ERPNext deste fork, branch `kubera-v16`.
- Bench com MariaDB, Redis, Node e Python nas versões suportadas pelo Frappe v16.
- Para Docker, use o [frappe_docker oficial](https://github.com/frappe/frappe_docker) com uma imagem própria. O `pwd.yml` daquele projeto é uma demonstração descartável e não instala este fork.

## Bench

```bash
bench get-app --branch kubera-v16 https://github.com/tenorioagencia-tech/kubera-erp.git
bench new-site kubera.localhost
bench --site kubera.localhost install-app erpnext
bench build --app erpnext
bench --site kubera.localhost migrate
```

Se o site já contém ERPNext v16, faça backup do banco e arquivos, atualize o checkout do app para `kubera-v16`, execute `bench --site <site> migrate`, `bench build --app erpnext` e limpe o cache. Verifique login e fluxos antes de liberar usuários. O patch `kubera_app_name` só troca nomes padrão (`ERPNext`, `Frappe` ou vazio); nomes personalizados não são sobrescritos.

## Imagem Docker personalizada

No repositório `frappe_docker`, crie `apps.json` com o app deste fork:

```json
[{"url":"https://github.com/tenorioagencia-tech/kubera-erp.git","branch":"kubera-v16"}]
```

Use a [construção oficial de imagem customizada](https://github.com/frappe/frappe_docker/blob/main/docs/02-setup/02-build-setup.md) com `FRAPPE_BRANCH=version-16` e o secret `apps_json`. Depois configure os serviços MariaDB/Redis, crie o site com `--install-app erpnext` e exponha a interface pelo frontend do compose. Não use credenciais da demonstração em produção.

## Marca, menus e papéis

- O app continua com o identificador técnico `erpnext`. Não renomeie pacotes Python, DocTypes, nomes de Workspace, `link_to` ou rotas.
- O nome exibido é **Kubera ERP**. `Website Settings.app_name` controla o texto do login; `Website Settings.app_logo` e `Navbar Settings.app_logo` podem substituir o logo do hook.
- O Dock usa rótulos em português, com destinos, ordem e visibilidade originais. Sidebars, Workspaces e menus mantêm as ações nativas.
- O fork não altera as permissões de DocTypes. Configure usuários, Role Profiles e Role Permission Manager no site, segundo a matriz de acesso da Kubera. Ocultar um menu não revoga acesso ao documento.

## Atualização

Mantenha o remote `upstream` para `frappe/erpnext`. Ao incorporar atualizações de `version-16`, compare as mudanças em hooks, Dock, Workspaces, assets e patches antes do merge. Execute os testes `test_kubera_*.py`, migração e verificação visual em ambiente de teste. Preserve `license.txt` e os avisos de autoria.
