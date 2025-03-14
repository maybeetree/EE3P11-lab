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

plot_args = dict(
    )

def readcsv(stem):
    csvfile = csvdir / f"{stem}.CSV"
    df = pd.read_csv(csvfile, skiprows=range(0, 19), header=None)
    df = df.iloc[:, 3:5]
    df.columns=['x', 'y']
    return df

ds_baseline_ch1 = readcsv('TEK0000')
ds_baseline_ch2 = readcsv('TEK0001')
ds_long_ch1 = readcsv('TEK0002')
ds_long_ch2 = readcsv('TEK0003')
ds_open = readcsv('TEK0004')
ds_short = readcsv('TEK0005')
ds_matched = readcsv('TEK0006')
ds_black = readcsv('TEK0007')
ds_gray = readcsv('TEK0008')

outdir.mkdir(exist_ok=True, parents=True)

def makegraph(builder, stem):
    fig, ax = plt.subplots(1)
    builder(fig, ax)
    ax.set_xlabel('Time [Seconds]')
    ax.set_ylabel('Voltage [V]')
    fig.savefig(outdir / f"{stem}.pdf")
    fig.savefig(outdir / f"{stem}.svg")

def build_baseline(fig, ax):
    ax.plot(
            ds_baseline_ch2['x'],
            ds_baseline_ch2['y'],
            label='Reference signal',
            **plot_args,
            )
    ax.plot(
            ds_baseline_ch1['x'],
            ds_baseline_ch1['y'],
            label='Propagated signal',
            **plot_args
            )
    fig.suptitle("Baseline")
    ax.legend()

def build_long(fig, ax):
    ax.plot(
            ds_long_ch2['x'],
            ds_long_ch2['y'],
            label='Reference signal',
            **plot_args,
            )
    ax.plot(
            ds_long_ch1['x'],
            ds_long_ch1['y'],
            label='Propagated signal',
            **plot_args,
            )
    fig.suptitle("Long cable")
    ax.legend()

def build_open(fig, ax):
    ax.plot(ds_open['x'], ds_open['y'], **plot_args)
    fig.suptitle("Open Circuit")

def build_short(fig, ax):
    ax.plot(ds_short['x'], ds_short['y'], **plot_args)
    fig.suptitle("Short Circuit")

def build_matched(fig, ax):
    ax.plot(ds_matched['x'], ds_matched['y'], **plot_args)
    fig.suptitle("Matched Load")

def build_black(fig, ax):
    ax.plot(ds_black['x'], ds_black['y'], **plot_args)
    fig.suptitle('"Black" Load')

def build_gray(fig, ax):
    ax.plot(ds_gray['x'], ds_gray['y'], **plot_args)
    fig.suptitle('"Gray" Load')

makegraph(build_baseline, 'baseline')
makegraph(build_long, 'long')
makegraph(build_open, 'open')
makegraph(build_short, 'short')
makegraph(build_matched, 'matched')
makegraph(build_black, 'black')
makegraph(build_gray, 'gray')

