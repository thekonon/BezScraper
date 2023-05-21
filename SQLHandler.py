import sqlite3 as sq3
from pandas import DataFrame
from ScrapedData import ExcelReader
import pathlib
import os

# db_name = 'results.db'
# os.remove(db_name)
# db_dir_path = str(pathlib.Path('results.db').parent.resolve())
# db_file_path = db_dir_path+"\\"+db_name
# con = sq3.connect(db_name)
# cur = con.execute('PRAGMA table_info(results)')
# #Check if table is emtpty, if is, crete new table:
# if not cur.fetchall():
#     print('Creating new table: ')
#     con.execute('CREATE TABLE results(address TEXT, price TEXT, energy TEXT, rooms TEXT, size TEXT, link TEXT, date TEXT)')
#     con.commit()
# #Add data info database
# data = [('a','a','a','a','a','a', '2023:02:12:43:34'),
#         ('a','a','a','a','a','a', '2023:02:17:43:34'),
#         ('a','a','a','a','a','a', '2023:02:14:43:34'),
#         ('a','a','a','a','a','a', '2023:02:16:43:34')]
# #Commit changes
# cur = con.executemany('INSERT INTO results VALUES(?, ?, ?, ?, ?, ?, ?)', data)
# con.commit()

# for row in cur.execute('SELECT * FROM results'):
#     print(row)
    
# con.close()

class dbHandler():
    """_summary_
    Class for handling SQLite databases
    use cases:
        -adding data into database
        
    Methods:
        -commit_prepared_data
        -data_frame_to_data
        -prepare_data
    """
    def __init__(self,*args, **kwargs) -> None:
        """Initialize dbHandler, kwargs:
        
            -db_name = 'Name of your database'
            
            -colums = [(column_name_1, column_type_1), (column_name_2, column_type_2), ...]
        """
        #Set up file and path vars
        self.db_name = 'results.db'
        self.db_dir_path = str(pathlib.Path('results.db').parent.resolve())
        self.db_file_path = self.db_dir_path+"\\"+self.db_name
        self.db_table_name = "scraped_data"
        
        #State variables
        self.is_initialized = 0 #1 if database is opened
        
        #Prealocated data list to be added
        self.prepared_data = []
        
        #Set up default columns names and types:
        self.columns = [
            ('address', 'TEXT'),
            ('price', 'TEXT'),
            ('energy', 'TEXT'),
            ('rooms', 'TEXT'),
            ('size', 'TEXT'),
            ('link', 'TEXT'),
            ('date', 'TEXT')]
        self._initialize_database()
    
    def commit_prepared_data(self):
        """_summary_:
        writes prepared data into database, removes everything from prepared data list
        """
        try:
            execute_string = f'INSERT INTO {self.db_table_name} VALUES(?, ?, ?, ?, ?, ?, ?)'
            self.conn.executemany(execute_string, self.prepared_data)
            self.conn.commit()
            self.prepared_data = []
        except Exception:
            pass
    
    def data_frame_to_data(self, data_frame: DataFrame):
        """_summary_
        converts data_frame into dictionaries, loads data into prepared_data list

        Args:
            data_frame (pd.dataframe): Pandas dataframe
        """
        for dict in data_frame.to_dict(orient='records'):
            self.prepare_data(dict)
            
    def prepare_data(self, data):
        """Adds row of data to preparation list
        
        Args:
            data (dictionary): dictionary of data, if column is not included, NULL is set
            E.G.: data = {'address': 'Plzen 12645', 'price': '1687'}
        """
        # data = {'address': 'Plzen 12645',
        #              'price': '1687',
        #              'rooms': '3'}
        
        self.prepared_data.append(tuple(data.get(column[0], 'NULL') for column in self.columns))
    
    def _initialize_database(self):
        self.conn = sq3.connect(self.db_name)
        if self.db_table_exists():
            print(f'Creating new table {self.db_table_name}: ')
            column_data_string = ', '.join([f"{column} {datatype}" for column, datatype in self.columns])
            create_table_string = f"CREATE TABLE {self.db_table_name}({column_data_string})"
            self.conn.execute(create_table_string)
            self.conn.commit()
        self.is_initialized = 1
    
    
    def db_table_exists(self):
        """Returns logical if table named self.db_table_name inside database exists
        """
        return not self.conn.execute(f'PRAGMA table_info({self.db_table_name})').fetchone()

    def close_db(self):
        """Closes database
        """
        try:
            self.conn.close()
            self.is_initialized = 0
        except:
            pass    
        
if __name__ == '__main__':
    #Removes old db
    db_name = 'results.db'
    #os.remove(db_name)
    
    #Create db handle
    my_db_handle = dbHandler()
    
    #Create excel reade obj
    excel_reader = ExcelReader('results.xlsx')
    data_frame = excel_reader.get_dataframe()
    
    #To be able succesfully match data - it is required to rename
    #Czech column names - located in excel into english one used in db
    data_frame.columns = [item[0] for item in my_db_handle.columns]
    
    #Prepare data to be send
    my_db_handle.data_frame_to_data(data_frame)
    #Send and save data into db
    my_db_handle.commit_prepared_data()
    #Close db relation
    my_db_handle.close_db()