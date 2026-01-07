# Proposta de Design: Dashboard Centauro (v1.0)

O **Dashboard Centauro** é o painel de controle da família. Ele não é apenas um índice de arquivos; é a **Árvore da Vida Matemática** onde o progresso de cada Viajante é visualizado de forma heráldica e orgânica.

## 🏛️ Conceito Visual: A Árvore de Maturação
- **Raiz:** Ciclo 0 (Vivência)
- **Tronco:** Raízes (1-5)
- **Galhos:** Lógica (6-8)
- **Copa e Frutos:** Legado (9-12)

---

## 🖼️ Wireframe (Estrutura da Página)

### 1. Hero: O Estado do Reino
- **Título:** "Bem-vindo à Jornada, Família Rodrigues."
- **Status:** "3 Viajantes em Campo | 450 Lições Conquistadas | 12 Banquetes Celebrados."

### 2. A Árvore Centauro (Visualização Central)
- Um diagrama SVG interativo que brilha conforme os bimestres são concluídos.
- **Nós de Progresso:**
    - [ ] **Sementes (5a):** 🟢 Verde (Ativo)
    - [ ] **Raízes (10a):** 🟡 Dourado (Próximo)
    - [ ] **Legado (16a):** ⚪ Prateado (Bloqueado)

### 3. A Mesa do Mestre (Sidebar ou Grid inferior)
- Atalhos rápidos para:
    - `[!MISE-EN-PLACE]` da próxima lição.
    - Oração da Ordem.
    - Guia do Lápis Verde.

---

## 🛠️ Tecnologias Sugeridas
1.  **HTML5/Vanilla CSS:** Para manter a "Translucidez" e leveza.
2.  **Gutenberg Engine (Python):** O script `gutenberg.py` lerá a pasta `curriculo` e gerará este Dashboard automaticamente.
3.  **Gráficos:** SVG para a árvore, garantindo escalabilidade.

---

## 🎨 Paleta Centauro
- **Fundo:** Dark Royal Blue (#0A192F) ou Cream (#F5F5DC) dependendo do modo (Phygital).
- **Acentos:** Gold (#D4AF37) e Emerald Green (#50C878).

---

## 📝 Próximos Passos
1.  Atualizar o template `index.html` básico para incluir esta estrutura.
2.  Modificar o `gutenberg.py` para injetar os dados reais da árvore de arquivos.
