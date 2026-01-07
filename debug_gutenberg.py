import sys
import os
import frontmatter

# Add scripts dir to path
sys.path.append(os.path.join(os.getcwd(), 'scripts'))
from gutenberg import process_custom_blocks, clean_block_content

file_path = "c:/Users/Raul/OneDrive/!RF 2026/Gravity Google/Projeto011-MatVivaV3RaulPessoal/curriculo/00_SEMENTES/000_INTRODUCAO_REINO_CONTADO.md"
post = frontmatter.load(file_path)
content = post.content

# Mimic gutenberg.py cleanup
import re
clean_content = re.sub(r'^#\s*.*?\n', '', content, flags=re.MULTILINE)
clean_content = re.sub(r'^-{3,}\n', '', clean_content, flags=re.MULTILINE)

print(f"--- Cleaned Content Preview ---")
print(clean_content[:200])

processed = process_custom_blocks(clean_content)

print(f"\n--- Processed Content Preview ---")
print(processed[:500])

if "narration-box" in processed:
    print("\nSUCCESS: 'narration-box' found in processed content.")
else:
    print("\nFAIL: 'narration-box' NOT found in processed content.")

if "ritual-box" in processed:
    print("SUCCESS: 'ritual-box' found.")
else:
    print("FAIL: 'ritual-box' NOT found.")
