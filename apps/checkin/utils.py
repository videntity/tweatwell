def update_filename(instance, filename):
    path = "freggie-pics/"
    format = instance.user.username + "-" + filename
    return os.path.join(path, format)