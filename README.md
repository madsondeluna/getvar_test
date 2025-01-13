# GET<i>Var</i> (Versão de Teste) 🧬👨🏻‍💻

## Aviso ⚠️

Esse é um **<i>repositório de testes</i>**. Pode apresentar instabilidades. 
Para a versão mais atualizadas acesse: 

```
https://github.com/madsondeluna/getvar_mvp
```

## Índice
1. [Descrição do Projeto](#descrição-do-projeto)
2. [Funcionalidades](#funcionalidades)
3. [Workflow da Aplicação](#workflow-da-aplicação)
4. [Tecnologias Utilizadas](#tecnologias-utilizadas)
5. [Estrutura do Projeto](#estrutura-do-projeto)
6. [Requisitos de Instalação](#requisitos-de-instalação)
7. [Instalação](#instalação)
8. [Execução](#execução)
9. [Exemplo de Uso](#exemplo-de-uso)
10. [Informações Adicionais de Uso](#informações-adicionais-de-uso)
11. [Usando o Dockerfile](#usando-o-dockerfile)
12. [Licença](#licença)
13. [Contato](#contato)
14. [Contribuindo](#contribuindo)

## Descrição do Projeto

O **GET<i>Var</i>** é uma ferramenta desenvolvida para **análise e anotação de variantes genéticas**. Com um workflow eficiente, a ferramenta integra dados de variantes genômicas para identificar e interpretar anotações de variantes de forma rápida e precisa em bancos de dados públicos.

## Funcionalidades

- **Análise de Variantes**: Processamento e visualização dados de variantes genéticas.
- **Anotação Funcional**: Integração de variantes com consulta em bancos de dados genéticos.
- **Automatização**: Workflow padronizado para maior eficiência.

## Workflow da Aplicação

1. **Entrada de Dados**:

   - Apenas arquivos **VCF** são válidos como entrada.

2. **Identificação de Variantes**:

   - A aplicação faz anotações com os seguintes campos:
     - **ID**: Identificador único da variante no banco de dados de referência.
     - **CHROM**: Cromossomo onde a variante está localizada.
     - **REF**: Alelo de referência no genoma.
     - **ALT**: Alelo alternativo identificado.
     - **Population Allele Frequency**: Frequência da variante em populações conhecidas.
     - **Var Class**: Classe da variante, como SNV (Single Nucleotide Variant) ou INDEL.
     - **Most Severe Consequence**: Consequência mais grave da variante em relação à função do gene.
     - **Clinical Significance**: Relevância clínica da variante com base em dados de referência.
     - **Synonyms**: Nomes alternativos ou identificadores da variante.
     - **Ambiguity**: Nível de ambiguïdade na identificação da variante.
     - **Minor Allele**: Alelo menos frequente encontrado na população.
     - **Mappings**: Mapemanto da variante em diferentes bancos e referências genômicas.

   - Os bancos consultados incluem **dbSNP** e **Ensembl**.

3. **Anotação Funcional**:

   - Integração com bancos de dados como dbSNP, ClinVar e Ensembl para fornecer informações funcionais e clínicas sobre as variantes.

## Tecnologias Utilizadas

- **Linguagem**: Python
- **Framework**: Bootstrap, Flask (para interface web)
- **Bancos de Dados**: Integrações com dbSNP, ClinVar e Ensembl

## Estrutura do Projeto

- **`src/main.py`**: Arquivo principal para executar a aplicação.
- **`src/api_getters.py`**: Contém funções para integrar e buscar dados externos.
- **`src/views.py`**: Gerencia as rotas e interações do usuário.
- **`src/utils.py`**: Contém funções utilitárias para processamento de dados.
- **`templates/`**: Arquivos HTML para visualização de resultados.
- **`src/static/`**: Arquivos de imagens e vídeos.
- **`requirements.txt`**: Lista de dependências.
- **`tests/`**: Arquivos de testes unitários e de integração.

## Requisitos de Instalação

Certifique-se de ter as seguintes ferramentas instaladas:

- Python >= 3.8
- Gerenciador de pacotes `pip`

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/madsondeluna/getvar_test.git
   cd getvar
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Execução

1. Inicie o servidor local:

   ```bash
   python3 src/main.py
   ```

2. Acesse a aplicação no navegador em:

   ```
   http://localhost:5000
   ```

## Exemplo de Uso

Submeta um arquivo **VCF** através da interface web. O sistema processará os dados, realizará as anotações e disponibilizará um relatório final em formato tabular que pode ser filtrada através das respectivas anotações. 

### Exemplo de Entrada

```vcf
##fileformat=VCFv4.2
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO
1       10177   rs367896724     A       AC      .       .       DP=100;AF=0.5
1       10352   rs555500075     T       TA      .       .       DP=200;AF=0.8
```

### Exemplo de Saída

| ID           | CHROM | REF | ALT | Population Allele Frequency | Var Class | Most Severe Consequence | Clinical Significance | Synonyms | Ambiguity | Minor Allele | Mappings |
|--------------|-------|-----|-----|-----------------------------|-----------|-------------------------|-----------------------|----------|-----------|--------------|----------|
| rs367896724  | 1     | A   | AC  | 0.5                         | SNV       | missense_variant        | Pathogenic            | rs12345  | None      | A            | ...      |
| rs555500075  | 1     | T   | TA  | 0.8                         | INDEL     | frameshift_variant      | Benign                | rs67890  | None      | T            | ...      |

## Informações Adicionais de Uso 

As APIs REST do dbSNP, ClinVar e Ensembl possuem um limite de até 30 requisições por solicitação. Por isso, a aplicação pode apresentar instabilidade ou lentidão em alguns momentos. Além disso, os servidores dessas plataformas ocasionalmente podem ficar instáveis ou não responder adequadamente às requisições. Nesses casos, o manual das APIs recomenda a resubmissão dos dados para completar o processo de anotação.

## Usando o Dockerfile

### Construindo a imagem Docker

Para construir a imagem Docker, execute o seguinte comando no diretório raiz do projeto:

```bash
docker build -t getvar_app .
```

### Executando o contêiner Docker

Para executar o contêiner Docker, use o seguinte comando:

```bash
docker run -p 5000:5000 getvar_app
```

Isso iniciará a aplicação Flask dentro de um contêiner Docker e a tornará acessível em `http://localhost:5000`.

## Licença

Este projeto está licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT). Consulte o arquivo LICENSE para mais informações.

## Contato

Madson Aragão\
[madsondeluna@gmail.com](mailto\:madsondeluna@gmail.com)\
[LinkedIn](https://www.linkedin.com/in/madsonaragao)

## Contribuindo

Obrigado por considerar contribuir para o GETVar! Agradecemos contribuições da comunidade para ajudar a melhorar o projeto. Por favor, reserve um momento para revisar estas diretrizes antes de começar a contribuir.

### Código de Conduta

Ao participar deste projeto, você concorda em seguir o [Código de Conduta](CODE_OF_CONDUCT.md). Por favor, leia-o para entender as expectativas para todos os colaboradores.

### Como Contribuir

1. **Fork o repositório**: Clique no botão "Fork" no canto superior direito da página do repositório para criar uma cópia do repositório na sua conta do GitHub.
2. **Clone o repositório**: Clone o repositório forkado para sua máquina local usando o seguinte comando:
   ```bash
   git clone https://github.com/seu-usuario/getvar.git
   ```
3. **Crie um novo branch**: Crie um novo branch para sua contribuição. Use um nome descritivo para seu branch para indicar o propósito das suas mudanças.
   ```bash
   git checkout -b feature/nome-da-sua-feature
   ```
4. **Faça suas mudanças**: Implemente suas mudanças no novo branch. Certifique-se de que seu código segue os padrões de codificação e inclui testes apropriados.
5. **Commit suas mudanças**: Commit suas mudanças com uma mensagem de commit clara e concisa.
   ```bash
   git commit -m "Adicionar feature: descrição da sua feature"
   ```
6. **Push suas mudanças**: Push suas mudanças para seu repositório forkado.
   ```bash
   git push origin feature/nome-da-sua-feature
   ```
7. **Crie um pull request**: Abra um pull request (PR) do seu branch para o branch `main` do repositório principal. Forneça uma descrição detalhada das suas mudanças e do problema que elas resolvem.

### Padrões de Codificação

- Siga o guia de estilo [PEP 8](https://www.python.org/dev/peps/pep-0008/) para código Python.
- Use nomes de variáveis e funções significativos.
- Escreva comentários e docstrings claros e concisos para explicar o propósito do seu código.
- Certifique-se de que seu código está bem organizado e modular.

### Convenções de Nomeação de Branch

- Use nomes descritivos para seus branches para indicar o propósito das suas mudanças.
- Use o seguinte formato para nomes de branches:
  - `feature/nome-da-sua-feature` para novas features.
  - `bugfix/nome-do-seu-bugfix` para correções de bugs.
  - `hotfix/nome-do-seu-hotfix` para correções urgentes.
  - `chore/nome-da-sua-tarefa` para tarefas de manutenção.

### Procedimentos de Pull Request

1. **Revise suas mudanças**: Antes de enviar um pull request, revise suas mudanças para garantir que elas atendem aos padrões de codificação do projeto e passam em todos os testes.
2. **Forneça uma descrição detalhada**: Na descrição do pull request, forneça uma explicação clara e concisa das mudanças que você fez e do problema que elas resolvem.
3. **Link para issues relevantes**: Se seu pull request resolver alguma issue aberta, inclua uma referência ao número da issue na descrição.
4. **Solicite uma revisão**: Solicite uma revisão de um ou mais mantenedores do projeto. Seja responsivo ao feedback e faça as mudanças necessárias.
5. **Aguarde a aprovação**: Uma vez que seu pull request for aprovado, ele será mesclado no repositório principal.

Obrigado por contribuir para o GETVar! Suas contribuições ajudam a tornar este projeto melhor para todos.

🌟 <i>Criado por Madson Aragão em algum lugar, onde bytes e biomoléculas colidem</i>.
