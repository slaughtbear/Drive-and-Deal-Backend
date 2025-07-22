from typing import Any
from fastapi import FastAPI


app = FastAPI()


def read_root() -> dict[str, Any]:
    return {'msg': 'welcome to drive and deal backend'}