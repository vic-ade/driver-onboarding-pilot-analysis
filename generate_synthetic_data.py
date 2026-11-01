"""Generate fictional delivery onboarding data for an educational portfolio.

No operational/company data are used. All sites, routes, drivers, outcomes
and parameters in this demonstration are invented.
"""
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
ROUTES_OUT = BASE / 'data' / 'synthetic_routes.csv'
DRIVERS_OUT = BASE / 'data' / 'synthetic_drivers.csv'
SEED = 20261101

# All settings are hypothetical and used solely to make the demonstration informative.
RATE_ASSUMPTIONS = {
    ('Pilot', 'Pre'): dict(late=0.235, dispatch=0.860, completion=0.982, safety=800),
    ('Pilot', 'Post'): dict(late=0.140, dispatch=0.920, completion=0.974, safety=783),
    ('Comparison', 'Pre'): dict(late=0.220, dispatch=0.855, completion=0.983, safety=798),
    ('Comparison', 'Post'): dict(late=0.204, dispatch=0.870, completion=0.982, safety=795),
}
RETENTION_ASSUMPTIONS = {
    ('Pilot', 'Pre'): 0.745,
    ('Pilot', 'Post'): 0.830,
    ('Comparison', 'Pre'): 0.752,
    ('Comparison', 'Post'): 0.768,
}


def generate(seed=SEED):
    rng = np.random.default_rng(seed)
    routes = []
    drivers = []
    route_id = driver_id = 0
    for site_num in range(1, 25):
        site = f'S{site_num:03d}'
        group = 'Pilot' if site_num <= 12 else 'Comparison'
        for period in ('Pre', 'Post'):
            cfg = RATE_ASSUMPTIONS[(group, period)]
            for _ in range(100):  # 24 sites * 2 periods * 100 = 4,800 fictional routes
                route_id += 1
                late = int(rng.random() < cfg['late'])
                # Flag is derived from overrun_minutes (and never simulated separately).
                overrun = int(rng.integers(31, 91) if late else rng.integers(-25, 31))
                completion = np.clip(rng.normal(cfg['completion'], 0.011), 0.90, 1.0)
                safety = np.clip(rng.normal(cfg['safety'], 33), 600, 900)
                routes.append({
                    'route_id': f'R{route_id:06d}',
                    'site_id': site,
                    'group': group,
                    'period': period,
                    'overrun_minutes': overrun,
                    'late_route_flag': int(overrun > 30),
                    'on_time_dispatch': int(rng.random() < cfg['dispatch']),
                    'delivery_completion_pct': round(float(completion * 100), 2),
                    'safety_proxy_score': round(float(safety), 1),
                })
            for _ in range(25):  # 24 sites * 2 periods * 25 = 1,200 fictional driver starts
                driver_id += 1
                drivers.append({
                    'driver_id': f'D{driver_id:05d}',
                    'site_id': site,
                    'group': group,
                    'period': period,
                    'eligible_day14': 1,  # Invented cohorts are all assumed matured
                    'active_day14': int(rng.random() < RETENTION_ASSUMPTIONS[(group, period)]),
                })
    routes_df, drivers_df = pd.DataFrame(routes), pd.DataFrame(drivers)
    ROUTES_OUT.parent.mkdir(parents=True, exist_ok=True)
    routes_df.to_csv(ROUTES_OUT, index=False)
    drivers_df.to_csv(DRIVERS_OUT, index=False)
    print(f'Created {len(routes_df):,} synthetic routes and {len(drivers_df):,} synthetic driver records.')
    return routes_df, drivers_df


if __name__ == '__main__':
    generate()
