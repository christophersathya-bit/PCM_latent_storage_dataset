# PCM Latent Heat Storage Dataset — ML-ready (v1.4)

Machine-learning-ready dataset of **561 phase change materials (PCMs)** for latent heat thermal energy storage, from −74 °C to 1085 °C.

Compiled October 2026 by Christopher Sathya.

## File

`data/pcm_ml_ready_v1_4.csv` — one row per material, 41 columns, UTF-8.

## Columns

| Column(s) | Meaning |
|---|---|
| `ID`, `Name`, `Category`, `Subclass` | Identifier and classification |
| `group_id` | Same material or same supplier share a group. Use for GroupKFold splits to avoid leakage between near-duplicates |
| `sample_weight` | Data-quality weight: 1.0 verified/datasheet/measured, 0.9 manufacturer listing, 0.8 literature/handbook, 0.7 secondary review table |
| `in_core_set` | 1 = pure compound with a parsed formula, or a eutectic |
| `is_organic` … `is_commercial` | One-hot category flags |
| `is_solid_solid` | 1 = solid–solid transition |
| `latent_is_total_storage` | 1 = supplier value is heat storage capacity over a range (latent + some sensible) |
| `Tm_C`, `latent_kJkg` | Melting temperature (°C) and latent heat (kJ/kg). Filled for every row |
| `volumetric_MJm3` | Latent heat × density / 1000 |
| `cp_kJkgK`, `k_WmK`, `rho_kgm3` + `*_phase` | Best available specific heat, thermal conductivity and density, with the phase they refer to. Blank = not reported |
| `cryst_T_C`, `supercooling_K_from_data` | Crystallization temperature and Tm − cryst_T, where reported |
| `formula_parsed` … `water_mass_frac` | Descriptors computed from the chemical formula (pure compounds): molar mass, atom counts, halogen/metal atoms, hydrate water count, water mass fraction |
| `C_chain_len_if_alkane`, `has_COOH_like` | Alkane chain length; carboxylic-acid flag |
| `Source key`, `Data status` | Source of each value and how it was obtained |

## Coverage

| Category | Rows |
|---|---|
| Organic | 58 |
| Inorganic | 58 |
| Metallic | 16 |
| Eutectic | 66 |
| Composite | 10 |
| Commercial products (10 suppliers) | 353 |

## Notes for use

- Do not fill blank cp, k or density values with zeros.
- Published values for the same material can differ by 10–20%; use `sample_weight` or filter on `Data status`.
- Commercial rows have no chemical formula, so formula descriptors are blank for them.

## Sources

Zalba 2003, Sharma 2009, Kenisarin 2010, Abhat 1983, Xie 2017, Hirschey 2018, Mao 2025, Müller et al. 2020, NIST WebBook/CRC, University of Lleida/CORA open datasets (CC BY 4.0: [10.34810/data1218](https://doi.org/10.34810/data1218), [10.34810/data2156](https://doi.org/10.34810/data2156), [10.34810/data1822](https://doi.org/10.34810/data1822)), and manufacturer datasheets (Rubitherm, PureTemp, PCM Products, Croda, Axiotherm, Pluss, Phase Change Solutions, Insolcorp, Sasol, Cowa).

## Licence

Private repository; no licence chosen yet. If shared, the Lleida/CORA rows must be attributed (CC BY 4.0).
