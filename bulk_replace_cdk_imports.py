import os

# Define the directory you want to scan
base_dir = './'

# Define the replacement rules
replacements = {
    'import aws_cdk as core': 'import aws_cdk as core',
    'import aws_cdk as cdk': 'import aws_cdk as cdk',
}

# Walk through all files and subfolders
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Apply replacements
            original_content = content
            for old, new in replacements.items():
                content = content.replace(old, new)

            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'✅ Updated: {file_path}')
