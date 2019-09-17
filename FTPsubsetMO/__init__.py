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

    typo = input("Please enter the FTP server to use which is based on the product chosen --> | NRT | MY |: ")
    pathfiles = input("Please enter the FTP path from /Core/... to the folder where you want to download the file/files: ")
    dselection = input("Please enter the the type of download  --> | FILE | ALLDIR |: ")

    print(" ")
    print("Now time to set the parameters for the subsetting...")
    print(" ")

    lon1 = input("Please to insert the West limit: ")
    lon2 = input("Please to insert the East limit: ")
    lat1 = input("Please to insert the Nord limit: ")
    lat2 = input("Please to insert the Sud limit: ")
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
