"""
Delete the migrated HTML files after migration to JSON is complete.
"""
import os

files_to_delete = [
    r"h:\Github\PrincipiaMetaphysica\foundations\kaluza-klein.html",
    r"h:\Github\PrincipiaMetaphysica\foundations\g2-manifolds.html",
    r"h:\Github\PrincipiaMetaphysica\foundations\calabi-yau.html"
]

for filepath in files_to_delete:
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"[DELETED] {os.path.basename(filepath)}")
    else:
        print(f"[SKIP] {os.path.basename(filepath)} - not found")

print("\n[OK] Deletion complete")
