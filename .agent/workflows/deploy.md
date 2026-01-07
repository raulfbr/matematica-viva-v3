---
description: Como realizar o deploy manual do Matemática Viva no Netlify
---

Para colocar o projeto no ar via Netlify de forma manual, siga estes passos:

1. **Gere os arquivos atualizados:**
   Certifique-se de que o build mais recente foi executado.
   // turbo
   `python scripts/gutenberg.py`

2. **Localize a pasta de saída:**
   Toda a estrutura pronta para a web está localizada em:
   `c:\Users\Raul Flávio\OneDrive\!RF 2026\Gravity Google\Porjeto11-MatVivaV3\dist\web`

3. **Inicie o Deploy:**
   - Acesse o painel do [Netlify](https://app.netlify.com/).
   - Vá em **"Sites"**.
   - Role até o final da página onde diz **"Want to deploy a new site without connecting to Git? Drag and drop your site folder here"**.

4. **Upload:**
   - Arraste a pasta `dist\web` inteira para dentro dessa área no navegador.
   - O Netlify processará os arquivos (incluindo o `404.html` que geramos para rotas inválidas).

5. **Acesse o Reino:**
   O Netlify gerará uma URL (ex: `mat-viva-xxxx.netlify.app`). Você pode renomear essa URL nas configurações do site no Netlify.

> [!TIP]
> Sempre que fizer alterações no conteúdo ou no design, rode o script `gutenberg.py` novamente e arraste a pasta para o Netlify para atualizar.
