import numpy as np
import pandas as pd


class TspMatrix(pd.DataFrame):

    def __init__(self, data, row_labels = [], col_labels = [], cost = 0, depot = None):
        pd.DataFrame.__init__(self,data)
        self.cost = cost

        if row_labels:
            self.index = row_labels

        if col_labels:
            self.columns = col_labels

        if depot == None:
            self.depot = self.index[0]
        else:
            self.depot = depot


    def get_no_rows(self):
        return self.shape[0]

    def get_no_cols(self):
        return self.shape[1]

    def get_row(self, index):
        return self.iloc[index]

    def get_col(self, index):
        return self.iloc[:,index]

    def sub_row_min(self):
        for r_i in range(self.get_no_rows()):
            min = self.iloc[r_i].min()
            self.iloc[r_i] = self.iloc[r_i] - min
            self.cost += min

    def sub_col_min(self):
        for c_i in range(self.get_no_cols()):
            min = self.iloc[:,c_i].min()
            self.iloc[:,c_i] = self.iloc[:,c_i] - min
            self.cost += min
