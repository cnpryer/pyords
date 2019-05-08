from fyords.preprocess.scgx import LlamaLoader, LlamaStage
import pandas as pd
import logging




if __name__ == '__main__':

    # correct test
    stage = LlamaStage('frontend')
    scg = LlamaLoader(
        stage=stage,
        scgpath='C:/Users/pryerc/My Repo/Documents/LLamasoft/Supply Chain Guru/',
        modelpath = 'C:/Users/pryerc/My Repo/Documents/LLamasoft/Supply Chain Guru/Puratos/',
        model='puratos-2017-a'
    )

    path = scg.scgpath + '/import-templates/pre-configured/frontend-configured/{}'
    transportation_assets = pd.read_excel(path.format('TransportationAssets.xlsx'))
    scg.stage(transportation_assets, 'TransportationAssets')
