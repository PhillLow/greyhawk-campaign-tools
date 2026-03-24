import os
import sys
import json
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.engine.srd_parser import parse_markdown_to_tree, MarkdownSection

def extract_feats():
    filepath = "dnd-5e-srd-markdown/feats.md"
    root = parse_markdown_to_tree(filepath)
    feats_data = {"Origin": [], "General": [], "Fighting Style": [], "Epic Boon": []}

    def find_feats_recursive(node: MarkdownSection, feats_list):
        if node.level == 4:
            feat_name = node.title.strip()
            
            desc_lines = []
            feat_type = "General"
            prereq_lvl = 1
            
            for line in node.content:
                cleaned = line.strip()
                # Remove markdown links or formatting if present
                if cleaned.startswith("_") and "Feat" in cleaned:
                    if "Origin" in cleaned: feat_type = "Origin"
                    elif "Fighting Style" in cleaned: feat_type = "Fighting Style"
                    elif "Epic Boon" in cleaned: feat_type = "Epic Boon"
                    else: feat_type = "General"
                    
                    if "Level" in cleaned:
                        m = re.search(r'Level (\d+)\+', cleaned)
                        if m: prereq_lvl = int(m.group(1))
                elif cleaned:
                    desc_lines.append(cleaned)
            
            # Special case for Fighting styles missing 'feats' prefix in our hardcoded class
            # We'll just keep the actual name from the markdown (e.g. "Archery")
            desc = " ".join(desc_lines)
            if len(desc) > 200: desc = desc[:197] + "..."
            
            if feat_type in feats_list:
                feats_list[feat_type].append({
                    "name": feat_name,
                    "description": desc,
                    "type": feat_type,
                    "prerequisite_level": prereq_lvl
                })
            else:
                feats_list["General"].append({
                    "name": feat_name,
                    "description": desc,
                    "type": "General",
                    "prerequisite_level": prereq_lvl
                })
            
        for child in node.subsections:
            find_feats_recursive(child, feats_list)
            
    find_feats_recursive(root, feats_data)

    out_path = "src/models/generated_feats.json"
    with open(out_path, "w", encoding="utf-8") as f:
         json.dump(feats_data, f, indent=4)
         
    total = sum(len(v) for v in feats_data.values())
    print(f"Generated {total} feats.")

if __name__ == "__main__":
    extract_feats()
