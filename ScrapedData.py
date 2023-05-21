import pandas as pd
from datetime import datetime
import numpy as np
class ScrapedDataHolder():
    def __init__(self):
        self.fulltext = []
        self.flat_size_rooms = []
        self.flat_size_m = []
        self.address = []
        self.city = []
        self.czech_part = []
        self.price = []
        self.extra_price = []
        self.link = []
        self.date = []
    
    def getDictionary(self):
        dictionary = {'Adresa: ':self.address,
                      'Cena: ': self.price,
                      'Energie': self.extra_price,
                      'Počet pokojů': self.flat_size_rooms,
                      'Velikost bytu': self.flat_size_m,
                      'Link': self.link,
                      'Datum': self.date}
        return dictionary

class ScreadDataWriter():
    def __init__(self, scraped_data):
        self.scraped_data = scraped_data
        self.scraped_data_dataframe = pd.DataFrame(self.scraped_data.getDictionary())
        
    def saveData(self, file_name):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        self.scraped_data_dataframe.to_excel(file_name+dt_string+'.xlsx')
        
class ExcelReader():
    def __init__(self, file_name) -> None:
        self.loaded_dataframe = pd.read_excel(file_name).iloc[:,1:] #Removes first col
    def get_dataframe(self):
        return self.loaded_dataframe
    
class ScrapedDataComparator:
    def __init__(self, excel_name1, excel_name2) -> None:
        self.excel_name1 = excel_name1
        self.excel_name2 = excel_name2
        
        self.data_frame1 = pd.read_excel(excel_name1).iloc[:, 1:]
        self.data_frame2 = pd.read_excel(excel_name2).iloc[:, 1:]
    
        self.find_differences()
    def find_differences(self):
        merged_df = self.data_frame1.merge(self.data_frame2, indicator=True, how='outer')
        diff_rows = merged_df[merged_df['_merge'] != 'both']
        
        if diff_rows.empty:
            print("No differences found between the DataFrames.")
        else:
            print("Differences found between the DataFrames:")
            print(diff_rows)    
        # self.data_frame1.sort_index(inplace=True)
        # self.data_frame2.sort_index(inplace=True)
        
        # self.data_frame2.columns = list(self.data_frame1.columns)
        # return self.data_frame1.compare(self.data_frame2)
        
        # self.merged_data_frame = pd.concat([self.data_frame1, self.data_frame2])
        # self.unique_data_frame = self.merged_data_frame.drop_duplicates()
        
        # for _, row in self.data_frame1.iterrows():
        #     for _, row2 in self.unique_data_frame.iterrows():
        #         counter = 0
        #         if not row.equals(row2):
        #             counter += 1
        #     if not counter:
        #         print('New element found in dataframe1')
        #         print('And that is: ')
        #         print(row)
        #     else:
        #         print(f'Total of {counter} elements are dup in DF1')
        # for _, row in self.data_frame2.iterrows():
        #     for _, row2 in self.unique_data_frame.iterrows():
        #         counter = 0
        #         if not row.equals(row2):
        #             counter += 1
        #     if not counter:
        #         print('New element found in dataframe2')
        #         print('And that is: ')
        #         print(row)
        #     else:
        #         print(f'Total of {counter} elements are dup in DF2')
                