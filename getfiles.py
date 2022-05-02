import os

def getFilesWithName(include=[], exclude=[], oneof=[], dir="""air_data/newa_2020/"""):
    """
    Returns list of files that contain all words in include, none of the words
    in exclude, and at least one of the words in oneof.

    include (str list): all words that must be in file name
    exclude (str list): all words that can not be in file name
    dir (str optional): directory to look for data
    """
    files = os.listdir(dir)
    # Line below gets all files that have all the words in include and none of the words
    # in exclude
    if oneof != []:
        ret = [_ for _ in files if all(w in _ for w in include) and any(w in _ for w in oneof) and not any(w in _ for w in exclude)]
    else:
        ret = [_ for _ in files if all(w in _ for w in include) and not any(w in _ for w in exclude)]
    return ret

def getFilesWithCol(keywords, dir = """air_data/newa_2020/"""):
    """
    Returns list of files from directory dir with following condition: All words in
    keywords will be arguments / column titles in the file.

    This assumes that all the files in dir are .csv files.

    Note: if there is an argument such as 'AVG_temp', and you just want temp, this will
    return files with AVG_temp. To avoid this, then include the delimiters around
    the columns.
    Ex): For a file with columns 'date,temp,wind,hour', use keyword=[',temp,'] as argument,
    not ['temp'].

    dir (str), keywords (str list)
    """
    files = os.listdir(dir)
    ret = [_ for _ in files if all(w in open(dir+_, "r").readline() for w in keywords)]
    return ret
