import re
def split_file(content):
    test = {}
    pattern = '\n语文|\n数学'


    results = re.split(pattern, content)

    for content in results:
        loc = content.index('：')
        key = content[:loc]
        key = key.strip('\n\r')
        item = content[loc + 1:]
        item = item.strip('\n\r')
        test[key] = item
    return test

