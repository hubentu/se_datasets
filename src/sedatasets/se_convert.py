# import argparse
import logging
import os

# import sys
import tempfile

# import glob
import anndata

# import pyarrow as pa
# import re
import datasets
import pandas as pd

from .se_class import AnnDataset, SEDataset, SEdatasets

# import numpy as np
# import torch
# from torch.utils.data import Dataset


_logger = logging.getLogger(__name__)


def split_h5ad(afile, size=6000, cache=tempfile.mkdtemp()):
    # split to fix bug with backed=r.
    ad = anndata.read_h5ad(afile, backed="r")
    n = ad.n_obs
    ad.file.close()
    hfiles = []
    if n > size:
        for i in range(n // size + 1):
            _logger.debug(f"split {afile}")
            ad = anndata.read_h5ad(afile, backed="r")
            idx_s = i * size
            idx_e = (i + 1) * size
            if ad.n_obs > idx_s:
                if idx_e > ad.n_obs:
                    idx_e = ad.n_obs
                ad1 = ad[idx_s:idx_e]
                f1 = os.path.join(cache, str(i) + ".h5ad")
                ad1.write(f1)
                hfiles.append(f1)
                _logger.debug(f"{f1}")
            ad.file.close()
    else:
        hfiles = [afile]
    return hfiles


def convert_ad(afile):
    def gen(afile):
        hfiles = split_h5ad(afile)
        for h1 in hfiles:
            ad = AnnDataset(h1)
            for idx in range(len(ad)):
                yield ad[idx].copy()  # add copy to realize

    ds = datasets.Dataset.from_generator(gen, gen_kwargs={"afile": afile})
    # ad = anndata.read_h5ad(afile, backed="r")
    # dset.info.post_processed = {'vid': ad.var.index.values.tolist()}
    ad = anndata.read_h5ad(afile, backed="r")
    dset = SEdatasets(ds, ad.var)
    ad.file.close()
    return dset


def AD2Datasets(afile, outdir):
    dset = convert_ad(afile)
    dset.save_to_disk(outdir)
    return outdir


def convert_se(efiles, pfile, ffile):
    # _logger.debug(f'expression files {efiles}')
    pdata = pd.read_csv(pfile, dtype=str).astype(str)
    fdata = pd.read_csv(ffile, dtype=str).astype(str)
    assays = {}
    # if exp_n is None:
    #     exp_n = ['exp'+str(i) for i in range(len(efiles))]

    # for k, afile in zip(exp_n, efiles):
    for k, afile in efiles.items():
        assays[k] = pd.read_csv(afile).astype(float)

    se = SEDataset(assays, pdata, fdata)

    def gen(se):
        for idx in range(len(se)):
            yield se[idx].copy()  # add copy to realize

    dset = datasets.Dataset.from_generator(gen, gen_kwargs={"se": se})
    # dset.info.post_processed = {'fdata': fdata.index.values.tolist()}
    seds = SEdatasets(dset, fdata)
    return seds


# se = convert_se(efiles, pfile, ffile)
def SE2Datasets(efiles, pfile, ffile, outdir):
    dset = convert_se(efiles, pfile, ffile)
    dset.save_to_disk(outdir)
    return outdir
