import pandas as pd

def makeFrame(filename : str, dir : str ="air_data/newa_2020/"):
    """
    Returns pandas dataframe using data from file.

    filename (str) : name of csv file.
    dir (str)      : directory that data is in.
    """
    if filename.find('.') == -1:
        end = ".csv"
    else:
        end = ""

    data = pd.read_csv(dir + filename + end)

    return data

def discretize(df, col, numbins = -1, bins=[], labels=[]):
    """
    Discretizes dataframe's values at column of name (col) into bins.

    Must either give the number of bins to categorize the data into or provide a
    bins list that specify which values will be grouped together. See bins argument
    from pandas.cut()

    """
    assert numbins > 0 or bins != [], "must specify bins or numbins"

    min, max = round(df[col].min()), round(df[col].max())

    if bins == []:
        bins = range(min, max, round((max-min)/(numbins+1)))
    if labels == []:
        for x in range(len(bins)):
            bins[x] = str(bins[x])
        labels = ["<" + bin[1]] + bin[1:-1] + [">" + bin[-1]]

    df[col] = pd.cut(x=df[col], bins=bins, labels=labels)
    return df
