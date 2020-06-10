#####################################################################
#Programm author: Carmelo Sammarco
#####################################################################

#< FTPsubsetMO - Python program to download from FTP and subset >
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
import pkg_resources

from ftplib import FTP
import xarray as xr
import netCDF4 as nc
import pandas as pd
import datetime
import os
import json

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext


def main(args=None):
    
    window = Tk()
    
    filejason =  pkg_resources.resource_filename('FTPsubsetMO', 'Database/CMEMS_Database.json')

    window.title("FTPsubsetMO-by_Carmelo_Sammarco")
    #window.geometry('500x600')

    

    def FTPsub():

        ##########################
        # CMEMS LOGIN CREDENTIAL #
        ##########################

        cmems_user = User.get()         
        cmems_pass = Pwd.get() 

        #########################
        # FTP SEARCH PARAMETERS #
        #########################

        pathfiles = FTPlk.get()

        #########################
        # SELECTION TIME WINDOW #
        #########################

        datastart = Ds.get()  
        dataend = De.get()     

        ############################
        # Bounding box information #
        ############################

        bbox = bb.get()  #(YES/NO)

        lon1 = float(lomin.get())     #(WEST)
        lon2 = float(lomax.get())     #(EAST)
        lat1 = float(lamin.get())     #(SOUTH)
        lat2 = float(lamax.get())     #(NORTH)


        #######################
        # SELECTION VARIABLES #
        #######################

        Vs = Vex.get()  #(YES/NO)

        variables = Vexlist.get()
        variableslist = variables.split(',')

        #####################
        # DEPTH INFORMATION #
        #####################

        DL = Dex.get()           #(YES/NO)

        RangeD = Dtype.get()    #(SINGLE/RANGE)

        #For "SINGLE" DEPTH extraction
        depth = sdepth.get()          

        #For "RANGE" DEPTHs extraction
        d1 = Rdepthmin.get()            
        d2 = Rdepthmax.get()

        #################
        # ROOT FOLDER #
        #################
  
        outpath = str(os.getcwd())  

        #########################################################
        # Few important points  before the start of the options #
        #########################################################

        typo = StringVar()
        structure = StringVar()
        ID = StringVar()
        Toidentify = StringVar()
        Pname = StringVar()

        Database = {}
        with open (filejason, "r") as config_file:
            Database = json.load(config_file)
            for key in Database.keys(): 
                if pathfiles in key:
                    #print(pathfiles)
                    
                    listdic = Database.get(pathfiles) 
                    #print(listdic)

                    typo = listdic[0] #(NRT/MY)
                    structure = listdic[1]  #M(monthly)/D(daily)  
                    ID = listdic[2]  #(BACK/FRONT)
                    Toidentify = listdic[3]   #part of the fine name used to select the files  

                    Pname = pathfiles.split("/")[2]

        #########################

        ys, ms, ds = datastart.split('-')
        ye, me, de = dataend.split('-')

        sdata = ys + "-" + ms
        edata = ye + "-" + me

        days = pd.date_range(datastart, dataend, freq='D')
        months = pd.date_range(*(pd.to_datetime([sdata, edata]) + pd.offsets.MonthEnd()), freq='M')


        SPECdatasets = ["/Core/OCEANCOLOUR_ARC_CHL_L4_REP_OBSERVATIONS_009_088/dataset-oc-arc-chl-multi_cci-l4-chl_1km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_ATL_CHL_L4_REP_OBSERVATIONS_009_091/dataset-oc-atl-chl-multi_cci-l4-chl_1km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_BS_CHL_L4_REP_OBSERVATIONS_009_079/dataset-oc-bs-chl-multi_cci-l4-chl_1km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_CHL_L4_REP_OBSERVATIONS_009_082/dataset-oc-glo-chl-multi-l4-gsm_100km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_CHL_L4_REP_OBSERVATIONS_009_082/dataset-oc-glo-chl-multi-l4-gsm_25km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_CHL_L4_REP_OBSERVATIONS_009_082/dataset-oc-glo-chl-multi-l4-gsm_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_CHL_L4_REP_OBSERVATIONS_009_093/dataset-oc-glo-chl-multi_cci-l4-chl_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-bbp443_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-cdm443_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-kd490_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-rrs412_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-rrs443_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-rrs490_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-rrs555_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-rrs670_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-spm_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-zsd_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_MED_CHL_L4_REP_OBSERVATIONS_009_078/dataset-oc-med-chl-multi_cci-l4-chl_1km_monthly-rep-v02/"]

        if lon1 > lon2:
            Crossing = "YES"

            #First request
            w2 = -180
            e2 = lon2
            s2 = lat1
            n2 = lat2

            #Second request
            w1 = lon1
            e1 = 180
            s1 = lat1
            n1 = lat2
        
        elif lon2 > 180:
            Crossing = "YES"

            factor = lon2 - 180
            lonf = float(factor) - 180 
            
            #First request
            w2 = -180
            e2 = lonf
            s2 = lat1
            n2 = lat2

            #Second request
            w1 = lon1
            e1 = 180
            s1 = lat1
            n1 = lat2

        else:
            Crossing = "NO"


        ##########################################################################################################################################
        ##########################################################################################################################################
        # MY DAILY 
        #######################

        #BBOX  
        if typo == "MY" and bbox == "YES" and Vs == "NO" and structure == "D" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for day in days :

                a = day.strftime('%Y')
                m = day.strftime('%m')
                g = day.strftime('%d')

                #########################

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                    
                outpath1 = outpath0 + "/" + str(a)
            
                path2 = os.path.join(outpath1, str(m))

                if not os.path.exists(path2):
                    os.mkdir(path2)

                ###########################

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
                            
                            DS = xr.open_dataset(data)
                        
                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")

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

                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            os.remove(data)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        else:
                            print(" Please to check the bounding box coordinates ")

            os.chdir(outpath)

            ftp.quit()



        #VAR 
        if typo == "MY" and bbox == "NO" and Vs == "YES" and structure == "D" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for day in days :

                a = day.strftime('%Y')
                m = day.strftime('%m')
                g = day.strftime('%d')

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                    
                outpath1 = outpath0 + "/" + str(a)
            
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

                        data = outpath1 + "/" + str(m) + "/" + file_name
                        out1 = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name
                        
                        DS = xr.open_dataset(data)

                        DSVar = DS[variableslist]
                        DSVar.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                        DS.close()

                        os.remove(data)

                        print("File: " + "Subset_" + file_name + " --> Subset completed")
                        print(" ") 

            os.chdir(outpath)                  

            ftp.quit()



        #BBOX + VAR 
        if typo == "MY" and bbox == "YES" and Vs == "YES" and structure == "D" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for day in days :

                a = day.strftime('%Y')
                m = day.strftime('%m')
                g = day.strftime('%d')

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                    
                outpath1 = outpath0 + "/" + str(a)
            
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
                        
                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))

                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")

                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            DS1Var = DS1[variableslist]
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
                        
                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            DS1Var = DS1[variableslist]
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

            os.chdir(outpath)

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

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                    
                outpath1 = outpath0 + "/" + str(a)
            
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
                        
                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))

                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")

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
                            
                            DS1.close()

                            DS2 = xr.open_dataset(out2)

                            DS2Var = DS2[variableslist]
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
                        
                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
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
                            
                            DS1.close()

                            DS2 = xr.open_dataset(out2)

                            DS2Var = DS2[variableslist]
                            DS2Var.to_netcdf(path=out3, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS2.close()

                            os.remove(data)
                            os.remove(out1)
                            os.remove(out2)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

            os.chdir(outpath)

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
                lastd = mon.strftime('%d')

                #################################

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                   
                outpath1 = outpath0 + "/" + str(a)

                ####################################

                if ID == "BACK":
                    look = mon.strftime(Toidentify+'%Y%m')

                elif pathfiles in SPECdatasets:
                    look = mon.strftime('%Y%m'+'01_m_'+'%Y%m%d' + Toidentify)

                else: #FRONT
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
                        
                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))

                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")


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
                        
                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            os.remove(data)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        else:
                            print (" Please to check the bounding box coordinates ")

            os.chdir(outpath)

            ftp.quit() 

        
        #VAR
        elif typo == "MY" and bbox == "NO" and Vs == "YES" and structure == "M" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for mon in months :

                a = mon.strftime('%Y')
                m = mon.strftime('%m')
                lastd = mon.strftime('%d')

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                   
                outpath1 = outpath0 + "/" + str(a)

                if ID == "BACK":
                    look = mon.strftime(Toidentify+'%Y%m')

                elif pathfiles in SPECdatasets:
                    look = mon.strftime('%Y%m'+'01_m_'+'%Y%m%d' + Toidentify)

                else: #FRONT
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

                        data = outpath1 +  "/" + file_name
                        out1 = outpath1 +  "/" + "Subset_" + file_name
                        
                        DS = xr.open_dataset(data)

                        DSVar = DS[variableslist]
                        DSVar.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                        DS.close()

                        os.remove(data)

                        print("File: " + "Subset_" + file_name + " --> Subset completed")
                        print(" ")

            os.chdir(outpath)                                    

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
                lastd = mon.strftime('%d')

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                   
                outpath1 = outpath0 + "/" + str(a)

                if ID == "BACK":
                    look = mon.strftime(Toidentify+'%Y%m')

                elif pathfiles in SPECdatasets:
                    look = mon.strftime('%Y%m'+'01_m_'+'%Y%m%d' + Toidentify)

                else: #FRONT
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
                        
                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))

                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")

                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            DSVar = DS1[variableslist]
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
                        
                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            DS1Var = DS1[variableslist]
                            DS1Var.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS1.close()

                            os.remove(data)
                            os.remove(out1)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        else:
                            print (" Please to check the bounding box coordinates ")

            os.chdir(outpath)

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
                lastd = mon.strftime('%d')

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                   
                outpath1 = outpath0 + "/" + str(a)

                if ID == "BACK":
                    look = mon.strftime(Toidentify+'%Y%m')

                elif pathfiles in SPECdatasets:
                    look = mon.strftime('%Y%m'+'01_m_'+'%Y%m%d' + Toidentify)

                else: #FRONT
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
                        
                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))

                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")

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

                            DS2Var = DS2[variableslist]
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
                            
                            box1 = outpath1 +  "/" + "Box1_" + file_name
                            box2 = outpath1 + "/" +  "Box2_" + file_name

                            
                            DS = xr.open_dataset(data)
                        
                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
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

                            DS2Var = DS2[variableslist]
                            DS2Var.to_netcdf(path=out3, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS2.close()

                            os.remove(data)
                            os.remove(out1)
                            os.remove(out2)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

            os.chdir(outpath)                

            ftp.quit()

       
       
        else:
            print("PROCESS COMPLETED")




    #######################
    #GUI interface
    #######################
   
    Username = Label(window, text="Username")
    Username.grid(column=0, row=0)
    User = Entry(window, width=13)
    User.grid(column=0, row=1)
    ##
    Password = Label(window, text="Password")
    Password.grid(column=1, row=0)
    Pwd = Entry(window, width=13, show="*")
    Pwd.grid(column=1, row=1)
    ##
    space = Label(window, text="")
    space.grid(column=0, row=2)
    space = Label(window, text="")
    space.grid(column=1, row=2)
    ##
    FTPlink = Label(window, text="FTP-URL")
    FTPlink.grid(column=0, row=3)
    FTPlk = Entry(window, width=13)
    FTPlk.grid(column=1, row=3)
    ##
    space = Label(window, text="")
    space.grid(column=1, row=4)
    ##
    Datest = Label(window, text="From(YYYY-MM-DD)")
    Datest.grid(column=0, row=6)
    Ds = Entry(window, width=13)
    Ds.grid(column=1, row=6)
    ##
    Daten = Label(window, text="To(YYYY-MM-DD)")
    Daten.grid(column=0, row=7)
    De = Entry(window, width=13)
    De.grid(column=1, row=7)
    ##
    space = Label(window, text="")
    space.grid(column=0, row=8)
    space = Label(window, text="")
    space.grid(column=1, row=8)
    ##
    boundingb = Label(window, text="Bounding-box?(YES/NO)")
    boundingb.grid(column=0, row=9)
    bb = Entry(window, width=13)
    bb.grid(column=1, row=9)
    ##
    longmin = Label(window, text="Long-min(W)")
    longmin.grid(column=0, row=10)
    lomin = Entry(window, width=8)
    lomin.grid(column=0, row=11)
    ##
    longmax = Label(window, text="Long-max(E)")
    longmax.grid(column=1, row=10)
    lomax = Entry(window, width=8)
    lomax.grid(column=1, row=11)
    ##
    latmin = Label(window, text="Lat-min(S)")
    latmin.grid(column=0, row=12)
    lamin = Entry(window, width=8)
    lamin.grid(column=0, row=13)
    ##
    latmax = Label(window, text="Lat-max(N)")
    latmax.grid(column=1, row=12)
    lamax = Entry(window, width=8)
    lamax.grid(column=1, row=13)
    ##
    space = Label(window, text="")
    space.grid(column=0, row=14)
    space = Label(window, text="")
    space.grid(column=1, row=14)
    ##
    Varex = Label(window, text="Variables?(YES/NO)")
    Varex.grid(column=0, row=15)
    Vex = Entry(window, width=13)
    Vex.grid(column=1, row=15)
    VexY = Label(window, text="Variables(var1,var2,...)")
    VexY.grid(column=0, row=16)
    Vexlist = Entry(window, width=13)
    Vexlist.grid(column=1, row=16)
    ##
    space = Label(window, text="")
    space.grid(column=0, row=17)
    space = Label(window, text="")
    space.grid(column=1, row=17)
    ##
    Depex = Label(window, text="Depths?(YES/NO | SINGLE/RANGE)")
    Depex.grid(column=0, row=18)
    Dex = Entry(window, width=13)
    Dex.grid(column=1, row=18)
    Dtype = Entry(window, width=13)
    Dtype.grid(column=2, row=18)
    ##
    Singledepth = Label(window, text="Single-depth")
    Singledepth.grid(column=0, row=19)
    sdepth = Entry(window, width=13)
    sdepth.grid(column=1, row=19)
    ##
    Rangedepth = Label(window, text="Range-depths(Min|Max)")
    Rangedepth.grid(column=0, row=20)
    Rdepthmin = Entry(window, width=13)
    Rdepthmin.grid(column=1, row=20)
    Rdepthmax = Entry(window, width=13)
    Rdepthmax.grid(column=2, row=20)
    ##
    space = Label(window, text="")
    space.grid(column=0, row=22)
    space = Label(window, text="")
    space.grid(column=1, row=22)
    ##
    
    btn1 = Button(window, text="Download", bg="red", command=FTPsub)
    btn1.grid(column=0, row=23)
    

    #################################################################

    window.mainloop()

