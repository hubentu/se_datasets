# sedatasets

`sedatasets` is a Python package to convert Bioconductor
`SummarizedExperiment` data structure to HuggingFace `datasets`.


# Usage
## Command line
```bash
python -m sedatasets.cli -h
```

## Python Module
```python
from sedatasets.se_convert import AD2Datasets, SE2Datasets

SE2Datasets(
    efiles={"exp": "tests/data/rse_counts.csv"},
    pfile="tests/data/rse_cdata.csv",
    ffile="tests/data/rse_rdata.csv",
    outdir='/tmp/rse',
)

AD2Datasets("tests/data/adata.h5ad", outdir='/tmp/anndata')

```
