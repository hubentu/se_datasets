import argparse
import logging
import sys

# from se_class import AnnDataset, SEDataset
from sedatasets import __version__

from .se_convert import AD2Datasets, SE2Datasets

# import glob
# import anndata

# import pyarrow as pa
# import re
# import datasets
# import pandas as pd

# import numpy as np
# import torch
# from torch.utils.data import Dataset


__author__ = "qhu"
__copyright__ = "qhu"
__license__ = "MIT"
# __version__ = "v0.0.1"

_logger = logging.getLogger(__name__)


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Covert SummarizedExperiment dataset to Huggingface datasets"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"sedatasets {__version__}",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-a", "--afile", dest="afile", help="h5ad anndata file", type=str
    )
    group.add_argument(
        "-e",
        "--efiles",
        dest="efiles",
        nargs="+",
        help="expression matrix files.",
        type=str,
    )
    parser.add_argument(
        "-o", "--outdir", dest="outdir", help="output datasets directory", type=str
    )
    parser.add_argument("-p", "--pfile", dest="pfile", help="phenotype file", type=str)
    parser.add_argument(
        "-f", "--ffile", dest="ffile", help="feature annotation file", type=str
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`AD2Datasets` to be called with string
    arguments in a CLI fashion

        Args:
          args (List[str]): command line parameters as list of strings
              (for example  ``["--verbose", "42"]``).

    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Start to converting...")

    if args.afile is None:
        SE2Datasets(args.efiles, args.pfile, args.ffile, args.outdir)
    else:
        AD2Datasets(args.afile, args.outdir)

    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m sedatasets.sedatasets -h
    #
    run()
