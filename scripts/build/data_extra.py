# Literature additions (same tuple format as data_lit.lit) + per-row status override (last element)
M="Muller2020"; MA="Mao2025"; N="NIST_dHfus"; Z="Zalba2003"
SEC="Secondary review table (Mao 2025) - verify against original reference"
MEAS="DSC-measured, consistent round-robin method (Muller 2020) - verify vs paper Table 5"
lit2 = [
("n-Decane","Organic","Paraffin (n-alkane)","C10H22","S-L",-30.2,207.3,None,None,None,None,None,None,M,"Melting onset; peak -27.8 °C",MEAS),
("Propionic acid","Organic","Fatty acid","C3H6O2","S-L",-25.7,143.7,None,None,None,None,None,None,M,"Melting onset",MEAS),
("Hexanoic acid","Organic","Fatty acid","C6H12O2","S-L",-4.7,141.2,None,None,None,None,None,None,M,"Melting onset",MEAS),
("1-Undecanol","Organic","Fatty alcohol","C11H24O","S-L",14.5,206.6,None,None,None,None,None,None,M,"Melting onset; peak 17.5 °C",MEAS),
("Ethyl octadecanoate (ethyl stearate)","Organic","Ester","C20H40O2","S-L",32.3,188.7,None,None,None,None,None,None,M,"Melting onset",MEAS),
("Methyl octadecanoate (methyl stearate)","Organic","Ester","C19H38O2","S-L",37.4,229.2,None,None,None,None,None,None,M,"Melting onset",MEAS),
("1-Octadecanol","Organic","Fatty alcohol","C18H38O","S-L",56.8,245.9,None,None,None,None,None,None,M,"Melting onset",MEAS),
("Polyethylene glycol 10000","Organic","Polyethylene glycol","H(OC2H4)nOH, Mw~10000","S-L",59.3,179.8,None,None,None,None,None,None,M,"Melting onset",MEAS),
("Calcium bromide hexahydrate","Inorganic","Salt hydrate","CaBr2·6H2O","S-L",32.7,125.1,None,None,None,None,None,None,M,"Melting onset; Zalba 2003 lists 34 °C / 115.5 kJ/kg",MEAS),
("Myristic-stearic acid (50:50 wt%)","Eutectic","Organic-organic","C14/C18 acid 50:50 wt%","S-L",45.7,180.0,None,None,None,None,None,None,M,"Melting onset",MEAS),
("n-Tetratriacontane","Organic","Paraffin (n-alkane)","C34H70","S-L",75.9,269,None,None,None,None,None,772.8,MA,"",SEC),
("Dimethyl adipate","Organic","Ester","C8H14O4","S-L",9.7,164.6,None,None,None,0.358,None,1062,MA,"",SEC),
("Adonitol (ribitol)","Organic","Sugar alcohol","C5H12O5","S-L",101.6,247,None,None,None,None,None,None,MA,"",SEC),
("Lithium chlorate trihydrate","Inorganic","Salt hydrate","LiClO3·3H2O","S-L",8.0,253,None,None,None,None,None,None,Z,"Also in Mao 2025",None),
("Iron(III) bromide hexahydrate","Inorganic","Salt hydrate","FeBr3·6H2O","S-L",21.0,105,None,None,None,None,None,None,Z,"Also in Mao 2025",None),
("Sodium bromide","Inorganic","Salt (anhydrous)","NaBr","S-L",749.0,255,None,None,None,None,3200,None,MA,"",SEC),
("Calcium chloride (anhydrous)","Inorganic","Salt (anhydrous)","CaCl2","S-L",772.0,253,None,None,None,None,2150,None,MA,"",SEC),
("Sodium sulfate (anhydrous)","Inorganic","Salt (anhydrous)","Na2SO4","S-L",884.0,165,None,None,None,None,2680,None,MA,"",SEC),
("Barium chloride","Inorganic","Salt (anhydrous)","BaCl2","S-L",961.0,76,None,None,None,None,3856,None,MA,"",SEC),
("Potassium chromate","Inorganic","Salt (anhydrous)","K2CrO4","S-L",973.0,170,None,None,None,None,2660,None,MA,"Toxic (Cr VI)",SEC),
("Lead sulfate","Inorganic","Salt (anhydrous)","PbSO4","S-L",1000.0,133,None,None,None,None,6200,None,MA,"Toxic",SEC),
("Mercury","Metallic","Pure metal","Hg","S-L",-38.9,11.4,None,None,8.3,None,None,13546,N,"Toxic; reference only",None),
("Caesium","Metallic","Pure metal","Cs","S-L",28.4,15.7,None,None,35.9,None,1930,None,N,"Highly reactive; value computed from molar ΔHfus",None),
("Rubidium","Metallic","Pure metal","Rb","S-L",39.3,25.6,None,None,58.2,None,1532,None,N,"Highly reactive; value computed from molar ΔHfus",None),
("Potassium","Metallic","Pure metal","K","S-L",63.5,59.6,None,None,102.5,None,862,None,N,"Highly reactive",None),
("Sodium","Metallic","Pure metal","Na","S-L",97.8,113,None,None,142,None,968,None,N,"Highly reactive; value computed from molar ΔHfus",None),
("Lithium","Metallic","Pure metal","Li","S-L",180.5,432,None,None,84.8,None,534,None,N,"Highly reactive; value computed from molar ΔHfus",None),
("Copper","Metallic","Pure metal","Cu","S-L",1084.6,209,None,None,401,None,8960,None,N,"Value computed from molar ΔHfus",None),
("Mg-Zn eutectic","Eutectic","Metal alloy","Mg-Zn 48:52 wt%","S-L",340.0,180,None,None,None,None,None,None,MA,"",SEC),
("Zn-Al eutectic","Eutectic","Metal alloy","Zn-Al 96:4 wt%","S-L",381.0,138,None,None,None,None,None,None,MA,"",SEC),
("Al-Cu eutectic","Eutectic","Metal alloy","Al-Cu 66.92:33.08 wt%","S-L",548.0,372,None,None,None,None,None,None,MA,"",SEC),
("Tetradecane-hexadecane","Eutectic","Organic-organic","C14/C16 91.67:8.33 wt%","S-L",1.7,156.2,None,None,None,None,None,None,MA,"",SEC),
("Capric-lauric acid (61.5:38.5 wt%)","Eutectic","Organic-organic","C10/C12 acid 61.5:38.5 wt%","S-L",19.1,132,None,None,None,None,None,None,MA,"",SEC),
("AlCl3-NaCl-KCl","Eutectic","Molten salt","60:26:14 wt%","S-L",93.0,213,None,None,None,None,None,None,MA,"Corrosive",SEC),
("LiNO3-NH4NO3-KNO3","Eutectic","Molten salt","27:68:5 wt%","S-L",81.6,108,None,None,None,None,None,None,MA,"",SEC),
("MgCl2-NaCl","Eutectic","Molten salt","38.5:61.5 wt%","S-L",435.0,351,None,None,None,None,None,None,MA,"",SEC),
("Na2CO3-Li2CO3","Eutectic","Molten salt","56:44 wt%","S-L",496.0,370,None,None,None,None,None,None,MA,"",SEC),
("NaCl-Na2CO3","Eutectic","Molten salt","40.55:59.45 wt%","S-L",635.0,311.6,None,None,None,None,None,None,MA,"Stable after 1,000 cycles (per Mao 2025)",SEC),
]
# Commercial: (name, sub, supplier, tm, L, src, notes, extra dict)
com = []
for n,tm,tc,lm,lc in [("CrodaTherm 5",5,4,217,219),("CrodaTherm 6.5",7,5,219,226),("CrodaTherm 9.5",9,9,220,216),("CrodaTherm 15",13,12,207,212),("CrodaTherm 19",18,18,206,208),("CrodaTherm 21",20,20,215,210),("CrodaTherm 24W",23,23,207,213),("CrodaTherm 29",28,27,223,222),("CrodaTherm 32",32,31,211,213),("CrodaTherm 37",36,36,216,217),("CrodaTherm 53",52,52,220,221),("CrodaTherm 60",60,60,215,219),("CrodaTherm 74",75,71,226,224)]:
    com.append((n,"Bio-based organic (macro wax)","Croda (UK)",tm,lm,"Croda",f"Crystallisation {tc} °C / {lc} J/g",{}))
for n,tm,tc,lm in [("CrodaTherm ME 24XD",24,19,160),("CrodaTherm ME 29D",29,24,183),("CrodaTherm ME 29XD",29,22,165),("CrodaTherm ME 29DS",29,21,175)]:
    com.append((n,"Microencapsulated organic (dispersion)","Croda (UK)",tm,lm,"Croda",f"Crystallisation {tc} °C; DSC after water evaporation",{}))
for n,tm,l in [("ATS -63",-63,190),("ATS -50",-50,220),("ATS -40",-40,180),("ATS -34",-34,240),("ATS -24",-24,340),("ATS -21",-21,320),("ATS -12",-12,360),("ATS -10",-10,345),("ATS -6",-6,360),("ATS -3",-3,330),("ATP 2",2,215),("ATP 4",4,260),("ATP 6",6,275),("ATP 12",12,245),("ATP 16",16,245),("ATP 18",18,270),("ATP 20",20,220),("ATP 23",23,230),("ATP 28",28,265),("ATS 30",30,200),("ATP 36",36,240),("ATP 43",43,265),("ATS 44",44,230),("ATS 50",50,230),("ATP 52",52,230),("ATS 58",58,240),("ATP 60",60,230),("ATP 70",70,250),("ATP 78",78,225),("ATS 84",84,145),("ATS 89",89,145),("ATS 115",115,160)]:
    sub="Salt-based (ATS)" if n.startswith("ATS") else "Paraffin-based (ATP)"
    com.append(("Axiotherm "+n,sub+" [inferred from grade prefix]","Axiotherm GmbH (DE)",tm,l,"Axiotherm","Heat storage capacity as listed",{}))
pl = "HS01 0 364;HS3N -3 359;HS10N -10 333;HS15N -15 341;HS18N -18 290;HS23N -23 261;HS26N -26 264;HS30N -30 197;HS65N -65 171.76;HS22 22 190;HS25 25 190;HS29 29 214;HS36 36 163;HS58 58 276;HS89 89 191;OM03 3 228;OM05-P 5 215;OM08 8 154;OM18 18 201;OM18-P 19 207;OM21 21 174;OM29 29 194;OM30 30 230;OM32 32 187;OM35 35 202;OM37 37 218;OM39 39 228;OM42 42 199;OM46 46 182;OM48 48 172;OM49 49 224;OM50 50 204;OM55 55 194;OM65 65 196;FS03 3 170;FS21R 21 170;FS29 29 160;FS30 30 171;FS42 42 182;FS65 65 188"
for it in pl.split(";"):
    n,tm,l=it.split(); sub={"HS":"Hydrated salt","OM":"Organic","FS":"Form-stable"}[n[:2]]
    com.append(("Pluss savE "+n,sub,"Pluss Advanced Technologies (IN)",float(tm),float(l),"Pluss","",{}))
for t,l in [("-25",200),("-22",200),("-18",200),("-15",200),("4",210),("6",210),("18",210),("18/23",210),("20",210),("23",210),("25",210)]:
    com.append((f"BioPCM {t} °C","Bio-based (gel/liquid/solid)","Phase Change Solutions (US)",float(t.split('/')[0]),l,"BioPCM","Listed as 'energy density' (J/g)"+("; dual-temperature product 18/23 °C" if "/" in t else ""),{}))
for t,l,cpl,cps,rs,rl,kl,ks in [(-70,193,2.9,3.1,1.7,1.6,0.5,2.1),(-21,285,3.05,3.29,1.24,1.21,.51,.56),(-16,300,3.9,4.1,1.07,1.06,.54,.57),(-12,310,3.6,3.9,1.12,1.09,.58,.61),(48,240,2.9,2.1,1.45,1.33,.51,.62),(53,285,2.9,2.1,1.48,1.4,.51,.62),(58,280,2.9,2.1,1.48,1.4,.51,.62)]:
    com.append((f"Insolcorp DuraTemp {t}C","Inorganic","Insolcorp (US)",t,l,"DuraTemp","Datasheet prints no units; kJ/kg, kJ/kg·K, g/ml, W/m·K assumed; >3000 cycles claimed",
        dict(cpl=cpl,cps=cps,rs=rs*1000,rl=rl*1000,kl=kl,ks=ks)))
com.append(("Sasol PARAFOL 18 PF","Paraffin (n-octadecane >97%)","Sasol (ZA/DE)",27,220,"PCMRAL2026","Melting enthalpy '>220 J/g'; RAL certified",{}))
SRC2 = {
 "Muller2020":("Müller L. et al., Consistent DSC and TGA methodology as basis for the measurement and comparison of thermo-physical properties of PCMs, Materials 13 (2020) 4486","https://doi.org/10.3390/ma13204486"),
 "Mao2025":("Mao S. et al., Thermal energy storage performance, application and challenge of phase change materials: a review, Energy Storage and Saving 4 (2025) 300-322","https://doi.org/10.1016/j.enss.2025.03.001"),
 "Croda":("Croda Industrial Specialties, CrodaTherm PCM wax and microencapsulated PCM tables, accessed 2026-10-29","https://www.crodaindustrialspecialties.com/en-gb/functions/phase-change-materials"),
 "Axiotherm":("Axiotherm GmbH, Axiotherm PCM product table, accessed 2026-10-29","https://www.axiotherm.de/en/produkte/axiotherm-pcm/"),
 "Pluss":("Pluss Advanced Technologies, savE PCM data sheets, accessed 2026-10-29","https://www.pluss.co.in/knowledge-center/data-sheets/"),
 "BioPCM":("Phase Change Solutions, BioPCM products, accessed 2026-10-29","https://phasechange.com/products-biopcm/"),
 "DuraTemp":("Insolcorp, DuraTemp PCM catalogue and datasheets, accessed 2026-10-29","https://insolcorp.com/catalog/"),
 "PCMRAL2026":("RAL Quality Association PCM, Phase Change Matters newsletter, March 2026","https://www.pcm-ral.de/phase-change-matters-newsletter-march-2026/"),
}
