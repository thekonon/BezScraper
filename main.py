from SQLHandler import dbHandler
from Scraperino import BezrealitkyScraper
from ScrapedData import ExcelReader, ScreadDataWriter

if __name__ == '__main__':
    #Create a Bezrealitky scraper
    br = BezrealitkyScraper()
    print('Closing driver')
    br.driver.close()
    print('Driver is closed now')

    #Save data to excel
    writer = ScreadDataWriter(br.scraped_data)
    writer.saveData('data/Bezrealitky')
    
    #Save data to db:
    my_db_handle = dbHandler()
    df2 = writer.scraped_data_dataframe
    df2.columns = [item[0] for item in my_db_handle.columns]
    my_db_handle.data_frame_to_data(df2)
    my_db_handle.commit_prepared_data()
    my_db_handle.close_db()