# -*- coding: utf-8 -*-
"""
metropy tutorial #1
basic use, examples using a single metro results file and accessing variables

Created on Tue Nov  3 15:47:20 2020
@author: VanTongeren_F
"""

print('\nThis is the metropy Tutorial #1' )

import os

import pandas as pd

from metro import metropy

pd.options.display.float_format = '{:.3f}'.format
PROJECT_ROOT_DIR = "."
DATA_DIR = "data"
GDX_PATH= os.path.join(PROJECT_ROOT_DIR, DATA_DIR)



#%% examples using a single metro results file and accessing variables

gdx_file = '20_8_7_v10L14_sim_Sim1.gdx'

'''
The first thing to do is to instantiate a metro_results object, tell it where to
find the gdx file and (optionally) add a legend:
'''
s1 = metropy.metro_data('sim1')
s1.path = os.path.join(GDX_PATH, gdx_file)
s1.legend ='Simulation no 1'

'''
The class metro_data() has a property called 'dimensions' which keeps track of
the elements found in the gdx results file.
Let's use this property to see what we have in s1:
'''
print(f'METRO results file {s1.legend}')
print(f'The pieces in the file are: { " ".join(s1.data.keys())}')
print(f'The elements in <results> are:')
for k in s1.dimensions.keys():
    print(f'{"-"*30}\n'
          f'{k}, size: {len(s1.dimensions[k])}\n'
          f'{"-"*30}\n'
          f'{" ".join(s1.dimensions[k])}\n')

'''
Note that s1.data is an orderd dict, and its elements are pandas data frames:
'''
print(f'type(s1.data): {type(s1.data)}\n'
      f'type(s1.data["results"]): {type(s1.data["results"])}')

'''
OK, now lets'access some variable in the results. For this, we use the
metro_data method 'get_variable' on our s1 object:
'''
GDP=s1.get_variable('rGDPEXP')
EXP=s1.get_variable('rEXPORT')
print(f'rGDPEXP:\n {GDP}\nrEXPORT: \n {EXP} \n')

#If we try to call a non-existing variable, we should raise an error:
check= s1.get_variable('check') #raises an error

''' Let's look at variables with multiple dimensions, such as exports:
'''

EXP_cuw=s1.get_variable('QER')
print(f'Straight output for multidimensional variable\nQER:\n {EXP_cuw}\n' )

'''
Make a nice bilateral trade table of only exports in intermediates.
The first step is to fetch the relevant columns and to reset the index that is
automatically created by pandas. Then we can apply the pandas pivot_table method
(you may see a performance warning, that can be igniored for now):
'''
tab=EXP_cuw.loc[:,('value','uint')].reset_index()
tab.columns =[a for a,_ in tab.columns] # get rid of unused level 1 
                                        # in column index
                                        # this avoids perf issues in pivot
print(f"Nicer bilateral trade table\nQER"
      f"{tab.pivot_table('value', index='dim1',columns='dim2')}")

# do this for all use dimensions just so:
for u in s1.dimensions['usecat']:
    tab=EXP_cuw.loc[:,('value',u)].reset_index()
    tab.columns =[a for a,_ in tab.columns] 
    print(f"Bilateral trade use category {u}\n "
          f"{tab.pivot_table('value', index='dim1',columns='dim2')}\n")
