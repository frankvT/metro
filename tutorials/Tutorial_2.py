# -*- coding: utf-8 -*-
"""
metropy tutorial #2
examples using a single metro results file, making summary calculations and
user-defined mappings

Created on Tue Nov  3 16:42:14 2020
@author: VanTongeren_F
"""


print('\nThis is the metropy Tutorial #2' )
import os

import pandas as pd

from metro import metropy

pd.options.display.float_format = '{:.3f}'.format
PROJECT_ROOT_DIR = "."
DATA_DIR = "data"
GDX_PATH= os.path.join(PROJECT_ROOT_DIR, DATA_DIR)



#%% Set up where tutorial #1 ended: retrieved an exports matrix

gdx_file =      '20_8_7_v10L14_sim_Sim1.gdx'

'''
The first thing to do is to instantiate a metro_results object, tell it where to
find the gdx file and (optionally) add a legend:
'''
s1 = metropy.metro_data('sim1')
s1.path = os.path.join(GDX_PATH, gdx_file)
s1.legend ='Simulation no 1'

EXP_cuw=s1.get_variable('QER')

'''
Let's make some summary calculations over columns of the exports matrix,
using pandas built in methods. First, let's inspect the structure of that
dataframe:
'''
print(EXP_cuw.head())

'''
If we groupby one column, we can calculate summatry statistics over the others:
'''
EXP_cuw.groupby(level='dim1').sum()  # aggregate over wReg and commodities
EXP_cuw.groupby(level='dim1').mean() # can also use other agg funcs
EXP_cuw.groupby(level='dim4').sum()  # aggregate over r and w

'''
We can add row and column totals to the dataframe by calls to metropy helper
functions (methods).
The next call creates a new dataframe with column totals, called 'WORLD'
The one after that creates a new dataframe with row totals, called 'TOTAL', which
is the default when no label is provided:
'''
print(f'Column totals added:\n {metropy.add_ctotal(EXP_cuw, "WORLD")}' )
print(f'Row totals added:\n {metropy.add_rtotal(EXP_cuw)}')

'''
We can also combine row and column totals in one call.
This returns a modified EXP_cuw with both row and column totals added.
Because this alters the index, it is best to put the result in a new df, just so:
'''
EXP_cuw_withtotals=metropy.add_ctotal(metropy.add_rtotal(EXP_cuw), 'WORLD')

'''
Adding totals also works on df obtained from grouping:
'''
grouped = EXP_cuw.groupby(level='dim1').sum()
print(metropy.add_ctotal(grouped))

'''
We often would like to present and analyze results with different groupings than
those used in a METRO simulation. To do this, we can easliy provide user-defined
aggregations and use the metropy add_mapper() method.
The example maps the first 3 commodities to 'agri'and the rest to 'other':
'''

newcoms=['agri']*3+['other']*(len(s1.dimensions['commodities'])-3)

'''The following is a compact way to create a mapping dict, that maps 'commodities' to 'newcoms'
    but you can also create it 'by hand':
'''
com_map=dict(zip(s1.dimensions['commodities'], newcoms))

# let's look at the mapper:
print(com_map)

'''
Usually we want to combine the mapping with a groupby operation to get the recon-
figured results. The following call chains adding mapper -> groupby -> sum
and creates a new mapped dataframe:
'''
mapped=metropy.add_mapper(EXP_cuw, 'dim4', com_map).groupby('dim4_map').sum()

'''
We can add row and column totals to the mapped df in one call.
We should make sure to first deal with the row totals, and then with the
column totals:
'''
mapped = metropy.add_ctotal(metropy.add_rtotal(mapped, 'sum over uses'), 'sum over sectors')

'''
A more complex grouping with two levels, keeping regions (dim1) in the rows
and adding row and column totals:
'''
mapped2=EXP_cuw.groupby(['dim1', 'dim4_map']).sum()
mapped2 = metropy.add_ctotal(metropy.add_rtotal(mapped2, 'sum over uses'), 'sum over regions & commodities')
