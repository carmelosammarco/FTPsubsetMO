# FTPsubsetMO - FTP subsetting service for Mercator Ocean

[![Build Status](https://travis-ci.com/carmelosammarco/FTPsubsetMO.png)](https://travis-ci.com/carmelosammarco/FTPsubsetMO) [![Build status](https://ci.appveyor.com/api/projects/status/y4glc7d7ccjb8diq?svg=true)](https://ci.appveyor.com/project/carmelosammarco/FTPsubsetMO) [![PyPi](https://img.shields.io/badge/PyPi-Project-yellow.svg)](https://pypi.org/project/FTPsubsetMO/) 

I developed this software while working as [AKKA](https://www.akka-technologies.com) consultant engeneer for the [CMEMS's Service Desk (Copernicus Marine Environment Monitoring Service)](http://marine.copernicus.eu). I was and I am inspired by the Mercator-Ocean's community (users, co-workers, web-forum discussions and many more) which gave me ideas and the motivational power to build this tool. It is the first python application of its kind created inside the CMEMS environment and I hope that with time it will became an ufficial CMEMS tool. The main goals that I wanted to adress were solving the most common user problems as the data-download requests and the netCDF file subsetting using as source the FTP protocol.

Many thanks to visit this page and try this software.

**Carmelo Sammarco**


## Be aware that:

The tool is in development so it can be possible find bugs, errors and imprecisions. Please to report them if you find one.

## Introduction:

Python software able to download files over FTP protocol and then able to subset the files retrieved by time-range, bounding box, variable and single/range Depth levels.

<p align="center">
   <img width="400" height="" src="FTPsubsetMO/IMAGES/GUI.png">
</p>

Together with this tool is distribuited a database which store all the information needed to download the files from each datasets (type of data-set (NRT/MY), time steps (DAILY/MONTLY) and other two parameters needed to correctly identify and select the files prior the download. The key value to retrive such information is the FTP URL of the targeted dataset. 

After the download using the python module "ftplib" (The files will be downloaded in the same directory where the tool run) all the subsequent analyses are mainly performed with xarray (another python module). Below the full list of dependencies required (which are installed automatically during the installation):

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

1. CMEMS personal login credential

2. FTP Link of the dataset (Our key value to extract from the data-base all the parameters needed to make the Tool works)

3. Time range

4. Geographic bounding box (if interested to subset by geographic area)

5. Variables name (if interested in extract a selection rather than all)

6. Depths information parameter values (if interested in a single o range of depths or all depths)


## Installation:

Just type in the terminal/command-prompt:

```
pip install FTPsubsetMO
```

To run the tool just type on terminal/command-prompt:

```
FTPsubsetMO
```
