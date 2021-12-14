from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
import pandas as pd
from tqdm.notebook import tqdm
import numpy as np
import cuml
import seaborn as sns
import matplotlib.pyplot as plt
from cuml.decomposition import PCA as cu_PCA
from cuml.metrics import trustworthiness as cu_trustworthiness
import cudf
from cuml import UMAP as cu_UMAP

#read smiles
#df = pd.read_csv("chembl_drugs.smi",sep="\t",header=None)
# may need to change to "\t" or " "
df = pd.read_csv("chembl_100k.smi.gz", sep = ' ', header = None)
df.columns = ["SMILES","Name"]

df['ROMol'] = [Chem.MolFromSmiles(x) for x in df.iloc[:,0]]

# generating fingerprints
df['fps'] = [AllChem.GetMorganFingerprintAsBitVect(m,2) for m in df['ROMol']]



X = []
fps = df['fps']
for fp in fps:
    arr = np.zeros((1,),np.int32)
    DataStructs.ConvertToNumpyArray(fp, arr)
    X.append(arr)


def np2cudf(arr):
    # convert numpy array to cudf dataframe
    df = pd.DataFrame({'fea%d'%i:arr[:,i] for i in range(arr.shape[1])})
    pdf = cudf.DataFrame()
    for c,column in enumerate(df):
        pdf[str(c)] = df[column]
    return pdf


cu_fp_df = np2cudf(np.array(X,dtype=np.float32))

n_neighbors = 50
umap = cu_UMAP(n_neighbors=n_neighbors, min_dist=0.6, verbose=False)

cu_ut = umap.fit_transform(cu_fp_df)

cu_df = pd.DataFrame(cu_ut.values,columns=["X","Y"])


cu_df['SMILES'] = df['SMILES']
cu_df['Name'] = df['Name']
df = df.drop(columns=['ROMol', 'fps'])
cu_df.to_csv("cu_df.csv", index = None, header= True)
df.to_csv("df.csv", index = None, header= True)
