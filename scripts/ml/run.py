import pandas as pd, numpy as np, warnings; warnings.filterwarnings("ignore")
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, Fragments
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel as C
from sklearn.linear_model import RidgeCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupKFold
from smiles import SMI
d=pd.read_csv('data/pcm_ml_ready_v1_4.csv')
d=d[d.formula_parsed.notna()].copy()
G='group_id (use for GroupKFold)'
d['T_K']=d.Tm_C+273.15
d['dS']=d.latent_kJkg*d.molar_mass_gmol/d.T_K   # J/mol/K
FORM=['molar_mass_gmol','n_atoms','n_C','n_H','n_O','n_N','n_halogen','n_metal_atoms','hydrate_water_n','water_mass_frac','is_organic','is_inorganic','is_metallic','has_COOH_like']
def rd(smi):
    m=Chem.MolFromSmiles(smi)
    return dict(MolWt=Descriptors.MolWt(m),Heavy=m.GetNumHeavyAtoms(),HBD=rdMolDescriptors.CalcNumHBD(m),HBA=rdMolDescriptors.CalcNumHBA(m),
      TPSA=rdMolDescriptors.CalcTPSA(m),RotB=rdMolDescriptors.CalcNumRotatableBonds(m),Rings=rdMolDescriptors.CalcNumRings(m),
      Arom=rdMolDescriptors.CalcNumAromaticRings(m),FCsp3=rdMolDescriptors.CalcFractionCSP3(m),LogP=Descriptors.MolLogP(m),
      LabuteASA=rdMolDescriptors.CalcLabuteASA(m),nOH=Fragments.fr_Al_OH(m)+Fragments.fr_Ar_OH(m),nCOOH=Fragments.fr_COO(m),
      nEster=Fragments.fr_ester(m),nAmide=Fragments.fr_amide(m)+Fragments.fr_urea(m),Sym=len(set(Chem.CanonicalRankAtoms(m,breakTies=False)))/m.GetNumHeavyAtoms(),
      HBperHeavy=(rdMolDescriptors.CalcNumHBD(m)+rdMolDescriptors.CalcNumHBA(m))/m.GetNumHeavyAtoms())
org=d[d.Name.isin(SMI)].copy()
R=pd.DataFrame([rd(SMI[n]) for n in org.Name],index=org.index); RD=list(R.columns); org=pd.concat([org,R],axis=1)
org['grp']=[Chem.MolToSmiles(Chem.MolFromSmiles(SMI[n]),isomericSmiles=False) for n in org.Name]   # stereoisomers share a group
d['grp']=d[G]; d.loc[org.index,'grp']=org['grp']
models={'Ridge':lambda:make_pipeline(StandardScaler(),RidgeCV(alphas=np.logspace(-3,3,25))),
        'RF':lambda:RandomForestRegressor(400,min_samples_leaf=2,random_state=0),
        'GBR':lambda:GradientBoostingRegressor(n_estimators=300,max_depth=2,learning_rate=0.05,subsample=0.8,random_state=0),
        'GP':lambda:make_pipeline(StandardScaler(),GaussianProcessRegressor(C(1.0)*RBF(np.ones(1)*3)+WhiteKernel(0.1),normalize_y=True,n_restarts_optimizer=3,random_state=0))}
def cv(df,X,ytrans,yinv,mname,k=5):
    p=np.zeros(len(df)); gk=GroupKFold(min(k,df.grp.nunique()))
    for tr,te in gk.split(df,groups=df.grp):
        m=models[mname](); m.fit(df.iloc[tr][X].fillna(0),ytrans(df.iloc[tr])); p[te]=yinv(m.predict(df.iloc[te][X].fillna(0)),df.iloc[te])
    return p
def score(y,p): return np.mean(np.abs(p-y)), 1-np.sum((p-y)**2)/np.sum((y-y.mean())**2)
res=[]
def run(label,df,X,target,route):
    y=df[target].values if target!='latent' else df.latent_kJkg.values
    for mn in models:
        if route=='direct': p=cv(df,X,lambda s:s.latent_kJkg if target=='latent' else s[target],lambda q,s:q,mn)
        else: p=cv(df,X,lambda s:s.dS,lambda q,s:q*s.T_K.values/s.molar_mass_gmol.values,mn)
        mae,r2=score(y,p); res.append(dict(experiment=label,n=len(df),target=('latent heat' if target=='latent' else 'Tm'),route=route,model=mn,MAE=round(mae,1),R2=round(r2,2)))
# --- latent heat ---
run('A. All 127, formula features (v1.4 baseline)',d,FORM,'latent','direct')
run('B. All 127, formula + measured Tm',d,FORM+['Tm_C'],'latent','direct')
run('C. All 127, entropy-of-fusion route (needs Tm)',d,FORM+['Tm_C'],'latent','dS')
inorg=d[d.is_organic==0]
run('D. Inorganic+metal only, formula + Tm',inorg,FORM+['Tm_C'],'latent','direct')
run('E. Inorganic+metal only, entropy route',inorg,FORM+['Tm_C'],'latent','dS')
run('F. Organic only, formula + Tm',org,FORM+['Tm_C'],'latent','direct')
run('G. Organic only, RDKit + Tm',org,RD+['Tm_C'],'latent','direct')
run('H. Organic only, RDKit, entropy route',org,RD+['Tm_C'],'latent','dS')
# --- melting temperature ---
run('T1. All 127, formula features',d,FORM,'Tm_C','direct')
run('T2. Organic only, formula features',org,FORM,'Tm_C','direct')
run('T3. Organic only, RDKit descriptors',org,RD,'Tm_C','direct')
r=pd.DataFrame(res); r.to_csv('data/results.csv',index=False)
best=r.sort_values('MAE').groupby('experiment',sort=False).head(1).sort_values('experiment')
print(best.to_string(index=False))
print('\nmean |latent| baseline MAE (predict mean): all',round(np.mean(np.abs(d.latent_kJkg-d.latent_kJkg.mean())),1),' org',round(np.mean(np.abs(org.latent_kJkg-org.latent_kJkg.mean())),1),' inorg',round(np.mean(np.abs(inorg.latent_kJkg-inorg.latent_kJkg.mean())),1))
print('Tm baseline: all',round(np.mean(np.abs(d.Tm_C-d.Tm_C.mean())),1),' org',round(np.mean(np.abs(org.Tm_C-org.Tm_C.mean())),1))
org[['Name','latent_kJkg','Tm_C','dS']+RD].to_csv('data/organic_rdkit_features.csv',index=False)
