import os
import re
from typing import Dict, List, Any

class MarkdownSection:
    def __init__(self, title: str, level: int):
        self.title = title
        self.level = level
        self.content = []
        self.subsections = []

    def get_text(self) -> str:
        return "\n".join(self.content).strip()

    def get_subsection(self, title: str):
        for sub in self.subsections:
            if sub.title.lower() == title.lower():
                return sub
        return None

def parse_markdown_to_tree(filepath: str) -> MarkdownSection:
    """Parses a markdown file into a hierarchy of headers and content."""
    root = MarkdownSection("Root", 0)
    stack = [root]
    
    # Check if the file exists, if not, adjust path for tests running from different directories
    if not os.path.exists(filepath):
        # try climbing up one directory and looking for dnd-5e-srd-markdown
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        alt_path = os.path.join(base_dir, filepath)
        if os.path.exists(alt_path):
            filepath = alt_path
        else:
            raise FileNotFoundError(f"Could not find markdown file: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            header_match = re.match(r'^(#{1,6})\s+(.*)', line)
            
            # Skip code blocks or HTML tables parsing for the plain header match (simplistic protection)
            if header_match and not line.strip().startswith('```'):
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                new_section = MarkdownSection(title, level)
                
                # Pop the stack until we find a parent level
                while stack and stack[-1].level >= level:
                    stack.pop()
                    
                stack[-1].subsections.append(new_section)
                stack.append(new_section)
            else:
                stack[-1].content.append(line.rstrip())
                
    return root
