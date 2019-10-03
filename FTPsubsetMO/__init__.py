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

#Import the modules needed
from ftplib import FTP
import xarray as xr
import netCDF4 as nc
import getpass
import os


def FTPcdo4mo():

    print("<FTPsubsetMO>  Copyright (C) <2019>  <Carmelo Sammarco>")
    print("This program comes with ABSOLUTELY NO WARRANTY")
    print("This is free software, and you are welcome to redistribute it under the GPLv3 conditions.")

    cmems_user = getpass.getpass("Please enter your USERNAME: ")
    cmems_pass = getpass.getpass("Please enter your PASSWORD: ")

    typo = input("Please enter the FTP server to use which is based on the product chosen --> | NRT | MY |: ")
    pathfiles = input("Please enter the FTP path from /Core/... to the folder where you want to download the file/files: ")
    dselection = input("Please enter the the type of download  --> | FILE | ALLDIR |: ")

    print(" ")
    print("Now time to set the parameters for the subsetting...")
    print(" ")

    lon1 = input("Please to insert the West limit: ")
    lon2 = input("Please to insert the East limit: ")
    lat1 = input("Please to insert the Sud limit: ")
    lat2 = input("Please to insert the North limit: ")
    variables = input("Please to insert the variables to extract (if more than one please divide them using a comma [var1,var2,var3...]): ")



    #For Near-Real-Time Server

    if typo == "NRT" and dselection == "ALLDIR" :

        print(" ")
        print("Download in progress.. Please wait!")
        print(" ")
        
        ftp = FTP('nrt.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

        ftp.cwd(pathfiles)
        #ftp.retrlines('LIST')
        
        filenames = ftp.nlst()
        for filename in filenames:
            ftp.retrbinary('RETR' + " " + filename, open(filename, 'wb').write)

            print(" ")
            print("The file was downloaded! Now it is time to subset!")
            print(" ")

            fout = "Subset_" + filename

            print(" ")
            print("The Subsetting process is starting... ")
            print(" ")

            command = "cdo -sellonlatbox," + lon1 + "," + lon2 + "," + lat1 + "," + lat2 + " " + "-select,name=" + variables + " " + filename + " " + fout
            print(command)
            os.system(command)

            os.remove(filename)

            print(" ")
            print("The subsetting process is completed!")
            print(" ")

        ftp.quit()

    if typo == "NRT" and dselection == "FILE" :

        filesel = input("Please enter the file name that you wish to Download and then Subset : ")

        print(" ")
        print("Download in progress.. Please wait!")
        print(" ")

        ftp = FTP('nrt.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

        ftp.cwd(pathfiles)
        #ftp.retrlines('LIST')

        ftp.retrbinary('RETR' + " " + filesel, open(filesel, 'wb').write)

        print(" ")
        print("The file was downloaded! Now it is time to subset!")
        print(" ")

        fout = "Subset_" + filesel

        print(" ")
        print("The Subsetting process is starting... ")
        print(" ")

        command = "cdo -sellonlatbox," + lon1 + "," + lon2 + "," + lat1 + "," + lat2 + " " + "-select,name=" + variables + " " + filesel + " " + fout
        print(command)
        os.system(command)

        os.remove(filesel)

        print(" ")
        print("The subsetting process is completed!")
        print(" ")

        ftp.quit()


    #For Multi-year Server

    if typo == "MY" and dselection == "ALLDIR" :

        print(" ")
        print("Download in progress.. Please wait!")
        print(" ")
        
        ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

        ftp.cwd(pathfiles)
        #ftp.retrlines('LIST')
        
        filenames = ftp.nlst()
        for filename in filenames:
            ftp.retrbinary('RETR' + " " + filename, open(filename, 'wb').write)

            print(" ")
            print("The file was downloaded! Now it is time to subset!")
            print(" ")

            fout = "Subset_" + filename

            print(" ")
            print("The Subsetting process is starting... ")
            print(" ")

            command = "cdo -sellonlatbox," + lon1 + "," + lon2 + "," + lat1 + "," + lat2 + " " + "-select,name=" + variables + " " + filename + " " + fout
            print(command)
            os.system(command)

            os.remove(filename)

            print(" ")
            print("The subsetting process is completed!")
            print(" ")

        ftp.quit()

    if typo == "MY" and dselection == "FILE" :

        filesel = input("Please enter the file name that you wish to Download and then Subset : ")

        print(" ")
        print("Download in progress.. Please wait!")
        print(" ")
        
        ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

        ftp.cwd(pathfiles)
        #ftp.retrlines('LIST')

        ftp.retrbinary('RETR' + " " + filesel, open(filesel, 'wb').write)

        print(" ")
        print("The file was downloaded! Now it is time to subset!")
        print(" ")

        fout = "Subset_" + filesel

        print(" ")
        print("The Subsetting process is starting... ")
        print(" ")

        command = "cdo -sellonlatbox," + lon1 + "," + lon2 + "," + lat1 + "," + lat2 + " " + "-select,name=" + variables + " " + filesel + " " + fout
        print(command)
        os.system(command)

        os.remove(filesel)

        print(" ")
        print("The subsetting process is completed... downloading next file!")
        print(" ")

        ftp.quit()


def FTPpy4mo():

    print("<FTPsubsetMO>  Copyright (C) <2019>  <Carmelo Sammarco>")
    print("This program comes with ABSOLUTELY NO WARRANTY")
    print("This is free software, and you are welcome to redistribute it under the GPLv3 conditions.")

    ############################
    print(" ")
    print("## CMEMS LOGIN CREDENTIAL ##")
    print(" ")

    cmems_user = getpass.getpass("USERNAME: ")
    cmems_pass = getpass.getpass("PASSWORD: ")
    print(" ")

    ###########################
    print("## FTP SERVER AND DATASET SELECTION ##")
    print(" ")

    typo = input("FTP server | MY | NRT | : ")
    pathdataset = input("FTP DATASET ADRESS [ex: /Core/GLOBAL_001_024/global-001-024 ] :  ")
    pathfiles = pathdataset + "/"
    print(" ")


    print("## TIME WINDOW ##")
    print(" ")

    yearstart = input("Please input the year of start: ")
    yearend = input("Please input the year of end: ")
    ys = int(yearstart)
    ye = int(yearend)
    yen = int(yearend) + 1 
    listmonths = input("Please input the months as 01 for Jenaury ,02 for Feb... [ex: 01,02,03]: ")
    print(" ")

    ##################################
    #Bounding box information
    #################################
    print("## GEOGRAPHIC BOUNDING BOX ##")
    print(" ")

    lon1 = input("Please input the WEST coordinate limit: ")
    lon2 = input("Please input the EST coordinate limit: ")
    lat1 = input("Please input the SUD coordinate limit: ")
    lat2 = input("Please input the NORD coordinate limit: ")
    print(" ")

    #############################
    #Selected variables
    #############################
    print("## VARIABLES SELECTION ##")
    print(" ")

    listvar = input("Please input the variables that you wish to extract [ex: 'var1','var2',... ]: ")
    variables = [listvar]
    print(" ")

    ##################################
    #Output folder
    #############################
    print("## SET OUTPUT FOLDER ##")
    print(" ")

    out = input("Please input here the output path location: ")

    print(" ")


    ######################################
    #Starting the loop for both MY and NRT 
    ######################################

    if typo == "NRT":

        print(" ")
        print("Connection to the FTP server...")
        
        ftp = FTP('nrt.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

        print("Connection exstabilished and download files in progress..")
        print(" ")
        
        for year in range(ys, yen):

            outpath = out + "/"

            path = os.path.join(outpath, str(year))
            os.mkdir(path)
            print("###########################")
            print ("Year directory '%s' created" %str(year))

            ftp.cwd(pathfiles + str(year) )

            months = [listmonths]

            for month in months:

                outpath1 = outpath + str(year)

                path = os.path.join(outpath1, str(month))
                os.mkdir(path)
                print ("Month directory '%s' created" %str(month))
                print("###########################")
                print(" ")
                
                ftp.cwd(pathfiles + str(year) + "/" + str(month) )

                filenames = ftp.nlst()

                for filename in filenames:

                    os.chdir(outpath1 + "/" + str(month))
                
                    outputfile = outpath1 + "/" + str(month) + "/" + filename
                
                    ftp.retrbinary('RETR' + " " + filename, open(filename, 'wb').write)

                    print("File: " + filename + " --> Download completed")

                    data = outpath1 + "/" + str(month) + "/" + filename
                    out1 = outpath1 + "/" + str(month) + "/" + "Subsetbbox_" + filename
                    out2 = outpath1 + "/" + str(month) + "/" + "Subset_" + filename

                    DS = xr.open_dataset(data)
                
                    DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                    DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4')
                    DS.close()

                    DS1 = xr.open_dataset(out1)

                    DS1bboxv = DS1[variables]
                    DS1bboxv.to_netcdf(path=out2, mode='w', format= 'NETCDF4')
                    DS1.close()
                    
                    os.remove(outputfile)
                    os.remove(out1)

                    print("File: " + "Subset_" + filename + " --> Subset completed")
                    print(" ")

        ftp.quit()


    if typo == "MY":

        print(" ")
        print("Connection to the FTP server...")
        
        ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

        print("Connection exstabilished and download files in progress..")
        print(" ")
        
        for year in range(ys, yen):

            outpath = out + "/"

            path = os.path.join(outpath, str(year))
            os.mkdir(path)
            print("###########################")
            print ("Year directory '%s' created" %str(year))

            ftp.cwd(pathfiles + str(year) )

            months = [listmonths]

            for month in months:

                outpath1 = outpath + str(year)

                path = os.path.join(outpath1, str(month))
                os.mkdir(path)
                print ("Month directory '%s' created" %str(month))
                print("###########################")
                print(" ")
                
                ftp.cwd(pathfiles + str(year) + "/" + str(month) )

                filenames = ftp.nlst()

                for filename in filenames:

                    os.chdir(outpath1 + "/" + str(month))
                
                    outputfile = outpath1 + "/" + str(month) + "/" + filename
                
                    ftp.retrbinary('RETR' + " " + filename, open(filename, 'wb').write)

                    print("File: " + filename + " --> Download completed")

                    data = outpath1 + "/" + str(month) + "/" + filename
                    out1 = outpath1 + "/" + str(month) + "/" + "Subsetbbox_" + filename
                    out2 = outpath1 + "/" + str(month) + "/" + "Subset_" + filename

                    DS = xr.open_dataset(data)
                
                    DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                    DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4')
                    DS.close()

                    DS1 = xr.open_dataset(out1)

                    DS1bboxv = DS1[variables]
                    DS1bboxv.to_netcdf(path=out2, mode='w', format= 'NETCDF4')
                    DS1.close()
                    
                    os.remove(outputfile)
                    os.remove(out1)

                    print("File: " + "Subset_" + filename + " --> Subset completed")
                    print(" ")

        ftp.quit()



