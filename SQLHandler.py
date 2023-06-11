import sqlite3 as sq3
from pandas import DataFrame, read_sql_query
import pathlib
import os

class dbHandler():
    """_summary_
    Class for handling SQLite databases
    use cases:
        -adding data into database

    Methods:
        -1) data_frame_to_data(data_frame)
        -2) commit_prepared_data
        
        -prepare_data
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize dbHandler, kwargs:

            -db_name = 'Name of your database'

            -colums = [(column_name_1, column_type_1), (column_name_2, column_type_2), ...]
        """
        # Set up file and path vars
        self.db_name = 'results.db'
        self.db_dir_path = str(pathlib.Path('results.db').parent.resolve())
        self.db_file_path = self.db_dir_path+"\\"+self.db_name
        self.db_table_name = "scraped_data"

        # State variables
        self.is_initialized = 0  # 1 if database is opened

        # Prealocated data list to be added
        self.prepared_data = []

        # Set up default columns names and types:
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
        self.prepared_data.append(
            tuple(data.get(column[0], 'NULL') for column in self.columns))

    def _initialize_database(self):
        self.conn = sq3.connect(self.db_name)
        if self.db_table_exists():
            print(f'Creating new table {self.db_table_name}: ')
            column_data_string = ', '.join(
                [f"{column} {datatype}" for column, datatype in self.columns])
            create_table_string = f"CREATE TABLE {self.db_table_name}({column_data_string})"
            self.conn.execute(create_table_string)
            self.conn.commit()
        self.is_initialized = 1

    def db_table_exists(self):
        """Returns logical if table named self.db_table_name inside database exists
        """
        return not self.conn.execute(f'PRAGMA table_info({self.db_table_name})').fetchone()

    def get_data(self):
        return read_sql_query(f"Select * FROM {self.db_table_name}", self.conn)
    
    def save_dataframe(self, data_frame: DataFrame):
        """OVERWRITES EXISTING DB TABLE WITH DATAFRAME

        Args:
            data_frame (DataFrame): _description_
        """
        #removes data
        self._drop_table()
        data_frame.to_sql(name=self.db_table_name, con=self.conn)
    
    def _drop_table(self):
        """DELETES TABLE IN DB
        """
        self.conn.execute(f"DROP TABLE {self.db_table_name}")
        self.conn.commit()
        print("Table successfuly removed")
    
    def close_db(self):
        """Closes database
        """
        try:
            self.conn.close()
            self.is_initialized = 0
        except:
            pass


if __name__ == '__main__':
    pass
