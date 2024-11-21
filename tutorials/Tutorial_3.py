# -*- coding: utf-8 -*-
"""
metropy tutorial #3
writing a dataframe to excel
and making a standard table with macro variables

Created on Tue Nov  3 16:42:14 2020
@author: VanTongeren_F
"""

print('\nThis is the metropy Tutorial #3' )
# standard library imports
import os

#local imports
from metro import metropy

PROJECT_ROOT_DIR = "."
DATA_DIR = "data"
GDX_PATH= os.path.join(PROJECT_ROOT_DIR, DATA_DIR)

#%% Set up where tutorial #2 ended, with a df based on a user-defined mapping

gdx_file = '20_8_7_v10L14_sim_Sim1.gdx'

s1 = metropy.metro_data('sim1')
s1.path = os.path.join(GDX_PATH, gdx_file)
s1.legend ='Simulation no 1'

EXP_cuw=s1.get_variable('QER')

newcoms=['agri']*3+['other']*(len(s1.dimensions['commodities'])-3)
com_map=dict(zip(s1.dimensions['commodities'], newcoms))
mapped=metropy.add_mapper(EXP_cuw, 'dim4', com_map).groupby('dim4_map').sum()
mapped = metropy.add_ctotal(metropy.add_rtotal(mapped, 'sum over uses'), 'sum over commodities')

mapped2=EXP_cuw.groupby(['dim1', 'dim4_map']).sum()
mapped2 = metropy.add_ctotal(metropy.add_rtotal(mapped2, 'sum over uses'), 'sum over commodities')

'''
First we should tell metropy where to put excel files.
NOTE: if the output diretcory does not exist, it will be created under the
curent work directory automatically.
'''
TABLE_DIR = "tables"
OUT_XLS_PATH = os.path.join(PROJECT_ROOT_DIR, TABLE_DIR, 'Tutorial_3a.xlsx')


'''
Next, we create a dict of metro.out_tables that we would like to write to excel:
'''
demo_tables = metropy.out_tables()

'''The most basic call to add a table to the dict and then write to excel
consists of 2 lines:
'''
metropy.add_to_out_tables(demo_tables, mapped)
metropy.write_to_excel(demo_tables, OUT_XLS_PATH)

'''
Voila! We should have an excel file .\tables\Tutorial_3a.xlsx
3 worksheets: A 'ReadMe' (which is almost empty), a 'Sheet' which is empty
and a 'Table(2,4)' with mapped dataframe.

Let's make this a bit nicer:
First close .\tables\Tutorial_3.xlsx if you have it open

We shall:
    - add some ReadMe information
    - add another table to the excel file
    - add some text info in each sheet, and
    - provide more meaningful sheet names.

First, we create a new dict of tables and add the ReadMe:
'''
demo_tables = metropy.out_tables()
demo_tables['ReadMe']= ['This is output from metropy Tutorial #3',
           'we have the following tables:',
           '"mapped" is a mapping of bilateral exports ',
           '"mapped2" is a more complex mapping of bilateral exports']


'''
A complete call to add_to_out_tables with sheet_name and info:
'''

metropy.add_to_out_tables(demo_tables, mapped, sheet_name = 'mapped',\
                        info = f'Mapped exports from {s1.legend}')

metropy.add_to_out_tables(demo_tables, mapped2, sheet_name = 'mapped2',\
                        info =  f'Double mapped exports from {s1.legend}')

OUT_XLS_PATH = os.path.join(PROJECT_ROOT_DIR, TABLE_DIR, 'Tutorial_3b.xlsx')
metropy.write_to_excel(demo_tables, OUT_XLS_PATH)

'''
We should now have an excel file .\tables\Tutorial_3b.xlsx

To go a bit further, metropy provides currently one standard output table,
which contains key macro variables. This can be created with a simple call
and added to the list of tables to be written:
'''
m1=metropy.macro_table(s1)
metropy.add_to_out_tables(demo_tables, m1, sheet_name= 'MACRO',\
                        info= f'Levels {s1.legend}')

'''add some info to the ReadMe sheet: '''
OUT_XLS_PATH = os.path.join(PROJECT_ROOT_DIR, TABLE_DIR, 'Tutorial_3c.xlsx')
demo_tables['ReadMe'].append('"MACRO" is a standard macro table')

'''if we also want no longname information for each variable, we call
metro.macro_table with longnames = True.
BUT: we need to tell where to find the XLS sets file used to make the
METRO aggregation (the module gdxpds cannot extract the longnames of sets and variables
from the gdx file, so this is a workaround) :
'''

s1.setpath= os.path.join(GDX_PATH,'20_8_7_v10L14.xlsm')
m2=metropy.macro_table(s1, longnames=True)

metropy.add_to_out_tables(demo_tables, m2, sheet_name= 'MACRO2',\
                        info= f'Levels with longnames of variables {s1.legend}')

metropy.write_to_excel(demo_tables, OUT_XLS_PATH)
# open excel app to view the last worksheet directly
os.startfile(OUT_XLS_PATH)


