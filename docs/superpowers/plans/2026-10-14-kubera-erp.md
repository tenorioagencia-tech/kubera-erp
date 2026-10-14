# Kubera ERP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publicar um fork instalável do ERPNext v16 com identidade Kubera ERP, conservando módulos e comportamento original.

**Architecture:** O pacote continua `erpnext`; hooks, assets, CSS e rótulos visuais fornecem o white-label. Um patch de configuração altera somente o nome padrão e preserva personalizações existentes. Uma comparação automatizada com o commit base protege os links e a visibilidade de navegação.

**Tech Stack:** Frappe/ERPNext v16, Python, JSON, SCSS/CSS, Docker, Vercel `agent-browser`.

**Spec:** `docs/superpowers/specs/2026-10-14-kubera-erp-design.md`

## Global Constraints

- App interno `erpnext`; nome visível exato `Kubera ERP`.
- Base `frappe/erpnext` `version-16` commit `7474d9e786277383de1242ab882f16856d17a9c9`.
- Nenhum novo módulo de negócio, DocType ou alteração em API, rota, `link_to`, `link_type`, `hidden`, ordem do Dock e permissões de DocType.
- Paleta `#f2efe8`, `#171714`, `#11110f`, `#ece6dc`; família Poppins com fallback.
- Preservar GPLv3, autoria Frappe e relação de fork com upstream.

## Review Focus

- Instância com nome personalizado: patch mantém o valor; testar antes de escrever.
- Usuário de website e usuário Desk não administrador: acesso ao app permanece como upstream; testar função de permissão e navegação.
- Tema escuro ou falta de fonte remota: interface continua legível; verificar no navegador.
- Menu oculto de CRM/Suporte: estado `hidden` permanece igual à base; teste de comparação JSON.
- Atualização upstream: não muda IDs internos nem destinos; teste automático compara campos protegidos com o commit base.

---

### Task 1: Assets e metadados de marca

**Files:** `erpnext/hooks.py`, `erpnext/public/images/kubera-logo-white.png`, `erpnext/public/images/kubera-icon.svg`, `erpnext/public/images/kubera-favicon.svg`, `erpnext/tests/test_kubera_branding.py`.

- [ ] Escrever teste falhando para `app_title`, `app_logo_url`, Apps Screen, favicon e preservação de `app_name`, `app_publisher`, `app_license`.
- [ ] Incorporar logo oficial e criar ícone/favicons com monograma Kubera em fundo `#11110f`.
- [ ] Ajustar apenas os campos de apresentação de hooks e executar teste.
- [ ] Conferir licença e `git diff`; commit da tarefa.

### Task 2: Configuração do site e migração idempotente

**Files:** `erpnext/setup/install.py`, `erpnext/patches.txt`, `erpnext/patches/v16_0/kubera_app_name.py`, `erpnext/tests/test_kubera_branding.py`.

- [ ] Escrever teste falhando: instalação usa Kubera ERP; patch converte `ERPNext` para `Kubera ERP`, preserva nome personalizado e não altera outros ajustes.
- [ ] Implementar patch com entrada ao final de `patches.txt` e ajustar instalador.
- [ ] Rodar testes da tarefa e compilação Python; commit.

### Task 3: Tema do Desk

**Files:** `erpnext/public/scss/erpnext.bundle.scss`, `erpnext/public/scss/kubera.scss`.

- [ ] Adicionar regras de marca ao bundle existente, com tokens de cores e tipografia, sem modificar layout de formulários.
- [ ] Verificar CSS compilado no ambiente Frappe e contraste visual nos estados claro e escuro.
- [ ] Commit.

### Task 4: Navegação de apresentação

**Files:** `erpnext/dock/erpnext/erpnext.json`, `erpnext/desktop_icon/erpnext.json`, `erpnext/desktop_icon/erpnext_settings.json`, `erpnext/tests/test_kubera_navigation.py`.

- [ ] Escrever teste que compara `link_to`, `link_type`, `hidden`, ordem e `name` com `git show 7474d9e:...` e verifica os novos rótulos.
- [ ] Renomear títulos visíveis do Dock em português: Configurações, Contabilidade, Vendas, Compras, Estoque, Produção, Projetos, Patrimônio, Qualidade, CRM, Suporte, Portal. Renomear somente `label` do Desktop Icon do app e de Configurações.
- [ ] Validar JSON/testes; commit.

### Task 5: Empacotamento, execução e verificação final

**Files:** `README-KUBERA.md`, `docs/kubera/deployment.md`, `docs/kubera/verification.md`.

- [ ] Documentar instalação Frappe v16, uso do fork `kubera-v16`, atualização, licença e configurações de marca/roles pelo Frappe.
- [ ] Subir ambiente local com o código modificado, instalar/migrar site e compilar assets.
- [ ] Instalar/usar `agent-browser` da Vercel para login, tela de apps, marca, navegação, captura e erros; registrar resultados reais.
- [ ] Executar testes automatizados, revisar `git diff` e status, publicar branch no fork e registrar limitações honestamente.

## Execution

Usar desenvolvimento com subagentes. Tasks 1 e 4 podem ser implementadas em paralelo porque não compartilham arquivos; Tasks 2 e 3 só começam depois da integração da Task 1. Revisar cada diff contra a especificação e executar verificação final em conjunto.
