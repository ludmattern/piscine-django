import polib
import os

po_file_path = "locale/fr/LC_MESSAGES/django.po"
mo_file_path = "locale/fr/LC_MESSAGES/django.mo"

if os.path.exists(po_file_path):
    po = polib.pofile(po_file_path)
    po.save_as_mofile(mo_file_path)
    print(f"Compiled {po_file_path} to {mo_file_path}")
else:
    print(f"File not found: {po_file_path}")
