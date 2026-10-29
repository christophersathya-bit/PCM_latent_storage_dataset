# PCM Latent Heat Storage Dataset (v1.4)

A curated dataset of **561 phase change materials (PCMs)** for latent heat thermal energy storage, from −74 °C to 1085 °C. Every row has its source (DOI or URL) and a data-status flag. An ML-ready version is included.

Compiled October 2026 by Christopher Sathya.

## Contents

| Path | What it is |
|---|---|
| `data/pcm_dataset_v1_4.xlsx` | Main workbook. Sheets: README, PCM_Data, Charts, Summary, Sources, Chart_Data, ML_Data, ML_Guide, ML_Results |
| `data/pcm_dataset_v1_4.csv` | Main table as CSV (34 columns) |
| `data/pcm_ml_ready_v1_4.csv` | ML-ready table (41 columns: one-hot categories, best-available cp/k/ρ with phase flags, formula descriptors, `group_id`, `sample_weight`) |
| `data/results.csv` | ML cross-validation results |
| `data/organic_rdkit_features.csv` | RDKit descriptors for 55 organic compounds |
| `data/archive/` | Earlier versions v1.0–v1.3 |
| `scripts/build/` | Python scripts that build the workbook and CSVs from the source data |
| `scripts/ml/` | ML experiment script (GroupKFold CV; Ridge, GP, RF, GBR) |

## Coverage

| Category | Entries |
|---|---|
| Organic (paraffins, fatty acids, alcohols, esters, sugar alcohols…) | 58 |
| Inorganic (salt hydrates, anhydrous salts) | 58 |
| Metallic | 16 |
| Eutectic (organic, salt hydrate, molten salt, metal) | 66 |
| Composite | 10 |
| Commercial products (10 suppliers) | 353 |

**Properties:** melting temperature and latent heat for all rows. Specific heat for ~53%, thermal conductivity for ~60%, density for ~63%. CAS number for 119 pure compounds. Some rows also have crystallization temperature, flash point, hazard level, degradation temperature and price.

## Main sources

- **Reviews:** Zalba 2003, Sharma 2009, Kenisarin 2010, Abhat 1983, Xie 2017, Hirschey 2018 (ORNL), Mao 2025
- **Measured data:** Müller et al. 2020 (consistent DSC method)
- **Open datasets:** University of Lleida / CORA, CC BY 4.0 ([10.34810/data1218](https://doi.org/10.34810/data1218), [10.34810/data2156](https://doi.org/10.34810/data2156), [10.34810/data1822](https://doi.org/10.34810/data1822))
- **Handbook data:** NIST WebBook / CRC
- **Manufacturer datasheets:** Rubitherm, PureTemp, PCM Products (PlusICE), Croda, Axiotherm, Pluss, Phase Change Solutions (BioPCM), Insolcorp, Sasol, Cowa

The full reference list is on the `Sources` sheet.

## Data quality

The `Data status` column says how each value was obtained:

- **Verified, measured or datasheet:** checked against the original document.
- **Literature/handbook value:** taken from the cited review; verify before publishing.
- **Secondary review table:** copied through a second review; verify against the original paper.

Published values for the same material can differ by 10–20%. Known discrepancies are recorded in `Notes`.

## ML summary

5-fold GroupKFold cross-validation; see the `ML_Results` sheet for details.

| Task | Best result |
|---|---|
| Latent heat, entropy-of-fusion route (needs Tm) | R² ≈ 0.74 (all), 0.78 (inorganics) |
| Latent heat, organics only | MAE ≈ 22 kJ/kg, R² ≈ 0.66 |
| Tm, organics with RDKit descriptors | MAE ≈ 20 °C, R² ≈ 0.72 |

## Rebuilding

```bash
pip install openpyxl pandas scikit-learn rdkit
python scripts/build/build.py     # rebuilds data/*.xlsx and data/*.csv
python scripts/ml/run.py          # reruns the ML experiments
```

`openpyxl` writes formulas without cached values, so open the rebuilt workbook in Excel or LibreOffice once to calculate them.

## Known gaps

- Rubitherm SP series and RT datasheets (cp, k, ρ)
- Microtek and Climator (no public numbers)
- Composites from 2020–2026 papers (only 10 so far)
- Supercooling and cycling stability (few rows)

## Licence and attribution

This repository is private and no licence has been chosen yet. If it is shared or published:

- The Lleida/CORA rows are **CC BY 4.0** and must be attributed (DOIs above).
- Values from reviews and manufacturer datasheets should be cited to their original sources (see `Sources`).
