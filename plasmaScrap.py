from selenium import webdriver
from selenium.webdriver.support.select import Select
from time import sleep
import pymongo

client = pymongo.MongoClient("mongodb+srv://saud:mlab3431@hospitals.5loco.mongodb.net/helpagainstcovid?retryWrites=true&w=majority")
mydatabase = client.helpagainstcovid
PATH = "chromedriver.exe"
op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op)
driver.implicitly_wait(8)
#driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(r'https://www.eraktkosh.in/BLDAHIMS/bloodbank/stockAvailability.cnt')
#driver.implicitly_wait(10)
sleep(4)
  
stateDropDown = Select(driver.find_element_by_xpath("//select[@name='stateCode']"))
stateDropDown.select_by_index(23)
s= stateDropDown.first_selected_option
s.click()
sleep(2)
#driver.implicitly_wait(10)
distDropDown = Select(driver.find_element_by_xpath("//select[@id='distList']"))
distDropDown.select_by_index(17)
d= distDropDown.first_selected_option
d.click()
sleep(2)
#driver.implicitly_wait(10)
plasmaDropDown = Select(driver.find_element_by_xpath("//select[@name='bloodComponentType']"))
plasmaDropDown.select_by_index(9)
p= plasmaDropDown.first_selected_option
p.click()
sleep(2)
#driver.implicitly_wait(10)
Button = driver.find_elements_by_xpath('//*[@id ="searchButton"]')
Button[0].click()
sleep(2)
#driver.implicitly_wait(10)

showDropDown = Select(driver.find_element_by_xpath("//select[@name='example-table_length']"))
showDropDown.select_by_index(3)
sh= showDropDown.first_selected_option
sh.click()

#text method for selected option text
#print("Selected option is: "+ o.text)
#driver.close()
    #Select period = new Select(driver.findElement(By.id("stateCode")));
    
sleep(4)

rows = len(driver.find_elements_by_xpath("//table/tbody/tr"))
cols = len(driver.find_elements_by_xpath("//table/tbody/tr[1]/td"))

print('Rows',rows)
print('Columns',cols)
for r in range(1,rows+1):
    centerName= driver.find_element_by_xpath("//table/tbody/tr["+str(r)+"]/td[2]").text
    centerType= driver.find_element_by_xpath("//table/tbody/tr["+str(r)+"]/td[3]").text
    centerAvail = driver.find_element_by_xpath("//table/tbody/tr["+str(r)+"]/td[4]").text
    date = driver.find_element_by_xpath("//table/tbody/tr["+str(r)+"]/td[5]").text
    addIndex = centerName.index('Mumbai')
    addIndex = centerName[:addIndex]
    try:
        '''
        response = requests.get('https://api.mapbox.com/geocoding/v5/mapbox.places/'+addIndex+'.json?access_token=pk.eyJ1Ijoic2NsdXRjaCIsImEiOiJja3N3NmF5ZDIxeG16Mm50Zjk3bWtwcGVuIn0.fEnRFuxoMz0ihSsdcqeDAA')
        data = response.json()
        d=data['features'][0]['center']'''
        print(centerName,centerType,centerAvail,date)
        test = {"info":centerName,"type":centerType,"avail":centerAvail,"datetime":date}
        rec = mydatabase.plasmadata.insert_one(test)

    except KeyError:
        continue