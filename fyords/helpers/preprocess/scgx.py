from os import getlogin, path as ospath
import pandas as pd
import logging

class LlamaStage:
    """Parent class to LlamaLoader. Abstracts the backend vs frontend staging
    differences.
    """
    def __init__(self, config: str='frontend'):
        self.configuration = config
        self.sheets = {
            'frontend': { # TODO: improve
                'TransportationAssets': 'TG_Assets',
                'Customers': 'Customers',
                'Sites': 'Sites',
                'Products': 'Products',
                'Shipments': 'Shipments',
                'AssetAvailability': 'AssetAvailability',
                'Rate': 'Rate',
                'TransportationPaths': 'TGpaths',
                'AdvancedCosting_StepCosts': 'AC_StepCosts',
                'AdvancedCosting_StepCostDefinitions':\
                    'AC_StepCostDefinitions',
                'RelationshipConstraint': 'RelationshipConstraint',
                'CustomerDemand': 'CustomerDemand'
            },
            'backend': {}
        }[config]

class LlamaLoader:
    """Provide assistance to premodeling aligned with an SCGX environment.
    The stage for the data in SCGX can be of two config types. These
    are 'frontend' and 'backend'. The main differences here would be field
    names and pointers. Each Llamaloader instance must be tied to a model by
    self.modelname (model). Initially this object will be developed to
    handle frontend integrations. Abstraction to incorporate backend as
    well will slowly roll out.

    Integrations:
    ------------
    SCGX, Pandas.
    """
    defaultpath = ('C:/Users/{}/Documents/LLamasoft/Supply Chain Guru'
                ).format(getlogin())
    def __init__(self, stage: LlamaStage, model: str='',
    scgpath:str=defaultpath, modelpath:str=defaultpath):
        # TODO: use abstraction to handle backend vs frontend differences.
        self.Stage = stage
        self.configure_scg(model, scgpath, modelpath)

    def configure_scg(self, model: str, scgpath: str, modelpath: str):
        """Configure LlamaLoader to point to an SCGX model stage (dir). Models
        must be found in the self.modelpath which is set here. This is
        currently limited to frontend.

        Parameters
        ----------
        name: name of the scgx model. This is typically the name of the
        .scgm file.
        scgpath: path to Llamasoft/Supply Chain Guru/. import-templates/
        is expected to be located here.
        modelpath: path to dir containing the model (where modelname.scgm
        is located). This defaults to the Supply Chain Guru folder
        (self.scgpath). Standard SCGX practice would be to create a project
        folder at LLamasoft/Supply Chain Guru/ProjectName/ and save the
        project file (.scgp), model file (.scgm), etc. here. With this
        method you could pass the string created from
        self.scgpath+'/ProjectName'.
        """
        print('\nInitiating with paths:\n{}\n{}\n{}'.format(
            scgpath, modelpath, ospath.join(modelpath, model+'.scgm')))
        if ospath.isdir(scgpath) and ospath.isdir(modelpath) \
        and ospath.isfile(ospath.join(modelpath, model+'.scgm')):
            self.scgpath = scgpath.rstrip('/')
            self.modelpath = modelpath.rstrip('/')
            self.modelname = model
        else:
            print('Could not find scgpath, modelpath, and model.')

    def stage(self, df: pd.DataFrame, tablename: str):
        """Stage dataframe to location for SCGX modeling. Templates must be
        saved to self.scgpath/import-templates/ and filenames should be
        stripped to read as just the table name (frontend). You can do this
        by exporting 0 rows of the desired table from inside SCGX. Then
        override the filename to include just the table name.

        Parameters
        ----------
        data: prepared dataframe (columns are aligned)
        tablename: SCGX Tablename (current scope: frontend)
        """
        # load scgx stage template
        print('\nLoading template.')
        template = pd.read_excel('{}/import-templates/{}.xlsx'.format(
            self.scgpath, tablename))
        print('Template loaded: {}'.format(template))

        # populate loaded template w
        template = template.append(df, sort=False)
        print('Template Populated:\nshape:\n{}\nnulls:{}'.format(
            template.shape,
            df.isna().sum() # TODO: do not need to print all columns for
            # template files
            )
        )

        # stage the data to the correct location (frontend)
        importpath = '{}/{}_{}_en.xlsx'.format(
            self.modelpath, self.modelname, tablename)
        template.to_excel(
            importpath,
            sheet_name=self.Stage.sheets[tablename],
            index=False)
        print('Template import stage (destination): {}'.format(importpath))
        print('{} staging finished'.format(tablename))
