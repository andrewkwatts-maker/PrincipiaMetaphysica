import re

# List of HTML files to update in root
html_names = [
    'appendices', 'beginners-guide', 'formulas', 'foundations',
    'paper', 'parameters', 'philosophical-implications',
    'references', 'sections', 'simulations', 'visualization-index'
]

# Update index.html
print("Updating index.html...")
with open(r'h:\Github\PrincipiaMetaphysica\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

original_content = content

# Replace links to moved HTML files
for name in html_names:
    # Match href="filename.html (with optional #anchor)
    pattern = f'href="{name}.html'
    replacement = f'href="Website/{name}.html'
    content = content.replace(pattern, replacement)

if content != original_content:
    with open(r'h:\Github\PrincipiaMetaphysica\index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated index.html - replaced {original_content.count('href=') - content.count('href=')} links")
else:
    print("No changes needed in index.html")

# Update files in Website folder - they may reference each other
website_files = [
    'appendices.html', 'beginners-guide.html', 'formulas.html',
    'foundations.html', 'paper.html', 'parameters.html',
    'philosophical-implications.html', 'references.html',
    'sections.html', 'simulations.html', 'visualization-index.html'
]

for filename in website_files:
    filepath = f'h:\\Github\\PrincipiaMetaphysica\\Website\\{filename}'
    print(f"\nUpdating {filename}...")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Update links to other files that are now in Website folder
        for name in html_names:
            # Match href="filename.html (direct reference, now same folder)
            # These should stay as-is since they're in the same folder
            pass

        # Update links back to index.html (which stayed in root)
        # Change href="index.html" to href="../index.html"
        if 'href="index.html"' in content:
            content = content.replace('href="index.html"', 'href="../index.html"')
            print(f"  Updated links to index.html")

        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  File updated")
        else:
            print(f"  No changes needed")

    except Exception as e:
        print(f"  Error: {e}")

print("\nLink updates complete!")
