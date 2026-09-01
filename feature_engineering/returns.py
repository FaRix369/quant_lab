import numpy as np
from database.querys import q_returns


def log_return(df):
    return_log = np.log(df['adj_close']/df['adj_close'].shift(1))
    return return_log

def log_return_digit(df):
    return_log = np.log(df['adj_close']/df['adj_close'].shift(1))
    return return_log.sum()

def simple_return(df):
    return_log = np.log(df['adj_close']/df['adj_close'].shift(1))
    return_simple = np.exp(return_log.sum()) - 1
    return return_simple

def aritmetic_return(df):
   adj_close_column = df['adj_close']
   return_aritmetic = adj_close_column.pct_change()
   return return_aritmetic

def aritmetic_return_digit(df):
    adj_close_column = df['adj_close']
    return_aritmetic = adj_close_column.pct_change()
    return return_aritmetic.add(1).prod() - 1