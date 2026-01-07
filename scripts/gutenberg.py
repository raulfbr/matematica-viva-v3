import os
import shutil
import re
import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader

# CONFIGURAÇÃO (Caminhos Robustos)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
SOURCE_DIR = os.path.join(BASE_DIR, "curriculo")
OUTPUT_DIR = os.path.join(BASE_DIR, "dist", "web")
TEMPLATE_DIR = os.path.join(SCRIPT_DIR, "templates")

# REGEX PARA BLOCOS CUSTOMIZADOS
# Captura > [!TYPE]\n> Conteúdo
# REGEX PARA BLOCOS CUSTOMIZADOS
# Captura > [!TYPE] até o fim do bloco de citações (linhas consecutivas com >)
# Explicação da Regex:
# (?m) -> Multiline mode (embora o re.sub use flags customizadas, vamos garantir)
# ^>\s*\[!TYPE\] -> Começa a linha com > [!TYPE]
# ((?:\n\s*>.*)*) -> Captura grupo 1: Quebras de linha seguidas de > e conteúdo, repetidamente.
patterns = {
    'RITUAL': r'(?m)^>\s*\[!RITUAL\]((?:\n\s*>.*)*)',
    'NARRATIVE': r'(?m)^>\s*\[!(?:NARRATIVE|NARRATIVA)\]((?:\n\s*>.*)*)',
    'TEACHER': r'(?m)^>\s*\[!(?:TEACHER|MESTRA)\]((?:\n\s*>.*)*)',
    'ACTIVITY': r'(?m)^>\s*\[!(?:ACTIVITY|ATIVIDADE)\]((?:\n\s*>.*)*)',
    'CONCEPT': r'(?m)^>\s*\[!(?:CONCEPT|CONCEITO)\]((?:\n\s*>.*)*)',
    'TIP': r'(?m)^>\s*\[!(?:TIP|POSTURA)\]((?:\n\s*>.*)*)',
    'CLOSING': r'(?m)^>\s*\[!(?:CLOSING|FECHAMENTO)\]((?:\n\s*>.*)*)',
    'NARRATION': r'(?m)^>\s*\[!(?:NARRATION|NARRAÇÃO|NARRACAO)\]((?:\n\s*>.*)*)',
    'NOTE': r'(?m)^>\s*\[!(?:NOTE|SABEDORIA|MESTRE)\]((?:\n\s*>.*)*)',
    'IMPORTANT': r'(?m)^>\s*\[!(?:IMPORTANT|IMPORTANTE|ALERTA)\]((?:\n\s*>.*)*)',
    'SPEECH': r'(?m)^>\s*\[!(?:SPEECH|FALA|ROTEIRO)\]((?:\n\s*>.*)*)',
}

def clean_block_content(text):
    """Remove os '>' do início das linhas de um bloco blockquote."""
    lines = text.strip().split('\n')
    cleaned = []
    for line in lines:
        cleaned.append(re.sub(r'^>\s?', '', line))
    return '\n'.join(cleaned)

def process_custom_blocks(md_content):
    """Transforma os alertas do Obsidian em DIVs do Noble CSS. Suporta aninhamento recursivo."""
    
    # Função auxiliar para substituição
    def replace_block(match, type_name, css_class):
        content = match.group(1)
        cleaned_content = clean_block_content(content)
        
        # Mapeamento de Títulos e Ícones Nobres
        titles = {
            'RITUAL': '🎇 Ritual Sagrado',
            'NARRATIVE': '🗺️ A Jornada',
            'TEACHER': '📜 Mise-en-place (Só para você)',
            'ACTIVITY': '🛠️ Hora de Fazer',
            'CONCEPT': '💡 Ideia Viva',
            'TIP': '🎧 Postura da Alma',
            'CLOSING': '🌌 Ritual de Encerramento',
            'NARRATION': '🗣️ Momento de Conversa',
            'NOTE': '🏛️ Por que isso importa?',
            'IMPORTANT': '⚠️ Importante',
            'SPEECH': '' # Speech não tem título automático para fluidez
        }
        title = titles.get(type_name, type_name)

        # Mapeamento de Classes CSS
        classes = {
            'RITUAL': 'ritual-box',
            'NARRATIVE': 'narrativa-box',
            'TEACHER': 'secao-template', # Estilo discreto
            'ACTIVITY': 'atividade-box',
            'CONCEPT': 'narrativa-box', # Conceito narrado
            'TIP': 'dica-box',
            'CLOSING': 'ritual-box', 
            'NARRATION': 'narration-box', # Nova classe visualmente distinta
            'NOTE': 'secao-template',
            'IMPORTANT': 'card-importante',
            'SPEECH': 'speech-box'
        }
        css_class = classes.get(type_name, 'card-default')

        # RECURSÃO: Processa blocos aninhados
        processed_inner = process_custom_blocks(cleaned_content)
        
        # Processa markdown interno
        html_inner = markdown.markdown(processed_inner, extensions=['nl2br', 'attr_list', 'fenced_code', 'tables'])
        
        # Special logic for Speech Box (No header via HTML, CSS handles labels)
        if type_name == 'SPEECH':
             return f'\n<div class="{css_class}">\n{html_inner}\n</div>\n'
        
        return f'\n<div class="{css_class}">\n<span class="card-header">{title}</span>\n{html_inner}\n</div>\n'

    processed = md_content

    # Mapeamento Tipo -> Classe CSS
    type_map = {
        'RITUAL': 'card-ritual',
        'NARRATIVE': 'card-narrativa',
        'TEACHER': 'card-mestra',
        'ACTIVITY': 'card-atividade',
        'CONCEPT': 'card-narrativa',
        'TIP': 'card-mestra',
        'CLOSING': 'card-ritual',
        'NARRATION': 'card-narrativa',
        'NOTE': 'card-mestra',
        'IMPORTANT': 'card-importante',
        'SPEECH': 'speech-box'
    }

    for key, regex in patterns.items():
        css_class = type_map.get(key, 'card-default')
        # Removido flag re.DOTALL pois agora usamos regex baseada em linhas (^>)
        processed = re.sub(regex, lambda m: replace_block(m, key, css_class), processed)

    return processed

def load_master_mappings():
    """Lê os arquivos de estratégia para criar um mapeamento ID -> TGTB Ref."""
    mappings = {}
    estrategia_dir = os.path.join(SOURCE_DIR, "_SISTEMA", "_ESTRATEGIA")
    
    if not os.path.exists(estrategia_dir):
        return mappings

    for file in os.listdir(estrategia_dir):
        if file.endswith(".md"):
            with open(os.path.join(estrategia_dir, file), 'r', encoding='utf-8') as f:
                content = f.read()
                # Procura por linhas de tabela: | MV-S-001 | 000-L1 ... |
                # Regex captura o ID e a referência TGTB
                matches = re.findall(r'\|\s*\*\*(MV-[A-Z]-\d+)\*\*\s*\|\s*([^|]+)\|', content)
                for id_licao, tgtb_ref in matches:
                    mappings[id_licao] = tgtb_ref.strip()
    return mappings

def render_markdown(text):
    # 1. Pré-processamento de Blocos Customizados
    text_with_blocks = process_custom_blocks(text)
    
    # 2. Conversão Padrão MD -> HTML
    # Extensions: checklist para [ ] e extra para funcionalidades extras
    html = markdown.markdown(text_with_blocks, extensions=['attr_list', 'def_list', 'fenced_code', 'tables'])
    
    # 3. Pós-processamento (Checkboxes & Instruções de Cena)
    
    # Transforma [ ] em <input type=checkbox>
    html = html.replace('[ ]', '<input type="checkbox">')
    html = html.replace('[x]', '<input type="checkbox" checked>')

    # Transforma [...] em <span class="instrucao-cena">
    # Regex: Procura colchetes que NÃO tenham <input dentro (evita checkboxes já processados)
    # E que não sejam seguidos por ( (evita links markdown remanescentes)
    # Transforma [...] em <span class="instrucao-cena">
    # Regex: Procura colchetes que NÃO tenham <input dentro (evita checkboxes já processados)
    # E que não sejam seguidos por ( (evita links markdown remanescentes)
    html = re.sub(r'\[([^\]]+?)\](?!\()', r'<span class="instrucao-cena">[\1]</span>', html)
    
    # 4. Transforma Imagens de Card em Visual Cards (Neuro-UX Impecável)
    # Regex: Procura <img ... alt="CARD: Titulo" ...>
    # Captura o Título do CARD do alt.
    def wrap_card(match):
        full_tag = match.group(0)
        alt_text = match.group(1)
        # Se quiser extrair subtítulo, poderia usar "CARD: Título | Subtítulo"
        # Por enquanto agrupa tudo no CARD
        return f'<div class="visual-card"><img alt="{alt_text}" {full_tag[full_tag.find("src"):]}</div>'
    
    # Encontra imagens que tenham alt começando com CARD:
    # <img alt="CARD: O Encontro" src="...">
    # A regex do Markdown já gerou <img ...>, então vamos processar o HTML.
    # Pattern: <img[^>]+alt="CARD:\s*([^"]+)"[^>]*>
    html = re.sub(r'<img[^>]+alt="CARD:\s*([^"]+)"[^>]*>', 
                  lambda m: f'<div class="visual-card">{m.group(0)}<div class="card-nome">{m.group(1)}</div></div>', 
                  html)

    # Limpeza final de paragrafos vazios que o markdown as vezes deixa ao redor de divs
    html = html.replace('<p><div class="visual-card">', '<div class="visual-card">')
    html = html.replace('</div></p>', '</div>')

    return html

def main():
    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('lesson.html')
    
    print(f"[INFO] Iniciando Gutenberg Engine...")
    print(f"[INFO] Fonte: {os.path.abspath(SOURCE_DIR)}")
    print(f"[INFO] Saida: {os.path.abspath(OUTPUT_DIR)}")
    
    # Carrega Mapeamentos TGTB
    tgtb_mappings = load_master_mappings()
    print(f"[INFO] Mapeamentos TGTB carregados: {len(tgtb_mappings)}")

    # Varredura
    lessons_db = {}
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                
                # Ignora arquivos de sistema
                if "_SISTEMA" in file_path or "TEMPLATE" in file:
                    continue

                print(f"   [Processing]: {file}...")
                
                # Parse Frontmatter
                post = frontmatter.load(file_path)
                metadata = post.metadata
                content = post.content

                # FILTRO DE SEGURANÇA: Ignora arquivos sem Título ou ID (não são lições)
                if 'titulo' not in metadata or 'id' not in metadata:
                    print(f"   [SKIPPING]: {file} (Sem metadados de lição)")
                    continue
                
                # Renderiza Corpo
                # LIMPANDO CONTEÚDO REDUNDANTE (Evita duplicar Título/ID/Guardião no HTML final)
                # Remove o H1 inicial e qualquer linha divisória logo após (---)
                clean_content = re.sub(r'^#\s*.*?\n', '', content, flags=re.MULTILINE)
                # clean_content = re.sub(r'^-{3,}\n', '', clean_content, flags=re.MULTILINE)
                
                # Remove especificamente o bloco de citações meta (Guardião, Local, Tempo, Meta)
                # Procura por blocos que começam com > **Guardião ou > **Guardiã
                clean_content = re.sub(r'^\s*>\s*\*\*Guardiã[o]?:\*\*.*?(?=\n\n|\n[^>])', '', clean_content, flags=re.DOTALL | re.MULTILINE).strip()
                # Remove divisórias órfãs que podem ter sobrado no topo
                # clean_content = re.sub(r'^(-{3,}\n)+', '', clean_content).strip()
                
                html_body = render_markdown(clean_content)
                
                # Renderiza Template Final
                # Dicionário de Cores dos Guardiões (Hex Oficial)
                guardian_colors = {
                    'noé': '#7B68B8',
                    'celeste': '#E8A87C',
                    'bernardo': '#8B7355',
                    'íris': '#7EC8C8', # Com acento
                    'iris': '#7EC8C8', # Sem acento
                    'melquior': '#D4A84B'
                }

                # LÓGICA DE GUARDIÃO (Prioridade Absoluta ao Metadata)
                guardia_nome_raw = str(metadata.get('guardia', '')).strip()
                
                # FALLBACK: Se não estiver no metadata, busca no corpo: > **Guardião:** 🐻 Bernardo
                meta_missao = metadata.get('meta', '')
                if not guardia_nome_raw:
                    # Regex robusta: Suporta Guardião ou Guardiã, opcionalmente precedidos por emojis e seguidos de dois pontos
                    match_guardiao = re.search(r'>\s*\*\*Guardiã[o]?:\*\*\s*(?:[^\w\s]*)\s*([A-Za-zÀ-ÿ]+)', content)
                    if match_guardiao:
                        guardia_nome_raw = match_guardiao.group(1)
                
                if not meta_missao:
                    # Busca a Meta no corpo: > **Meta:** ...
                    match_meta = re.search(r'>\s*\*\*Meta:\*\*\s*(.*)', content)
                    if match_meta:
                        meta_missao = match_meta.group(1).strip()
                
                # Default final
                if not guardia_nome_raw:
                    guardia_nome_raw = 'Melquior'

                # Extrai apenas o nome puro (evita emojis e parênteses)
                guardia_search = re.search(r'([A-Za-zÀ-ÿ]+)', guardia_nome_raw)
                guardia_nome = guardia_search.group(1).title() if guardia_search else 'Melquior'
                guardia_key = guardia_nome.lower()
                
                # Default Logic
                cor_tema = guardian_colors.get('melquior')
                
                # Tenta casar a cor pelo nome do guardião
                if guardia_key in guardian_colors:
                    cor_tema = guardian_colors[guardia_key]
                else:
                    # Fallback (Procura no conteúdo APENAS se não estiver definido no meta)
                    if 'guardia' not in metadata:
                        for nome, hex_code in guardian_colors.items():
                            if nome in content.lower():
                                cor_tema = hex_code
                                guardia_nome = nome.title()
                                break
                    else:
                        # Se tem guardião definido mas não temos cor mapeada, usa Melquior/Dourado
                        cor_tema = guardian_colors.get('melquior')

                # Calcula Caminho Relativo para a Raiz (dist/web)
                rel_dir = os.path.relpath(root, SOURCE_DIR)
                depth = len(rel_dir.split(os.sep)) if rel_dir != '.' else 0
                path_to_root = '../' * depth if depth > 0 else './'
                if path_to_root.endswith('/') and len(path_to_root) > 1:
                    path_to_root = path_to_root.rstrip('/')

                # Icon Mapper
                icons = {'Noé': '🦉', 'Celeste': '🦊', 'Bernardo': '🐻', 'Íris': '🐦', 'Iris': '🐦', 'Melquior': '🦁'}
                icon = icons.get(guardia_nome, '🦁') # Default Lion

                # Injeta metadados default se faltar
                licao_id = metadata.get('id', '')
                tgtb_ref = metadata.get('tgtb') or tgtb_mappings.get(licao_id)

                meta_safe = {
                    'titulo': metadata.get('titulo', 'Lição Sem Título'),
                    'fase': metadata.get('fase', 'Geral'),
                    'versao': metadata.get('versao', '3.5 (Sovereign Positive)'),
                    'cor_theme': cor_tema,
                    'cor_guardiao': cor_tema,
                    'guardia': guardia_nome, 
                    'guardia_icon': icon,
                    'tempo': metadata.get('tempo', '15 min'),
                    'local': metadata.get('local', 'Reino'),
                    'clima': metadata.get('clima', ''),
                    'meta': meta_missao,
                    'root_path': path_to_root,
                    'tgtb': tgtb_ref
                }

                final_html = template.render(meta=meta_safe, content_html=html_body)
                
                # Caminho de Saída
                rel_path = os.path.relpath(root, SOURCE_DIR)
                out_folder = os.path.join(OUTPUT_DIR, rel_path)
                os.makedirs(out_folder, exist_ok=True)
                
                out_filename = os.path.splitext(file)[0] + ".html"
                out_path = os.path.join(out_folder, out_filename)
                
                # Salva metadados da lição para o Index
                relative_url = os.path.join(rel_path, out_filename).replace(os.sep, '/')
                
                # Icon Mapper
                icons = {'Noé': '🦉', 'Celeste': '🦊', 'Bernardo': '🐻', 'Íris': '🐦', 'Iris': '🐦', 'Melquior': '🦁'}
                icon = icons.get(guardia_nome, '🦁') # Default Lion

                lesson_data = {
                    'title': meta_safe['titulo'],
                    'path': relative_url,
                    'theme_color': meta_safe['cor_theme'],
                    'guardian': guardia_nome,
                    'guardian_icon': icon,
                    'duration': meta_safe['tempo'],
                    'weather': meta_safe['clima'],
                    'tgtb': meta_safe['tgtb'], # ADDED THIS
                    'phase': meta_safe['fase']
                }
                
                # Normalização inteligente: extrai a fase base e o nível (I, II, etc.)
                normalized_fase = str(meta_safe['fase']).lower()
                fase_key = 'outros'

                # Mapeamento de Fases Base
                if any(x in normalized_fase for x in ['ciclo 0', 'vivência', 'vivencia']):
                    fase_key = 'ciclo 0'
                elif 'sementes' in normalized_fase:
                    fase_key = 'sementes'
                elif 'raízes' in normalized_fase or 'raizes' in normalized_fase:
                    fase_key = 'raízes'
                elif 'lógica' in normalized_fase or 'logica' in normalized_fase:
                    fase_key = 'lógica'
                elif 'legado' in normalized_fase:
                    fase_key = 'legado'
                elif 'ouro' in normalized_fase:
                    fase_key = 'ouro'

                # Se for uma fase com níveis (I, II, III...), tenta capturar o algarismo romano
                if fase_key in ['raízes', 'lógica', 'legado']:
                    roman_match = re.search(r'\b(v|iv|iii|ii|i)\b', normalized_fase)
                    if roman_match:
                        fase_key = f"{fase_key} {roman_match.group(1)}"

                if fase_key not in lessons_db:
                    lessons_db[fase_key] = []
                
                lessons_db[fase_key].append({
                    'data': lesson_data,
                    'html_body': html_body,
                    'meta': meta_safe,
                    'out_path': out_path,
                    'rel_path_from_root': relative_url
                })

    # PÓS-PROCESSAMENTO: ORDENAÇÃO E VIZINHOS
    # Ordena as lições dentro de cada fase pelo nome do arquivo (ex: 001 vem antes de 002)
    # E gera o HTML final de cada lição injetando prev/next
    
    print("[INFO] Calculando Rotas de Navegação...")
    
    for fase, lessons in lessons_db.items():
        # Sort by filename inside 'path' or 'title' might be safer if files have prefixes
        lessons.sort(key=lambda x: x['data']['path']) 
        
        for i, lesson in enumerate(lessons):
            # Vizinhos
            prev_lesson = lessons[i-1] if i > 0 else None
            next_lesson = lessons[i+1] if i < len(lessons) - 1 else None
            
            # Prepara Breadcrumb Data
            nav_meta = lesson['meta'].copy()
            
            if prev_lesson:
                # Calcula caminho relativo DA lição PARA o vizinho
                prev_rel = os.path.relpath(os.path.join(OUTPUT_DIR, prev_lesson['data']['path']), os.path.dirname(lesson['out_path'])).replace(os.sep, '/')
                nav_meta['prev'] = {'title': prev_lesson['data']['title'], 'url': prev_rel}
            
            if next_lesson:
                next_rel = os.path.relpath(os.path.join(OUTPUT_DIR, next_lesson['data']['path']), os.path.dirname(lesson['out_path'])).replace(os.sep, '/')
                nav_meta['next'] = {'title': next_lesson['data']['title'], 'url': next_rel}

            # Renderiza HTML Final da Lição (Agora com Nav)
            final_html = template.render(meta=nav_meta, content_html=lesson['html_body'])
            
            with open(lesson['out_path'], 'w', encoding='utf-8') as f:
                f.write(final_html)

    
    # GERAÇÃO DO DASHBOARD (INDEX)
    print("   [INFO] Gerando O Mirante do Reino...")
    
    # Extrai apenas os 'data' dicts para o dashboard template
    def get_lessons(key):
        return [l['data'] for l in lessons_db.get(key, [])]

    # Mapeamento Oficial Expandido (Ano a Ano)
    cycles_map = {
        'ciclo 0': {
            'display_name': 'Vivência Orgânica',
            'internal_name': '0 - 5 anos',
            'age_range': 'Vivência',
            'icon': '🌱',
            'lessons': get_lessons('ciclo 0')
        },
        'sementes': {
            'display_name': 'Jardim de Infância',
            'internal_name': '4 - 6 anos',
            'age_range': 'Sementes',
            'icon': '🌿',
            'lessons': get_lessons('sementes')
        },
        'raízes i': {
            'display_name': 'Raízes I',
            'internal_name': '1º Ano (Fundamental)',
            'age_range': '7 anos',
            'icon': '🌳',
            'lessons': get_lessons('raízes i')
        },
        'raízes ii': {
            'display_name': 'Raízes II',
            'internal_name': '2º Ano (Fundamental)',
            'age_range': '8 anos',
            'icon': '🌳',
            'lessons': get_lessons('raízes ii')
        },
        'raízes iii': {
            'display_name': 'Raízes III',
            'internal_name': '3º Ano (Fundamental)',
            'age_range': '9 anos',
            'icon': '🌳',
            'lessons': get_lessons('raízes iii')
        },
        'raízes iv': {
            'display_name': 'Raízes IV',
            'internal_name': '4º Ano (Fundamental)',
            'age_range': '10 anos',
            'icon': '🌳',
            'lessons': get_lessons('raízes iv')
        },
        'raízes v': {
            'display_name': 'Raízes V',
            'internal_name': '5º Ano (Fundamental)',
            'age_range': '11 anos',
            'icon': '🌳',
            'lessons': get_lessons('raízes v')
        },
        'lógica i': {
            'display_name': 'Lógica I',
            'internal_name': '6º Ano (Fundamental)',
            'age_range': '12 anos',
            'icon': '🛡️',
            'lessons': get_lessons('lógica i')
        },
        'lógica ii': {
            'display_name': 'Lógica II',
            'internal_name': '7º Ano (Fundamental)',
            'age_range': '13 anos',
            'icon': '🛡️',
            'lessons': get_lessons('lógica ii')
        },
        'lógica iii': {
            'display_name': 'Lógica III',
            'internal_name': '8º Ano (Fundamental)',
            'age_range': '14 anos',
            'icon': '🛡️',
            'lessons': get_lessons('lógica iii')
        },
        'legado i': {
            'display_name': 'Legado I',
            'internal_name': '9º Ano / 1º Médio',
            'age_range': '15 anos',
            'icon': '👑',
            'lessons': get_lessons('legado i')
        },
        'legado ii': {
            'display_name': 'Legado II',
            'internal_name': '2º Ensino Médio',
            'age_range': '16 anos',
            'icon': '👑',
            'lessons': get_lessons('legado ii')
        },
        'legado iii': {
            'display_name': 'Legado III',
            'internal_name': '3º Ensino Médio',
            'age_range': '17 anos',
            'icon': '👑',
            'lessons': get_lessons('legado iii')
        },
        'legado iv': {
            'display_name': 'Legado IV',
            'internal_name': 'Pré-Universitário',
            'age_range': '18 anos',
            'icon': '👑',
            'lessons': get_lessons('legado iv')
        },
        'ouro': {
            'display_name': 'Livro Dourado',
            'internal_name': 'Biografias Vivas',
            'age_range': 'Acervo Especial',
            'icon': '💎',
            'lessons': get_lessons('ouro')
        },
        'outros': {
            'display_name': 'Acervo & Extras',
            'internal_name': 'Documentos Gerais',
            'age_range': '---',
            'icon': '📜',
            'lessons': get_lessons('outros')
        }
    }
    
    # Render Dashboard
    dash_template = env.get_template('dashboard.html')
    dash_html = dash_template.render(cycles=cycles_map)
    
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(dash_html)
        
    # GERAÇÃO DO MANIFESTO (FAMILIA)
    print("[INFO] Gerando Manifesto da Família...")
    manifesto_template = env.get_template('manifesto.html')
    manifesto_html = manifesto_template.render()
    with open(os.path.join(OUTPUT_DIR, 'familia.html'), 'w', encoding='utf-8') as f:
        f.write(manifesto_html)

    # GERAÇÃO DA LANDING PAGE
    print("[INFO] Gerando Landing Page...")
    landing_template = env.get_template('landing.html')
    landing_html = landing_template.render()
    with open(os.path.join(OUTPUT_DIR, 'landing.html'), 'w', encoding='utf-8') as f:
        f.write(landing_html)

    # GERAÇÃO DA 404 (Para Netlify)
    print("[INFO] Gerando Página 404...")
    error_template = env.get_template('404.html')
    error_html = error_template.render()
    with open(os.path.join(OUTPUT_DIR, '404.html'), 'w', encoding='utf-8') as f:
        f.write(error_html)

    # GERAÇÃO DO START (Primeiros Passos)
    print("[INFO] Gerando Página Primeiros Passos...")
    start_template = env.get_template('start.html')
    start_html = start_template.render()
    with open(os.path.join(OUTPUT_DIR, 'start.html'), 'w', encoding='utf-8') as f:
        f.write(start_html)

    # GERAÇÃO DA BIBLIOTECA (Acervo Dourado)
    print("[INFO] Gerando Biblioteca Real...")
    biblio_template = env.get_template('biblioteca.html')
    biblio_html = biblio_template.render()
    with open(os.path.join(OUTPUT_DIR, 'biblioteca.html'), 'w', encoding='utf-8') as f:
        f.write(biblio_html)

    # COPIA DE ASSETS (Para Deploy Autônomo)
    print("[INFO] Espelhando Assets para dist/web...")
    src_assets = os.path.join(os.path.dirname(SOURCE_DIR), 'assets') # ../assets
    dst_assets = os.path.join(OUTPUT_DIR, 'assets')
    
    # Usa dirs_exist_ok=True (Python 3.8+) para evitar erros de permissão ao deletar
    try:
        shutil.copytree(src_assets, dst_assets, dirs_exist_ok=True)
    except Exception as e:
        print(f"[WARN] Não foi possível copiar assets automaticamente: {e}")
        print("[TIP] Copie a pasta 'assets' manualmente para 'dist/web' antes do deploy.")

    print("[SUCCESS] Build Concluido com Sucesso!")

if __name__ == "__main__":
    main()
