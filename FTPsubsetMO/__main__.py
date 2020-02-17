#####################################################################
#Programm for Mercator Ocean by Carmelo Sammarco
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

    #image = pkg_resources.resource_filename('FTPsubsetMO', 'IMAGES/LOGO.gif')
    filejason =  pkg_resources.resource_filename('FTPsubsetMO', 'Database/CMEMS_Database.json')
    #photo = PhotoImage(file=image)
    #w = photo.width()
    #h = photo.height()
    #cv = Canvas(window, width=w, height=h)
    #cv = Canvas(window)
    #cv.pack(side='top', fill='x')
    #cv.create_image(0,0, image=photo, anchor='nw') 

    tab_control = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control)
    #tab2 = ttk.Frame(tab_control)
    tab_control.add(tab1, text='FTPsubsetter')
    #tab_control.add(tab2, text='netCDF-Manipulation')

    window.title("FTPsubsetMO-by_Carmelo_Sammarco")

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

        lon1 = lomin.get()     #(WEST)
        lon2 = lomax.get()     #EAST)
        lat1 = lamin.get()     #(SOUTH)
        lat2 = lamax.get()     #(NORTH)

        #######################
        # SELECTION VARIABLES #
        #######################

        Vs = Vex.get()  #(YES/NO)

        variables = [Vexlist.get()]     

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
        # OUTPUT FOLDER #
        #################

        #outpath = str(os.getcwd()) + "/"  
        outpath = str(os.getcwd())  

        #########################################################
        # Few important points  before the start of the options #
        #########################################################

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

                    #print(typo)
                    #print(structure)
                    #print(ID)
                    #print(Toidentify)

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




    #######################
    #GUI interface
    #######################
   
    Username = Label(tab1, text="Username")
    Username.grid(column=0, row=0)
    User = Entry(tab1, width=13)
    User.grid(column=0, row=1)
    ##
    Password = Label(tab1, text="Password")
    Password.grid(column=1, row=0)
    Pwd = Entry(tab1, width=13, show="*")
    Pwd.grid(column=1, row=1)
    ##
    space = Label(tab1, text="")
    space.grid(column=0, row=2)
    space = Label(tab1, text="")
    space.grid(column=1, row=2)
    ##
    FTPlink = Label(tab1, text="FTP-URL")
    FTPlink.grid(column=0, row=3)
    FTPlk = Entry(tab1, width=13)
    FTPlk.grid(column=1, row=3)
    ##
    space = Label(tab1, text="")
    space.grid(column=1, row=4)
    ##
    Datest = Label(tab1, text="From(YYYY-MM-DD)")
    Datest.grid(column=0, row=6)
    Ds = Entry(tab1, width=13)
    Ds.grid(column=1, row=6)
    ##
    Daten = Label(tab1, text="To(YYYY-MM-DD)")
    Daten.grid(column=0, row=7)
    De = Entry(tab1, width=13)
    De.grid(column=1, row=7)
    ##
    space = Label(tab1, text="")
    space.grid(column=0, row=8)
    space = Label(tab1, text="")
    space.grid(column=1, row=8)
    ##
    boundingb = Label(tab1, text="Bounding-box?(YES/NO)")
    boundingb.grid(column=0, row=9)
    bb = Entry(tab1, width=13)
    bb.grid(column=1, row=9)
    ##
    longmin = Label(tab1, text="Long-min(W)")
    longmin.grid(column=0, row=10)
    lomin = Entry(tab1, width=8)
    lomin.grid(column=0, row=11)
    ##
    longmax = Label(tab1, text="Long-max(E)")
    longmax.grid(column=1, row=10)
    lomax = Entry(tab1, width=8)
    lomax.grid(column=1, row=11)
    ##
    latmin = Label(tab1, text="Lat-min(S)")
    latmin.grid(column=0, row=12)
    lamin = Entry(tab1, width=8)
    lamin.grid(column=0, row=13)
    ##
    latmax = Label(tab1, text="Lat-max(N)")
    latmax.grid(column=1, row=12)
    lamax = Entry(tab1, width=8)
    lamax.grid(column=1, row=13)
    ##
    space = Label(tab1, text="")
    space.grid(column=0, row=14)
    space = Label(tab1, text="")
    space.grid(column=1, row=14)
    ##
    Varex = Label(tab1, text="Variables?(YES/NO)")
    Varex.grid(column=0, row=15)
    Vex = Entry(tab1, width=13)
    Vex.grid(column=1, row=15)
    VexY = Label(tab1, text="Variables('var1','var2'...)")
    VexY.grid(column=0, row=16)
    Vexlist = Entry(tab1, width=13)
    Vexlist.grid(column=1, row=16)
    ##
    space = Label(tab1, text="")
    space.grid(column=0, row=17)
    space = Label(tab1, text="")
    space.grid(column=1, row=17)
    ##
    Depex = Label(tab1, text="Depths?(YES/NO | SINGLE/RANGE)")
    Depex.grid(column=0, row=18)
    Dex = Entry(tab1, width=13)
    Dex.grid(column=1, row=18)
    Dtype = Entry(tab1, width=13)
    Dtype.grid(column=2, row=18)
    ##
    Singledepth = Label(tab1, text="Single-depth")
    Singledepth.grid(column=0, row=19)
    sdepth = Entry(tab1, width=13)
    sdepth.grid(column=1, row=19)
    ##
    Rangedepth = Label(tab1, text="Range-depths(Min|Max)")
    Rangedepth.grid(column=0, row=20)
    Rdepthmin = Entry(tab1, width=13)
    Rdepthmin.grid(column=1, row=20)
    Rdepthmax = Entry(tab1, width=13)
    Rdepthmax.grid(column=2, row=20)
    ##
    space = Label(tab1, text="")
    space.grid(column=0, row=22)
    space = Label(tab1, text="")
    space.grid(column=1, row=22)
    ##
    
    btn1 = Button(tab1, text="Download", bg="red", command=FTPsub)
    btn1.grid(column=0, row=23)
    

    #################################################################

    tab_control.pack(expand=1, fill='both')

    window.mainloop()

