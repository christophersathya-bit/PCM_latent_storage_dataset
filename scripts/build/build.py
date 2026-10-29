import re
import csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.chart import ScatterChart, Reference, Series
from data_lit import lit
from data_extra import lit2, com, SRC2
from data_v13 import lit3, enrich, SRC3
import data_v14 as V

SRC = {
 "Zalba2003": ("Zalba B. et al., Review on thermal energy storage with phase change: materials, heat transfer analysis and applications, Applied Thermal Engineering 23 (2003) 251-283","https://doi.org/10.1016/S1359-4311(02)00192-8"),
 "Sharma2009": ("Sharma A. et al., Review on thermal energy storage with phase change materials and applications, Renewable & Sustainable Energy Reviews 13 (2009) 318-345","https://doi.org/10.1016/j.rser.2007.10.005"),
 "Kenisarin2010": ("Kenisarin M.M., High-temperature phase change materials for thermal energy storage, Renewable & Sustainable Energy Reviews 14 (2010) 955-970","https://doi.org/10.1016/j.rser.2009.11.011"),
 "Abhat1983": ("Abhat A., Low temperature latent heat thermal energy storage: heat storage materials, Solar Energy 30 (1983) 313-332","https://doi.org/10.1016/0038-092X(83)90186-X"),
 "NIST_dHfus": ("Handbook thermodynamic data (NIST Chemistry WebBook / CRC Handbook); latent heat = molar enthalpy of fusion / molar mass","https://webbook.nist.gov/chemistry/"),
 "Fatahi2024": ("Fatahi H. et al., Thermal conductivity improvement of adipic acid by the addition of AlO(OH) and AlO(OH)@SiO2 core-shell nanoparticles, Int. J. Thermofluids 22 (2024) 100617","https://doi.org/10.1016/j.ijft.2024.100617"),
 "Fu2025": ("Fu K. et al., Enhancement of thermal characteristics of a novel stearic acid-adipic acid eutectic PCM integrated with expanded graphite, J. Energy Storage 121 (2025) 116536","https://doi.org/10.1016/j.est.2025.116536"),
 "Snekha2024": ("Snekha N.R. et al., ZnO-adipic acid composites as phase change material for latent heat thermal energy storage systems, Micro and Nano Systems Letters 12 (2024) 24","https://doi.org/10.1186/s40486-024-00212-2"),
 "Rubitherm": ("Rubitherm GmbH, RT product listing (melting area, heat storage capacity), accessed 2026-10-29","https://www.rubitherm.eu/en/index.php/productcategory/organische-pcm-rt"),
 "PureTemp": ("PureTemp LLC, technical data sheets, accessed 2026-10-29","https://puretemp.com/home/data-sheets/"),
 "PlusICE": ("PCM Products Ltd, PlusICE Range 2021 catalogue, accessed 2026-10-29","http://www.pcmproducts.net/files/PlusICE%20Range%202021-1.pdf"),
}

SRC.update(SRC2); SRC.update(SRC3)
COLS = ["ID","Name","Category","Subclass","Supplier","Composition / formula","Transition","Tm (°C)","Latent heat (kJ/kg)",
 "cp solid (kJ/kg·K)","cp liquid (kJ/kg·K)","cp unspecified (kJ/kg·K)",
 "k solid (W/m·K)","k liquid (W/m·K)","k unspecified (W/m·K)",
 "ρ solid (kg/m³)","ρ liquid (kg/m³)","ρ unspecified (kg/m³)","Max operating T (°C)",
 "Volumetric latent heat (MJ/m³)","Source key","Source reference","Source URL / DOI","Data status","Notes",
 "CAS number","Crystallization / congealing T (°C)","Supercooling (K)","Cycling stability","Flash point / flammability","Hazard level (Lleida 0–3)","Degradation T (°C)","Corrosion rate (mm/yr)","Price (€/kJ, Lleida)"]

rows=[]
def add(**r): rows.append(r)

for (n,cat,sub,f,tr,tm,L,cps,cpl,ks,kl,rs,rl,src,notes) in lit:
    add(name=n,cat=cat,sub=sub,sup="",f=f,tr=tr,tm=tm,L=L,cps=cps,cpl=cpl,cpu=None,ks=ks,kl=kl,ku=None,rs=rs,rl=rl,ru=None,tmax=None,src=src,
        status="Literature/handbook value - verify against cited reference",notes=notes)

for (n,cat,sub,f,tr,tm,L,cps,cpl,ks,kl,rs,rl,src,notes,st) in lit2+lit3:
    add(name=n,cat=cat,sub=sub,sup="",f=f,tr=tr,tm=tm,L=L,cps=cps,cpl=cpl,cpu=None,ks=ks,kl=kl,ku=None,rs=rs,rl=rl,ru=None,tmax=None,src=src,
        status=st or "Literature/handbook value - verify against cited reference",notes=notes)
for (n,sub,sup,tm,L,src,notes,ex) in com:
    r=dict(name=n,cat="Commercial",sub=sub,sup=sup,f="",tr="S-L",tm=float(tm),L=float(L),cps=None,cpl=None,cpu=None,ks=None,kl=None,ku=None,rs=None,rl=None,ru=None,tmax=None,src=src,
        status=("Industry newsletter - verify with datasheet" if src=="PCMRAL2026" else "Manufacturer listing - checked 2026-10-29"),notes=notes)
    r.update(ex); add(**r)
# Rubitherm RT
rt = """RT -9 HC|-9|250;RT -4|-4|180;RT 0|0|175;RT 2 HC|2|200;RT 3 HC_1|3|190;RT 4|4|175;RT 5|5|180;RT 5 HC|5|250;RT 8|8|175;RT 8 HC|8|190;RT 9|9|175;RT 10|10|160;RT 10 HC|10|200;RT 11 HC|11|200;RT 12|12|155;RT 15|15|155;RT 18 HC|18|260;RT 21|21|155;RT 21 HC|21|190;RT 22 HC|22|190;RT 24|24|160;RT 25|25|170;RT 25 HC|25|230;RT 26|26|180;RT 28 HC|28|250;RT 31|31|165;RT 35|35|160;RT 35 HC|35|240;RT 42|42|165;RT 44 HC|44|250;RT 47|47|165;RT 50|50|160;RT 54 HC|54|200;RT 55|55|170;RT 60|60|160;RT 62 HC|62|230;RT 64 HC|64|250;RT 65|65|150;RT 69 HC|69|230;RT 70 HC|70|260;RT 80 HC|78|220;RT 82|82|170;RT 90 HC|90|170"""
for it in rt.split(";"):
    n,t,l=it.split("|")
    add(name="Rubitherm "+n,cat="Commercial",sub="Organic (paraffin-based)",sup="Rubitherm GmbH (DE)",f="Paraffin blend",tr="S-L",tm=float(t),L=float(l),
        cps=None,cpl=None,cpu=None,ks=None,kl=None,ku=None,rs=None,rl=None,ru=None,tmax=None,src="Rubitherm",
        status="Manufacturer listing - checked 2026-10-29",notes="Tm = 'melting area' from listing; heat storage capacity over manufacturer-defined range (latent+sensible)")

# PureTemp: name, tm, L, rho_l, rho_s, cp_l, cp_s, k_l, k_s
pt = [("PureTemp -37",-37,145,0.88,0.97,1.99,1.39,0.15,0.25),("PureTemp -21",-21,239,1.17,1.09,3.43,1.83,0.55,2.39),
("PureTemp -15",-15,301,1.04,0.98,3.5,1.84,0.55,2.34),("PureTemp 4",5,187,0.88,0.96,2.26,1.78,0.15,0.25),
("PureTemp 8",8,178,0.86,0.95,2.15,1.85,0.14,0.22),("PureTemp 15",15,182,0.86,0.95,2.56,2.25,0.15,0.25),
("PureTemp 17",17,217,None,None,2.20,1.88,0.14,0.32),("PureTemp 18",18,192,0.86,0.95,1.74,1.47,0.15,0.25),
("PureTemp 20",20,171,0.86,0.95,2.15,2.07,0.14,0.23),("PureTemp 23",23,227,0.83,0.91,1.99,1.84,0.15,0.25),
("PureTemp 25",25,187,0.86,0.95,2.29,1.99,0.15,0.25),("PureTemp 27",27,202,0.86,0.95,2.63,2.46,0.15,0.25),
("PureTemp 29",29,202,0.85,0.94,1.94,1.77,0.15,0.25),("PureTemp 37",37,210,0.84,0.92,2.63,2.21,0.15,0.25),
("PureTemp 48",49,230,0.82,0.90,2.27,2.10,0.15,0.25),("PureTemp 58",58,225,0.81,0.89,2.71,2.47,0.15,0.25),
("PureTemp 60",57,200,0.87,0.96,2.38,2.04,0.15,0.25),("PureTemp 63",63,206,0.84,0.92,2.16,1.99,0.15,0.25),
("PureTemp 68",68,213,0.87,0.96,1.91,1.85,0.15,0.25),("PureTemp 108",108,180,0.80,0.87,None,None,0.15,0.25),
("PureTemp 151",151,217,1.36,1.49,2.17,2.06,0.15,0.25)]
for n,tm,L,rl,rs,cpl,cps,kl,ks in pt:
    sub = "Salt-water / inorganic" if tm in (-21,-15) else "Bio-based organic"
    note=""
    if n=="PureTemp 17": note="Data sheet gives density ~0.77 g/ml at 25 °C (phase not stated)"
    if n=="PureTemp 60": note="Data sheet: 57 °C / 200 J/g; listing page shows 61 °C / 220 J/g"
    if tm in (-21,-15): note=(note+"; " if note else "")+"Subclass inferred from high cp/k (water-based)"
    ru = 770 if n=="PureTemp 17" else None
    add(name=n,cat="Commercial",sub=sub,sup="PureTemp LLC (US)",f="",tr="S-L",tm=tm,L=L,cps=cps,cpl=cpl,cpu=None,ks=ks,kl=kl,ku=None,
        rs=rs*1000 if rs else None,rl=rl*1000 if rl else None,ru=ru,tmax=None,src="PureTemp",status="Manufacturer data sheet - checked 2026-10-29",notes=note)

# PlusICE: series -> rows of name,tm,rho,L,vol,cp,k,tmax
plus = {
"S":("Salt hydrate","""S8 8 1475 130 1.9 0.44 60;S10 10 1470 170 1.9 0.43 60;S13 13 1515 150 1.9 0.43 60;S15 15 1510 180 1.9 0.43 60;S17 17 1525 155 1.9 0.43 60;S18 18 1520 145 1.9 0.43 60;S19 19 1520 175 1.9 0.43 60;S20 20 1530 195 2.2 0.54 60;S21 21 1530 220 2.2 0.54 60;S22 22 1530 215 2.2 0.54 60;S23 23 1530 200 2.2 0.54 60;S24 24 1530 180 2.2 0.54 60;S25 25 1530 175 2.2 0.54 60;S27 27 1530 185 2.2 0.54 60;S32 32 1460 220 1.9 0.51 60;S34 34 2100 140 2.1 0.52 70;S46 46 1610 110 2.2 0.60 120;S47 47 1610 110 2.25 0.60 120;S48 48 1565 110 2.35 0.61 120;S49 49 1560 110 2.38 0.61 120;S50 50 1545 110 2.41 0.62 120;S51 51 1515 110 2.45 0.63 120;S52 52 1512 115 2.45 0.63 120;S53 53 1510 115 2.5 0.65 120;S54 54 1510 120 2.5 0.65 120;S55 55 1508 120 2.5 0.65 120;S56 56 1505 130 2.5 0.67 120;S57 57 1505 135 2.5 0.67 120;S58 58 1505 145 2.55 0.69 120;S70 70 1680 100 2.1 0.57 120;S72 72 1666 155 2.13 0.58 120;S83 83 1600 100 2.31 0.62 120;S89 89 1550 145 2.48 0.67 120;S117 117 1450 125 2.61 0.70 140"""),
"A":("Organic","""A2 2 765 230 2.2 0.21 150;A3 3 765 230 2.2 0.21 150;A4 4 766 235 2.18 0.21 150;A5 5 768 170 2.18 0.22 150;A6 6 768 185 2.17 0.21 150;A6.5 6.5 770 190 2.18 0.22 150;A7 7 770 190 2.18 0.22 150;A8 8 770 180 2.16 0.21 150;A9 9 770 190 2.16 0.21 150;A10 10 770 210 2.16 0.22 150;A11 11 775 210 2.16 0.22 150;A12 12 775 215 2.16 0.22 150;A13 13 775 225 2.16 0.22 150;A14 14 775 200 2.16 0.22 150;A15 15 780 205 2.16 0.18 150;A16 16 780 225 2.16 0.18 150;A17 17 780 235 2.18 0.18 200;A18 18 765 155 2.18 0.22 200;A19 19 765 150 2.18 0.22 200;A20 20 770 160 2.2 0.22 200;A21 21 770 160 2.2 0.22 200;A22 22 785 160 2.2 0.18 200;A23 23 785 155 2.2 0.18 200;A24 24 790 155 2.22 0.18 200;A25 25 785 220 2.22 0.18 200;A26 26 790 230 2.22 0.21 200;A27 27 768 250 2.22 0.22 200;A28 28 789 265 2.22 0.21 200;A29 29 785 230 2.22 0.21 200;A30 30 790 230 2.22 0.21 200;A31 31 790 230 2.22 0.21 200;A32 32 845 120 2.2 0.21 250;A33 33 790 230 2.22 0.21 200;A34 34 790 230 2.22 0.21 200;A36 36 776 250 2.3 0.22 250;A39 39 900 135 2.22 0.22 250;A42 42 905 140 2.22 0.21 250;A43 43 780 280 2.37 0.18 250;A46 46 910 155 2.22 0.22 250;A48 48 810 230 2.85 0.18 250;A53 53 910 155 2.22 0.22 250;A58 58 820 240 2.85 0.18 200;A62 62 910 205 2.2 0.22 250;A70 70 890 225 2.2 0.23 250;A73 73 890 225 2.2 0.23 250;A78 78 890 225 2.2 0.23 250;A82 82 930 240 2.2 0.23 250;A95 95 900 260 2.2 0.22 300;A118 118 900 195 2.2 0.22 250;A133 133 880 200 2.2 0.23 250;A144 144 880 115 2.2 0.23 250;A155 155 880 102 2.2 0.23 250;A164 164 1500 305 2.42 nd 200"""),
"E":("Eutectic (water-salt, sub-zero)","""E0 0 1000 395 4.19 0.58 100;E-2 -2 1070 325 3.8 0.58 100;E-3 -4 1060 330 3.84 0.60 100;E-6 -6 1110 300 3.83 0.56 100;E-11 -12 1090 310 3.55 0.57 100;E-15 -15 1060 320 3.87 0.53 100;E-19 -19 1125 300 3.29 0.58 100;E-21 -21 1240 285 3.13 0.51 100;E-22 -22 1180 305 3.34 0.57 100;E-26 -26 1250 265 3.67 0.58 100;E-29 -29 1420 250 3.69 0.64 100;E-32 -32 1290 225 2.95 0.56 100;E-34 -34 1205 200 3.05 0.54 100;E-37 -37 1500 225 3.15 0.54 100;E-48 -48 1510 202 3.28 0.56 100;E-49 -49 1510 202 3.28 0.56 100;E-50 -50 1325 175 3.28 0.56 100;E-51 -51 1500 206 3.15 0.54 100;E-52 -52 1480 211 3.15 0.54 100;E-53 -53 1460 215 3.15 0.54 100;E-54 -54 1440 219 3.15 0.54 100;E-55 -55 1420 223 3.15 0.54 100;E-56 -56 1400 228 3.15 0.54 100;E-57 -57 1380 230 3.15 0.54 100;E-58 -58 1350 200 3.15 0.54 100;E-59 -59 1320 206 3.15 0.54 100;E-60 -60 1290 212 3.15 0.54 100;E-61 -61 1260 218 3.15 0.54 100;E-62 -62 1230 224 3.15 0.54 100;E-63 -63 1200 230 3.15 0.54 100;E-65 -65 1180 240 3.15 0.56 100;E-67 -67 1380 200 3.15 0.54 100;E-68 -68 1360 205 3.15 0.54 100;E-69 -69 1350 202 3.15 0.54 100;E-70 -70 1350 200 3.15 0.54 100;E-71 -71 1333 208 3.15 0.54 100;E-72 -72 1315 215 3.15 0.54 100;E-73 -73 1298 223 3.15 0.54 100;E-74 -74 1280 230 3.15 0.54 100"""),
"X":("Solid-solid","""X25 25 1055 110 1.63 0.36 125;X30 30 1050 115 1.65 0.36 125;X40 40 1046 150 1.67 0.36 125;X55 55 1060 115 1.62 0.36 125;X70 70 1085 160 1.57 0.36 180;X80 80 1193 160 1.52 0.36 190;X90 90 1200 170 1.51 0.36 190;X95 95 1215 140 1.51 0.36 190;X120 120 1245 185 1.50 0.36 160;X130 130 1280 315 1.47 0.36 160;X165 165 1304 225 1.43 0.36 200;X180 180 1330 275 1.40 0.36 200"""),
"H":("High-temperature salt/alloy","""H105 104 1700 125 1.5 0.50 390;H115 114 2200 100 1.51 0.50 390;H120 120 2220 120 1.51 0.51 390;H160 162 1910 105 1.51 0.51 200;H190 191 2300 170 1.51 0.51 500;H220 220 2000 100 1.52 0.52 390;H230 227 1553 105 1.52 0.52 300;H250 250 2380 280 1.53 0.52 600;H255 254 2380 270 1.53 0.52 600;H280 282 2250 160 1.54 0.53 500;H285 285 2200 85 1.54 0.53 390;H290 292 2200 150 1.55 0.53 500;H300 302 1900 130 1.55 0.54 500;H305 305 1570 150 1.56 0.54 350;H320 320 2100 70 1.5 0.55 390;H325 327 2110 80 1.51 0.55 390;H335 334 2110 80 1.51 0.55 390;H355 353 2060 230 1.52 0.56 1300;H380 382 2050 225 1.53 0.56 1300;H395 395 2330 215 1.53 0.56 800;H425 425 2100 220 1.54 0.57 1400;H430 430 2160 125 1.54 0.57 1400;H485 483 2220 200 1.55 0.57 800;H500 500 2220 300 1.55 0.57 800;H500A 500 2140 140 1.56 0.57 1400;H525 525 2350 155 1.56 0.57 1000;H535 535 2320 130 1.57 0.56 1000;H610 610 2070 410 1.57 0.56 1300;H640 640 2380 338 1.58 0.56 800;H650 652 2450 300 1.58 0.56 800;H690 687 2400 250 1.59 0.56 800;H695 695 2460 280 1.59 0.56 800;H700 699 2410 250 1.60 0.57 800;H705 705 2430 250 1.60 0.57 800;H705A 705 2040 452 1.60 0.57 1400;H725 725 2210 602 1.59 0.58 1300;H755 755 2160 466 1.59 0.58 800;H845 845 2530 276 1.58 0.59 900;H885 885 2290 236 1.58 0.59 900"""),
}
for ser,(sub,txt) in plus.items():
    for it in txt.split(";"):
        n,tm,rho,L,cp,k,tmax=it.split()
        add(name="PlusICE "+n,cat="Commercial",sub=sub,sup="PCM Products Ltd (UK)",f="",tr="S-S" if ser=="X" else "S-L",
            tm=float(tm),L=float(L),cps=None,cpl=None,cpu=float(cp),ks=None,kl=None,ku=None if k=="nd" else float(k),
            rs=None,rl=None,ru=float(rho),tmax=float(tmax),src="PlusICE",status="Manufacturer catalogue - checked 2026-10-29",
            notes="Phase of cp/k/density not stated in catalogue")

for r in rows:
    if r["name"] in enrich:
        e=dict(enrich[r["name"]]); x=e.pop("extra"); r.update(e); r["notes"]=(r["notes"]+"; " if r["notes"] else "")+x
NEWK=["cas","cryst","supc","cyc","flash","haz","degr","corr","price"]
for (n,sub,sup,tm,L,src,notes,st,ex) in V.NEW_COM:
    r=dict(name=n,cat="Commercial",sub=sub,sup=sup,f="",tr="S-L",tm=tm,L=L,cps=None,cpl=None,cpu=None,ks=None,kl=None,ku=None,rs=None,rl=None,ru=None,tmax=None,src=src,status=st,notes=notes); r.update(ex); rows.append(r)
have={r["name"] for r in rows}
for code in ("HS48","HS78"):
    if "Pluss savE "+code not in have:
        rows.append(dict(name="Pluss savE "+code,cat="Commercial",sub="Hydrated salt",sup="Pluss Advanced Technologies (IN)",f="",tr="S-L",tm=0,L=0,cps=None,cpl=None,cpu=None,ks=None,kl=None,ku=None,rs=None,rl=None,ru=None,tmax=None,src="Pluss",status="",notes="Datasheet only (not in web table)"))
def app(r,t): r["notes"]=(r["notes"]+"; " if r.get("notes") else "")+t
for r in rows:
    for k in NEWK: r.setdefault(k,None)
    n=r["name"]
    if n in V.CAS: r["cas"]=V.CAS[n]
    if n in V.SUPERCOOL: r["supc"]=V.SUPERCOOL[n]
    if n in V.CYCLING: r["cyc"]=V.CYCLING[n]
    if n in V.MU_EXTRA: app(r,V.MU_EXTRA[n])
    if n in V.MU:
        on,pk,L,cr,mx=V.MU[n]; r["tm"]=on; r["L"]=L; r["cryst"]=V.mid(cr); r["tmax"]=mx
        r["status"]="DSC-measured (Müller 2020) - verified vs paper Table 5 on 2026-10-30"
        r["notes"]=f"Melting onset {on} °C, peak {pk} °C; crystallization onset {cr} °C"+(f"; max operating T {mx} °C (TGA)" if mx else "")
    m=re.search(r"Crystallisation (-?[\d.]+) °C",r.get("notes") or "")
    if m and r["src"]=="Croda": r["cryst"]=float(m.group(1))
    if r["src"].startswith("Lleida"):
        nt=r["notes"] or ""
        for key,pat in (("degr",r"[Dd]egradation (?:temperature )?([\d.]+)"),("haz",r"[Hh]azard (?:level )?(\d)"),("price",r"([\d.]+) €/kJ"),("corr",r"Corrosion ([\d.]+) mm/yr")):
            mm=re.search(pat,nt)
            if mm: r[key]=float(mm.group(1))
        mo=re.search(r"Max operating ([\d.]+)",nt)
        if mo: r["tmax"]=float(mo.group(1))
    if r["src"]=="Axiotherm":
        code=n.replace("Axiotherm ","")
        if code in V.AX:
            mr,cg,L,cp,rho,k,tmax,fl=V.AX[code]
            if L!=r["L"]: app(r,f"web table lists {r['L']:g} kJ/kg; datasheet value used")
            r.update(L=float(L),cpu=cp,rl=rho,ku=k,tmax=tmax,flash=fl,cryst=V.mid(cg))
            app(r,f"Melting range {mr} °C"+(f"; congealing {cg} °C" if cg else "")+"; datasheet v. 31.01.2018"+("; corrosive to metals" if code.startswith("ATS") else ""))
            if code=="ATP 20": app(r,"cp printed as 2-3 kJ/kg·K")
            r["status"]="Manufacturer datasheet - checked 2026-10-30"
    if r["src"]=="Pluss":
        code=n.replace("Pluss savE ","")
        if code in V.PL:
            Tm,Tf,Lm,Lf,rs,rl,cps,cpl,ks,kl,tmax,fl=V.PL[code]
            if r["tm"] and (Tm!=r["tm"] or Lm!=r["L"]): app(r,f"web table: {r['tm']:g} °C / {r['L']:g} kJ/kg")
            lab="liquid/solid-labelled latent heat" if code in V.PL_LABEL_LS else "melting/freezing latent heat"
            r.update(tm=float(Tm),L=float(Lm),cryst=float(Tf),rs=rs,rl=rl,cps=cps,cpl=cpl,ks=ks,kl=kl,tmax=tmax,flash=fl)
            app(r,f"Freezing {Tf} °C"+(f" / {Lf} kJ/kg" if Lf else "")+f" ({lab}, as printed)")
            if code=="OM39": app(r,"Datasheet marked PROVISIONAL")
            if code=="HS65N": app(r,"Datasheet gives liquid-phase values only")
            r["status"]="Manufacturer datasheet - checked 2026-10-30"
            r["sub"]={"HS":"Hydrated salt (inorganic)","OM":"Organic","FS":"Form-stable (liquid PCM in polymer matrix)"}[code[:2]]
    if r["src"]=="DuraTemp" and not r["flash"]: r["flash"]="Non-flammable (datasheet)"
    if r["src"]=="Lleida_HT2024" or r["src"]=="Lleida_Ind2024" or r["src"]=="Lleida_HTexp2025": pass
# sort: category order then Tm
order={"Organic":0,"Inorganic":1,"Metallic":2,"Eutectic":3,"Composite":4,"Commercial":5}
rows.sort(key=lambda r:(order[r["cat"]],r["sup"],r["tm"]))
for i,r in enumerate(rows,1): r["id"]=f"PCM-{i:04d}"

def vol(r):
    rho = r["rs"] or r["ru"] or r["rl"]
    return round(r["L"]*rho/1000,1) if rho else None

keys=["id","name","cat","sub","sup","f","tr","tm","L","cps","cpl","cpu","ks","kl","ku","rs","rl","ru","tmax"]
NEWK=["cas","cryst","supc","cyc","flash","haz","degr","corr","price"]
# CSV
with open("data/pcm_dataset_v1_4.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh); w.writerow(COLS)
    for r in rows:
        w.writerow([("" if r[k] is None else r[k]) for k in keys]+[("" if vol(r) is None else vol(r)),r["src"],SRC[r["src"]][0],SRC[r["src"]][1],r["status"],r["notes"]]+[("" if r[k] is None else r[k]) for k in NEWK])

# XLSX
wb=Workbook(); ws=wb.active; ws.title="PCM_Data"
F="Arial"; hdr=PatternFill("solid",fgColor="1F4E78")
ws.append(COLS)
for c in ws[1]:
    c.font=Font(name=F,bold=True,color="FFFFFF"); c.fill=hdr; c.alignment=Alignment(wrap_text=True,vertical="center")
fills={"Organic":"E2EFDA","Inorganic":"DDEBF7","Metallic":"EDEDED","Eutectic":"FFF2CC","Composite":"E4DFEC","Commercial":"FCE4D6"}
for i,r in enumerate(rows,2):
    vals=[r[k] for k in keys]
    ws.append(vals+[None,r["src"],SRC[r["src"]][0],SRC[r["src"]][1],r["status"],r["notes"]]+[r[k] for k in NEWK])
    ws.cell(i,20).value=f'=IF(ISNUMBER(I{i}),IF(ISNUMBER(P{i}),I{i}*P{i}/1000,IF(ISNUMBER(R{i}),I{i}*R{i}/1000,IF(ISNUMBER(Q{i}),I{i}*Q{i}/1000,""))),"")'
    for c in ws[i]: c.font=Font(name=F,size=10)
    ws.cell(i,3).fill=PatternFill("solid",fgColor=fills[r["cat"]])
    ws.cell(i,20).number_format="0.0"
    ws.cell(i,23).hyperlink=SRC[r["src"]][1]; ws.cell(i,23).font=Font(name=F,size=10,color="0563C1",underline="single")
widths=[10,38,12,26,22,24,9,9,10,9,9,9,9,9,9,9,9,9,10,12,13,50,40,34,50,13,13,14,28,18,11,11,11,11]
for j,wd in enumerate(widths,1): ws.column_dimensions[get_column_letter(j)].width=wd
ws.row_dimensions[1].height=45
ws.freeze_panes="C2"; ws.auto_filter.ref=f"A1:{get_column_letter(len(COLS))}{len(rows)+1}"
n=len(rows)+1

# Summary sheet
sm=wb.create_sheet("Summary")
sm["A1"]="PCM dataset v1 — summary"; sm["A1"].font=Font(name=F,bold=True,size=14)
sm.append([]); sm.append(["Category","Entries","Min Tm (°C)","Max Tm (°C)","Mean latent heat (kJ/kg)"])
for c in sm[3]: c.font=Font(name=F,bold=True,color="FFFFFF"); c.fill=hdr
for j,cat in enumerate(order,4):
    sm.cell(j,1,cat)
    sm.cell(j,2,f'=COUNTIF(PCM_Data!$C$2:$C${n},A{j})')
    sm.cell(j,3,f'=_xlfn.MINIFS(PCM_Data!$H$2:$H${n},PCM_Data!$C$2:$C${n},A{j})')
    sm.cell(j,4,f'=_xlfn.MAXIFS(PCM_Data!$H$2:$H${n},PCM_Data!$C$2:$C${n},A{j})')
    sm.cell(j,5,f'=AVERAGEIF(PCM_Data!$C$2:$C${n},A{j},PCM_Data!$I$2:$I${n})'); sm.cell(j,5).number_format="0.0"
T=4+len(order); sm.cell(T,1,"Total"); sm.cell(T,2,f"=SUM(B4:B{T-1})")
for row in sm.iter_rows(min_row=4,max_row=T):
    for c in row: c.font=Font(name=F,bold=(c.row==T))
for col,wd in zip("ABCDE",[16,10,13,13,24]): sm.column_dimensions[col].width=wd
ch=ScatterChart(); ch.title="Latent heat vs melting temperature"; ch.style=13
ch.x_axis.title="Tm (°C)"; ch.y_axis.title="Latent heat (kJ/kg)"; ch.height=10; ch.width=20
s=Series(Reference(ws,min_col=9,min_row=2,max_row=n),Reference(ws,min_col=8,min_row=2,max_row=n),title="All PCMs")
s.marker.symbol="circle"; s.marker.size=4; s.graphicalProperties.line.noFill=True
ch.series.append(s); ch.legend=None; ch.x_axis.delete=False; ch.y_axis.delete=False
sm.add_chart(ch,"G3")

# Sources
so=wb.create_sheet("Sources"); so.append(["Key","Reference","URL / DOI","Entries"])
for c in so[1]: c.font=Font(name=F,bold=True,color="FFFFFF"); c.fill=hdr
for i,(k,(ref,url)) in enumerate(SRC.items(),2):
    so.append([k,ref,url,f'=COUNTIF(PCM_Data!$U$2:$U${n},A{i})'])
    for c in so[i]: c.font=Font(name=F,size=10)
    so.cell(i,3).hyperlink=url
so.column_dimensions["A"].width=15; so.column_dimensions["B"].width=95; so.column_dimensions["C"].width=55

# README
rd=wb.create_sheet("README",0)
lines=[("PCM Latent Heat Storage Dataset — v1.4 (2026-10-30)",True),
("",False),
("Contents",True),
("PCM_Data: one row per material/product. Filter with the header arrows; freeze panes keep Name visible.",False),
("Summary: counts, temperature span and mean latent heat by category, plus a latent-heat vs Tm chart.",False),
("ML_Data / ML_Guide: machine-learning-ready table (one-hot categories, best-available cp/k/ρ with phase flags, formula descriptors, group_id for leakage-free splits, sample_weight from data quality); also exported as pcm_ml_ready_v1_4.csv.",False),
("Charts: 5 research charts (latent heat vs Tm, zoomed −80–150 °C view, conductivity vs Tm (log), volumetric vs gravimetric latent heat, PCM count per temperature band). Chart_Data holds the live formula links.",False),
("Sources: full references and links; every row carries a Source key.",False),
("",False),
("Column notes",True),
("Tm: melting / phase-change temperature (peak or nominal value as reported).",False),
("Latent heat: as reported. Rubitherm values are 'heat storage capacity' over a manufacturer-defined range (latent + some sensible).",False),
("cp / k / ρ 'unspecified': supplier gives one value without stating solid or liquid phase (PlusICE).",False),
("Volumetric latent heat: formula = latent heat × density / 1000, using ρ solid, else unspecified, else liquid.",False),
("Transition: S-L = solid–liquid, S-S = solid–solid.",False),
("Data status: 'checked 2026-10-29' = values taken from supplier pages on that date; 'Literature/handbook value' = compiled from the cited review; verify against the original before publishing.",False),
("",False),
("v1.4 changes: +9 columns (CAS, crystallization T, supercooling, cycling, flash point, hazard, degradation T, corrosion, price); Axiotherm (32) and Pluss (41) datasheet cp/k/ρ/max T; Pluss HS48 & HS78 added; Müller 2020 rows verified vs paper; CAS for 119 pure compounds (PubChem, checked); CrodaTherm 17 and Cowa SAT added.",False),
("v1.3 changes: +Lleida/CORA open datasets (3 datasets, 46 rows; 3 Rubitherm rows enriched), +Xie 2017 salt hydrates & eutectics, +Hirschey 2018 (ORNL) salt hydrates, +Jebasingh 2016 fatty-acid ternaries & composites.",False),
("v1.2 changes: +Croda (17), Axiotherm (32), Pluss savE (40), BioPCM (11), Insolcorp DuraTemp (7), Sasol (1); +38 literature entries (Müller 2020 DSC set, Mao 2025 review, alkali metals, metal & salt eutectics).",False),
("v1.1 changes: added adipic acid (pure) and stearic acid–adipic acid eutectic/EG composite; new Composite category.",False),
("",False),
("Known gaps / next steps",True),
("Rubitherm SP (salt) series and RT datasheets (cp, k, ρ) – site was down on 2026-10-30; retry later.",False),
("Not yet added (no public numeric data): Microtek MPCM/nextek grades (on request), Climator ClimSel (only range -21 to +70 °C published), Rubitherm SP series.",False),
("Recent papers without full values: Ren 2025 multi-component nitrate/chloride salt (Tm 202.9 °C, latent heat not public); 2026 graphene oxide-molten salt and cold-sintered sodium salt composites (pages not accessible).",False),
("Composites / shape-stabilised PCMs and more eutectics from recent literature.",False),
("Literature cp, k and ρ are sparse; fill from original papers or own DSC/LFA measurements.",False),
("Add columns as needed: supercooling (K), cycling stability, cost, toxicity, CAS number.",False),
]
for i,(t,b) in enumerate(lines,1):
    rd.cell(i,1,t).font=Font(name=F,bold=b,size=14 if i==1 else 10)
rd.column_dimensions["A"].width=140
from charts import build_charts
build_charts(wb, rows, F)
from ml import build_ml, build_results
build_ml(wb, rows, F, "data/pcm_ml_ready_v1_4.csv")
build_results(wb, F)
wb.save("data/pcm_dataset_v1_4.xlsx")
print(len(rows))
