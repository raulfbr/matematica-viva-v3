# 🖨️ PLANO DE ARQUITETURA: TEMPLATE MASTER V3.5 (DUAL PRINTING)

Este plano define a evolução do template de lições para suportar a **Impressão Dual**: uma experiência rica em tela (interativa/vídeo) e uma experiência "livro" em papel (econômica/legível).

## 🎯 Objetivo Soberano
Um único arquivo HTML que serve como:
1.  **Guia Digital (Tablet/Celular):** Interativo, colorido, vídeos embutidos, checklists clicáveis.
2.  **Material Físico (Papel/PDF):** Limpo, tipografia serifada, sem ruído de UI, pronto para fichário.

---

## 🌊 FASE 1: A LÓGICA DO DUAL
*Como o arquivo se comporta em cada meio.*

### 🖥️ MODO TELA (Screen)
*   **Fundo:** Creme Quente (`#F8F5E9`).
*   **Contraste:** Verde Floresta e Dourado.
*   **Componentes:** Cards com sombras, acordeões (se houver), vídeos e áudios visíveis.
*   **Navegação:** Botões "Anterior/Próxima" e Breadcrumbs visíveis.

### 📄 MODO PAPEL (Print)
*   **Fundo:** Branco Puro (Economia de tinta e contraste máximo).
*   **Contraste:** Preto e Cinza Escuro.
*   **Remoções:**
    *   `nav`, `button`, `video`, `audio`, `footer` do site.
    *   Cards de "Mise-en-place" (opcional - decidir se imprime ou não).
*   **Tipografia:**
    *   Corpo: Serifada (*Merriweather*) para leitura longa.
    *   Tamanho: 12pt (ideal para leitura física).
*   **Layout:**
    *   `display: block` em grids (evitar quebras ruins).
    *   `page-break-inside: avoid` em `blockquote` e tabelas.
    *   Checkboxes renderizados como quadrados vazios `⬜`.

---

## 🌊 FASE 2: ENGENHARIA DO CSS (noble_v3.5.css)

### Variáveis de Impressão
Criaremos um bloco `@media print` robusto:

```css
@media print {
    /* RESET */
    body { 
        background: #fff; 
        color: #000; 
        font-size: 12pt;
        line-height: 1.5;
    }

    /* REMOÇÃO DE RUÍDO */
    .no-print, nav, button, .video-wrapper, .bg-texture { 
        display: none !important; 
    }

    /* TIPOGRAFIA DE LIVRO */
    h1, h2, h3 { 
        color: #000 !important; 
        font-family: "Merriweather", serif;
        page-break-after: avoid; 
    }

    /* CARDS */
    .card-mestra, .card-atividade {
        border: 1px solid #000;
        box-shadow: none;
        background: none;
        page-break-inside: avoid;
    }

    /* LINKS */
    a { 
        text-decoration: none; 
        color: #000; 
    }
    a::after { 
        content: " (" attr(href) ")"; 
        font-size: 0.8em; 
    }
}
```

## 🌊 FASE 3: A ESTRUTURA HTML (Template Mestre)

### Header Híbrido
```html
<!-- Visível apenas na impressão -->
<div class="print-header-only">
    <h1>Matemática Viva | Lição 001</h1>
    <p>Guia do Professor - Família Rodrigues</p>
    <hr>
</div>
```

### Seções Inteligentes
Usar classes utilitárias para controlar a visibilidade:
*   `.screen-only`: Só aparece na tela (ex: vídeos, botões de nav).
*   `.print-only`: Só aparece na impressão (ex: linhas para anotação, rodapé de folha).

---

## 🛠️ PRÓXIMOS PASSOS
1.  Atualizar `noble.css` com as diretrizes de impressão.
2.  Refatorar `001_OS_PRIMEIROS_NUMEROS.html` para aplicar as classes `.no-print` e o header de impressão.
3.  Testar a "Impressão" (Via PDF Preview).
