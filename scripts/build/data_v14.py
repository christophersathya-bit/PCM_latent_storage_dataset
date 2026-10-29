import json, re
CAS=json.load(open('scripts/build/cas_raw.json'))
# Axiotherm datasheets: name -> (melt range, congeal range, L, cp, rho_l kg/m3, k, tmax, flash)
AX = {"ATS -63":("-65 to -61","",190,3,1350,0.6,50,"Non-flammable"),"ATS -50":("-51 to -49","",220,3,1240,0.6,50,"Non-flammable"),
"ATS -40":("-40 to -36","-42 to -39",180,3,1450,0.6,40,"Non-flammable"),"ATS -34":("-34 to -32","-42 to -37",240,3,1180,0.6,40,"Non-flammable"),
"ATS -24":("-24 to -21","-27 to -24",340,3,1120,0.6,60,"Non-flammable"),"ATS -21":("-21 to -18","-28 to -22",320,3,1160,0.6,60,"Non-flammable"),
"ATS -12":("-14 to -11","-17 to -11",360,3,1100,0.6,40,"Non-flammable"),"ATS -10":("-11 to -8","-13 to -11",345,3,1160,0.6,40,"Non-flammable"),
"ATS -6":("-6 to -5","-8 to -7",362,3,1100,0.6,40,"Non-flammable"),"ATS -3":("-4 to -2","-5 to -3",330,3,1100,0.6,40,"Non-flammable"),
"ATP 2":("2 to 4","1 to 2",215,2,760,0.2,50,">120"),"ATP 4":("3 to 6","1 to 4",260,2,750,0.2,50,">150"),"ATP 6":("4 to 6","4 to 6",275,2,740,0.2,50,">150"),
"ATP 12":("12 to 14","10 to 12",215,2,800,0.2,100,">180"),"ATP 16":("12 to 16","12 to 16",245,2,770,0.2,50,">180"),"ATP 18":("17 to 18","17 to 18",270,2,760,0.2,50,">180"),
"ATP 20":("20","20",220,None,840,0.2,70,">150"),"ATP 23":("21 to 24","19 to 21",230,2,800,0.2,100,">180"),"ATP 28":("27 to 29","26 to 28",265,2,760,0.2,70,">180"),
"ATS 30":("28 to 33","27 to 30",220,2,1300,0.6,50,"Non-flammable"),"ATP 36":("35 to 37","35 to 36",240,2,800,0.2,100,">180"),"ATP 43":("41 to 43","39 to 43",265,2,760,0.2,80,">180"),
"ATS 44":("45 to 48","41 to 44",230,3,1400,0.6,70,"Non-flammable"),"ATS 50":("49 to 50","43 to 47",228,3,1300,0.6,70,"Non-flammable"),"ATP 52":("50 to 53","50 to 53",230,2,800,0.2,100,">180"),
"ATS 58":("56 to 58","54 to 57",240,3,1280,0.6,80,"Non-flammable"),"ATP 60":("57 to 60","57 to 60",230,2,800,0.2,120,">200"),"ATP 70":("66 to 71","66 to 71",240,2,800,0.2,120,">200"),
"ATP 78":("75 to 79","75 to 78",225,2,800,0.2,100,">180"),"ATS 84":("81 to 85","81 to 83",143,2,1650,0.6,99,"Non-flammable"),"ATS 89":("88 to 91","86 to 90",145,2,1580,0.6,99,"Non-flammable"),
"ATS 115":("115 to 118","113 to 116",158,2,1500,0.6,150,"Non-flammable")}
# Pluss datasheets: code -> (Tm, Tf, Lmelt, Lfreeze, rs, rl, cps, cpl, ks, kl, tmax, flash)
PL = {"HS01":(0,0,359,364,924,1010,2.0,3.9,2.20,0.55,90,None),"HS3N":(-2,-3,359,329,985,1060,1.80,3.98,2.2,0.35,80,None),
"HS10N":(-10,-11,330,333,1057,1125,1.9,3.40,4.25,0.60,90,None),"HS15N":(-16,-17,327,341,1016,1070,1.87,3.40,5.26,0.53,90,None),
"HS18N":(-18,-18,260,290,1083,1095,3.90,3.48,None,0.44,90,None),"HS23N":(-22,-23,274,261,1078,1155,1.58,3.40,4.976,0.702,90,None),
"HS26N":(-26,-26,264,182,1122,1200,1.7,3.6,None,None,90,None),"HS30N":(-30,-31,197,201,1460,1425,2.1,2.7,None,None,90,None),
"HS65N":(-65,-74,172,None,None,1158,None,3.38,None,0.50,80,None),"HS22":(23,22,190,162,1651,1540,2.27,2.53,1.13,0.56,40,None),
"HS25":(25,24,190,None,1717,1557,2.07,2.42,1.05,0.55,80,None),"HS29":(29,28,214,190,1681,1530,1.51,2.62,0.478,0.382,90,None),
"HS36":(35,36,163,163,1967,1850,1.98,2.32,0.50,0.47,90,None),"HS48":(50,49,211,225,1400,1380,3.10,3.47,0.60,0.46,75,None),
"HS58":(58,56,267,276,1400,1320,2.40,3.15,0.61,0.51,75,None),"HS78":(78,77,240,242,1890,1900,1.46,1.59,0.70,0.89,90,None),
"HS89":(87,87,188,191,1630,1540,3.80,2.65,None,None,90,None),"OM03":(5,3,196,228,912,835,1.76,1.91,0.224,0.146,90,"140"),
"OM05-P":(6,5,220,215,810,763,2.05,1.82,0.13,0.12,80,"100"),"OM08":(7,8,154,150,1190,1020,1.71,2.11,0.235,0.118,90,"110"),
"OM18":(18,17,169,201,906,880,2.92,2.69,0.182,0.175,90,"150 (flammable)"),"OM18-P":(19,17,228,207,820,763,3.86,3.50,0.13,0.15,90,"140"),
"OM21":(22,19,174,171,931,891,2.82,2.85,0.21,0.14,90,None),"OM29":(28,25,194,188,976,870,2.32,2.71,0.293,0.172,90,"200"),
"OM30":(32,30,206,230,906,878,2.60,2.68,0.185,0.123,90,"200"),"OM32":(33,30,156,187,926,870,3.21,2.81,0.219,0.145,90,"160"),
"OM35":(35,34,171,202,900,870,2.57,2.78,0.20,0.16,90,"200"),"OM37":(38,36,186,196,973,860,2.55,2.63,0.16,0.13,90,None),
"OM39":(39,35,229,228,850,824,2.0,2.4,0.190,0.165,None,None),"OM42":(44,43,199,190,903,863,2.71,2.78,0.19,0.10,90,"200"),
"OM46":(47,45,177,182,917,880,2.5,2.7,0.2,0.1,90,None),"OM48":(51,48,165,172,960,875,2.02,2.35,0.20,0.10,90,"200"),
"OM49":(49,48,224,230,816,780,2.1,2.4,0.33,0.27,100,None),"OM50":(50,50,189,204,961,859,3.33,2.78,0.21,0.14,90,"200"),
"OM55":(55,54,188,194,935,841,2.68,2.76,0.16,0.10,90,"200"),"OM65":(67,66,188,196,924,847,3.48,3.32,0.19,0.13,90,"200"),
"FS03":(5,3,214,217,854,None,2.2,2.0,0.15,None,120,"140"),"FS29":(27,23,160,146,1040,952,2.7,2.1,0.45,None,90,"200"),
"FS30":(29,29,132,171,1058,960,2.46,2.77,0.496,0.340,90,"200"),"FS42":(44,41,136,182,997,1100,3.01,2.68,0.30,None,90,"160"),
"FS65":(66,66,159,188,842,None,2.54,2.16,0.25,None,90,"200")}
PL_LABEL_LS = {"HS23N","HS26N","HS48","HS58","HS78","OM30","OM32","OM42"}  # printed as Liquid/Solid rather than melt/freeze
# Müller 2020 Table 5 (verified verbatim 2026-10-30): name -> (onset, peak, L, cryst onset range, max op T)
MU = {"n-Decane":(-30.2,-27.8,207.32,"-40.33 to -36.97",None),"Propionic acid":(-25.7,-22.2,143.7,"-46.6 to -44.49",None),
"Hexanoic acid":(-4.7,-1.2,141.21,"-14.59 to -12.09",55.4),"1-Undecanol":(14.5,17.5,206.62,"10.35 to 11.54",82.5),
"Ethyl octadecanoate (ethyl stearate)":(32.3,34.5,188.74,"30.74 to 30.79",149.4),"Calcium bromide hexahydrate":(32.7,35.4,125.1,"23.37 to 24.46",46.1),
"Methyl octadecanoate (methyl stearate)":(37.4,40.1,229.16,"33.76 to 34.76",141),"Myristic-stearic acid (50:50 wt%)":(45.7,48.2,179.97,"43.58 to 43.96",147.5),
"1-Octadecanol":(56.8,59.1,245.93,"57.19 to 57.26",147.6),"Polyethylene glycol 10000":(59.3,62.1,179.8,"46.52 to 50.14",364.8)}
MU_EXTRA = {"n-Dodecane":"Müller 2020 DSC: onset -10.2 °C / 209.14 J/g; cryst. onset -14.69 to -13.45 °C",
"Methyl palmitate":"Müller 2020 DSC: onset 28.9 °C, peak 31.5 °C / 205.03 J/g; cryst. 25.32–28.31 °C; max op 111.5 °C",
"Calcium chloride hexahydrate":"Müller 2020 DSC: onset 29.2 °C / 197.97 J/g; cryst. onset -24.1 to -16.4 °C (strong supercooling)",
"n-Eicosane":"Müller 2020 DSC: onset 36.0 °C / 246.44 J/g; cryst. 35.94–35.96 °C; max op 154.5 °C",
"1-Tetradecanol":"Müller 2020 DSC: onset 37.3 °C / 226.26 J/g; cryst. 37.66–37.77 °C; max op 110.8 °C",
"Sodium acetate trihydrate":"Müller 2020 DSC (Cowa SAT): onset 57.5 °C / 228.28 J/g; cryst. 33.18–46.26 °C",
"Mg(NO3)2·6H2O + MgCl2·6H2O":"Müller 2020 DSC (59:41 wt%): onset 58.1 °C / 151.66 J/g; cryst. 31.85–32.89 °C; max op 60.5 °C",
"Palmitic acid":"Müller 2020 DSC: onset 62.1 °C / 216.72 J/g; cryst. 59.55–60.65 °C; max op 171.7 °C",
"Stearic acid":"Müller 2020 DSC: onset 67.8 °C / 228.26 J/g; cryst. 63.66–66.31 °C; max op 195.4 °C",
"Erythritol":"Müller 2020 DSC: onset 118.7 °C / 337.76 J/g; cryst. onset 22.99–32.29 °C (~90 K supercooling); max op 192.3 °C",
"Galactitol (dulcitol)":"Müller 2020 DSC: onset 186.6 °C / 352.91 J/g; cryst. 105.35–119.2 °C; max op 242.4 °C"}
SUPERCOOL = {"Adipic acid":"4.1–6.1","Erythritol":"~90 (Müller 2020)","Calcium chloride hexahydrate":"~45–50 (Müller 2020)",
"Sodium acetate trihydrate":"~11–24 (Müller 2020); can supercool to -12.7 °C","Galactitol (dulcitol)":"~70–80 (Müller 2020)",
"Capric-myristic-palmitic acid (CA-MA-PA)":"~9 (onset melt 17.7 vs freeze 8.4 °C)"}
CYCLING = {"Adipic acid":"~23% latent heat loss after 110 cycles (Snekha 2024)","Stearic acid–adipic acid eutectic / expanded graphite":"Stable over 500 cycles",
"NaCl-Na2CO3":"Stable after 1,000 cycles (per Mao 2025)"}
NEW_COM = [("CrodaTherm 17","Bio-based organic","Croda (UK)",16.0,184.74,"Muller2020","DSC onset; peak 18.6 °C; cryst. 14.48–14.51 °C; max op 143.8 °C","DSC-measured (Müller 2020) - verified vs paper 2026-10-30",dict(cryst=14.5,tmax=143.8)),
("Cowa SAT (sodium acetate trihydrate)","Salt hydrate","Cowa Thermal Solutions (CH)",57.5,228.28,"Muller2020","DSC onset; peak 60.4 °C; cryst. 33.18–46.26 °C; max op 204.6 °C","DSC-measured (Müller 2020) - verified vs paper 2026-10-30",dict(cryst=39.7,tmax=204.6,cas="6131-90-4"))]
def mid(s):
    if s is None or s=="": return None
    v=[float(x) for x in re.findall(r"-?\d+(?:\.\d+)?",s)]
    return round(sum(v)/len(v),2) if v else None
