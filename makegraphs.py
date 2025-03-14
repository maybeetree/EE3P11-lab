#!/usr/bin/env python

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sys import stderr

def log(*args, **kwargs):
    kwargs['file'] = stderr
    return print(*args, **kwargs)

csvdir = Path('data/Session1-EMLabs')
outdir = Path('output')

scatter_args = dict(
    # Make the scatter point small
    s=2,
    linewidth=0
    )

titles = {
    "TEK0001": "Foobar",
    }

outdir.mkdir(exist_ok=True, parents=True)

for csvfile in csvdir.rglob('*.CSV'):

    stem = csvfile.stem
    log(f"Making plot for {stem}")
    if stem not in titles.keys():
        log(f"Not title specified!")

    # read csv into datafram
    df = pd.read_csv(csvfile, skiprows=range(0, 19), header=None)

    # Get dataserieses from cols 3, 4
    ds1 = df.iloc[:, 3]
    ds2 = df.iloc[:, 4]

    fig, ax = plt.subplots(1)
    ax.scatter(ds1, ds2, **scatter_args)
    fig.suptitle(titles.get(stem, stem))
    ax.set_xlabel('Time [???]')
    ax.set_ylabel('Voltage [V]')
    fig.savefig(outdir / f"{stem}.pdf")



