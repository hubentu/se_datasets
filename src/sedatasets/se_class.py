# import json
from os.path import isfile, join

import anndata
import datasets
import pandas as pd
from torch.utils.data import Dataset


class AnnDataset(Dataset):
    """build `Dataset` from `anndata` h5ad file.
    Parameters
    ------
    h5ad
        A h5ad file from anndata package.
    """

    def __init__(self, h5ad):
        self.h5ad = h5ad
        self.ad = anndata.read_h5ad(h5ad)
        self.n = self.ad.n_obs
        # self.vid = self.ad.var.index.values
        self.rdict = {}

    def __len__(self):
        return self.n

    def __getitem__(self, idx):
        # ad = anndata.read_h5ad(self.h5ad, backed='r')
        ad1 = self.ad[idx]
        # self.rdict['gene_id'] = ad1.var.index.values
        self.rdict["X"] = ad1.X.toarray()[0]
        # sample annotation
        obs1 = ad1.obs.iloc[0].astype(str).to_dict().copy()
        # ad.file.close()
        if "X" in obs1:
            obs1["obs_X"] = obs1.pop("X")
        self.rdict.update(obs1)
        return self.rdict


class SEDataset(Dataset):
    """build `Dataset` from raw matrix.
    Parameters
    ------
    assays
        A dict of assay matrix.
    pfile
        Phenotype dataframe.
    ffile
        Feature dataframe.
    """

    def __init__(self, assays, pdata, fdata):
        self.pdata = pdata
        self.fdata = fdata
        self.assays = assays
        self.rdict = {}

    def __len__(self):
        return self.pdata.shape[0]

    def __getitem__(self, idx):
        for k, v in self.assays.items():
            self.rdict[k] = v.iloc[:, idx].values

        # sample annotation
        obs1 = self.pdata.iloc[idx].to_dict()
        self.rdict.update(obs1)

        return self.rdict


class SEdatasets:
    """build `SEdatasets` from `datasets` and feature annotation `fdata`.
    Parameters
    ------
    ds
        A `datasets` object.
    fdata
        Feature annotation dataframe.
    dataset_path
        The path to save or load the data.
    """

    def __init__(self, ds=None, fdata=None):
        # super().__init__(self)
        self.fdata = fdata
        self.datasets = ds

    def save_to_disk(self, dataset_path, **kwargs):
        self.datasets.save_to_disk(dataset_path, **kwargs)
        if self.fdata is not None:
            if self.fdata.index.values[0] != 0:
                if self.fdata.index.name not in self.fdata.columns:
                    self.fdata.reset_index(inplace=True)
            self.fdata.to_csv(join(dataset_path, "fdata.csv"), index=False)

    def load_from_disk(self, dataset_path, **kwargs):
        self.datasets = datasets.load_from_disk(dataset_path, **kwargs)
        fpath = join(dataset_path, "fdata.csv")
        if isfile(fpath):
            self.fdata = pd.read_csv(fpath)
        return self

    def __repr__(self):
        ds_pr = self.datasets.__repr__()
        if self.fdata is not None:
            f_pr = f"fdata: {self.fdata.columns.to_list()}"
        else:
            f_pr = None
        return f"{ds_pr}\n{f_pr}"
