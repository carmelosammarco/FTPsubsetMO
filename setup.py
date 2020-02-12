from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(name='FTPsubsetMO',
      version='0.1.5',
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
        'FTPsubsetMO' : ['DATA/CMEMS_Database.json'],
        'FTPsubsetMO' : ['DATA/LOGO.gif']

      },

      install_requires=[
        'ftputil>=3.4',
        'netCDF4>=1.4.2', 
        'pandas>=0.23.4', 
        'xarray>=0.11.0',
        'json',
        'hdf5',
        'h5py',
        'h5netcdf'


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
