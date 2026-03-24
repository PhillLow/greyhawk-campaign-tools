import os
import sys
import json
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.engine.srd_parser import parse_markdown_to_tree, MarkdownSection

def extract_magic_items():
    filepath = "dnd-5e-srd-markdown/magic-items.md"
    root = parse_markdown_to_tree(filepath)
    magic_items_data = []

    def find_magic_items_recursive(node: MarkdownSection):
        if node.level == 4:
            item_name = node.title.strip()
            
            desc_lines = []
            meta_line = ""
            
            for line in node.content:
                cleaned = line.strip()
                if cleaned.startswith("_") and (cleaned.endswith("_") or "Uncommon" in cleaned or "Rare" in cleaned or "Legendary" in cleaned):
                    meta_line = cleaned
                elif cleaned and not cleaned.startswith("<table>") and not cleaned.startswith("<table"):
                    if not cleaned.startswith("<th>") and not cleaned.startswith("<td>") and not cleaned.startswith("<tr>") and not cleaned.startswith("<tbody>") and not cleaned.startswith("<thead>") and not cleaned.startswith("</table>"):
                         desc_lines.append(cleaned)
            
            if meta_line and ("Wondrous Item" in meta_line or "Weapon" in meta_line or "Armor" in meta_line or "Ring" in meta_line or "Wand" in meta_line or "Staff" in meta_line or "Rod" in meta_line or "Potion" in meta_line or "Scroll" in meta_line):
                desc = " ".join(desc_lines)
                desc = re.sub(r'<[^>]+>', '', desc) # Strip HTML tags if any sneaked in
                
                if len(desc) > 300: desc = desc[:297] + "..."
                
                type_cat = "Wondrous Item"
                if "Weapon" in meta_line: type_cat = "Weapon"
                elif "Armor" in meta_line: type_cat = "Armor"
                elif "Ring" in meta_line: type_cat = "Ring"
                elif "Wand" in meta_line: type_cat = "Wand"
                elif "Staff" in meta_line: type_cat = "Staff"
                elif "Rod" in meta_line: type_cat = "Rod"
                elif "Potion" in meta_line: type_cat = "Potion"
                elif "Scroll" in meta_line: type_cat = "Scroll"
                
                rarity = "Uncommon"
                lower_meta = meta_line.lower()
                if "legendary" in lower_meta: rarity = "Legendary"
                elif "very rare" in lower_meta: rarity = "Very Rare"
                elif "rare" in lower_meta: rarity = "Rare"
                elif "uncommon" in lower_meta: rarity = "Uncommon"
                elif "common" in lower_meta: rarity = "Common"
                elif "artifact" in lower_meta: rarity = "Legendary"
                
                req_attunement = "requires attunement" in lower_meta
                
                magic_items_data.append({
                    "name": item_name,
                    "description": desc,
                    "category": type_cat,
                    "rarity": rarity,
                    "requires_attunement": req_attunement
                })
            
        for child in node.subsections:
            find_magic_items_recursive(child)
            
    find_magic_items_recursive(root)

    out_path = "src/models/generated_magic_items.json"
    with open(out_path, "w", encoding="utf-8") as f:
         json.dump(magic_items_data, f, indent=4)
         
    print(f"Generated {len(magic_items_data)} magic items.")

if __name__ == "__main__":
    extract_magic_items()
