import re
import frontmatter

file_path = "c:/Users/Raul/OneDrive/!RF 2026/Gravity Google/Projeto011-MatVivaV3RaulPessoal/curriculo/00_SEMENTES/000_INTRODUCAO_REINO_CONTADO.md"

post = frontmatter.load(file_path)
content = post.content

print(f"Content length: {len(content)}")
print(f"First 1000 chars: {content[:1000]}")

patterns = {
    'RITUAL': r'(?m)^>\s*\[!RITUAL\]((?:\n\s*>.*)*)',
    'NARRATION': r'(?m)^>\s*\[!(?:NARRATION|NARRAÇÃO|NARRACAO)\]((?:\n\s*>.*)*)',
    'NOTE': r'(?m)^>\s*\[!(?:NOTE|SABEDORIA|MESTRE)\]((?:\n\s*>.*)*)'
}

for key, regex in patterns.items():
    print(f"Testing {key} with regex: {regex}")
    match = re.search(regex, content)
    if match:
        print(f"  [MATCH] Found {key}!")
        print(f"  Group 1 length: {len(match.group(1))}")
    else:
        print(f"  [FAIL] Did not find {key}")
        # Try finding the string literal to see if it exists
        if f"[!{key}]" in content or f"[!{key[:4]}" in content:
             print(f"  But string literal seems to exist in content.")

