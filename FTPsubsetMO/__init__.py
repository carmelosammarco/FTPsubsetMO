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
import os
import getpass


def FTPds():

    print("<FTPsubsetMO>  Copyright (C) <2019>  <Carmelo Sammarco>")
    print("This program comes with ABSOLUTELY NO WARRANTY")
    print("This is free software, and you are welcome to redistribute it under the GPLv3 conditions.")


    cmems_user = getpass.getpass("Please enter your USERNAME: ")
    cmems_pass = getpass.getpass("Please enter your PASSWORD: ")

    typo = input("Please enter which type of DU --> | NRT | MY |: ")
    pathfiles = input("Please enter the FTP path from /Core/... to the folder where you want to download the file: ")
    filesel = input("Please enter the file name that you wish to Download and then Subset : ")

    print(" ")
    print("Download in progress.. Please wait!")
    print(" ")

    if typo == "NRT" :
        
        ftp = FTP('nrt.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

        #ftp.cwd('/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024/2019/01/')

        ftp.cwd(pathfiles)

        #ftp.retrlines('LIST')

        ftp.retrbinary('RETR' + " " + filesel, open(filesel, 'wb').write)

        print(" ")
        print("The file was downloaded! Now it is time to set the parameter for the subsetting")
        print(" ")

        lon1 = input("Please to insert the West limit: ")
        lon2 = input("Please to insert the East limit: ")
        lat1 = input("Please to insert the Nord limit: ")
        lat2 = input("Please to insert the Sud limit: ")
        var1 = input("Please to insert the variable to extract: ")

        fout = "Subset_" + filesel

        print(" ")
        print("The Subsetting process is starting... ")
        print(" ")

        command = "cdo -sellonlatbox," + lon1 + "," + lon2 + "," + lat1 + "," + lat2 + " " + "-select,name=" + var1 + " " + filesel + " " + fout
        print(command)
        os.system(command)

        os.remove(filesel)

        print(" ")
        print("The subsetting process is completed!")
        print(" ")

        ftp.quit()


    if typo == "MY" :
        
        ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

        #ftp.cwd('/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024/2019/01/')

        ftp.cwd(pathfiles)

        #ftp.retrlines('LIST')

        ftp.retrbinary('RETR' + " " + filesel, open(filesel, 'wb').write)

        print(" ")
        print("The file was downloaded! Now it is time to set the parameter for the subsetting")
        print(" ")

        lon1 = input("Please to insert the West limit: ")
        lon2 = input("Please to insert the East limit: ")
        lat1 = input("Please to insert the Nord limit: ")
        lat2 = input("Please to insert the Sud limit: ")
        var1 = input("Please to insert the variable to extract: ")

        fout = "Subset_" + filesel

        print(" ")
        print("The Subsetting process is starting... ")
        print(" ")

        command = "cdo -sellonlatbox," + lon1 + "," + lon2 + "," + lat1 + "," + lat2 + " " + "-select,name=" + var1 + " " + filesel + " " + fout
        print(command)
        os.system(command)

        os.remove(filesel)

        print(" ")
        print("The subsetting process is completed!")
        print(" ")

        ftp.quit()