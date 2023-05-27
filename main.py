from Scraperino import BezrealitkyScraper
from ScrapedData import NewDataHandle, ScreadDataWriter

if __name__ == '__main__':
    #Create a Bezrealitky scraper
    bez_realitky = BezrealitkyScraper()
    bez_realitky.driver.close()
    
    #Save data to excel
    writer = ScreadDataWriter(bez_realitky.scraped_data)
    writer.saveData('data/Bezrealitky')
    
    #Compare new data with stored ones
    comparator = NewDataHandle(bez_realitky.scraped_data.get_dataframe())
    
    new_data = comparator.new_data
    removed_data = comparator.missing_data
    
    print("_"*10)
    print("Nově umístěné nabídky: ")
    print(new_data)
    print("_"*10)
    print("Stažené nabídky: ")
    print(removed_data)
    print("_"*10)
    
    
    