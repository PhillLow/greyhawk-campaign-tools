import os
import sys
import json
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.engine.srd_parser import parse_markdown_to_tree, MarkdownSection

def extract_toolbox():
    filepath = "dnd-5e-srd-markdown/gameplay-toolbox.md"
    root = parse_markdown_to_tree(filepath)
    poisons_data = []

    def find_poisons_recursive(node: MarkdownSection):
        if node.level == 4 and " GP)" in node.title:
            item_name = node.title.strip()
            m = re.match(r"(.*?)\s*\(([\d,]+)\s*GP\)", item_name)
            name = item_name
            cost = 0
            if m:
                name = m.group(1).strip()
                cost = int(m.group(2).replace(",", ""))
                
            desc_lines = []
            poison_type = "Ingested"
            for line in node.content:
                cleaned = line.strip()
                if cleaned.startswith("_") and cleaned.endswith("Poison_"):
                    poison_type = cleaned.replace("_", "").split(" ")[0]
                elif cleaned:
                    desc_lines.append(cleaned)
                    
            poisons_data.append({
                "name": name,
                "cost_gp": cost,
                "type": poison_type,
                "description": " ".join(desc_lines)
            })
            
        for child in node.subsections:
            find_poisons_recursive(child)
            
    find_poisons_recursive(root)

    out_path = "src/models/generated_poisons.json"
    with open(out_path, "w", encoding="utf-8") as f:
         json.dump(poisons_data, f, indent=4)
         
    print(f"Generated {len(poisons_data)} poisons.")

if __name__ == "__main__":
    extract_toolbox()
