from selenium import webdriver
from bs4 import BeautifulSoup


def get_items():

    chrome_path = r'C:\Users\to0dl\Documents\driver\chromedriver.exe'
    driver = webdriver.Chrome(chrome_path)
    driver.get('https://www.tq-db.net/en/category/axe')
    all_items=[]
    all_items_data=[]
    scroll=driver.execute_script('return document.body.scrollHeight;')
    
    for i in range(scroll//500):
        
        driver.execute_script(r"window.scrollTo(0,"+str(i*500)+")")
        grid = driver.find_element_by_xpath("""//*[@id="app"]/div/div[2]/div[2]/main/div[1]/div/div""")
        items = grid.find_elements_by_class_name("AE")
        
        for item in items:
            
            if item not in all_items:
                
                all_items.append(item)
                all_items_data.append(item.get_attribute('innerHTML'))

    return all_items_data,[len(all_items),len(all_items_data)]

def bonus_digester(bonus_list,name):
    for i in bonus_list:
        if 'Pierce Damage' in i:
            if 'Chance' in i:
                print(i.split()[0],i.split()[3],'A')
            else:
                print(i.split()[0],'B')
        if 'Stun' in i:
            if 'Resistance' in i:
                print(i,'C')
            if 'Chance' in i:
                print(i,'D')

def main_bow():

    all_items_data = get_items()[0]

    items_data=[]

    for item in all_items_data:            
        soup = BeautifulSoup(item,'lxml')

        bonus_list=[]
        holder = soup.div.findAll('div', class_ = 'Aw')
        
        for item in holder:
            for description in item.div.div:
                for line in description.findAll('li'):
                    bonus_list.append(line.text)
                    
        match1 = soup.div.find('div', class_='A1')
        
        name = match1.find('a', class_='A5').text
        
        base_stats = match1.find('div', class_='A2').div 
        base=base_stats.prettify().split('\n')
        
        dmg=(int(base[2].split()[0])+int(base[2].split()[2]))/2

        ratio = base[5].strip()[0:2]

        speed = base[7][9:]

        bonus_digester(bonus_list,name)
        
        try:
            items_data.append([[name,dmg,ratio,speed],bonus_list])
        except:
            print(name.text,"Error")

    for i in sorted(items_data,key=lambda dmg: dmg[1])[::-1]:
        print(i)

def main_axe():

    all_items_data = get_items()[0]

    items_data=[]

    for item in all_items_data:            
        soup = BeautifulSoup(item,'lxml')

        bonus_list=[]
        holder = soup.div.findAll('div', class_ = 'Aw')
        
        for item in holder:
            for description in item.div.div:
                for line in description.findAll('li'):
                    bonus_list.append(line.text)
                    
        match1 = soup.div.find('div', class_='A1')
        
        name = match1.find('a', class_='A5').text
        
        base_stats = match1.find('div', class_='A2').div 
        base=base_stats.prettify().split('\n')

        dmg_holder = base[2].split()

        if len(dmg_holder)==5:
            dmg=(int(dmg_holder[0])+int(dmg_holder[2]))/2
        else:
            dmg=int(dmg_holder[0])
            
        ratio = base[5].strip()[0:2]

        speed = base[7][9:]

        bonus_digester(bonus_list,name)
        
        try:
            items_data.append([[name,dmg,ratio,speed],bonus_list])
        except:
            print(name.text,"Error")

    for i in sorted(items_data,key=lambda dmg: dmg[1])[::-1]:
        print(i)
        
main_axe()
    
