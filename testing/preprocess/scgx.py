from fyords.preprocess.scgx import LlamaLoader
import pandas as pd
import logging




if __name__ == '__main__':

    # should fail because my path isn't default
    print('\nFaulty test:')
    scg = LlamaLoader()

    # correct test
    scg = LlamaLoader(
        scgpath='C:/Users/pryerc/My Repo/Documents/LLamasoft/Supply Chain Guru/',
        modelpath = 'C:/Users/pryerc/My Repo/Documents/LLamasoft/Supply Chain Guru/Puratos/',
        model='puratos-2017-a'
    )

    path = scg.scgpath + '/import-templates/pre-configured/frontend-configured/{}'
    transportation_assets = pd.read_excel(path.format('TransportationAssets.xlsx'))
    scg.stage(transportation_assets, 'TransportationAssets')
