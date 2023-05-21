import pandas as pd
from datetime import datetime
import numpy as np

from SQLHandler import dbHandler
# Classes used for data manipulation


class ScrapedDataHolder():
    """Class used as data container for scraped data

    """

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
        dictionary = {'Adresa: ': self.address,
                      'Cena: ': self.price,
                      'Energie': self.extra_price,
                      'Počet pokojů': self.flat_size_rooms,
                      'Velikost bytu': self.flat_size_m,
                      'Link': self.link,
                      'Datum': self.date}
        return dictionary


class ScreadDataWriter():
    """ScrapedDataWriter
    Use case:
        - Data saved in ScrapedDataHolder class are transformed into pandas DataFrame
        - Used for saving dataframe to excel
    """

    def __init__(self, scraped_data):
        """_summary_

        Args:
            scraped_data (ScrapedDataHolder): data stored in ScrapedDataHolder
        """
        self.scraped_data = scraped_data
        self.scraped_data_dataframe = pd.DataFrame(
            self.scraped_data.getDictionary())

    def saveData(self, file_name):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
        self.scraped_data_dataframe.to_excel(file_name+dt_string+'.xlsx')


class ExcelReader():
    """ExcelReadcer class:
    Class for reading saved excels
    use-cases:
        -load data from excel into pandas dataframe
    Methods:
        -get_dataframe: returns pandasDataframe
    """

    def __init__(self, file_name) -> None:
        self.loaded_dataframe = pd.read_excel(
            file_name).iloc[:, 1:]  # Removes first col

    def get_dataframe(self):
        return self.loaded_dataframe


class ScrapedDataComparator:
    """Class used for comparing two excels
    """

    def __init__(self, excel_name1, excel_name2) -> None:
        self.excel_name1 = excel_name1
        self.excel_name2 = excel_name2

        self.data_frame1 = pd.read_excel(excel_name1).iloc[:, 1:]
        self.data_frame2 = pd.read_excel(excel_name2).iloc[:, 1:]

        self.find_differences()

    def find_differences(self):
        merged_df = self.data_frame1.merge(
            self.data_frame2, indicator=True, how='outer')
        diff_rows = merged_df[merged_df['_merge'] != 'both']

        if diff_rows.empty:
            print("No differences found between the DataFrames.")
        else:
            print("Differences found between the DataFrames:")
            print(diff_rows)
            
        


class NewDataHandle():
    """Class for adding newly scraped data into db
    use cases:
        - return new data
        - return missing data (withdrawn offers)

    1) create pandas dataframe from existing db
    2) diff db dataframe with new dataframe
    3) return new data / removed data
    4) save new table

    """
    def __init__(self, new_data_dataframe) -> None:
        self.new_data_dataframe = new_data_dataframe
        self.db_handler = dbHandler()
        self._rename_columns()
        self.load_db_data()
        self.diff_data()
        print("Nalezeny nové nabídky bydlení: ")
        print(self.new_data)
        print("Tyto nabídky byly staženy: ")
        print(self.missing_data)
        #self.save_new_data()
        self.db_handler.close_db()
    def load_db_data(self):
        # Crate df from db
        self.db_dataframe = self.db_handler.get_data().drop('index',axis=1) #Removes time data
    def diff_data(self):
        """Find differences between dataframes
        - new data are saved to new_data
        - withdrawn offeres are in missing_data
        """
        #Find differences between dataframes
        merged_df = self.db_dataframe.merge(self.new_data_dataframe, indicator=True, how='outer')
        diff_rows = merged_df[merged_df['_merge'] != 'both']
        
        self.new_data = diff_rows[diff_rows['_merge'] == 'right_only']
        self.missing_data = diff_rows[diff_rows['_merge'] == 'left_only']
        
        #Find which data are new and which are missing
        #self.new_data = self.db_dataframe[~diff_rows.isin(self.new_data_dataframe)].dropna()
        #self.missing_data = self.new_data_dataframe[~diff_rows.isin(self.db_dataframe)].dropna()
    def save_new_data(self):
        self.db_handler.save_dataframe(self.new_data_dataframe)
        
    def _rename_columns(self):
        self.new_data_dataframe['D'] = 'a'
        self.new_data_dataframe.columns = [item[0] for item in self.db_handler.columns]
    
    
if __name__ == '__main__':
    # # Create excel reade obj
    excel_reader = ExcelReader('data/'+'Bezrealitky2023-05-21-18-47-39'+'.xlsx')
    data_frame = excel_reader.get_dataframe().drop('Datum', axis=1)
    new_data_handle = NewDataHandle(data_frame)
    # Create db handle
    # my_db_handle = dbHandler()

    # # To be able succesfully match data - it is required to rename
    # # Czech column names - located in excel into english one used in db
    # # Extract name part of tuples ('name', 'type')
    # data_frame.columns = [item[0] for item in my_db_handle.columns]

    # # Close db relation
    # my_db_handle.close_db()
