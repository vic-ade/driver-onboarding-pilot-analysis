"""Reproducible descriptive analysis of *synthetic* driver-onboarding data.

The two-period difference-in-differences estimates here are illustrative;
there is no evidence of causal identification in this simulated exercise.
"""
from pathlib import Path
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / 'data'
FIG = BASE / 'figures'
ORDER = ['Pilot', 'Comparison']
COL = {'Pilot':'#0B8B77', 'Comparison':'#7D8BA4'}


def summaries(routes, drivers):
    # Derive the outcome so the flag can be checked against source minutes.
    assert (routes['late_route_flag'] == (routes['overrun_minutes'] > 30).astype(int)).all()
    assert routes['route_id'].is_unique and drivers['driver_id'].is_unique
    assert (drivers['eligible_day14'] == 1).all()
    rt = routes.groupby(['group', 'period'], observed=True).agg(
        n_routes=('route_id', 'count'),
        late_rate=('late_route_flag', 'mean'),
        dispatch_rate=('on_time_dispatch', 'mean'),
        completion_pct=('delivery_completion_pct', 'mean'),
        safety_score=('safety_proxy_score', 'mean'),
    ).reset_index()
    rt['late_rate'] *= 100
    rt['dispatch_rate'] *= 100
    dr = drivers[drivers['eligible_day14'] == 1].groupby(['group', 'period'], observed=True).agg(
        n_drivers=('driver_id', 'count'),
        day14_retention=('active_day14', 'mean'),
    ).reset_index()
    dr['day14_retention'] *= 100
    return rt, dr


def get_value(t, group, period, metric):
    vals = t.loc[(t.group == group) & (t.period == period), metric]
    assert len(vals) == 1
    return float(vals.iloc[0])


def did(t, metric):
    """DiD in original metric units: (pilot post-pre) - (comparison post-pre)."""
    return (get_value(t, 'Pilot', 'Post', metric) - get_value(t, 'Pilot', 'Pre', metric)
            - get_value(t, 'Comparison', 'Post', metric) + get_value(t, 'Comparison', 'Pre', metric))


def grouped_chart(table, metric, title, ylabel, filename, ylim=None):
    FIG.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9.8, 5.2), dpi=150)
    for group in ORDER:
        pre, post = [get_value(table, group, p, metric) for p in ('Pre', 'Post')]
        ax.plot([0,1], [pre,post], marker='o', markersize=10, linewidth=3.1,
                color=COL[group], label=group)
        for x,y in [(0,pre),(1,post)]:
            ax.annotate(f'{y:.1f}', (x,y), xytext=(0,10), textcoords='offset points',
                        ha='center', fontsize=11, fontweight='bold', color=COL[group])
    ax.set_xticks([0,1], ['Before','After'])
    ax.set_xlim(-.17,1.17)
    if ylim: ax.set_ylim(*ylim)
    ax.set_ylabel(ylabel)
    ax.set_title(title, loc='left', fontweight='bold', fontsize=16, pad=14)
    ax.grid(axis='y', alpha=.18)
    ax.spines[['top','right']].set_visible(False)
    ax.legend(frameon=False, loc='best')
    fig.tight_layout(pad=2)
    fig.savefig(FIG / filename, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def run():
    routes = pd.read_csv(DATA / 'synthetic_routes.csv')
    drivers = pd.read_csv(DATA / 'synthetic_drivers.csv')
    rt, dr = summaries(routes, drivers)
    summary = {
        'notice': 'ALL DATA AND NUMBERS ARE SYNTHETIC; NOT REAL-WORLD RESULTS',
        'n_routes': int(len(routes)), 'n_drivers': int(len(drivers)),
        'n_sites': int(routes['site_id'].nunique()),
        'late_route_did_pp': round(did(rt, 'late_rate'), 3),
        'retention_did_pp': round(did(dr, 'day14_retention'), 3),
        'dispatch_did_pp': round(did(rt, 'dispatch_rate'), 3),
        'completion_did_pp': round(did(rt, 'completion_pct'), 3),
        'safety_score_did': round(did(rt, 'safety_score'), 3),
        'routes_table': rt.round(3).to_dict(orient='records'),
        'drivers_table': dr.round(3).to_dict(orient='records'),
    }
    grouped_chart(rt, 'late_rate', 'Late-route rate | synthetic comparison', 'Routes >30 min over plan (%)', 'late_route_rates.png', (0,31))
    grouped_chart(dr, 'day14_retention', 'Day-14 activity | synthetic comparison', 'Eligible drivers still active (%)', 'retention_rates.png', (60,100))
    grouped_chart(rt, 'completion_pct', 'Delivery completion | synthetic comparison', 'Average delivery completion (%)', 'completion_rates.png', (94,100))
    FIG.mkdir(parents=True, exist_ok=True)
    (FIG / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print('Illustrative difference-in-differences (percentage points):')
    print(f"  Late routes: {summary['late_route_did_pp']:+.2f} pp")
    print(f"  Day-14 retention: {summary['retention_did_pp']:+.2f} pp")
    print(f"  Delivery completion: {summary['completion_did_pp']:+.2f} pp")
    print('Figures written to figures/. No real operational data used.')
    return summary


if __name__ == '__main__':
    run()
