import os
import sys
import json
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.engine.srd_parser import parse_markdown_to_tree, MarkdownSection

def extract_spells():
    filepath = "dnd-5e-srd-markdown/spells.md"
    root = parse_markdown_to_tree(filepath)
    spells_data = []

    def find_spells_recursive(node: MarkdownSection):
        if node.level == 4:
            item_name = node.title.strip()
            
            meta_line = ""
            casting_time = ""
            range_val = ""
            components = ""
            duration = ""
            desc_lines = []
            
            for line in node.content:
                cleaned = line.strip()
                if not cleaned: continue
                
                if cleaned.startswith("_") and cleaned.endswith("_") and not meta_line:
                    meta_line = cleaned.replace("_", "")
                elif cleaned.startswith("**Casting Time:**"):
                    casting_time = cleaned.replace("**Casting Time:**", "").strip()
                elif cleaned.startswith("**Range:**"):
                    range_val = cleaned.replace("**Range:**", "").strip()
                elif cleaned.startswith("**Components:**"):
                    components = cleaned.replace("**Components:**", "").strip()
                elif cleaned.startswith("**Duration:**"):
                    duration = cleaned.replace("**Duration:**", "").strip()
                else:
                    if not cleaned.startswith("<table>") and not cleaned.startswith("<table"):
                        if not cleaned.startswith("<th>") and not cleaned.startswith("<td>") and not cleaned.startswith("<tr>") and not cleaned.startswith("<tbody>") and not cleaned.startswith("<thead>") and not cleaned.startswith("</table>"):
                            desc_lines.append(cleaned)
                            
            if meta_line and ("Evocation" in meta_line or "Abjuration" in meta_line or "Conjuration" in meta_line or "Divination" in meta_line or "Enchantment" in meta_line or "Illusion" in meta_line or "Necromancy" in meta_line or "Transmutation" in meta_line):
                
                m = re.match(r'(?:Level (\d+)\s+)?([A-Za-z]+)(?:\s+Cantrip)?(?:\s+\((.*?)\))?', meta_line)
                level = 0
                school = "Evocation"
                classes = []
                if m:
                    if m.group(1): level = int(m.group(1))
                    if m.group(2): school = m.group(2).capitalize()
                    if m.group(3): 
                        classes = [c.strip() for c in m.group(3).split(",")]
                
                desc = "\n".join(desc_lines)
                
                spells_data.append({
                    "name": item_name,
                    "level": level,
                    "school": school,
                    "classes": classes,
                    "casting_time": casting_time,
                    "range": range_val,
                    "components": components,
                    "duration": duration,
                    "concentration": "Concentration" in duration,
                    "ritual": "Ritual" in casting_time,
                    "description": desc
                })
            
        for child in node.subsections:
            find_spells_recursive(child)
            
    find_spells_recursive(root)

    out_path = "src/models/generated_spells.json"
    with open(out_path, "w", encoding="utf-8") as f:
         json.dump(spells_data, f, indent=4)
         
    print(f"Generated {len(spells_data)} spells.")

if __name__ == "__main__":
    extract_spells()
