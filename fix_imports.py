#!/usr/bin/env python3
import os

# Bulk update CDK v2 imports (aws_cdk_lib) to CDK v1 style (aws_cdk)
replacements = {
    'import aws_cdk as core': 'import aws_cdk as core',
    'import aws_cdk as cdk':  'import aws_cdk as cdk',
    'from aws_cdk import':    'from aws_cdk import',
}

# Scan all .py files in the project recursively
base_dir = os.path.abspath(os.path.dirname(__file__))
for root, dirs, files in os.walk(base_dir):
    for fn in files:
        if fn.endswith('.py'):
            file_path = os.path.join(root, fn)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            updated = content
            for old, new in replacements.items():
                updated = updated.replace(old, new)

            if updated != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated)
                print(f'✓ Updated imports in: {file_path}')

