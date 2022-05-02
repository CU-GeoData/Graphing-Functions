# Credit: phobson on github
# https://gist.github.com/phobson/41b41bdd157a2bcf6e14

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pandafuncs import *
import getfiles

def _convert_dir(directions, N=None):
    if N is None:
        N = directions.shape[0]
    barDir = directions * np.pi/180. - np.pi/N
    barWidth = 2 * np.pi / N
    return barDir, barWidth

def make_wind_rose(rosedata, wind_dirs, title, palette=None):
    if palette is None:
        palette = sns.color_palette('crest_r', n_colors=rosedata.shape[1])

    bar_dir, bar_width = _convert_dir(wind_dirs)

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.set_theta_direction('clockwise')
    ax.set_theta_zero_location('N')

    for n, (c1, c2) in enumerate(zip(rosedata.columns[:-1], rosedata.columns[1:])):
        if n == 0:
            # first column only
            ax.bar(bar_dir, rosedata[c1].values,
                   width=bar_width,
                   color=palette[0],
                   edgecolor='none',
                   label=c1,
                   linewidth=0)
        ax.bar(bar_dir, rosedata[c2].values,
               width=bar_width,
               bottom=rosedata.cumsum(axis=1)[c1].values,
               color=palette[n+1],
               edgecolor='none',
               label=c2,
               linewidth=0)

    ax.set_title(title)

    return fig

def windrose(file, range):
    kpdx = makeFrame(file)
    # Create bins to filter out unwanted windspeeds
    if range[1] != np.inf:
        spd_bins = [0, range[0], range[1], np.inf]
        range_str = str(range[0]) + " - " + str(range[1]) + " mph"
        spd_labels = ["-1", range_str, "-1"]
    else:
        spd_bins = [0, range[0], np.inf]
        range_str = ">" + str(range[0]) + " mph"
        spd_labels = ["-1", range_str]

    # Group windspeeds into wanted or unwanted
    kpdx['wspd'] = pd.cut(kpdx['wspd'], bins = spd_bins, labels = spd_labels, right = True, ordered = False)
    # Remove unwanted windspeeds
    removeThese = kpdx.index[kpdx['wspd']=="-1"].tolist()
    kpdx = kpdx.drop(removeThese)
    kpdx = kpdx.dropna(how='any')


    dir_bins = np.arange(-7.5, 370, 15)
    dir_labels = (dir_bins[:-1] + dir_bins[1:]) / 2
    total_count = kpdx['wspd'].shape[0]
    rose = (
        kpdx.assign(WindDir_bins=lambda df:
            pd.cut(df['wdir'], bins=dir_bins, labels=dir_labels, right=False)
         )
        .replace({'WindDir_bins': {360: 0}})
        .groupby(by=['wspd', 'WindDir_bins'])
        .size()
        .unstack(level='wspd')
        .sort_index(axis=1)
        .applymap(lambda x: x / total_count * 100)
    )
    directions = np.arange(0, 360, 15)
    fig = make_wind_rose(rose, directions, file[:-4] + " " + range_str)
    plt.show()

# specify directory with dir argument 
for f in getfiles.getFilesWithName(include=["2020", "Summer"], exclude=["Processed", "Clean"]):
    windrose(f, [3, np.inf])
