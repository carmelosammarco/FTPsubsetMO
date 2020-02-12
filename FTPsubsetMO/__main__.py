#####################################################################
#Programm for Mercator Ocean by Carmelo Sammarco
#####################################################################

#< FTPsubsetMO - Interactive terminal session to download from FTP and subset >
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

    image = pkg_resources.resource_filename('FTPsubsetMO', 'DATA/LOGO.gif')
    photo = PhotoImage(file=image)
    w = photo.width()
    h = photo.height()
    cv = Canvas(window, width=w, height=h)
    cv.pack(side='top', fill='x')
    cv.create_image(0,0, image=photo, anchor='nw') 

    tab_control = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab1, text='FTPsubsetter')
    tab_control.add(tab2, text='netCDF-Manipulation')

    window.title("FTPsubsetter-by-Carmelo-Sammarco")


    #################
    #FTP function to download
    #################

    def FTPsub():

        ##########################
        # CMEMS LOGIN CREDENTIAL #
        ##########################

        cmems_user = ""          

        cmems_pass = ""         

        #########################
        # FTP SEARCH PARAMETERS #
        #########################

        pathfiles = "/Core/GLOBAL_REANALYSIS_PHY_001_025/global-reanalysis-phy-001-025-monthly/"

        #########################
        # SELECTION TIME WINDOW #
        #########################

        datastart = "2013-12-29"   
        dataend = "2014-01-01"        

        ############################
        # Bounding box information #
        ############################

        bbox = "YES"   #(YES/NO)

        lon1 = -170     #(WEST)
        lon2 = -150    #EAST)
        lat1 = -10     #(SOUTH)
        lat2 = 10      #(NORTH)

        #######################
        # SELECTION VARIABLES #
        #######################

        Vs = "YES"  #(YES/NO)

        variables = ["u","v"]     

        #####################
        # DEPTH INFORMATION #
        #####################

        DL = "YES"            #(YES/NO)

        RangeD = "RANGE"    #(SINGLE/RANGE)

        #For "SINGLE" DEPTH extraction
        depth = 100          

        #For "RANGE" DEPTHs extraction
        d1 = 100             
        d2 = 200

        #################
        # OUTPUT FOLDER #
        #################

        #outpath = str(os.getcwd()) + "/"  
        outpath = str(os.getcwd())  

        #########################################################
        # Few important points  before the start of the options #
        #########################################################

        ds = StringVar()
        de = StringVar()
        ysi = StringVar()
        yef = StringVar()
        g = StringVar()

        filejason =  pkg_resources.resource_filename('FTPsubsetMO', 'DATA/CMEMS_Database.json')

        Database = {}

        with open (filejason, "r") as config_file:
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
        ##########################################################################################################################################


        #######################
        # MY DAILY BBOX + VAR #
        #######################

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

        ###############################
        # MY DAILY BBOX + VAR + DEPTH #
        ###############################  

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

        ###############################################################################################################################
        ###############################################################################################################################

        #########################
        # MY MONTHLY BBOX + VAR #
        #########################

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

        #################################
        # MY MONTHLY BBOX + VAR + DEPTH #
        #################################

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

    #######################
    #GUI interface
    #######################
   
    Username1 = Label(tab1, text="Username")
    Username1.grid(column=0, row=0)
    User1 = Entry(tab1, width=13)
    User1.grid(column=0, row=1)
    ##
    Password1 = Label(tab1, text="Password")
    Password1.grid(column=1, row=0)
    Pwd1 = Entry(tab1, width=13, show="*")
    Pwd1.grid(column=1, row=1)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=2)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=2)
    ##
    Product1 = Label(tab1, text="Product")
    Product1.grid(column=0, row=3)
    Pd1 = Entry(tab1, width=13)
    Pd1.grid(column=0, row=4)
    ##
    Dataset1 = Label(tab1, text="Dataset")
    Dataset1.grid(column=1, row=3)
    Ds1 = Entry(tab1, width=13)
    Ds1.grid(column=1, row=4)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=5)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=5)
    ##
    longmin1 = Label(tab1, text="Long min")
    longmin1.grid(column=0, row=6)
    lomin1 = Entry(tab1, width=13)
    lomin1.grid(column=0, row=7)
    ##
    longmax1 = Label(tab1, text="Long max")
    longmax1.grid(column=1, row=6)
    lomax1 = Entry(tab1, width=13)
    lomax1.grid(column=1, row=7)
    ##
    latmin1 = Label(tab1, text="Lat min")
    latmin1.grid(column=0, row=8)
    lamin1 = Entry(tab1, width=13)
    lamin1.grid(column=0, row=9)
    ##
    latmax1 = Label(tab1, text="Lat max")
    latmax1.grid(column=1, row=8)
    lamax1 = Entry(tab1, width=13)
    lamax1.grid(column=1, row=9)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=10)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=10)
    ##
    depthmin1 = Label(tab1, text="Depth min")
    depthmin1.grid(column=0, row=11)
    dmin1 = Entry(tab1, width=13)
    dmin1.grid(column=0, row=12)
    ##
    depthmax1 = Label(tab1, text="Depth max")
    depthmax1.grid(column=1, row=11)
    dmax1 = Entry(tab1, width=13)
    dmax1.grid(column=1, row=12)
    ##
    space1 = Label(tab1, text=" ")
    space1.grid(column=0, row=13)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=13)
    ##
    stardate1 = Label(tab1, text="From date: YYYY-MM-DD")
    stardate1.grid(column=0, row=14)
    sd1 = Entry(tab1, width=13)
    sd1.grid(column=0, row=15)
    ##
    enddate1 = Label(tab1, text="To date: YYYY-MM-DD")
    enddate1.grid(column=1, row=14)
    ed1 = Entry(tab1, width=13)
    ed1.grid(column=1, row=15)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=16)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=16)
    ##
    hourdate1 = Label(tab1, text="From time: HH:MM:SS")
    hourdate1.grid(column=0, row=17)
    hhstartentry = Entry(tab1, width=13)
    hhstartentry.grid(column=0, row=18)
    ##
    houredate1 = Label(tab1, text="To time: HH:MM:SS")
    houredate1.grid(column=1, row=17)
    hhendentry = Entry(tab1, width=13)
    hhendentry.grid(column=1, row=18)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=19)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=19)
    ##
    Variable1 = Label(tab1, text="Variable-1")
    Variable1.grid(column=0, row=20)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=21)
    ##
    Variable2 = Label(tab1, text="Variable-2")
    Variable2.grid(column=0, row=22)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=23)
    ##
    Variable3 = Label(tab1, text="Variable-3")
    Variable3.grid(column=0, row=24)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=25)

    ##
    V11 = Entry(tab1, width=13)
    V11.grid(column=1, row=20)

    V12 = Entry(tab1, width=13)
    V12.grid(column=1, row=22)

    V13 = Entry(tab1, width=13)
    V13.grid(column=1, row=24)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=25)
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=25)
    ##
    filename1 = Label(tab1, text="File name")
    filename1.grid(column=0, row=26)
    fname1 = Entry(tab1, width=13)
    fname1.grid(column=1, row=26)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=27)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=27)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=28)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=28)
    #
    btn1 = Button(tab1, text="Link-NRT", bg="green", command=FTPsub)
    btn1.grid(column=1, row=29)
    ##
    btn1 = Button(tab1, text="Link-MY", bg="green", command=FTPsub)
    btn1.grid(column=1, row=30)
    ##
    txt1 = scrolledtext.ScrolledText(tab1,width=45,height=10)
    txt1.grid(column=1,row=31)
    ##
    Out1 = Button(tab1, text="Out-DIR", bg="yellow", command=FTPsub)
    Out1.grid(column=0, row=31)
    ##
    btn1 = Button(tab1, text="Clean-link", bg="white", command=FTPsub)
    btn1.grid(column=1, row=32)
    ##
    btn1 = Button(tab1, text="Download Single-file", bg="red", command=FTPsub)
    btn1.grid(column=0, row=33)
    ##
    btn1 = Button(tab1, text="Download Montly", bg="red", command=FTPsub)
    btn1.grid(column=0, row=34)
    ###
    btn1 = Button(tab1, text="Download Daily", bg="red", command=FTPsub)
    btn1.grid(column=0, row=35)
    ###
    btn1 = Button(tab1, text="Download by Depths", bg="red", command=main)
    btn1.grid(column=0, row=36)
    ###
    btn1 = Button(tab1, text="Download by Month&Depth", bg="red", command=main)
    btn1.grid(column=0, row=37)
    ###
    btn1 = Button(tab1, text="Download by Years", bg="red", command=main)
    btn1.grid(column=0, row=38)
    ###
    

    #################################################################

    tab_control.pack(expand=1, fill='both')

    window.mainloop()

