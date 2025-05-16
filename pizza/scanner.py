import os
import ast

# This scans for imports&hidden imports used in the project when building with pyinstaller esp when building obfuscated code
# This file should not be in the executable

def find(directory):
    for root, d, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                yield os.path.join(root, file)

def extract(file_path):
    imports = []
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for ali in node.names:
                    imports.append(ali.name)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)
    return imports

def getImports(directory):
    imports = set()
    for file in find(directory):
        imports.update(extract(file))
    return imports

directory = "pizza/src" 
imports = getImports(directory)
himports = ' '.join([f'--hidden-import={imp}' for imp in imports])
print(f"{himports}")
