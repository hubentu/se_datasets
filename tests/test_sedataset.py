import tempfile

import datasets

from sedatasets.se_convert import AD2Datasets, SE2Datasets

# import pytest


__author__ = "qhu"
__copyright__ = "qhu"
__license__ = "MIT"


def test_se2ds():
    dout = tempfile.mkdtemp()
    SE2Datasets(
        efiles={"exp": "tests/data/rse_counts.csv"},
        pfile="tests/data/rse_cdata.csv",
        ffile="tests/data/rse_rdata.csv",
        outdir=dout,
    )
    dset = datasets.load_from_disk(dout)
    assert dset.num_rows == 6


def test_ad2ds():
    dout = tempfile.mkdtemp()
    AD2Datasets("tests/data/adata.h5ad", outdir=dout)
    dset = datasets.load_from_disk(dout)
    assert dset.num_rows == 30
