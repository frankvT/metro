#Readme.txt

metro Python package to read OECD METRO gdx results files into pandas and perform common manipulations
version 0.1.0, November 2020

Installation:
the following are necessary
1/ create the python-GAMS bindings by running in the relevant GAMS api directory (depends on your installed python version, 3.6, 3.7, 3.8 and assumes that you have GAMS installed locally at the root directory C:\ ). 
- Open and anaconda command prompt
- Go to "(anaconda3)C:\GAMS\win64\30.2\apifiles\Python\api_37"
- Run: python setup.py install

this should now make teh GAMS-PYTHON API available for the python interpreter on your machine


2/ install the package "gdxpds"  from  https://github.com/NREL/gdx-pandas
there is a'install' button that should work. 
Check out the gdxpds documentation


3/ install the package "metro" on your machine
- put the directory "metro" and all its subdirectories on your system (e.g. G:\my_python\metro)
- to make sure that the python interpreter finds the package from wherever you work it is best to install it as a local package uing pip. This is not necessary, but makes it easier 
  to import the package into your own scripts without having to worry about pathname acrobatics: 
	- open an anaconda command prompt
	- go into the metro directory
	- Run pip install -e .

	This should create all the necessary links in your local python installation so you can import the package and its modules.


	
\metro
|
|
--\metro
|	|
|	|-- __init__.py
|  	|-- metropy.py
|	|-- statstools.py
|
--\tutorials
|	|
|	|--\data
|	|	|
|	|	-- some gdx files and xlsx files
|	|
|	|--\tables
|	|	|
|		-- empty
|
|-- local_metro.egg-info  *** created by pip install *** 
|--	setup.cfg
|-- setup.py
|-- Readme.txt


Tutorials:
There are 4 tutorials that show how to use the package. The tutorials are Python scripts that can be run in a notebook or python development environment, e.g. Spyder or IDLE

Tutorial_1.py: basic use, examples using a single metro results file and accessing variables
Tutorial_2.py: examples using a single metro results file, making summary calculations and user-defined mappings
Tutorial_3.py: writing a dataframe to excel and making a standard table with macro variables
Tutorial_4.py: using multiple METRO results files





