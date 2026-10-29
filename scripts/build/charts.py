from openpyxl.chart import ScatterChart, BarChart, Reference, Series
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.chart.axis import ChartLines
from openpyxl.styles import Font, PatternFill, Alignment

CATS=["Organic","Inorganic","Metallic","Eutectic","Composite","Commercial"]
COL={"Organic":"2A78D6","Inorganic":"EB6834","Metallic":"1BAF7A","Eutectic":"EDA100","Composite":"E87BA4","Commercial":"008300"}
SYM={"Organic":"circle","Inorganic":"diamond","Metallic":"triangle","Eutectic":"square","Composite":"x","Commercial":"circle"}
GRID="E6E5E0"; AX="8A8983"

def _axis(ax,title,fmt="General",mn=None,mx=None,log=False,unit=None):
    ax.crosses="min"; ax.title=title; ax.delete=False; ax.number_format=fmt; ax.majorTickMark="out"; ax.tickLblPos="low"
    ax.majorGridlines=ChartLines(); ax.majorGridlines.spPr=GraphicalProperties(ln=LineProperties(solidFill=GRID,w=6350))
    ax.spPr=GraphicalProperties(ln=LineProperties(solidFill=AX,w=9525))
    if mn is not None: ax.scaling.min=mn
    if mx is not None: ax.scaling.max=mx
    if log: ax.scaling.logBase=10
    if unit: ax.majorUnit=unit

def _scatter(title,xt,yt,blocks,ws,xcol,ycol,xfmt="General",yfmt="General",ylog=False,xmin=None,xmax=None,ymin=None,ymax=None,xunit=None,yunit=None):
    ch=ScatterChart(); ch.title=title; ch.style=2; ch.height=11; ch.width=22; ch.scatterStyle="marker"
    _axis(ch.x_axis,xt,xfmt,xmin,xmax,unit=xunit); _axis(ch.y_axis,yt,yfmt,ymin,ymax,log=ylog,unit=yunit)
    for cat in ["Commercial"]+[c for c in CATS if c!="Commercial"]:
        r0,r1=blocks[cat]
        if r1<r0: continue
        s=Series(Reference(ws,min_col=ycol,min_row=r0,max_row=r1),Reference(ws,min_col=xcol,min_row=r0,max_row=r1),title=f"{cat} (n={r1-r0+1})")
        s.marker.symbol=SYM[cat]; s.marker.size=6 if cat!="Commercial" else 5
        s.marker.graphicalProperties=GraphicalProperties(solidFill=COL[cat]); s.marker.graphicalProperties.line.solidFill="FFFFFF"
        s.graphicalProperties.line.noFill=True
        ch.series.append(s)
    ch.legend.position="b"
    return ch

def build_charts(wb, rows, F):
    ws=wb["PCM_Data"]; cd=wb.create_sheet("Chart_Data"); hdr=PatternFill("solid",fgColor="1F4E78")
    # row index in PCM_Data for each record
    idx={r["id"]:i for i,r in enumerate(rows,2)}
    def kbest(r):
        for k in ("ks","ku","kl"):
            if r[k] is not None: return k
    KCOL={"ks":13,"kl":14,"ku":15}
    def has_vol(r): return r["L"] is not None and any(r[k] for k in ("rs","ru","rl"))
    sections=[("A","All PCMs: Tm vs latent heat",["Category","Name","Tm (°C)","Latent heat (kJ/kg)"],lambda r:True,lambda r,i:[f"=PCM_Data!C{i}",f"=PCM_Data!B{i}",f"=PCM_Data!H{i}",f"=PCM_Data!I{i}"]),
              ("F","PCMs with thermal conductivity",["Category","Name","Tm (°C)","k (W/m·K)"],lambda r:kbest(r) is not None,lambda r,i:[f"=PCM_Data!C{i}",f"=PCM_Data!B{i}",f"=PCM_Data!H{i}",f"=PCM_Data!{chr(64+KCOL[kbest(r)])}{i}"]),
              ("K","PCMs with density",["Category","Name","Latent heat (kJ/kg)","Volumetric (MJ/m³)"],has_vol,lambda r,i:[f"=PCM_Data!C{i}",f"=PCM_Data!B{i}",f"=PCM_Data!I{i}",f"=PCM_Data!T{i}"])]
    blocks={}
    for col0,title,heads,flt,fn in sections:
        c0=ord(col0)-64
        cd.cell(1,c0,title).font=Font(name=F,bold=True)
        for j,h in enumerate(heads): 
            c=cd.cell(2,c0+j,h); c.font=Font(name=F,bold=True,color="FFFFFF"); c.fill=hdr
        rr=3; bl={}
        for cat in CATS:
            start=rr
            for r in rows:
                if r["cat"]==cat and flt(r):
                    for j,v in enumerate(fn(r,idx[r["id"]])): cd.cell(rr,c0+j,v).font=Font(name=F,size=9)
                    rr+=1
            bl[cat]=(start,rr-1)
        blocks[col0]=bl
    # histogram by 20 °C bins (-80..140) + >140
    c0=16; cd.cell(1,c0,"Count of PCMs per melting-temperature band (formulas)").font=Font(name=F,bold=True)
    heads=["Band","From (°C)","To (°C)"]+CATS
    for j,h in enumerate(heads):
        c=cd.cell(2,c0+j,h); c.font=Font(name=F,bold=True,color="FFFFFF"); c.fill=hdr
    n=len(rows)+1; bins=list(range(-80,140,20)); rr=3
    for lo in bins+[140]:
        hi=lo+20 if lo<140 else 2000
        cd.cell(rr,c0,f"{lo} to {hi}" if lo<140 else "≥140"); cd.cell(rr,c0+1,lo); cd.cell(rr,c0+2,hi)
        for j,cat in enumerate(CATS):
            cd.cell(rr,c0+3+j,f'=COUNTIFS(PCM_Data!$C$2:$C${n},"{cat}",PCM_Data!$H$2:$H${n},">="&Q{rr},PCM_Data!$H$2:$H${n},"<"&R{rr})')
        for c in cd[rr][c0-1:c0+9]: c.font=Font(name=F,size=9)
        rr+=1
    hist_last=rr-1
    for col,wd in zip("ABCDEFGHIJKLMNOPQRSTUVWX",[11,30,9,11,2,11,30,9,9,2,11,30,11,13,2,11,9,9,9,9,9,9,10,11]): cd.column_dimensions[col].width=wd

    chs=wb.create_sheet("Charts",2)
    chs["A1"]="Charts — every chart reads live from PCM_Data via the Chart_Data sheet; filter or edit PCM_Data and they update."; chs["A1"].font=Font(name=F,bold=True,size=12)
    chs["A2"]="Colour + marker shape = category (legend below each chart). Hover a point in Excel to see its values."; chs["A2"].font=Font(name=F,size=9,color="555555")
    c1=_scatter("Latent heat vs melting temperature (all PCMs)","Melting temperature, Tm (°C)","Latent heat (kJ/kg)",blocks["A"],cd,3,4,xmin=-100,xmax=1100,ymin=0,ymax=1100,xunit=100,yunit=100)
    chs.add_chart(c1,"A4")
    c1b=_scatter("Latent heat vs melting temperature, −80 to 150 °C (building / cold-chain / solar range)","Melting temperature, Tm (°C)","Latent heat (kJ/kg)",blocks["A"],cd,3,4,xmin=-80,xmax=150,ymin=0,ymax=450,xunit=20,yunit=50)
    chs.add_chart(c1b,"N4")
    c2=_scatter("Thermal conductivity vs melting temperature (log scale)","Melting temperature, Tm (°C)","Thermal conductivity, k (W/m·K) — log scale",blocks["F"],cd,8,9,yfmt="0.0#",ylog=True,xmin=-100,xmax=1100,ymin=0.1,ymax=1000,xunit=100)
    chs.add_chart(c2,"A27")
    c3=_scatter("Volumetric vs gravimetric latent heat","Latent heat (kJ/kg)","Volumetric latent heat (MJ/m³)",blocks["K"],cd,13,14,xmin=0,xmax=1100,ymin=0,xunit=100,yunit=200)
    chs.add_chart(c3,"N27")
    b=BarChart(); b.type="col"; b.grouping="stacked"; b.overlap=100; b.gapWidth=40; b.title="Number of PCMs per melting-temperature band"; b.height=11; b.width=22; b.style=2
    data=Reference(cd,min_col=19,max_col=24,min_row=2,max_row=hist_last); b.add_data(data,titles_from_data=True)
    b.set_categories(Reference(cd,min_col=16,min_row=3,max_row=hist_last))
    for s,cat in zip(b.series,CATS): s.graphicalProperties=GraphicalProperties(solidFill=COL[cat]); s.graphicalProperties.line.solidFill="FFFFFF"
    _axis(b.x_axis,"Melting-temperature band (°C)"); b.x_axis.majorGridlines=None; _axis(b.y_axis,"Number of PCMs","0")
    b.legend.position="b"; chs.add_chart(b,"A50")
    # Summary chart replaced with categorised version
    sm=wb["Summary"]; sm._charts=[]
    sm.add_chart(_scatter("Latent heat vs melting temperature","Melting temperature, Tm (°C)","Latent heat (kJ/kg)",blocks["A"],cd,3,4,xmin=-100,xmax=1100,ymin=0,ymax=1100,xunit=100,yunit=100),"G3")
