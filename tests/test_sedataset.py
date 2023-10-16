# import pytest

# from sedatasets.sedataset import SE2Datasets

__author__ = "qhu"
__copyright__ = "qhu"
__license__ = "MIT"


def test_se2ds():
    pass


# def test_fib():
#     """API Tests"""
#     assert fib(1) == 1
#     assert fib(2) == 1
#     assert fib(7) == 13
#     with pytest.raises(AssertionError):
#         fib(-10)


# def test_main(capsys):
#     """CLI Tests"""
#     # capsys is a pytest fixture that allows asserts against stdout/stderr
#     # https://docs.pytest.org/en/stable/capture.html
#     main(["7"])
#     captured = capsys.readouterr()
#     assert "The 7-th Fibonacci number is 13" in captured.out


# h = ""

# efile = ""
# pfile = ""
# ffile = ""

# pdata = pd.read_csv(pfile, index_col=0, dtype=str).astype(str)
# fdata = pd.read_csv(ffile, index_col=0, dtype=str).astype(str)
# assays = {}
# exp_n = ["exp" + str(i) for i in range(len([efile]))]

# for k, afile in zip(exp_n, [efile]):
#     assays[k] = pd.read_csv(afile, index_col=0)

# se1 = SEDataset(assays, pdata, fdata)

# dset = datasets.load_from_disk("../../tests/outdir/")

# python ../src/sedatasets/sedatasets.py -e se_exprs.csv -o out1 -p
# se_pdata.csv -f se_fdata.csv -vv
