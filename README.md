# FTPsubsetMO - FTP subsetting service 

[![Build Status](https://travis-ci.com/carmelosammarco/FTPsubsetMO.png)](https://travis-ci.com/carmelosammarco/FTPsubsetMO) [![Build status](https://ci.appveyor.com/api/projects/status/y4glc7d7ccjb8diq?svg=true)](https://ci.appveyor.com/project/carmelosammarco/FTPsubsetMO) [![PyPi](https://img.shields.io/badge/PyPi-Project-yellow.svg)](https://pypi.org/project/FTPsubsetMO/) 

**I developed this software because motivated to improve my efficiency and productivity. It is just an attemp/idea/prototype and it is not fully optimased or considered stable.**

**Carmelo Sammarco**


## Be aware that:

The tool is in development so it can be possible find bugs, errors and imprecisions. Please to report them if you find one.

In the Database just the MY datasets are avaiable (still missing NRT datasets).

For more detailed information about the MULTI YEAR datasets please to look the [MY_datasets](FTPsubsetMO/Database/datasets_MY.pdf) file.

## Introduction:

Python software which is able to download files over FTP protocol and subset the files retrieved by parameters as time-range, bounding box, variables and single/range Depth levels (below the GUI interface displayed on a Linux system).

<p align="center">
   <img width="400" height="" src="FTPsubsetMO/IMAGES/GUI.png">
</p>

Together with this tool is distribuited a database which store all the information needed to download the files from each datasets (type of data-set (NRT/MY), time steps (DAILY/MONTLY) and other two parameters needed to correctly identify and select the files prior the download. The key value to retrive such information is the FTP URL of the targeted dataset. It was ideated and implemented by me to adress the download automatization. However I really push the Producers to uniform all the data_structure/file_names and Metadata info (which will make easier the database creation/updates).

After the download which uses the python module "ftplib" (The files are downloaded in the same directory where the tool run) all the subsequent analyses are mainly performed with xarray (another python module). Below the full list of dependencies required (They are installed automatically during the installation if not avaiable in the python environment used):

- [x] xarray
- [x] ftputil>=3.4
- [x] netCDF4
- [x] pandas
- [x] datetime
- [x] os
- [x] json
- [x] hdf5
- [x] h5py
- [x] h5netcdf

## What the user needs to input?

1. **CMEMS personal login credential**

- Username
- Password

2. **FTP Link of the dataset** (Our key value to extract from the data-base all the parameters needed to make the Tool works) as example below:

```
/Core/GLOBAL_REANALYSIS_PHY_001_025/global-reanalysis-phy-001-025-monthly/
```

3. **Time range**

- Date start
- Date end

Date format as YYYY-MM-DD also in the case of the MONTHLY dataset where the term "DD" can be set to any real value.


4. **Geographic bounding box** (if interested to subset by geographic area)

5. **Variables name** (if interested in extract a selection rather than all)

6. **Depths** information parameter values (if interested in a SINGLE/RANGE  or all the depths)


## Python module/script installation:

Just type in the terminal/command-prompt:

```
pip install FTPsubsetMO
```

After that you are free to decide if you want to use the GUI interface or exexute it as script. The latter will allow the maximum customization but as cons it is not very user friendly. 

-----

**To use the GUI interface**  just type on terminal/command-prompt:

```
FTPsubsetMO
```

After that just type on the pop upped screen the parameters asked/required. Finally just click on the red download button to start the download/subsetting process.

-----

**To use the program as a script** and then be able to be free in look/modify/customise the code please to:

1. Open the Terminal/command_prompt in the location where you desire download the files or anyway have the script

2. Activate your python environment and import the module:

```
from FTPsubsetMO import script
```
3. Run the function "script" as follow: 

```
script()
```

The above function will allow you to add, in the path folder where you run the command, the files needed  to run the subsetting process in a pure scripting way. "FTPsubsetMO.py" is the only file to modify based on your data request needs. The script's inputs are highlighted with **""**. More information can be found as form of comments in FTPsubsetMO.py script.
