from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(name='FTPsubsetMO',
      version='0.5.6',
      description='Python module able to download a file from FTP and subset it using time-range,bounding-box,variables and depths',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url="https://github.com/carmelosammarco/FTPsubsetMO",
      author='Carmelo Sammarco',
      author_email='sammarcocarmelo@gmail.com',
      license='gpl-3.0',
      python_requires='>=3',
      zip_safe=False,
      platforms='OS Independent',

      include_package_data=True,
      package_data={
        'FTPsubsetMO' : ['Database/CMEMS_Database.json','IMAGES/LOGO.gif','IMAGES/GUI.gif','Script/CMEMS_Database.json','Script/FTPsubsetMO.py','Database/datasets_MY.pdf']

      },

      install_requires=[
        'ftputil>=3.4',
        'netCDF4>=1.4.2', 
        'pandas>=0.23.4', 
        'xarray>=0.11.0',
        'json5>=0.9.1',
        'h5py>=2.10.0',
        'h5netcdf>=0.8.0'


      ],

      packages=find_packages(),

      entry_points={
        'console_scripts':['FTPsubsetMO = FTPsubsetMO.__main__:main']
        
      },
      
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3.6',
       ], 

)
