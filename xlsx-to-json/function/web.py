import os
from tempfile import NamedTemporaryFile
from typing import Any, Dict, List

from fastapi import FastAPI, File
from openpyxl import load_workbook  # type: ignore

from . import __version__
from .xlsxutils import read_worksheet_data

## TODO: Read the Sentry DSN from the secret store instead?
if "WEBAPP_SENTRY_DSN" in os.environ:
    from sentry_sdk import init

    init(os.environ["WEBAPP_SENTRY_DSN"])


#: Provides the web aplication instance.
app = FastAPI()


@app.get("/_meta")
async def metadata() -> Dict[str, str]:
    """
    Returns the application metadata.

    >>> import asyncio
    >>> assert asyncio.run(metadata()) == {"version": __version__}
    """
    return {"version": __version__}


@app.post("/")
async def root(file: bytes = File(...)) -> Dict[str, List[Dict[str, Any]]]:
    """
    Converts the given XLSX to JSON.
    """
    ## Work with a temporary file:
    with NamedTemporaryFile(suffix=".xlsx") as ofile:
        ## Write the contents to the temporary file:
        ofile.write(file)

        ## Load the workbook:
        workbook = load_workbook(ofile.name, data_only=True, read_only=True, keep_links=False, keep_vba=False)

        ## Iterate over workbook, read data and write to return value:
        retval = {s.title: list(read_worksheet_data(s)) for s in workbook.worksheets}

    ## Done, return:
    return retval
