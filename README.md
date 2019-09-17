# FTPsubsetMO - FTP subsetting service for Mercator Ocean

[![Build Status](https://travis-ci.com/carmelosammarco/FTPsubsetMO.png)](https://travis-ci.com/carmelosammarco/FTPsubsetMO) [![Build status](https://ci.appveyor.com/api/projects/status/y4glc7d7ccjb8diq?svg=true)](https://ci.appveyor.com/project/carmelosammarco/FTPsubsetMO) [![PyPi](https://img.shields.io/badge/PyPi-Project-yellow.svg)](https://pypi.org/project/FTPsubsetMO/) 

I developed this software while working as [AKKA](https://www.akka-technologies.com) consultant engeneer for the [CMEMS's Service Desk (Copernicus Marine Environment Monitoring Service)](http://marine.copernicus.eu). I was and I am inspired by the Mercator-Ocean's community (users, co-workers, web-forum discussions and many more) which gave me ideas and the motivational power to build this tool. It is the first python application of its kind created inside the CMEMS environment and I hope that with time it will became an ufficial CMEMS tool. The main goals that I wanted to adress were solving the most common user problems as the data-download requests and the netCDF file subsetting using as source the FTP protocol.

Many thanks to visit this page and try this software.

**Carmelo Sammarco**

## Introduction:

Python module able to download files over FTP protocol and then able to subset them using a bounding box and variable selection.

<p align="center">
  <img width="" height="380" src="DATA/FILE">
</p>

## Be aware that:

The tool is in development so it can be possible find bugs, errors and imprecisions. Please to report them if you find one.

## Dependencies:

The dependencies required is listed below:

- [x] cdo>=1.4.0
- [x] ftputil>=3.4

## Installation for Unix users (Linux distros and Mac-OSX systems):

As first things please install [cdo - climate data operator](https://code.mpimet.mpg.de/projects/cdo). It is required to run few functions contained in the python module. You can use the following command:

```
sudo apt-get install cdo
```

Also please consider to install [Anaconda](https://www.anaconda.com) 3.* version (Be aware that to use this software is suggested python ~=3.6). Once the Anaconda bash file (.sh) is downloaded, you can execute it in the terminal using the following command:

```
bash file_installation_Anaconda_downloaded.sh
```

 Furthermore, an update of pip, setuptools and wheels is suggested. You can do it executing the following command:

```
python -m pip install --upgrade pip setuptools wheel
```

After that run the software installation with:

```
pip install FTPsubsetMO
```
we can import the module as:

```
from FTPsubsetMO import FTPds
```
Once the module is imported we can call the interactive download process typing:

```
FTPds()
```
At this point the interactive terminal session  start and it is going to ask in the following order:

- CMEMS Login credentials (Username and Password)
- Which server to use (if multiyear [MY] or Near real time [NRT] )
- The FTP path from /Core.. to where we want to download the file(s)
- Select the type of download to use (download a single file [SINGLE] or all the files inside the directory [ALLDIR])
- The geograpic bounding box that you wish to extract
- The variables that you wish to extract




