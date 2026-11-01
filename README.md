# Driver Onboarding Pilot | Performance & Retention Analysis

> **PUBLIC PORTFOLIO DEMONSTRATION — ALL DATA ARE SYNTHETIC.**  
> This is a newly created, fictionalised case study demonstrating an analytical approach. It does **not** publish, reproduce or validate any employer's confidential data, pilot results, business assumptions or internal materials. Names, site IDs, dates, group composition and outcomes are invented.

![Synthetic case study — presentation cover](figures/presentation_cover.png)

**Quick links:** [Portfolio PDF presentation](presentation/Driver_Onboarding_Pilot_Portfolio.pdf) · [Editable PowerPoint](presentation/Driver_Onboarding_Pilot_Portfolio.pptx) · [Executed Jupyter notebook](notebooks/pilot_evaluation.ipynb)

## Business question

**Does a revised onboarding pathway help new delivery drivers complete routes more reliably and remain active — without creating quality or safety trade-offs?**

This project demonstrates how I would assess an operational change by comparing a pilot group with a comparison group **before and after** implementation.

## Skills demonstrated

**Python · pandas · Data validation · KPI design · Difference-in-differences (DiD) · Cohort retention · Data visualisation · Business communication**

## Project at a glance

| Item | Public demonstration |
|---|---|
| Design | Pilot vs. comparison, pre vs. post |
| Data | 4,800 **synthetic** routes; 1,200 **synthetic** driver records |
| Sites | 24 fictional sites |
| Primary KPI | Late-route rate: share of routes >30 minutes beyond plan |
| Retention | Day-14 activity among eligible fictional starters |
| Guardrails | On-time dispatch, delivery completion, safety-proxy score |
| Status | Educational case study, **not a causal or financial claim** |

## Method

1. **Generate synthetic data:** reproducible seed and documented assumptions, with no confidential inputs.
2. **Validate quality:** unique IDs, complete group/period categories and consistency between overrun minutes and late-route flags.
3. **Calculate metrics:** aggregate pilot/comparison rates in pre/post periods; use eligible starter cohorts for day-14 activity.
4. **Estimate the DiD contrast:**

   `DiD = (Pilot_Post − Pilot_Pre) − (Comparison_Post − Comparison_Pre)`

5. **Interpret trade-offs:** compare a primary improvement against quality and safety proxy outcomes; note limitations and next steps.

## What the fictional data show

**Every value below is generated for this demonstration and must not be interpreted as an actual business result.**

| Illustrative metric | Pilot-relative change (DiD) | Interpretation |
|---|---:|---|
| Late-route rate | **-12.75 percentage points** | Lower is better |
| Day-14 activity | **+11.67 percentage points** | Higher is better |
| On-time dispatch | **+2.75 percentage points** | Higher is better |
| Delivery completion | **-0.68 percentage points** | Negative change warrants investigation |
| Safety-proxy score | **-14.07 points** | Proxy only; lower score warrants investigation |

### Route performance

![Synthetic late-route comparison](figures/late_route_rates.png)

### Driver activity after 14 days

![Synthetic driver retention comparison](figures/retention_rates.png)

### Delivery quality safeguard

![Synthetic delivery completion comparison](figures/completion_rates.png)

## Business interpretation

In this **fictional exercise**, route reliability and day-14 activity improve more in the pilot group than in the comparison group. However, completion and the safety proxy shift in an unfavourable direction. A decision-maker should investigate these trade-offs before treating the pilot as a success.

**Important limitations:** The sites are not randomly assigned; the data contain just two labelled periods, so parallel trends cannot be tested; day-14 activity is not long-term retention or proof of competence; and none of these numbers represent realised financial savings. This is a descriptive demonstration of DiD calculations, **not proof of causation**.

## Repository contents

```text
driver-onboarding-pilot-analysis/
├── README.md
├── PUBLICATION_CHECKLIST.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── synthetic_routes.csv
│   └── synthetic_drivers.csv
├── src/
│   ├── generate_synthetic_data.py
│   └── analyze_pilot.py
├── notebooks/
│   └── pilot_evaluation.ipynb
├── figures/
│   ├── presentation_cover.png
│   ├── late_route_rates.png
│   ├── retention_rates.png
│   ├── completion_rates.png
│   └── summary.json
└── presentation/
    ├── Driver_Onboarding_Pilot_Portfolio.pptx
    └── Driver_Onboarding_Pilot_Portfolio.pdf
```

## Reproduce locally (Windows / macOS / Linux)

```bash
python -m pip install -r requirements.txt
python src/generate_synthetic_data.py
python src/analyze_pilot.py
jupyter notebook
```

Open `notebooks/pilot_evaluation.ipynb` from Jupyter after the scripts run. The scripts use a fixed random seed; generated figures and tables should match the version committed here.

## Why this analysis matters

A useful analyst moves beyond saying whether one KPI increased or decreased. The value is in understanding the counterfactual comparison, asking what else changed, checking the quality/safety guardrails, and communicating what evidence would be required before an operational decision.

## Public-release disclaimer

This is an educational reconstruction inspired by the **type** of analytical problem encountered in operational performance work. All data, scenario settings, observations and conclusions in this repository are synthetic. This repo does not contain operational source documents, confidential results, proprietary identifiers or company branding. Before publishing, verify that the description itself complies with any applicable agreement or employer policy.
