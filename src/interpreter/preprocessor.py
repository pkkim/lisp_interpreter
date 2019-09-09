def remove_comments(code):
    result = []
    for line in code.splitlines():
        try:
            comment_index = line.index(';')
        except ValueError:
            result.append(line)
        else:
            result.append(line[:comment_index])
    return '\n'.join(result)
