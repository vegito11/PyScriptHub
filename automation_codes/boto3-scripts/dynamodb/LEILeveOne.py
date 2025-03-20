import pandas as pd
from utils import get_file_path, clean_data, rename_cols, merge_region_country, return_not_na_val
from constants import LEVEL_1_REQ_COLS, LEVEL_1_RENAME_COL_MAPPING
import io

class LEILevelOne(object):

    def __init__(self, file_name, file_type, sheet_name=None):
        
        self.data_frame = self.read_data(file_name, file_type, sheet_name).head(5)

        # print(self.data_frame.columns)
        self.process_data_frame()
        # print(self.data_frame.columns)

    def read_data(self, file_name, file_type, sheet_name=None):
        
        if file_type == "csv":
            return pd.read_csv(get_file_path(file_name), usecols=LEVEL_1_REQ_COLS)
        
        elif file_type == "excel":
            if sheet_name:
                return pd.read_excel(get_file_path(file_name), sheet_name=sheet_name, usecols=LEVEL_1_REQ_COLS)
            else:
                return pd.read_excel(get_file_path(file_name), usecols=LEVEL_1_REQ_COLS, dtype=str)


    def process_data_frame(self):
        clean_data(self.data_frame)
        rename_cols(self.data_frame, LEVEL_1_RENAME_COL_MAPPING)
        self.add_legal_address_col2()
        # self.add_legal_address_col()
        # self.add_hq_address_col()
    
    def add_legal_address_col2(self):
        for row in range(self.data_frame.shape[0]):

            self.data_frame.loc[row, "legal_address"] = str(self.data_frame.loc[row, "legal_first_address_line"]) \
                                                        + "," + self.data_frame.loc[row, "legal_address_city"]
             
            region_country = self.data_frame.loc[row, "legal_address_region"], self.data_frame.loc[row, "legal_address_country"]
            self.data_frame.loc[row, "legal_address"] += merge_region_country(region_country)
            self.data_frame.loc[row, "legal_address"] += return_not_na_val(self.data_frame.loc[row, "legal_address_postalcode"])
            self.data_frame.loc[row, "legal_address"] += return_not_na_val(
                                                             self.data_frame.loc[row, "legal_address_line_1"], sep=",\n")
            self.data_frame.loc[row, "legal_address"] += return_not_na_val(
                                                             self.data_frame.loc[row, "legal_address_line_2"], sep=",\n")
            self.data_frame.loc[row, "legal_address"] += return_not_na_val(
                                                             self.data_frame.loc[row, "legal_address_line_3"], sep=",\n")

        drop_col_list = ["legal_first_address_line", "legal_address_city", "legal_address_region", "legal_address_postalcode",
                         "legal_address_line_1", "legal_address_line_2", "legal_address_line_3"]

        self.data_frame.drop(columns=drop_col_list, inplace=True)
        

    def add_legal_address_col(self):

        self.data_frame["legal_address"] = self.data_frame["legal_first_address_line"].astype(str) + "," + \
            self.data_frame["legal_address_city"] + \
            self.data_frame[["legal_address_region", "legal_address_country"]].apply(
            merge_region_country, axis=1) + \
            self.data_frame["legal_address_postalcode"].apply(return_not_na_val) + \
            self.data_frame["legal_address_line_1"].apply(return_not_na_val, sep=",\n") + \
            self.data_frame["legal_address_line_2"].apply(return_not_na_val, sep=",\n") + \
            self.data_frame["legal_address_line_3"].apply(
                return_not_na_val, sep=",\n")

        drop_col_list = ["legal_first_address_line", "legal_address_city", "legal_address_region", "legal_address_postalcode",
                         "legal_address_line_1", "legal_address_line_2", "legal_address_line_3"]

        self.data_frame.drop(columns=drop_col_list, inplace=True)
        print(self.data_frame['legal_address'])

    def add_hq_address_col(self):
        self.data_frame["head_quarter_address"] = self.data_frame["hq_first_address_line"].astype(str) + "," + \
            self.data_frame["hq_address_city"] + \
            self.data_frame[["hq_address_region", "hq_address_country"]].apply(merge_region_country, axis=1) + \
            self.data_frame["hq_address_postalcode"].apply(return_not_na_val) + \
            self.data_frame["hq_address_line_1"].apply(return_not_na_val, sep=",\n") + \
            self.data_frame["hq_address_line_2"].apply(return_not_na_val, sep=",\n") + \
            self.data_frame["hq_address_line_3"].apply(
                return_not_na_val, sep=",\n")

        drop_col_list = ["hq_first_address_line", "hq_address_city", "hq_address_region", "hq_address_postalcode",
                         "hq_address_line_1", "hq_address_line_2", "hq_address_line_3"]

        self.data_frame.drop(columns=drop_col_list, inplace=True)


if __name__ == '__main__':
    ob = LEILevelOne("LEI-Data.xlsx", "excel")
