import os
import sys
import json
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.engine.srd_parser import parse_markdown_to_tree, MarkdownSection

def find_features(node: MarkdownSection) -> list:
    features = []
    match = re.search(r'Level (\d+):\s*(.*)', node.title, re.IGNORECASE)
    if match:
        level = int(match.group(1))
        feat_name = match.group(2).strip()
        
        desc = ""
        for line in node.content:
            cleaned = line.strip()
            if cleaned and not cleaned.startswith('<') and not cleaned.startswith('_') and not cleaned.startswith('|'):
                desc = cleaned
                break
        if not desc:
            desc = feat_name
        if len(desc) > 150: desc = desc[:147] + "..."
        
        features.append({
            "name": feat_name,
            "level": level,
            "description": desc
        })
        
    for sub in node.subsections:
        features.extend(find_features(sub))
    return features

def extract_features():
    filepath = "dnd-5e-srd-markdown/classes.md"
    root = parse_markdown_to_tree(filepath)
    
    if not root.subsections:
        print("No subsections in root")
        return
        
    classes_node = root.subsections[0]
    classes_data = {}
    
    for cls_node in classes_node.subsections:
        cls_name = cls_node.title.upper()
        features = find_features(cls_node)
        
        if features:
            classes_data[cls_name] = features
            
    out_path = "src/models/generated_class_features.json"
    with open(out_path, "w", encoding="utf-8") as f:
         json.dump(classes_data, f, indent=4)
         
    print(f"Generated {sum(len(v) for v in classes_data.values())} features across {len(classes_data)} classes.")

if __name__ == "__main__":
    extract_features()
