# tuple: (name,cat,sub,formula,tr,Tm,L,cp_s,cp_l,k_s,k_l,rho_s,rho_l,src,notes,status)
X="Xie2017"; H="Hirschey2018"; J="Jebasingh2016"; L1="Lleida_HT2024"; L2="Lleida_HTexp2025"; L3="Lleida_Ind2024"
XS="Review table (Xie 2017) - verify against original reference"
JS="Secondary table (Jebasingh 2016) - verify against original reference"
LS="Lleida/CORA open dataset (CC BY 4.0) - downloaded 2026-10-29"
LE="Lleida/CORA dataset, DSC/hot-disk measured - downloaded 2026-10-29"
S=lambda n,f,tm,l,src,st,notes="",cat="Inorganic",sub="Salt hydrate",**k:(n,cat,sub,f,"S-L",tm,l,k.get('cps'),k.get('cpl'),k.get('ks'),k.get('kl'),k.get('rs'),k.get('rl'),src,notes,st)
lit3 = [
# Xie 2017 Table 1 (new salt hydrates)
S("Lithium bromide dihydrate","LiBr·2H2O",34,124,X,XS,"Printed as 'LiBr2·2H2O' in source"),
S("Potassium fluoride dihydrate","KF·2H2O",42,162,X,XS),
S("Magnesium iodide dihydrate","MgI2·2H2O",42,133,X,XS),
S("Iron(III) nitrate nonahydrate","Fe(NO3)3·9H2O",47,155,X,XS,"Printed as 'Fe(NO3)2·9H2O' in source"),
S("Sodium metasilicate tetrahydrate","Na2SiO3·4H2O",48,168,X,XS),
S("Dipotassium phosphate heptahydrate","K2HPO4·7H2O",48,99,X,XS),
S("Magnesium sulfate heptahydrate","MgSO4·7H2O",48.5,202,X,XS),
S("Calcium nitrate trihydrate","Ca(NO3)2·3H2O",51,104,X,XS,"",rs=1460),
S("Iron(III) chloride dihydrate","FeCl3·2H2O",56,90,X,XS),
S("Nickel nitrate hexahydrate","Ni(NO3)2·6H2O",57,169,X,XS),
S("Magnesium chloride tetrahydrate","MgCl2·4H2O",58,178,X,XS),
S("Trisodium phosphate dodecahydrate","Na3PO4·12H2O",67,190,X,XS,"Reported 65–69 °C"),
S("Lithium acetate dihydrate","LiCH3COO·2H2O",70,150,X,XS),
S("Sodium pyrophosphate hydrate","Na4P2O7·10H2O",70,184,X,XS,"Printed as 'Na2P2O7·12H2O' in source; formula uncertain"),
S("Aluminium nitrate hydrate","Al(NO3)3·xH2O",89.3,150,X,XS,"Printed as 'Al(NO3)2·8H2O'; hydrate uncertain (usually nonahydrate)"),
# Hirschey 2018
S("Dipotassium phosphate hexahydrate","K2HPO4·6H2O",13.3,109.3,H,"Review table (Hirschey 2018, ORNL) - verify against original","Also 14 °C / 108 kJ/kg (Lane 1983); density 1750 kg/m³; ~$1.45/kg",rs=1750),
S("Iron(III) chloride hexahydrate","FeCl3·6H2O",37.0,186.2,H,"Review table (Hirschey 2018, ORNL) - verify against original","DSC (Guion 1983); Kauffman & Pan 1973: 36.1 °C / 226 kJ/kg; ~$2.64/kg",rs=1820),
S("Calcium chloride tetrahydrate","CaCl2·4H2O",44.2,99.6,H,"Review table (Hirschey 2018, ORNL) - verify against original","DSC (Ushak 2016)",rs=1567),
# Xie 2017 Table 2 eutectics
S("CaCl2·6H2O + CaBr2·6H2O","55:45 wt%",14.7,140,X,XS,cat="Eutectic",sub="Inorganic-inorganic"),
S("CaCl2·6H2O + MgCl2·6H2O (75:25)","75:25 wt%",21.4,102.3,X,XS,cat="Eutectic",sub="Inorganic-inorganic"),
S("Na2CO3·10H2O + Na2HPO4·12H2O","40:60 wt%",27.3,220.2,X,XS,cat="Eutectic",sub="Inorganic-inorganic"),
S("Ca(NO3)2·4H2O + Mg(NO3)2·6H2O","47:33 wt% (as printed)",30,136,X,XS,"Hydrates printed as ·10H2O in source",cat="Eutectic",sub="Inorganic-inorganic"),
S("Na2SO4·10H2O + Na2HPO4·12H2O","25:75 wt%",31.2,262.3,X,XS,cat="Eutectic",sub="Inorganic-inorganic"),
S("Mg(NO3)2·6H2O + MgCl2·6H2O (80:20)","80:20 wt%",60,150,X,XS,"Also in Lleida industrial dataset (hazard level 3)",cat="Eutectic",sub="Inorganic-inorganic"),
S("Mg(NO3)2·6H2O + Al(NO3)3·9H2O","53:47 wt%",66,168,X,XS,cat="Eutectic",sub="Inorganic-inorganic"),
S("LiNO3·3H2O + Mg(NO3)2·6H2O","14:86 wt%",72,180,X,XS,cat="Eutectic",sub="Inorganic-inorganic"),
# Jebasingh 2016 ternary fatty acids + composites
S("Capric-myristic-palmitic acid (CA-MA-PA)","64.8:22.6:12.6 wt%",17.7,148.7,J,"Measured (Jebasingh 2016) - verify vs paper","Freezing onset 8.4 °C / 144.2 J/g",cat="Eutectic",sub="Organic ternary",kl=0.149),
S("Lauric-palmitic-stearic acid (LA-PA-SA)","ternary",31.8,151.6,J,JS,"Zhang et al. 2014",cat="Eutectic",sub="Organic ternary"),
S("Lauric-myristic-palmitic acid (LA-MA-PA)","ternary",30.94,145.3,J,JS,"Zhang et al. 2013",cat="Eutectic",sub="Organic ternary"),
S("Lauric-myristic-stearic acid (LA-MA-SA)","ternary",29.05,140.9,J,JS,"Liu et al. 2014",cat="Eutectic",sub="Organic ternary"),
S("CA-MA-PA / exfoliated graphite (xG-F)","5 wt% xG-F",17.5,143.7,J,"Measured (Jebasingh 2016) - verify vs paper","k +14% vs pure eutectic",cat="Composite",sub="Fatty acid eutectic + graphite",kl=0.170),
S("Capric acid / expanded graphite","20 wt% EG",27.8,132.64,J,JS,"Sari et al. 2008",cat="Composite",sub="Fatty acid + EG"),
S("Palmitic acid / expanded graphite","20 wt% EG",60.88,148.36,J,JS,"Sari & Karaipekli 2009",cat="Composite",sub="Fatty acid + EG"),
S("LA-PA-SA / expanded perlite","45 wt% EP",31.8,81.5,J,JS,"Zhang et al. 2014",cat="Composite",sub="Fatty acid eutectic + perlite"),
S("LA-MA-PA / expanded graphite","5.3 wt% EG",30.94,135.9,J,JS,"Zhang et al. 2013",cat="Composite",sub="Fatty acid eutectic + EG"),
S("LA-MA-SA / expanded graphite","7.69 wt% EG",29.05,137.1,J,JS,"Liu et al. 2014",cat="Composite",sub="Fatty acid eutectic + EG"),
S("Paraffin / exfoliated graphite nanoplatelets","5 wt% xGnP",50.8,131.5,J,JS,"",cat="Composite",sub="Paraffin + graphite"),
S("Palmitic-stearic acid / carbon nanotubes","8 wt% CNT",53.59,165,J,JS,"Zhang et al. 2014",cat="Composite",sub="Fatty acid eutectic + CNT"),
S("CA-MA-PA / expanded graphite","7.69 wt% EG",18.61,128.2,J,JS,"Yuan et al. 2014",cat="Composite",sub="Fatty acid eutectic + EG"),
# Lleida HT screening 2024
S("MnCl2-NaCl","64.33:35.67 wt%",426,230,L1,LS,"Hazard 3; photosensitive; price 0.24 €/kJ",cat="Eutectic",sub="Molten salt (chloride)"),
S("LiF-LiOH (20:80 mol%)","20:80 mol%",427,869,L1,LS,"Hazard 3; hygroscopic; 0.35 €/kJ",cat="Eutectic",sub="Molten salt (hydroxide-fluoride)",cps=0.80,cpl=1.00,rs=1600),
S("LiF-LiOH (21.33:78.67 wt%)","21.33:78.67 wt%",431,889,L1,LS,"Hazard 3; hygroscopic; 0.35 €/kJ",cat="Eutectic",sub="Molten salt (hydroxide-fluoride)"),
S("MgCl2-KCl","39:61 wt%",435,351,L1,LS,"Corrosion 1.00 mm/yr; degradation 700 °C; hazard 3; 0.28 €/kJ",cat="Eutectic",sub="Molten salt (chloride)",cps=0.80,cpl=0.96,rs=2110,kl=0.81),
S("MgCl2-RbCl","21.65:78.35 wt%",446,136,L1,LS,"Hazard 3; hygroscopic",cat="Eutectic",sub="Molten salt (chloride)"),
S("LiCl-MgCl2","49.65:50.35 wt%",447,401,L1,LS,"Hazard 3; hygroscopic",cat="Eutectic",sub="Molten salt (chloride)"),
S("LiF-LiBr","8.62:91.38 wt%",450,275,L1,LS,"Hazard 3; deliquescent",cat="Eutectic",sub="Molten salt (halide)"),
S("NaCl-MgCl2 (48:52 wt%)","48:52 wt%",450,430,L1,LS,"Hazard 0; hygroscopic; 0.25 €/kJ",cat="Eutectic",sub="Molten salt (chloride)",cps=0.92,cpl=1.00,rs=2230,kl=0.95),
S("CaCl2-KCl-MgCl2-NaCl","55.06:1.95:9.97:33.02 wt%",460,245,L1,LS,"Hazard 2; 1.00 €/kJ",cat="Eutectic",sub="Molten salt (chloride)"),
S("CaCl2-KCl-NaCl (64.63:6.29:29.08)","64.63:6.29:29.08 wt%",465,245,L1,LS,"Hazard 2; 1.00 €/kJ",cat="Eutectic",sub="Molten salt (chloride)"),
S("KCl-CaCl2-MgCl2","25:27:48 wt%",487,342,L1,LS,"Hazard 2; 0.72 €/kJ; Lleida 2025 DSC measured 447.5 °C / 105.9 J/g",cat="Eutectic",sub="Molten salt (chloride)",cps=0.80,rs=2530,kl=0.88),
S("Li2CO3-K2CO3","47:53 wt%",488,342,L1,LS,"Degradation 530 °C; hazard 3; 0.99 €/kJ",cat="Eutectic",sub="Molten salt (carbonate)",cps=1.03,cpl=1.34,rs=2220,kl=1.99),
S("Li2CO3-Na2CO3 (44:56 wt%)","44:56 wt%",496,370,L1,LS,"Degradation 530 °C; hazard 3; 0.21 €/kJ; same as Mao 2025 entry",cat="Eutectic",sub="Molten salt (carbonate)",cps=1.80,cpl=2.09,rs=2320,kl=2.09),
S("NaCl-CaCl2","33:67 wt%",500,393,L1,LS,"Hazard 2; 0.90 €/kJ",cat="Eutectic",sub="Molten salt (chloride)",cps=0.84,cpl=1.00,rs=2160,kl=1.20),
S("CaCl2-KCl-NaCl (66:5:29)","66:5:29 wt%",504,279,L1,LS,"Hazard 2; 1.26 €/kJ",cat="Eutectic",sub="Molten salt (chloride)",cps=1.17,cpl=1.00,rs=2150,kl=1.00),
S("Calcium nitrate (anhydrous)","Ca(NO3)2",560,145,L1,LS,"Degradation 500 °C; hazard 3; deliquescent",sub="Salt (anhydrous)",rs=2113),
S("NaCl-KCl-Na2CO3","25:33:42 wt%",569,249,L1,LS,"Hazard 2; 0.16 €/kJ",cat="Eutectic",sub="Molten salt (mixed)",cps=1.34,cpl=1.41,rs=1700,rl=2000,kl=0.50),
S("NaCl-Na2CO3 (48:52 wt%)","48:52 wt%",580,339,L1,LS,"Hazard 2; 0.11 €/kJ",cat="Eutectic",sub="Molten salt (mixed)",cps=1.30,rs=2000,kl=0.60),
S("Li2CO3-Na2CO3-K2CO3","22:16:62 wt%",580,288,L1,LS,"Degradation 827 °C; hazard 3; 0.22 €/kJ",cat="Eutectic",sub="Molten salt (carbonate)",cps=1.80,cpl=2.90,rs=2340,kl=1.95),
S("NaCl-Na2SO4-Na2CO3","31:30:39 wt%",597,221,L1,LS,"Hazard 2; 0.15 €/kJ",cat="Eutectic",sub="Molten salt (mixed)",cps=1.20,cpl=1.30,rs=2000,kl=0.50),
# Lleida 2025 experimental
S("CaCl2-KCl-MgCl2-NaCl (41.6:2.2:8.8:47.4 mol%) [measured]","41.6:2.2:8.8:47.4 mol%",497.8,104.8,L2,LE,"Max operating 760.4 °C",cat="Eutectic",sub="Molten salt (chloride)",ks=0.76),
S("KCl-CaCl2-MgCl2 (25:27:48 wt%) [measured]","25:27:48 wt%",447.5,105.9,L2,LE,"Max operating 720.7 °C; literature 487 °C / 342 J/g",cat="Eutectic",sub="Molten salt (chloride)",ks=1.04),
S("Li2CO3-K2CO3 (47:53 wt%) [measured]","47:53 wt%",488.1,240.2,L2,LE,"Max operating 580.8 °C; literature 342 J/g",cat="Eutectic",sub="Molten salt (carbonate)",ks=1.42),
S("Li2CO3-Na2CO3 (44:56 wt%) [measured]","44:56 wt%",495.9,220.9,L2,LE,"Max operating 640.3 °C; literature 370 J/g",cat="Eutectic",sub="Molten salt (carbonate)",ks=1.26),
S("NaCl-KCl-Na2CO3 (25:33:42 wt%) [measured]","25:33:42 wt%",570.4,254.2,L2,LE,"Max operating 650.7 °C",cat="Eutectic",sub="Molten salt (mixed)",ks=1.89),
# Lleida industrial 2024
S("Mg(NO3)2·6H2O + MgCl2·6H2O (60:40)","60:40 wt%",60,132.3,L3,LS,"Degradation 130 °C; hazard 3",cat="Eutectic",sub="Inorganic-inorganic",cps=2.3,cpl=2.8,rs=1517,rl=1512),
S("Salicylic acid","C7H6O3",159,180.5,L3,LS,"Latent heat reported 162–199 J/g (midpoint used); hazard 2",cat="Organic",sub="Aromatic acid"),
S("LiNO3-NaNO3","49:51 wt%",193,248,L3,LS,"Hazard 2",cat="Eutectic",sub="Molten salt (nitrate)"),
S("NaNO3-KNO3 (50:50 wt%)","50:50 wt%",221,100.5,L3,LS,"Reported 220–222 °C, 100–101 J/g; hazard 2",cat="Eutectic",sub="Molten salt (nitrate)",cps=2.25,cpl=1.35,rs=1920,kl=0.56),
S("Solar salt NaNO3-KNO3 (60:40 wt%)","60:40 wt%",224,109.5,L3,LS,"Reported 221–227 °C, 109–110 J/g; degradation 589–624 °C; hazard 2",cat="Eutectic",sub="Molten salt (nitrate)",cpl=1.42,kl=0.24),
]
# enrich existing Rubitherm rows from Lleida industrial dataset: name -> dict
enrich = {
 "Rubitherm RT 54 HC": dict(cps=2,cpl=2,rs=990,rl=850,ks=0.2,kl=0.2,extra="cp/ρ/k from Lleida industrial dataset (DOI 10.34810/data1822), which lists 182 kJ/kg"),
 "Rubitherm RT 55": dict(cps=2,cpl=2,rs=880,rl=770,ks=0.2,kl=0.2,extra="cp/ρ/k from Lleida industrial dataset (DOI 10.34810/data1822), which lists 158 kJ/kg"),
 "Rubitherm RT 64 HC": dict(cps=2,cpl=2,rs=880,rl=780,ks=0.2,kl=0.2,extra="cp/ρ/k from Lleida industrial dataset (DOI 10.34810/data1822), which lists 242 kJ/kg"),
}
SRC3 = {
 "Xie2017":("Xie N. et al., Inorganic salt hydrate for thermal energy storage, Applied Sciences 7 (2017) 1317","https://doi.org/10.3390/app7121317"),
 "Hirschey2018":("Hirschey J. et al., Review of inorganic salt hydrates with phase change temperature in range of 5 °C to 60 °C and material cost comparison with common waxes, 5th Int. High Performance Buildings Conf., Purdue (2018)","https://www.osti.gov/servlets/purl/1468092"),
 "Jebasingh2016":("Jebasingh E.B., Effects of various types of graphite on the thermal conductivity and energy storage properties of ternary eutectic fatty acid-based composite as PCM, Renewables: Wind, Water, and Solar 3 (2016) 8","https://doi.org/10.1186/s40807-016-0028-2"),
 "Lleida_HT2024":("Cabeza L.F., Borri E., Martínez Alcocer R., Screening of potential materials to be used as PCM for high temperature application, CORA dataset v1.0 (2024), CC BY 4.0","https://doi.org/10.34810/data1218"),
 "Lleida_HTexp2025":("Martínez Alcocer F.R. et al., Suitable phase change materials for high-temperature applications, CORA dataset v1.0 (2025), CC BY 4.0","https://doi.org/10.34810/data2156"),
 "Lleida_Ind2024":("Cabeza L.F. et al., Suitable materials to be used as PCM for industrial applications, CORA dataset v1.0 (2024), CC BY 4.0","https://doi.org/10.34810/data1822"),
}
