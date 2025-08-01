def check(file_path):
    import zipfile
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            return z.testzip() is None
    except Exception:
        return False
