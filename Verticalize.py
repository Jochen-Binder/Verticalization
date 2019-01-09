#!/usr/bin/env python
from __future__ import print_function
import numpy as np
import pandas as pd
import sys
from itertools import product
import copy


class verticalize(object):

    def __init__(self, df):
        """
        Initialize the verticalize class
        
        """
        self.original = df
        self.original['tmp_ID'] = range(len(self.original))
        self.cols = df.columns

        
    def melt(self, df, columns, separator = "_"):
        melt_cols = columns 
        cols = self.cols
        diff = cols.difference(melt_cols)
        df['tmp_ID']=range(len(df))
    
        # Keeping the order of the original df frame
        ordered_cols = [item for item in self.cols if item in diff]
    
        # Verticalize the df set
        df = pd.melt(df, id_vars=ordered_cols, value_vars=melt_cols, var_name='variable_original')
    
        # Deleting unneded helper variables
        del(ordered_cols, melt_cols, diff, cols)
    
        # Create 'brand' and 'item' variable and strip unnecessary strings
        df['brand'] = df['variable_original'].apply(lambda x: x.split(sep=separator)[1])
        df['variable'] = df['variable_original'].map(lambda x: x.split(sep=separator)[0] 
                                                        if x.count(separator)<=1 
                                                        else x.split(sep=separator)[0]+'_'+x.split(sep=separator)[2])
        del df['variable_original']
        
        return df
    
    def pivot(self, df, variable='variable', value='value'):
        cols = [c for c in df.columns if c not in {variable, value}]
        df = df.set_index(cols + [variable]).unstack(variable)
        df.columns = df.columns.levels[1]
        df.columns.name = None
        df = df.reset_index()
        
        #https://stackoverflow.com/questions/17333644/pandas-dataframe-transforming-frame-using-unique-values-of-a-column
        
        #cols = [c for c in new.columns if c not in {'variable', 'value'}]
        #df2 = new.set_index(cols + ['variable']).unstack('variable')
        #df2.columns = df2.columns.levels[1]
        #df2.columns.name = None
        #df2.reset_index()
        
        
        return df
