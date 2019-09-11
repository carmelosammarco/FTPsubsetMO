from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(name='FTPsubsetMO',
      version='0.0.2',
      description='Python module able to download a file from FTP and subset it using bounding box and variable',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url="https://github.com/carmelosammarco/FTPsubsetMO",
      author='Carmelo Sammarco',
      author_email='sammarcocarmelo@gmail.com',
      license='gpl-3.0',
      python_requires='>=3',

      install_requires=[
        'getpass',
        'ftplib'

      ],

      packages=find_packages(),
      
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3.6',
       ], 

)
