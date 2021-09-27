from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import argparse
def Checker(upc,zipcode,stores,output=None):
    ret_dict = {}
    for elem in stores:
        if elem == 'Target':
            url = 'https://brickseek.com/target-inventory-checker'
        elif elem == 'Walmart':
            url = 'https://brickseek.com/walmart-inventory-checker'
        elif elem == 'Lowes':
            url = 'https://brickseek.com/lowes-inventory-checker'
        elif elem == 'OfficeDepot':
            url = 'https://brickseek.com/office-depot-inventory-checker/'
        elif elem == 'Staples':
            url = 'https://brickseek.com/staples-inventory-checker/'
        try:
            ret_dict[elem]= store_inventory(upc,zipcode,url)
        except:
            ret_dict[elem] = "No Availible Products"
    with open(output+'.txt','w') as json_file:
        json.dump(ret_dict,json_file,indent=4)

def store_inventory(upc,zipcode,url):
    options1 = webdriver.ChromeOptions()
    options1.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options1)
    driver.get(url)
    #Selects UPC option
    typeA = driver.find_element_by_xpath('//*[@id="main"]/div/form/div/div[1]/div/div/label[2]')
    typeA.click()
    #Enters upc and zipcode
    upc_in = driver.find_element_by_id('inventory-checker-form-upc')
    upc_in.send_keys(upc)
    searchbar = driver.find_element_by_id('inventory-checker-form-zip')
    searchbar.send_keys(zipcode)
    searchbar.send_keys(Keys.ENTER)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    stores_list = soup.find_all('div',{'class':'table__row'})
    store_dict = {}
    i = 0
    for elem in stores_list:
        try:
            store_name= elem.find('strong').text.replace('\n','')
            addy = elem.find('address').text
            addy = addy[0:addy.index('\n\n')].replace('\n','')
            avail = elem.find('span',{'class':'availability-status-indicator__text'}).text
            if avail == 'In Stock':
                quant= elem.find('span', {'class': 'table__cell-quantity'})
            price = elem.find('span',{'class':'price-formatted price-formatted--style-display'}).text
            disc = elem.find('span',{'class':'table__cell-price-discount'}).text
            store_dict[i]={'store_name':store_name,'addy':addy,'avail':avail,'price':price,'disc':disc}
            i+=1
        except:
            continue 
    return store_dict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the Inventory and Price of Item\'s given a UPC value')
    parser.add_argument('--upc','-u',type=str, metavar='',required=True,help='UPC of the Item')
    parser.add_argument('--zip','-z',type=str, metavar='',required=True,help='Your Current ZipCode')
    parser.add_argument('--stores','-s',type=str, metavar='',required=True,help='Stores You want to search In', choices=['a','w','t','l','o','s'])
    parser.add_argument('--output','-o',type=str, metavar='',help='Output json to a given file')
    args=parser.parse_args()
    stores = []
    if args.stores =='a':
        stores.append('Walmart')
        stores.append('Target')
        stores.append('Lowes')
        stores.append('OfficeDepot')
        stores.append('Staples')
    elif args.stores == 't':
        stores.append('Target')
    elif args.stores == 'w':
        stores.append('Walmart')
    elif args.stores == 'l':
        stores.append('Lowes')
    elif args.stores == 'o':
        stores.append('OfficeDepot')
    elif args.stores == 's':
        stores.append('Staples')
    Checker(args.upc,args.zip,stores,args.output)
