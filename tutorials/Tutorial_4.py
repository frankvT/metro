# -*- coding: utf-8 -*-
"""
metropy tutorial #4
using multiple METRO results files

Created on Tue Nov  9 16:42:14 2020
@author: VanTongeren_F
"""

print('\nThis is the metropy Tutorial #4' )

# standard library imports
import os

# third party imports
import pandas as pd

#local imports
from metro import metropy
from metro import stattools as st

pd.options.display.float_format = '{:.3f}'.format
PROJECT_ROOT_DIR = "."
DATA_DIR = "data"
TABLE_DIR = "tables"
GDX_PATH= os.path.join(PROJECT_ROOT_DIR, DATA_DIR)
OUT_XLS_PATH = os.path.join(PROJECT_ROOT_DIR, TABLE_DIR, 'Tutorial_4.xlsx')

''' We shall load multiple files, so let us put all those in list:'''
gdx_file_list =['20_8_7_v10L14_res_base.gdx',
                '20_8_7_v10L14_sim_Sim1.gdx',
                '20_8_7_v10L14_sim_Sim2.gdx'
                ]

'''Let us start by instantiating metro_data objects and loading results files:'''
base=metropy.metro_data('base')
base.legend= 'base data'
base.path=os.path.join(GDX_PATH, gdx_file_list[0])

s1=metropy.metro_data('sim1')
s1.path= os.path.join(GDX_PATH, gdx_file_list[1])
s1.legend='Simulation no 1'

s2=metropy.metro_data('sim2')
s2.path= os.path.join(GDX_PATH, gdx_file_list[2])
s2.legend='Simulation no 2'

'''metropy provides a class 'result_stack'  that holds all the results in one place
as a list of metropy.metro_data objects and provides some tools to access
variables across all the results.
We first instatiate it, and then put the results just loaded into the stack: '''

allresults= metropy.result_stack()
allresults.add_result(base)
allresults.add_result(s1)
allresults.add_result(s2)


print(f'We now have loaded the following:\n {allresults.get_dataIDs()}')
print(f'Their full names are:\n {allresults.get_fullnames()}')

''' We can easily retrieve a variable from the results stack:  '''
gdp=allresults.get_var('rGDPEXP')

'''When we retrieve a variable, it is kept in a dict, so it has a key and items:'''
print(f'the keys: {gdp.keys()}\n')
print(f'the items retrieved:\n {gdp.items()}')

''' We can iterate over the elements in the result_stack using the
get_results method, which delivers a list of metropy.metro_data objects which
can then be accessed: '''
for s in allresults.get_results():
    print(f'World rGDPEXP in: {s} equals: {s.get_variable("rGDPEXP").sum():.1f} ')

''' Note that print(s) yields the name, fullname and path. So we can do:'''
print(base)

''' Variables with higher dimensions work equally well: '''
exp=allresults.get_var('QER')

''' meytropy has a method to calculate percent differences between results.
The simplest version is to compare just two sets of results:'''

dif_pct = metropy.pct_diff(gdp['base'], gdp['sim1'])

'''Or you compare a list [] of results to a base: '''
metropy.pct_diff_list(gdp['base'], [gdp['sim1'], gdp['sim2']])

'''The complete call has headers and a basecolumn that we can switch on or off.
In  case we deal with a series (and not a dataframe) the basecolumn will contain
the base values and it will be put at the left hand side of the output df.
It also and yields prettier output:'''
gdp_compare = metropy.pct_diff_list(gdp['base'], [gdp['sim1'], gdp['sim2']], \
                                  headers=['base','sim1', 'sim2'], basecol=True)

''' if you try to comaprte two frames with different dimensions - it should raise
an AssertionError:'''
#metro.pct_diff(exp['base'], gdp['sim1'])


'''Thi is a more complex calculation: exports by source and destination region
and commodity and and by use category.
# the same , but with headers and
basecol= True (which will be ignored becasue df has more than 1 column)
'''
exp_compare = metropy.pct_diff_list(exp['base'], [exp['sim1'], exp['sim1']],\
                                  headers=['base','sim1', 'sim2'], basecol=True)

'''You acan make a table in 'long'format that can be pivoted just so: '''
exp_compare_long= exp_compare.stack()


''' We can also compute some statistics using the stattools module:
To get summary statistics by region apply a pandas groupby (dim1)
and then pass the groupby opbject to st.get_stats()
(get_stats accepts a single column or a groupby object):'''

st.get_stats(gdp_compare.groupby('dim1', level=1))

'''To get column sum (world) totals into the comparison, you can add totals as in
Tutorial #2:'''
gdpB_with_totals= metropy.add_ctotal(gdp['base'], name='World')
gdpS1_with_totals = metropy.add_ctotal(gdp['sim1'], name='World')
w1 = metropy.pct_diff(gdpB_with_totals, gdpS1_with_totals)
print(f'Percent difference GDP sim1 to base : \n'
      f'{w1}')

'''Weighted average of one column (fillna because otherwise wavg is not defined)'''
w2=st.get_wavg(gdp_compare.fillna(0), 'sim1', 'Base values')

'''both methods should yield the same: '''
print(f'World avg using pct_diff: {w1.iloc[-1]}\n'
      f'World avg using get_wavg: {w2:.3f}')

''' Finally, we can also create and write comparative macro tables to excel:'''

t0 = metropy.macro_table(base)
t1 = metropy.macro_table(s1)
t2 = metropy.macro_table(s2)

macro_diff = metropy.pct_diff_list(t0, [t1, t2], ['base', 'sim1', 'sim2'])

OUT_TABLES = metropy.out_tables()
OUT_TABLES['ReadMe'] = ['This is a test readme text',
                         'We have an interesting table of macro differences',
                         'but it does not have informative longnames',
                         ' ',
                         'CONGRATULATIONS! You made it to the end of the metropy tutorial']

metropy.add_to_out_tables(OUT_TABLES, macro_diff, sheet_name = 'MACROdiff',\
                        info = f'Percent difference to {base.legend}')

metropy.write_to_excel(OUT_TABLES, OUT_XLS_PATH)

os.startfile(OUT_XLS_PATH)



