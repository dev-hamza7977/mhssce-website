from pathlib import Path
from tools import common_vars as cv
import pandas as pd
import os

abs_path = os.path.abspath(__file__)
dir_path = os.path.dirname(abs_path)
parent_path = Path(dir_path).parent
db_base_location = os.path.join(parent_path, "static\\db")
db_image_location = os.path.join(parent_path, "static\\image")


def get_db_from_csv_to_dict(_db_name: str):
    _db_path = os.path.join(db_base_location, _db_name + ".csv")
    if os.path.exists(_db_path):
        _db = pd.read_csv(_db_path, index_col=False)
        return _db.loc[_db[cv.columnname_ENABLED]].to_dict(orient="records")


def get_db_from_csv_to_df(_db_name: str):
    _db_path = os.path.join(db_base_location, _db_name + ".csv")
    if os.path.exists(_db_path):
        _db = pd.read_csv(_db_path, index_col=False)
        return _db.loc[_db[cv.columnname_ENABLED]]


def append_dict_to_csv(_data: dict, _db_name: str):
    _db_path = os.path.join(db_base_location, _db_name + ".csv")
    if os.path.exists(_db_path):
        _db = pd.read_csv(_db_path, index_col=False)
        _db = _db.append(_data, ignore_index=True)
        _db.to_csv(_db_path, index=False)


def disable_item(_db_name: str, _id: str):
    _db_path = os.path.join(db_base_location, _db_name + ".csv")
    if os.path.exists(_db_path):
        _db = pd.read_csv(_db_path, index_col=False)
        _db.loc[_db[cv.columnname_ID] == _id, [cv.columnname_ENABLED]] = False
        _db.to_csv(_db_path, index=False)
