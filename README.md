# Matemática Viva (V3)

> "A Matemática não é uma coleção de truques abstratos, é a linguagem com a qual Deus escreveu o Universo." — *Visão do Projeto*

Bem-vindo ao repositório oficial do **Matemática Viva**, um projeto de educação matemática vivo, inspirado na filosofia de Charlotte Mason e na pedagogia clássica, focado em trazer a beleza, a verdade e a bondade dos números para a vida das famílias educadoras.

## 📚 Sobre o Projeto

Este portal (`dist/web`) é gerado a partir de um "Jardim Digital" de arquivos Markdown, processados por um motor customizado em Python ("Gutenberg Engine") para criar uma experiência de navegação fluida, bela e focada no conteúdo.

### Estrutura do Repositório

*   `curriculo/`: O coração do projeto. Contém todas as lições, narrativas e rituais escritos em Markdown.
*   `scripts/`: O motor "Gutenberg". Scripts Python que transformam o conteúdo bruto em um site HTML estático.
*   `assets/`: Imagens, estilos (CSS) e recursos visuais.
*   `docs/`: Documentação técnica e de governança do projeto.

## 🛠️ Tecnologia

O projeto utiliza uma arquitetura simples e robusta de **Geração de Site Estático (SSG)**:

*   **Linguagem**: Python 3.10+
*   **Template Engine**: Jinja2
*   **Conteúdo**: Markdown + Frontmatter (Metadados)
*   **Deploy**: Vercel (Build Automático via `requirements.txt`)

## 🚀 Como Rodar Localmente

1.  Clone o repositório:
    ```bash
    git clone https://github.com/raulfbr/matematica-viva-v3.git
    cd matematika-viva-v3
    ```

2.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

3.  Gere o site:
    ```bash
    python scripts/gutenberg.py
    ```

4.  O site gerado estará na pasta `dist/web`.

## 📜 Licenciamento

### Conteúdo Educacional
Todo o conteúdo original do portal (textos, roteiros, lições e narrativas em `curriculo/`) é disponibilizado sob a **Licença Creative Commons Atribuição 4.0 Internacional (CC BY 4.0)**.

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Licença Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />Isso permite que você:
*   **Compartilhe**: copie e redistribua o material em qualquer suporte ou formato.
*   **Adapte**: remix, transforme e crie a partir do material para qualquer fim, mesmo que comercial.
*   **Sob a condição**: Você deve dar o crédito apropriado, prover um link para a licença e indicar se mudanças foram feitas.

### Código Fonte
Os scripts de geração (`scripts/`) e o código fonte da infraestrutura são disponibilizados sob a licença **MIT**, garantindo liberdade total para uso técnico e derivação da tecnologia.

---
*Construído com ❤️ para o florescimento das famílias.*
