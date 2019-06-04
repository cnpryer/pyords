from fyords.helpers.preprocess.scgx import LlamaLoader, LlamaStage
import pytest
import pandas as pd
import os
import logging



@pytest.mark.skip(reason='no way of currently testing this')
def test_basic_usage():

    # correct test
    stage = LlamaStage('frontend')
    scg = LlamaLoader(
        stage=stage,
        scgpath='C:/Users/pryerc/My Repo/Documents/LLamasoft/Supply Chain Guru/',
        modelpath = 'C:/Users/pryerc/My Repo/Documents/LLamasoft/Supply Chain Guru/Puratos/',
        model='puratos-2017-a')

    path = scg.scgpath + '/import-templates/pre-configured/frontend-configured/{}'
    transportation_assets = pd.read_excel(path.format('TransportationAssets.xlsx'))
    scg.stage(transportation_assets, 'TransportationAssets')
    assert os.path.exists(path[:-2])
