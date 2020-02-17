import pkg_resources
import shutil
import os

forfolder1 =  pkg_resources.resource_filename('FTPsubsetMO', 'Script/CMEMS_Database.json')
forfolder2 =  pkg_resources.resource_filename('FTPsubsetMO', 'Script/FTPsubsetMO.py')


def script():
    outpath = str(os.getcwd())
    shutil.copy(forfolder1, outpath)
    shutil.copy(forfolder2, outpath)