#####################################################################
#Programm for Mercator Ocean by Carmelo Sammarco
#####################################################################

#< FTPsubsetMO - Script to download from FTP and subset >
#Copyright (C) <2019>  <Carmelo Sammarco - sammarcocarmelo@gmail.com>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################################################################

#########################
# IMPORT MODULES NEEDED #
#########################
from ftplib import FTP
import xarray as xr
import netCDF4 as nc
import pandas as pd
import datetime
import os

import json


##########################
# CMEMS LOGIN CREDENTIAL #
##########################

cmems_user = "#####"          

cmems_pass = "#####"         

#########################
# FTP SEARCH PARAMETERS #
#########################

pathfiles = "#####"

#########################
# SELECTION TIME WINDOW #
#########################

datastart = "####"   
dataend = "####"        

############################
# Bounding box information #
############################

bbox = " "   #(YES/NO)

lon1 =      #(WEST)
lon2 =      #EAST)
lat1 =      #(SOUTH)
lat2 =      #(NORTH)

#######################
# SELECTION VARIABLES #
#######################

Vs = "#####"  #(YES/NO)

variables = ["####","####","####"]     # ex ["uo","vo"]

#####################
# DEPTH INFORMATION #
#####################

DL = "####"            #(YES/NO)

RangeD = "####"    #(SINGLE/RANGE)

#For "SINGLE" DEPTH extraction
depth =           

#For "RANGE" DEPTHs extraction
d1 =             
d2 = 

#################
# OUTPUT FOLDER #
#################

#outpath = str(os.getcwd()) + "/"  
outpath = str(os.getcwd())  

#########################################################
# Few important points  before the start of the options #
#########################################################

Database = {}

with open ("CMEMS_Database.json", "r") as config_file:
    Database = json.load(config_file)
    for key in Database.keys():  
        if pathfiles in key:

            typo = Database.get(pathfiles)[0]  #(NRT/MY)

            structure = Database.get(pathfiles)[1]  #M(monthly)/D(daily)  

            ID = Database.get(pathfiles)[2]  #(BACK/FRONT)

            Toidentify = Database.get(pathfiles)[3]   #part of the fine name used to select the files        

#########################

ys, ms, ds = datastart.split('-')
ye, me, de = dataend.split('-')

ysi=int(ys)
yei=int(ye)
yef = int(yei) + 1

sdata = ys + "-" + ms 
men =  int(me) 
mef = int(men) + 1  
#mef = int(men)
edata = str(ye) + "-" + str(mef)

days = pd.date_range(datastart, dataend, freq='D')
months = pd.date_range(sdata, edata, freq='M')

if lon1 > lon2:
    Crossing = "YES"
else:
    Crossing = "NO"

#First request
w1 = -180
e1 = lon2
s1 = lat1
n1 = lat2

#Second request
w2 = lon1
e2 = 180
s2 = lat1
n2 = lat2

##########################################################################################################################################
##########################################################################################################################################
# MY DAILY 
#######################

#BBOX  
if typo == "MY" and bbox == "YES" and Vs == "NO" and structure == "D" and DL == "NO" :

    print(" ")
    print("Connection to the FTP server...")
    
    ftp = FTP('my.cmems-du.eu', user=User.get(), passwd=Pwd.get())

    print("Connection exstabilished and download files in progress..")
    print(" ")
    
    for day in days :

        a = day.strftime('%Y')
        m = day.strftime('%m')
        g = day.strftime('%d')

        path = os.path.join(outpath, str(a))

        if not os.path.exists(path):
            os.mkdir(path)
            
        #outpath1 = outpath +  str(a)
        outpath1 = outpath + "/" + str(a)
    
        path2 = os.path.join(outpath1, str(m))

        if not os.path.exists(path2):
            os.mkdir(path2)

        if ID == "BACK":
            look = day.strftime(Toidentify+'%Y%m%d')
        else:
            look = day.strftime('%Y%m%d'+ Toidentify)
        
        #ftp.cwd(pathfiles + str(a) + "/" + str(m))
        ftp.cwd(pathfiles + str(a) + "/" + str(m))

        filenames = ftp.nlst()

        files = pd.Series(filenames)

        for file_name in files[files.str.contains(look)]:

            os.chdir(outpath1 + "/" + str(m))
            outputfile = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name

            if os.path.isfile(outputfile):
                print ("File: " + "Subset_" + file_name + " --> File already processed")
            else:
        
                ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)

                print("File: " + file_name + " --> Download completed")

                if Crossing == "NO":

                    data = outpath1 + "/" + str(m) + "/" + file_name
                    out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                    
                    DS = xr.open_dataset(data)
                
                    DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                    DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS.close()

                    os.remove(data)

                    print("File: " + "Subset_" + file_name + " --> Subset completed")
                    print(" ")

                elif Crossing == "YES":

                    data = outpath1 + "/" + str(m) + "/" + file_name
                    out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                    
                    box1 = outpath1 + "/" + str(m) + "/" + "Box1_" + file_name
                    box2 = outpath1 + "/" + str(m) + "/" + "Box2_" + file_name
                    
                    DS = xr.open_dataset(data)
                
                    DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                    DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')

                    DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                    DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                    DSbbox = xr.merge([DSbbox1,DSbbox2])
                    DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS.close()

                    os.remove(data)
                    os.remove(box1)
                    os.remove(box2)

                    print("File: " + "Subset_" + file_name + " --> Subset completed")
                    print(" ")

                else:
                    print(" Please to check the bounding box coordinates ")

    ftp.quit()



#BBOX + VAR 
if typo == "MY" and bbox == "YES" and Vs == "YES" and structure == "D" and DL == "NO" :

    print(" ")
    print("Connection to the FTP server...")
    
    ftp = FTP('my.cmems-du.eu', user=User.get(), passwd=Pwd.get())

    print("Connection exstabilished and download files in progress..")
    print(" ")
    
    for day in days :

        a = day.strftime('%Y')
        m = day.strftime('%m')
        g = day.strftime('%d')

        path = os.path.join(outpath, str(a))

        if not os.path.exists(path):
            os.mkdir(path)
            
        #outpath1 = outpath +  str(a)
        outpath1 = outpath + "/" + str(a)
    
        path2 = os.path.join(outpath1, str(m))

        if not os.path.exists(path2):
            os.mkdir(path2)

        if ID == "BACK":
            look = day.strftime(Toidentify+'%Y%m%d')
        else:
            look = day.strftime('%Y%m%d'+ Toidentify)
        
        #ftp.cwd(pathfiles + str(a) + "/" + str(m))
        ftp.cwd(pathfiles + str(a) + "/" + str(m))

        filenames = ftp.nlst()

        files = pd.Series(filenames)

        for file_name in files[files.str.contains(look)]:

            os.chdir(outpath1 + "/" + str(m))
            outputfile = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name

            if os.path.isfile(outputfile):
                print ("File: " + "Subset_" + file_name + " --> File already processed")
            else:
        
                ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)

                print("File: " + file_name + " --> Download completed")

                if Crossing == "NO":

                    data = outpath1 + "/" + str(m) + "/" + file_name
                    out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                    out2 = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name
                    
                    DS = xr.open_dataset(data)
                
                    DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                    DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS.close()

                    DS1 = xr.open_dataset(out1)

                    DS1Var = DS1[variables]
                    DS1Var.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS1.close()

                    os.remove(data)
                    os.remove(out1)

                    print("File: " + "Subset_" + file_name + " --> Subset completed")
                    print(" ")

                elif Crossing == "YES":

                    data = outpath1 + "/" + str(m) + "/" + file_name
                    out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                    out2 = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name
                    
                    box1 = outpath1 + "/" + str(m) + "/" + "Box1_" + file_name
                    box2 = outpath1 + "/" + str(m) + "/" + "Box2_" + file_name
                    
                    DS = xr.open_dataset(data)
                
                    DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                    DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')

                    DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                    DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                    DSbbox = xr.merge([DSbbox1,DSbbox2])
                    DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS.close()


                    DS1 = xr.open_dataset(out1)

                    DS1Var = DS1[variables]
                    DS1Var.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS1.close()

                    os.remove(data)
                    os.remove(out1)
                    os.remove(box1)
                    os.remove(box2)

                    print("File: " + "Subset_" + file_name + " --> Subset completed")
                    print(" ")

                else:
                    print(" Please to check the bounding box coordinates ")

    ftp.quit()



#BBOX + VAR + DEPTH 
elif typo == "MY" and bbox == "YES" and Vs == "YES" and structure == "D" and DL == "YES" :

    print(" ")
    print("Connection to the FTP server...")
    
    ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

    print("Connection exstabilished and download files in progress..")
    print(" ")
    
    for day in days :

        a = day.strftime('%Y')
        m = day.strftime('%m')
        g = day.strftime('%d')

        path = os.path.join(outpath, str(a))

        if not os.path.exists(path):
            os.mkdir(path)
            
        #outpath1 = outpath +  str(a)
        outpath1 = outpath + "/" + str(a)
    
        path2 = os.path.join(outpath1, str(m))

        if not os.path.exists(path2):
            os.mkdir(path2)

        if ID == "BACK":
            look = day.strftime(Toidentify+'%Y%m%d')
        else:
            look = day.strftime('%Y%m%d'+ Toidentify)

        ftp.cwd(pathfiles + str(a) + "/" + str(m))

        filenames = ftp.nlst()

        files = pd.Series(filenames)

        for file_name in files[files.str.contains(look)]:

            os.chdir(outpath1 + "/" + str(m))
            outputfile = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name

            if os.path.isfile(outputfile):
                print ("File: " + "Subset_" + file_name + " --> File already processed")
            else:
        
                ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)

                print("File: " + file_name + " --> Download completed")

                if Crossing == "NO":

                    data = outpath1 + "/" + str(m) + "/" + file_name
                    out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                    out2 = outpath1 + "/" + str(m) + "/" + "SubsetDepth_" + file_name
                    out3 = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name
                    
                    DS = xr.open_dataset(data)
                
                    DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                    DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS.close()

                    DS1 = xr.open_dataset(out1)

                    if RangeD == "SINGLE" :
                        DSdepth = DS1.sel(depth=int(depth), method="nearest")
                        DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                        DS1.close()
                    else:
                        DSdepth = DS1.sel(depth=slice(float(d1),float(d2)))
                        DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                        DS1.close()

                    DS2 = xr.open_dataset(out2)

                    DS2Var = DS2[variables]
                    DS2Var.to_netcdf(path=out3, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS2.close()

                    os.remove(data)
                    os.remove(out1)
                    os.remove(out2)

                    print("File: " + "Subset_" + file_name + " --> Subset completed")
                    print(" ")

                else:

                    data = outpath1 + "/" + str(m) + "/" + file_name
                    out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                    out2 = outpath1 + "/" + str(m) + "/" + "SubsetDepth_" + file_name
                    out3 = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name
                    
                    box1 = outpath1 + "/" + str(m) + "/" + "Box1_" + file_name
                    box2 = outpath1 + "/" + str(m) + "/" + "Box2_" + file_name
                    
                    DS = xr.open_dataset(data)
                
                    DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                    DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')

                    DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                    DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                    DSbbox = xr.merge([DSbbox1,DSbbox2])
                    DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS.close()

                    DS1 = xr.open_dataset(out1)

                    if RangeD == "SINGLE" :
                        DSdepth = DS1.sel(depth=int(depth), method="nearest")
                        DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                        DS1.close()
                    else:
                        DSdepth = DS1.sel(depth=slice(float(d1),float(d2)))
                        DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                        DS1.close()

                    DS2 = xr.open_dataset(out2)

                    DS2Var = DS2[variables]
                    DS2Var.to_netcdf(path=out3, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS2.close()

                    os.remove(data)
                    os.remove(out1)
                    os.remove(out2)
                    os.remove(box1)
                    os.remove(box2)

                    print("File: " + "Subset_" + file_name + " --> Subset completed")
                    print(" ")

    ftp.quit()




##########################################################################################################################################
##########################################################################################################################################
# MY - MONTHLY 
#######################


#BBOX 
elif typo == "MY" and bbox == "YES" and Vs == "NO" and structure == "M" and DL == "NO" :

    print(" ")
    print("Connection to the FTP server...")
    
    ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

    print("Connection exstabilished and download files in progress..")
    print(" ")
    
    for mon in months :

        a = mon.strftime('%Y')
        m = mon.strftime('%m')

        path = os.path.join(outpath, str(a))

        if not os.path.exists(path):
            os.mkdir(path)
            
        outpath1 = outpath + "/" + str(a)

        if ID == "BACK":
            look = mon.strftime(Toidentify+'%Y%m')
        else:
            look = mon.strftime('%Y%m'+ Toidentify)

        ftp.cwd(pathfiles + str(a))

        filenames = ftp.nlst()

        files = pd.Series(filenames)

        for file_name in files[files.str.contains(look)]:

            os.chdir(outpath1)
            outputfile = outpath1 + "/"  + "Subset_" + file_name

            if os.path.isfile(outputfile):
                print ("File: " + "Subset_" + file_name + " --> File already processed")
            
            else:
                ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)
                print("File: " + file_name + " --> Download completed")

                if Crossing == "NO":

                    data = outpath1 +  "/" + file_name
                    out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                    
                    DS = xr.open_dataset(data)
                
                    DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                    DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS.close()

                    os.remove(data)
                    

                    print("File: " + "Subset_" + file_name + " --> Subset completed")
                    print(" ")
                
                elif Crossing == "YES":

                    data = outpath1 +  "/" + file_name
                    out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                    
                    box1 = outpath1 +  "/" + "Box1_" + file_name
                    box2 = outpath1 + "/" +  "Box2_" + file_name
                    
                    DS = xr.open_dataset(data)
                
                    DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                    DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')

                    DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                    DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                    DSbbox = xr.merge([DSbbox1,DSbbox2])
                    DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS.close()

                    os.remove(data)
                    os.remove(box1)
                    os.remove(box2)

                    print("File: " + "Subset_" + file_name + " --> Subset completed")
                    print(" ")

                else:
                    print (" Please to check the bounding box coordinates ")

    ftp.quit() 



#BBOX + VAR
elif typo == "MY" and bbox == "YES" and Vs == "YES" and structure == "M" and DL == "NO" :

    print(" ")
    print("Connection to the FTP server...")
    
    ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

    print("Connection exstabilished and download files in progress..")
    print(" ")
    
    for mon in months :

        a = mon.strftime('%Y')
        m = mon.strftime('%m')

        path = os.path.join(outpath, str(a))

        if not os.path.exists(path):
            os.mkdir(path)
            
        outpath1 = outpath + "/" + str(a)

        if ID == "BACK":
            look = mon.strftime(Toidentify+'%Y%m')
        else:
            look = mon.strftime('%Y%m'+ Toidentify)

        ftp.cwd(pathfiles + str(a))

        filenames = ftp.nlst()

        files = pd.Series(filenames)

        for file_name in files[files.str.contains(look)]:

            os.chdir(outpath1)
            outputfile = outpath1 + "/"  + "Subset_" + file_name

            if os.path.isfile(outputfile):
                print ("File: " + "Subset_" + file_name + " --> File already processed")
            
            else:
                ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)
                print("File: " + file_name + " --> Download completed")

                if Crossing == "NO":

                    data = outpath1 +  "/" + file_name
                    out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                    out2 = outpath1 +  "/" + "Subset_" + file_name
                    
                    DS = xr.open_dataset(data)
                
                    DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                    DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS.close()

                    DS1 = xr.open_dataset(out1)

                    DSVar = DS1[variables]
                    DSVar.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS1.close()

                    os.remove(data)
                    os.remove(out1)

                    print("File: " + "Subset_" + file_name + " --> Subset completed")
                    print(" ")
                
                elif Crossing == "YES":

                    data = outpath1 +  "/" + file_name
                    out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                    out2 = outpath1 +  "/" + "Subset_" + file_name
                    
                    box1 = outpath1 +  "/" + "Box1_" + file_name
                    box2 = outpath1 + "/" +  "Box2_" + file_name
                    
                    DS = xr.open_dataset(data)
                
                    DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                    DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')

                    DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                    DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                    DSbbox = xr.merge([DSbbox1,DSbbox2])
                    DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS.close()

                    DS1 = xr.open_dataset(out1)

                    DSVar = DS1[variables]
                    DSVar.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS1.close()

                    os.remove(data)
                    os.remove(out1)
                    os.remove(box1)
                    os.remove(box2)

                    print("File: " + "Subset_" + file_name + " --> Subset completed")
                    print(" ")

                else:
                    print (" Please to check the bounding box coordinates ")

    ftp.quit() 




#BBOX + VAR + DEPTH
elif typo == "MY" and bbox == "YES" and Vs == "YES" and structure == "M" and DL == "YES":

    print(" ")
    print("Connection to the FTP server...")
    
    ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

    print("Connection exstabilished and download files in progress..")
    print(" ")
    
    for mon in months :

        a = mon.strftime('%Y')
        m = mon.strftime('%m')

        path = os.path.join(outpath, str(a))

        if not os.path.exists(path):
            os.mkdir(path)
            
        #outpath1 = outpath +  str(a)
        outpath1 = outpath + "/" + str(a)

        if ID == "BACK":
            look = mon.strftime(Toidentify+'%Y%m')
        else:
            look = mon.strftime('%Y%m'+ Toidentify)

        ftp.cwd(pathfiles + str(a))

        filenames = ftp.nlst()

        files = pd.Series(filenames)

        for file_name in files[files.str.contains(look)]:

            os.chdir(outpath1)
            outputfile = outpath1 + "/"  + "Subset_" + file_name

            if os.path.isfile(outputfile):
                print ("File: " + "Subset_" + file_name + " --> File already processed")
            else:
        
                ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)

                print("File: " + file_name + " --> Download completed")

                if Crossing == "NO":

                    data = outpath1 +  "/" + file_name
                    out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                    out2 = outpath1 +  "/" + "SubsetDepth_" + file_name
                    out3 = outpath1 +  "/" + "Subset_" + file_name
                    
                    DS = xr.open_dataset(data)
                
                    DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                    DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS.close()

                    DS1 = xr.open_dataset(out1)

                    if RangeD == "SINGLE" :
                        DSdepth = DS1.sel(depth=int(depth), method="nearest")
                        DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                        DS1.close()
                    else:
                        DSdepth = DS1.sel(depth=slice(float(d1),float(d2)))
                        DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                        DS1.close()

                    DS2 = xr.open_dataset(out2)

                    DS2Var = DS2[variables]
                    DS2Var.to_netcdf(path=out3, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS2.close()

                    os.remove(data)
                    os.remove(out1)
                    os.remove(out2)

                    print("File: " + "Subset_" + file_name + " --> Subset completed")
                    print(" ")

                else:

                    data = outpath1 +  "/" + file_name
                    out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                    out2 = outpath1 +  "/" + "SubsetDepth_" + file_name
                    out3 = outpath1 +  "/" + "Subset_" + file_name
                    
                    box1 = outpath1 + "/" + str(m) + "/" + "Box1_" + file_name
                    box2 = outpath1 + "/" + str(m) + "/" + "Box2_" + file_name
                    
                    DS = xr.open_dataset(data)
                
                    DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                    DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')

                    DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                    DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                    DSbbox = xr.merge([DSbbox1,DSbbox2])
                    DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS.close()

                    DS1 = xr.open_dataset(out1)

                    if RangeD == "SINGLE" :
                        DSdepth = DS1.sel(depth=int(depth), method="nearest")
                        DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                        DS1.close()
                    else:
                        DSdepth = DS1.sel(depth=slice(float(d1),float(d2)))
                        DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                        DS1.close()

                    DS2 = xr.open_dataset(out2)

                    DS2Var = DS2[variables]
                    DS2Var.to_netcdf(path=out3, mode='w', format= 'NETCDF4', engine='h5netcdf')
                    DS2.close()

                    os.remove(data)
                    os.remove(out1)
                    os.remove(out2)
                    os.remove(box1)
                    os.remove(box2)

                    print("File: " + "Subset_" + file_name + " --> Subset completed")
                    print(" ")

    ftp.quit()



else:
    print("test version")