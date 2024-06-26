"""Tests for convnwb.io.io"""

import os

import numpy as np
import pandas as pd

from convnwb.tests.tsettings import TEST_FILE_PATH

from convnwb.io.io import *

###################################################################################################
###################################################################################################

def test_save_nwbfile(tnwbfile):

    test_fname = 'test_nwbfile'
    save_nwbfile(tnwbfile, test_fname, TEST_FILE_PATH)
    assert os.path.exists(TEST_FILE_PATH / (test_fname + '.nwb'))

def test_load_nwbfile():

    test_fname = 'test_nwbfile'
    tnwbfile = load_nwbfile(test_fname, TEST_FILE_PATH)
    assert tnwbfile

def test_save_config():

    cdict1 = {'d1' : 1, 'd2' : 'name', 'd3' : ['a', 'b', 'c']}
    f_name1 = 'test_config1'
    save_config(cdict1, f_name1, TEST_FILE_PATH)

    assert os.path.exists(TEST_FILE_PATH / (f_name1 + '.yaml'))

    cdict2 = {'d1' : 'words', 'd2' : None, 'd3' : ['list', 'of', 'terms']}
    f_name2 = 'test_config2'
    save_config(cdict2, f_name2, TEST_FILE_PATH)

    assert os.path.exists(TEST_FILE_PATH / (f_name2 + '.yaml'))

def test_load_config():

    f_name1 = 'test_config1'
    config = load_config(f_name1, TEST_FILE_PATH)
    assert isinstance(config, dict)

def test_load_configs():

    f_names = ['test_config1', 'test_config2']
    configs = load_configs(f_names, TEST_FILE_PATH)
    assert isinstance(configs, dict)

def test_save_object(ttask, tbundle, telectrodes):

    f_name = 'task_obj'
    save_object(ttask, f_name, TEST_FILE_PATH)
    assert os.path.exists(TEST_FILE_PATH / (f_name + '.task'))

    f_name = 'bundle_obj'
    save_object(tbundle, f_name, TEST_FILE_PATH)
    assert os.path.exists(TEST_FILE_PATH / (f_name + '.bundle'))

    f_name = 'electrodes_obj'
    save_object(telectrodes, f_name, TEST_FILE_PATH)
    assert os.path.exists(TEST_FILE_PATH / (f_name + '.electrodes'))

def test_load_object():

    f_name = 'task_obj.task'
    task = load_object(f_name, TEST_FILE_PATH)
    assert task

    f_name = 'bundle_obj.bundle'
    bundle = load_object(f_name, TEST_FILE_PATH)
    assert bundle

    f_name = 'electrodes_obj.electrodes'
    electrodes = load_object(f_name, TEST_FILE_PATH)
    assert electrodes

def test_save_txt():

    text = "Words, words, words."
    f_name = 'test_txt'

    save_txt(text, f_name, TEST_FILE_PATH)
    assert os.path.exists(TEST_FILE_PATH / (f_name + '.txt'))

def test_load_txt():

    f_name = 'test_txt'
    text = load_txt(f_name, TEST_FILE_PATH)
    assert text

def test_save_json():

    data = {'a' : 12, 'b' : 21}
    f_name = 'test_json'

    save_json(data, f_name, TEST_FILE_PATH)
    assert os.path.exists(TEST_FILE_PATH / (f_name + '.json'))

def test_load_json():

    f_name = 'test_json'
    data = load_json(f_name, TEST_FILE_PATH)
    assert data

def test_save_jsonlines():

    data = [{'A1' : {'a' : 12, 'b' : 21}},
            {'A2' : {'a' : 21, 'b' : 12}}]
    f_name = 'test_jsonlines'

    save_jsonlines(data, f_name, TEST_FILE_PATH)
    assert os.path.exists(TEST_FILE_PATH / (f_name + '.json'))

def test_load_jsonlines():

    f_name = 'test_jsonlines'
    data = load_jsonlines(f_name, TEST_FILE_PATH)
    assert data
    assert isinstance(data, dict)
    assert isinstance(data[list(data.keys())[0]], dict)

def test_load_jsons_to_df():

    files = ['test_json', 'test_json']
    out = load_jsons_to_df(files, TEST_FILE_PATH)
    assert isinstance(out, pd.DataFrame)
    assert len(out) == len(files)

    # Test giving a file location
    out = load_jsons_to_df(TEST_FILE_PATH)
    assert isinstance(out, pd.DataFrame)

def test_access_h5file():

    f_name = 'test_hdf5'
    h5file = access_h5file(f_name, TEST_FILE_PATH)
    assert h5file
    h5file.close()

def test_open_h5file():

    f_name = 'test_hdf5'
    with open_h5file(f_name, TEST_FILE_PATH) as h5file:
        assert h5file

def test_save_to_h5file():

    tdata = {
        'data1' : np.array([1, 2, 3, 4]),
        'data2' : np.array([1.5, 2.5, 3.5, 4.5]),
    }

    test_fname = 'test_hdf5_saved'

    save_to_h5file(tdata, test_fname, TEST_FILE_PATH)
    assert os.path.exists(TEST_FILE_PATH / (test_fname + '.h5'))

def test_load_from_h5file():

    # Note: this test loads data saved from `test_save_to_h5file`
    f_name = 'test_hdf5_saved'

    # Test loading single field
    dataset = load_from_h5file('data1', f_name, TEST_FILE_PATH)
    assert dataset is not None
    assert np.all(dataset['data1'])

    # Test loading multiple fields
    datasets = load_from_h5file(['data1', 'data2'], f_name, TEST_FILE_PATH)
    assert datasets is not None
    assert np.all(datasets['data1'])
    assert np.all(datasets['data2'])
