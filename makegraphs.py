#!/usr/bin/env python

from pathlib import Path
import pandas as pd
import numpy as np
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


outdir.mkdir(exist_ok=True, parents=True)

# ============  Propagation distance graph ==============

ds_distance = pd.DataFrame(
    [
        [0, -18.27],
        [10, -19.95],
        [20, -21.93],
        [30, -25.34],
        [40, -26.90],
        [50, -27.00],
        ],
    columns=['x', 'y']
    )

fig, ax = plt.subplots(1)
ax.set_xlabel('Distance [cm]')
ax.set_ylabel('System Transfer [gain]')

fig.suptitle("Distance vs system transfer")

ax.scatter(
    ds_distance['x'],
    np.pow(10, ds_distance['y'] / 10)
    )

fig.savefig(outdir / f"prop_distance.pdf")
fig.savefig(outdir / f"prop_distance.svg")

# ================== Cable propagation =================

ds_baseline_ch1 = readcsv('TEK0000')
ds_baseline_ch2 = readcsv('TEK0001')
ds_long_ch1 = readcsv('TEK0002')
ds_long_ch2 = readcsv('TEK0003')
ds_open = readcsv('TEK0004')
ds_short = readcsv('TEK0005')
ds_matched = readcsv('TEK0006')
ds_black = readcsv('TEK0007')
ds_gray = readcsv('TEK0008')

def timedelay(ref, prop):
    ref_10percent = (ref.y[len(ref.y) - 1] - ref.y[0]) * 0.1
    prop_10percent = (prop.y[len(prop.y) - 1] - prop.y[0]) * 0.1

    ref_index = (ref.y - ref_10percent).abs().argmin()
    prop_index = (prop.y - prop_10percent).abs().argmin()

    ref_time = ref.x[ref_index]
    prop_time = prop.x[prop_index]

    delta_time = prop_time - ref_time

    return ref_index, prop_index, ref_time, prop_time

def avglevels(y, string):
    rng = y.max() - y.min()
    y_max_avg = (y[y >= rng * 0.9]).mean()
    y_min_avg = (y[y <= rng * 0.1]).mean()
    y_mid_avg = (y[[a and b for a, b in zip(y <= rng * 0.25, y <= rng * 0.75)]]).mean()
    print(f"{string} {y_min_avg=:.3E}")
    print(f"{string} {y_max_avg=:.3E}")
    print(f"{string} {y_mid_avg=:.3E}")
    return y_min_avg, y_max_avg

def makegraph(builder, stem):
    fig, ax = plt.subplots(1)
    builder(fig, ax)
    ax.set_xlabel('Time [Seconds]')
    ax.set_ylabel('Voltage [V]')
    fig.savefig(outdir / f"{stem}.pdf")
    fig.savefig(outdir / f"{stem}.svg")

def build_baseline(fig, ax):
    ref_index, prop_index, ref_time, prop_time = timedelay(ds_baseline_ch2, ds_baseline_ch1)

    log(f'Baseline Time delay: {prop_time - ref_time:.6E} s')

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
    ax.axvline(ref_time, -1, 1, color='green')
    ax.axvline(prop_time, -1, 1, color='green')
    ax.annotate(
        f'Time delay:\n{prop_time - ref_time:.3E} s',
        xy = ((prop_time - ref_time) / 2, ds_baseline_ch2.y[ref_index]), 
        xytext = (-150, 100),
        textcoords='offset pixels',
        fontsize = 12,
        arrowprops = dict(facecolor = 'red'),
        color = 'g'
        )
    fig.suptitle("Baseline")
    ax.legend()

    #ymin, ymax = avglevels(ds_baseline['y'], 'baseline')

def build_long(fig, ax):
    ref_index, prop_index, ref_time, prop_time = timedelay(ds_long_ch2, ds_long_ch1)

    log(f'Long Time delay: {prop_time - ref_time:.6E} s')
    #ymin, ymax = avglevels(ds_long['y'], 'long')

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
    ax.axvline(ref_time, -1, 1, color='green')
    ax.axvline(prop_time, -1, 1, color='green')
    ax.text(
        s=f'Time delay:\n{prop_time - ref_time:.3E} s',
        x = (prop_time - ref_time) / 2,
        y = ds_long_ch2.y[ref_index],
        fontsize = 12,
        color = 'g'
        )
    fig.suptitle("Long cable")
    ax.legend()

def build_open(fig, ax):
    ax.plot(ds_open['x'], ds_open['y'], **plot_args)

    ymin, ymax = avglevels(ds_open['y'], 'open')

    #ax.axhline(ymin, -1, 1, color='green')
    #ax.axhline(ymax, -1, 1, color='green')
    #ax.text(
    #    s=f'Max Average Value:\n{ymax:.3E} s',
    #    x = 0,
    #    y = ymax * 0.9,
    #    fontsize = 11,
    #    color = 'g'
    #    )
    #ax.text(
    #    s=f'Min Average Value:\n{ymin:.3E} s',
    #    x = ds_open['x'].max() * 0.5,
    #    y = ymin * 1.5,
    #    fontsize = 11,
    #    color = 'g'
    #    )

    fig.suptitle("Open Circuit")

def build_short(fig, ax):
    ax.plot(ds_short['x'], ds_short['y'], **plot_args)
    ymin, ymax = avglevels(ds_short['y'], 'short')
    fig.suptitle("Short Circuit")

def build_matched(fig, ax):
    ax.plot(ds_matched['x'], ds_matched['y'], **plot_args)
    ymin, ymax = avglevels(ds_matched['y'], 'matched')
    fig.suptitle("Matched Load")

def build_black(fig, ax):
    ax.plot(ds_black['x'], ds_black['y'], **plot_args)
    ymin, ymax = avglevels(ds_black['y'], 'black')
    fig.suptitle('"Black" Load')

def build_gray(fig, ax):
    ax.plot(ds_gray['x'], ds_gray['y'], **plot_args)
    ymin, ymax = avglevels(ds_gray['y'], 'gray')
    fig.suptitle('"Gray" Load')

makegraph(build_baseline, 'baseline')
makegraph(build_long, 'long')
makegraph(build_open, 'open')
makegraph(build_short, 'short')
makegraph(build_matched, 'matched')
makegraph(build_black, 'black')
makegraph(build_gray, 'gray')

