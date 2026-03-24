import re

def fix():
    filename = "src/models/class_model.py"
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    fixed_text = re.sub(
        r'ClassFeature\(name=([^,]+),\s*level=([^,]+),\s*description=([^\)]+)\)',
        r'{"name": \1, "level": \2, "description": \3}',
        text
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(fixed_text)

if __name__ == "__main__":
    fix()
