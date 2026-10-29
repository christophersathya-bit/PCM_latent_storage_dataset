import re, csv
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
AM={'H':1.008,'Li':6.94,'B':10.81,'C':12.011,'N':14.007,'O':15.999,'F':18.998,'Na':22.990,'Mg':24.305,'Al':26.982,'Si':28.085,'P':30.974,'S':32.06,'Cl':35.45,'K':39.098,'Ca':40.078,'Cr':51.996,'Mn':54.938,'Fe':55.845,'Ni':58.693,'Cu':63.546,'Zn':65.38,'Ga':69.723,'Br':79.904,'Rb':85.468,'Cd':112.41,'In':114.82,'Sn':118.71,'I':126.90,'Cs':132.91,'Ba':137.33,'Hg':200.59,'Pb':207.2,'Bi':208.98}
METALS={'Li','Na','K','Rb','Cs','Mg','Ca','Ba','Al','Zn','Fe','Ni','Mn','Cu','Cr','Ga','In','Sn','Pb','Bi','Hg','Cd'}
def _parse(s):
    s=s.replace(' ','')
    def grp(i):
        cnt={}
        while i<len(s) and s[i]!=')':
            if s[i]=='(':
                sub,i=grp(i+1); i+=1
                m=re.match(r'\d+',s[i:]); k=int(m.group()) if m else 1; i+=len(m.group()) if m else 0
                for e,v in sub.items(): cnt[e]=cnt.get(e,0)+v*k
            else:
                m=re.match(r'([A-Z][a-z]?)(\d*)',s[i:])
                if not m: raise ValueError(s)
                e=m.group(1); k=int(m.group(2) or 1)
                if e not in AM: raise ValueError(e)
                cnt[e]=cnt.get(e,0)+k; i+=len(m.group())
        return cnt,i
    c,i=grp(0)
    if i!=len(s): raise ValueError(s)
    return c
def parse_formula(f):
    if not f or any(x in f for x in [',','/',':','~','%',' acid','-','xH2O','n']) and not re.fullmatch(r'[A-Za-z0-9()·]+',f.replace(' ','')): return None
    f=f.replace(' ','')
    if not re.fullmatch(r'[A-Za-z0-9()·.]+',f): return None
    parts=re.split(r'[·.]',f); tot={}; water=0
    try:
        for p in parts:
            m=re.fullmatch(r'(\d*)H2O',p)
            if m: water+=int(m.group(1) or 1); continue
            for e,v in _parse(p).items(): tot[e]=tot.get(e,0)+v
    except ValueError: return None
    anh=dict(tot); 
    for e,v in (('H',2*water),('O',water)): tot[e]=tot.get(e,0)+v
    M=sum(AM[e]*v for e,v in tot.items()); Mw=water*18.015
    return dict(elements=tot,anh=anh,M=M,water=water,wfrac=Mw/M if M else 0)

def weight(st,src):
    s=(st or "").lower()
    if "verified" in s or "datasheet" in s or "lleida" in s or "dsc-measured" in s or "measured" in s: return 1.0
    if "manufacturer" in s: return 0.9
    if "literature/handbook" in s: return 0.8
    if "review" in s or "secondary" in s: return 0.7
    return 0.5

CATS=["Organic","Inorganic","Metallic","Eutectic","Composite","Commercial"]
def best(r,keys):
    for k,ph in keys:
        if r.get(k) is not None: return r[k],ph
    return None,""

def build_ml(wb,rows,F,csv_path):
    ws=wb.create_sheet("ML_Data")
    cols=["ID","Name","Category","Subclass","group_id (use for GroupKFold)","sample_weight","in_core_set (pure/eutectic, formula known)",
          "is_organic","is_inorganic","is_metallic","is_eutectic","is_composite","is_commercial","is_solid_solid","latent_is_total_storage",
          "Tm_C","latent_kJkg","volumetric_MJm3","cp_kJkgK","cp_phase","k_WmK","k_phase","rho_kgm3","rho_phase","cryst_T_C","supercooling_K_from_data",
          "formula_parsed","molar_mass_gmol","n_atoms","n_C","n_H","n_O","n_N","n_halogen","n_metal_atoms","hydrate_water_n","water_mass_frac",
          "C_chain_len_if_alkane","has_COOH_like","Source key","Data status"]
    ws.append(cols)
    hdr=PatternFill("solid",fgColor="1F4E78")
    for c in ws[1]: c.font=Font(name=F,bold=True,color="FFFFFF",size=9); c.fill=hdr; c.alignment=Alignment(wrap_text=True,vertical="center")
    out=[]
    for r in rows:
        p=parse_formula(r.get("f") or "") if r["cat"] in ("Organic","Inorganic","Metallic") else None
        e=p["elements"] if p else {}
        cp,cph=best(r,[("cps","solid"),("cpu","unspecified"),("cpl","liquid")])
        k,kph=best(r,[("ks","solid"),("ku","unspecified"),("kl","liquid")])
        rho,rph=best(r,[("rs","solid"),("ru","unspecified"),("rl","liquid")])
        vol=round(r["L"]*rho/1000,2) if rho else None
        sc=round(r["tm"]-r["cryst"],2) if r.get("cryst") is not None else None
        name=r["name"]
        grp=(r["sup"] or "") if r["cat"]=="Commercial" else re.sub(r"\s*\[measured\]|\s*\(.*?\)","",name).strip().lower()
        alk=None
        if p and set(e)=={"C","H"} and e["H"]==2*e["C"]+2: alk=e["C"]
        cooh=1 if (r["sub"] or "").lower().startswith(("fatty acid","dicarboxylic","aromatic acid")) else 0
        core=1 if (p is not None or r["cat"]=="Eutectic") else 0
        row=[r["id"],name,r["cat"],r["sub"],grp,weight(r["status"],r["src"]),core]+[1 if r["cat"]==c else 0 for c in CATS]+[1 if r["tr"]=="S-S" else 0,
             1 if r["src"] in ("Rubitherm","Axiotherm") else 0,
             r["tm"],r["L"],vol,cp,cph,k,kph,rho,rph,r.get("cryst"),sc,
             (r.get("f") if p else None),(round(p["M"],3) if p else None),(sum(e.values()) if p else None),
             e.get("C",0) if p else None,e.get("H",0) if p else None,e.get("O",0) if p else None,e.get("N",0) if p else None,
             (sum(e.get(x,0) for x in ("F","Cl","Br","I")) if p else None),(sum(v for x,v in e.items() if x in METALS) if p else None),
             (p["water"] if p else None),(round(p["wfrac"],4) if p else None),alk,cooh,r["src"],r["status"]]
        ws.append(row); out.append(row)
    for row in ws.iter_rows(min_row=2):
        for c in row: c.font=Font(name=F,size=9)
    for j,w in enumerate([10,34,11,22,22,8,8]+[6]*8+[8]*11+[14,10,8]+[6]*8+[8,8,8,12,30],1): ws.column_dimensions[get_column_letter(j)].width=w
    ws.row_dimensions[1].height=60; ws.freeze_panes="C2"; ws.auto_filter.ref=f"A1:{get_column_letter(len(cols))}{len(out)+1}"
    with open(csv_path,"w",newline="",encoding="utf-8") as fh:
        w=csv.writer(fh); w.writerow(cols); [w.writerow(["" if v is None else v for v in r]) for r in out]
    # data dictionary sheet
    dd=wb.create_sheet("ML_Guide")
    guide=[("ML_Data — how to use",""),("",""),
     ("Column","Meaning"),
     ("group_id","Same material / same supplier share a group. Split train/test with GroupKFold on this column to avoid leakage between near-duplicates (e.g. PlusICE grades, repeated salts)."),
     ("sample_weight","Data-quality weight: 1.0 verified/datasheet/measured; 0.9 manufacturer listing; 0.8 literature/handbook; 0.7 secondary review table; 0.5 other."),
     ("in_core_set","1 = pure compound with parsed formula, or a eutectic. Best subset for structure→property models."),
     ("is_* columns","One-hot category flags. is_solid_solid = solid–solid transition."),
     ("latent_is_total_storage","1 = supplier reports 'heat storage capacity' over a temperature range (latent + some sensible), not pure latent heat (Rubitherm, Axiotherm)."),
     ("Tm_C, latent_kJkg","Main targets. 100% filled."),
     ("cp / k / rho + *_phase","Best available value; phase says which (solid preferred, then unspecified, then liquid). Blank = not reported. Do NOT fill blanks with zeros."),
     ("volumetric_MJm3","latent × density / 1000 using the density shown."),
     ("cryst_T_C, supercooling_K_from_data","Crystallization/congealing T where reported; supercooling = Tm − cryst_T (only meaningful for DSC/datasheet values)."),
     ("Formula descriptors","molar mass, atom counts, halogen/metal atom counts, hydrate water count and water mass fraction — computed from the chemical formula (pure compounds only). Alkane chain length for n-alkanes."),
     ("",""),("Suggested tasks","Regress latent_kJkg or Tm_C on formula descriptors (in_core_set=1, ~200 rows); classify category; screen by temperature window."),
     ("Suggested models","Small data: gradient boosting / random forest / Gaussian process first; small NN only with strong regularisation. Report GroupKFold CV error."),
     ("Caveats","Values from different sources can differ 10–20%; commercial rows lack composition; cp/k/ρ ~50% missing; few composites; dense in 0–60 °C."),
     ("Export","Same table is saved as pcm_ml_ready_v1_4.csv (UTF-8)."),]
    for i,(a,b) in enumerate(guide,1):
        dd.cell(i,1,a).font=Font(name=F,bold=(i in (1,3) or a in("Suggested tasks","Suggested models","Caveats","Export")),size=12 if i==1 else 10)
        dd.cell(i,2,b).font=Font(name=F,size=10); dd.cell(i,2).alignment=Alignment(wrap_text=True,vertical="top")
    dd.column_dimensions["A"].width=34; dd.column_dimensions["B"].width=120
    return out

def build_results(wb,F,path="data/results.csv"):
    import os
    if not os.path.exists(path): return
    r=list(csv.DictReader(open(path)))
    ws=wb.create_sheet("ML_Results")
    ws["A1"]="ML experiments — 5-fold GroupKFold cross-validation (no material appears in both train and test)"; ws["A1"].font=Font(name=F,bold=True,size=12)
    ws["A2"]="MAE = mean absolute error (kJ/kg for latent heat, °C for Tm). R² = 1 is perfect, 0 = no better than predicting the mean. Run 2026-10-30 on pcm_ml_ready_v1_4.csv."; ws["A2"].font=Font(name=F,size=9,color="555555")
    exps=[];[exps.append(x["experiment"]) for x in r if x["experiment"] not in exps]
    models=["Ridge","GP","RF","GBR"]
    head=["Experiment","n","Target","Route"]+[f"MAE {m}" for m in models]+[f"R² {m}" for m in models]
    hdr=PatternFill("solid",fgColor="1F4E78")
    for j,h in enumerate(head,1):
        c=ws.cell(4,j,h); c.font=Font(name=F,bold=True,color="FFFFFF",size=9); c.fill=hdr
    good=PatternFill("solid",fgColor="E2EFDA")
    for i,e in enumerate(exps,5):
        sub={x["model"]:x for x in r if x["experiment"]==e}; x0=next(iter(sub.values()))
        vals=[e,int(x0["n"]),x0["target"],"entropy of fusion" if x0["route"]=="dS" else "direct"]+[float(sub[m]["MAE"]) for m in models]+[float(sub[m]["R2"]) for m in models]
        for j,v in enumerate(vals,1):
            c=ws.cell(i,j,v); c.font=Font(name=F,size=9)
            if j>8 and isinstance(v,float) and v>=0.65: c.fill=good
    last=4+len(exps)
    notes=["","Key findings",
     "1. Entropy-of-fusion route works: predict ΔS_fus = L·M/T_m (J/mol·K), then convert back L = ΔS·T_m/M. Latent heat R² rises from ~0.3 to 0.72–0.78 (all compounds and inorganics), robust across Ridge/GP/RF. Requires a known (measured) Tm.",
     "2. Per-class models help: organics alone reach MAE ≈ 22 kJ/kg (R² 0.66) vs 41 kJ/kg for predicting the mean.",
     "3. RDKit molecular descriptors help Tm prediction for organics (R² 0.43 → 0.72, MAE ≈ 20 °C) but not latent heat (n = 55 is too small and alkane-heavy).",
     "4. Direct prediction of latent heat from formula alone remains weak (R² ≈ 0.3).",
     "Caveats: small samples (55 organic, 72 inorganic/metal); reported best = best of 4 models on the same CV, so slightly optimistic; entropy route needs Tm as input; eutectics, composites and commercial products excluded (no structure).",
     "Recommended pipeline: (1) predict Tm with class-specific model (RDKit for organics); (2) predict ΔS_fus; (3) L = ΔS·Tm/M. Validate on new measured compounds before use."]
    for k,t in enumerate(notes,last+1):
        c=ws.cell(k,1,t); c.font=Font(name=F,size=10,bold=(t=="Key findings")); 
    ws.column_dimensions["A"].width=48
    for col in "BCDEFGHIJKL": ws.column_dimensions[col].width=10
    ws.column_dimensions["C"].width=12; ws.column_dimensions["D"].width=16
