# Kubera ERP

![Kubera Mobiliário Sob Medida](erpnext/public/images/kubera-logo-white.png)

Kubera ERP é a edição visual da [Kubera Mobiliário Sob Medida](https://kuberamobiliariosobmedida.com.br/) sobre o ERPNext Community v16. Preserva os módulos, documentos, APIs e fluxos do ERPNext. Esta edição altera marca, cores, rótulos de navegação e o nome padrão exibido no site. O app instalável continua chamado `erpnext` para manter compatibilidade com o Frappe.

## Funcionalidades

Contabilidade, vendas, compras, estoque, produção, projetos, ativos, qualidade, CRM, suporte e portal continuam disponíveis conforme os papéis e as configurações originais do ERPNext. Nenhum módulo de negócio foi adicionado nesta etapa.

## Instalação

Use Frappe Framework `version-16` e esta branch `kubera-v16`. Com um bench v16 preparado:

```bash
bench get-app --branch kubera-v16 https://github.com/tenorioagencia-tech/kubera-erp.git
bench new-site kubera.localhost
bench --site kubera.localhost install-app erpnext
bench build --app erpnext
bench --site kubera.localhost migrate
```

O nome interno `erpnext` é necessário para a instalação; `Kubera ERP` é o nome exibido. Consulte [implantação](docs/kubera/deployment.md) para Docker, migração e configurações do site.

## Personalização e acesso

O logo e o nome padrão são fornecidos pelo fork. Um administrador pode ajustá-los em Website Settings e Navbar Settings do Frappe. Perfis e permissões de DocTypes permanecem os originais; defina uma matriz de acesso de negócio no Role Permission Manager antes de atribuir papéis aos usuários.

## Origem e licença

Este repositório é um fork de [frappe/erpnext](https://github.com/frappe/erpnext) baseado na branch `version-16`, commit `7474d9e786277383de1242ab882f16856d17a9c9`. O código original e suas alterações continuam sob [GNU GPL v3](license.txt). Frappe Technologies Pvt. Ltd. permanece creditada como autora do projeto original. “ERPNext” é marca de Frappe Technologies; a marca de produto desta edição é “Kubera ERP”. Consulte a [política de marcas do projeto original](TRADEMARK_POLICY.md).

## Verificação

Os testes de marca, configuração e navegação estão em `erpnext/tests/test_kubera_*.py`. O estado real da validação e suas limitações estão em [verification.md](docs/kubera/verification.md).
