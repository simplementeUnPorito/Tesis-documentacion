"""Agrega a [Content_Types].xml los Default que python-pptx omite (jpg), para que validate.py pase."""
import sys, zipfile, shutil, os
for path in sys.argv[1:]:
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename == "[Content_Types].xml":
                x = data.decode("utf-8")
                for ext, ct in (("jpg", "image/jpeg"), ("jpeg", "image/jpeg")):
                    if f'Extension="{ext}"' not in x:
                        x = x.replace("<Default ", f'<Default Extension="{ext}" ContentType="{ct}"/><Default ', 1)
                data = x.encode("utf-8")
            zout.writestr(it, data)
    os.replace(tmp, path); print("ok", path)
