import os


def get_file_paths(directory, batch_size, include_subdirectories=False, extensions=None, case_sensitive=False):
    file_paths = []

    if extensions and not case_sensitive:
        extensions = [ext.lower() for ext in extensions]

    if include_subdirectories:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if extensions is None or any(
                        (file.lower() if not case_sensitive else file).endswith(ext) for ext in extensions):
                    file_paths.append(os.path.abspath(os.path.join(root, file)))
    else:
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                if extensions is None or any(
                        (file.lower() if not case_sensitive else file).endswith(ext) for ext in extensions):
                    file_paths.append(os.path.abspath(os.path.join(directory, file)))

    total = len(file_paths)
    processed = 0

    print("文件搜索完毕，共计{}个文件。".format(total))

    for i in range(0, len(file_paths), batch_size):
        print("已经完成{}个文件（{}%）".format(processed, (processed/total)*100))
        processed += batch_size
        yield file_paths[i:i + batch_size]
