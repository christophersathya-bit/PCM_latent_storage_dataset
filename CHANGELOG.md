# Changelog

All notable changes to the PCM Latent Heat Storage Dataset.

## v1.7 — 2026-11-01

- **Solid–liquid PCMs only.** Removed 13 solid–solid PCMs (pentaerythritol and the PlusICE X series). Material IDs were renumbered.
- **Literature expansion.** Composite PCMs (porous silica, carbon-filled and form-stable, microencapsulated, stabilised eutectic salt hydrates), fatty-acid eutectics (Ke 2017, Zhou 2023, Liu 2023), salt–water eutectic solutions (−31 to −1.5 °C), water/ice (IAPWS), PEG grades and other pure compounds, and building products (Rubitherm SP/GR, Micronal, Energain, Devan, Henkel).
- **New file** `data/pcm_composites_v1_7.csv`: 197 composite PCMs with base PCM, support/shell, filler, loading, Tm, latent heat, conductivity, nucleating agent and supercooling, plus `columns_composites.csv`.
- **Licence** CC BY 4.0 added; `CITATION.cff` added.
- Totals: 766 materials, 302 CFD-ready (tier A 1, B 64, C 237), 36 source keys.

## v1.6

- Filled missing specific heat for 63 pure compounds from NIST WebBook / Shomate equations, plus conductivity and density from Mao 2025, Vélez and Rubitherm datasheets.
- CFD subset: materials with only phase-unspecified or one-phase values are included as tier C, with a `phase_assumed` column explaining what was copied.

## v1.5

- Added 12 CFD and chemistry columns: liquid viscosity, thermal expansion β, solidus/liquidus, volume change on melting, melting behaviour, literature supercooling, InChIKey and SMILES.
- NIST reference viscosity and conductivity for molten salts, n-octadecane review correlations, solar salt (DLR 2022).
- First CFD-ready subset file.

## v1.4

- Added 9 columns: CAS, crystallisation temperature, supercooling, cycling, flash point, hazard, degradation temperature, corrosion and price.
- Axiotherm and Pluss datasheet cp/k/ρ/max T; Müller 2020 rows verified against the paper; CAS numbers for 119 pure compounds (PubChem).

## v1.3

- Added the University of Lleida / CORA open datasets (CC BY 4.0), Xie 2017 salt hydrates and eutectics, Hirschey 2018 (ORNL) salt hydrates, and Jebasingh 2016 fatty-acid ternaries.

## v1.2

- Added Croda, Axiotherm, Pluss, BioPCM, Insolcorp and Sasol products, and 38 literature entries (Müller 2020 DSC set, Mao 2025 review, alkali metals, metal and salt eutectics).

## v1.1

- Added adipic acid and a stearic acid–adipic acid eutectic composite; new Composite category.

## v1.0

- First release: pure organics, salt hydrates, molten salts, metals, eutectics and commercial products from reviews and manufacturer datasheets.
