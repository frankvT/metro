# -*- coding: utf-8 -*-
"""
A small statistical toolbox

@author: VanTongeren_F
"""
import numpy as np
from scipy import stats

def get_stats(g)-> dict:
    '''
    Calculates summary statistics of a column or groupby object in a pandas
    dataframe
    ...
    Parameters
    ----------
    g: pandas data frame column or dataframe groupby object

    RETURNS
    -------
    summary statistics as a dict
    '''

    return {'count': g.count(),'min': g.min(), 'max':g.max(),
             'mean': g.mean(), 'stdev': g.std(), '|t-ratio|':
              abs(g.mean()/g.std()), 'sum': g.sum() }
# end get_stats()

def get_wavg(g, data, weights)->float:
    '''
    Calculates weighted averages of columns in a pandas dataframe
    ...
    Parameters
    ----------
    g:      pandas data frame (or group)

    data:   str
        the label of the column in g  over which to calculate the weighted average
    weights: str
        the label of the colun in g to use as weights

    RETURNS
    -------
    weighted average
    '''
    return np.average(g[data], weights=g[weights])
# end get_wavg()

def comp_tstat(group, variable)->list:
    '''
    Computes t-statistics for testing signifcance of difference of group means
    assuming unequal variance (Welsh test)
    ...
    PARAMETERS
    group:      pandas groupby object
    variable: str
        label of the variable to select from group

    RETURNS
    -------
    tstat: list of tuples with 4 elements each:
    the 2 elemements in the group to compare, the t-statistic and the p-value
    '''

    n=  group.ngroups
    g = group.groups.keys()
    x = [0]*n
    tstat=[]

    for z, (i,b) in enumerate(zip(x,g)):
            x[z] = group.get_group(b)[variable]

    for s1 in enumerate(g):
        for s2 in enumerate(g):
            if s1<s2:
                t= stats.ttest_ind(x[s1[0]], x[s2[0]], equal_var=False)
                tstat.append((s1,s2,t[0],t[1]))

    return tstat
#end comp_tstat()

def main():
    pass
if __name__ == "__main__":
    main()
