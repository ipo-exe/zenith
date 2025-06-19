import os

from src.base import MbaE
from src.collection import Collection
from src.dataset.base import DataSet
from src.dataset.budget import Budget
from src.dataset.file_sys import FileSys
from src.dataset.record_table import RecordTable
from src.note import Note


def test_mbae_instantiation():
    instance = MbaE()
    assert isinstance(instance, MbaE)


def test_collection_instantiation():
    instance = Collection(MbaE)
    assert isinstance(instance, Collection)


def test_dataset_instantiation():
    instance = DataSet()
    assert isinstance(instance, DataSet)


def test_record_table_instantiation():
    instance = RecordTable()
    assert isinstance(instance, RecordTable)


def test_file_system_instantiation():
    instance = FileSys(os.getcwd())
    assert isinstance(instance, FileSys)


def test_budget_instantiation():
    instance = Budget()
    assert isinstance(instance, Budget)


def test_note_instantiation():
    instance = Note()
    assert isinstance(instance, Note)
