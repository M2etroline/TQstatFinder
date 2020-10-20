from selenium import webdriver
from bs4 import BeautifulSoup
import pickle

def get_links():
    
    chrome_path = r'C:\Users\to0dl\Documents\driver\chromedriver.exe'
    driver = webdriver.Chrome(chrome_path)
    driver.get('https://www.tq-db.net')
    grid = driver.find_element_by_xpath("""//*[@id="app"]/div/div[1]/nav/div""")
    soup = BeautifulSoup(grid.get_attribute('innerHTML'),'lxml')
    links = soup.findAll('a')
    links.remove(links[22])
    links_text=[]
    for i in links[5:]:
        links_text.append(i.get('href'))
    return links_text

def get_items(link):

    chrome_path = r'C:\Users\to0dl\Documents\driver\chromedriver.exe'
    driver = webdriver.Chrome(chrome_path)
    driver.get('https://www.tq-db.net'+link)
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

def bonus_digester(bonus_list,item,name,percent,sortby):
    for i in bonus_list:
        splat=i.split()
        lesplat=len(splat)
        try:
            if lesplat>4:
                if splat[4]=='~':
                    #print(splat)
                    if set(name.split()).issubset(splat):
                        if len(splat)==len(name.split())+5:
                            if sortby == 'chance':
                                return [float(splat[0]),i,item]
                            else:
                                return [(float(splat[3])+float(splat[5]))/2,i,item]         
            if 'Chance' in i:
                if len(splat)==len(name.split())+2:
                    if set(name.split()).issubset(splat):
                        if percent == 1:
                            if '%' in splat[3]:
                                if sortby == 'chance':
                                    return [float(splat[0]),i,item]
                                else:
                                    if '+' in splat[3]:
                                        return [float(splat[3][1:-1]),i,item]
                                    elif '-' in splat[3]:
                                        return [-float(splat[3][1:-1]),i,item]
                                    else:
                                        return [float(splat[3][:-1]),i,item]
                        else:
                            if '%' not in splat[3]:
                                return [float(splat[3][1:]),i,item]
            elif 'over' in i:
                if len(splat)==len(name.split())+5:
                    if set(name.split()).issubset(splat):
                        if sortby == 'time':
                            return [float(splat[-2]),i,item]
                        else:
                            return [float((float(splat[0])+float(splat[2]))/2),i,item]
                
            else:
                if len(splat)==len(name.split())+1:
                    if set(name.split()).issubset(splat):       
                        if percent:
                            if '%' in i:
                                if '+' in i:
                                    return [float(splat[0][1:-1]),i,item]
                                elif '-' in i:
                                    return [-float(splat[0][1:-1]),i,item]
                                else:
                                    return [float(splat[0][:-1]),i,item]
                        else:
                            if '%' not in i:
                                if '+' in i:
                                    return [float(splat[0][1:]),i,item]
                                elif '-' in i:
                                    return [-float(splat[0][1:]),i,item]
                                else:
                                    return [float(splat[0]),i,item]
            
        except:
            print(i,item)


def core():

    item_data=[]

    count=0
    
    for link in ['/en/category/staff']:
        
        all_items_data= get_items(link)[0]
        item_data.append([link[13:],[]])

        
        for item in all_items_data:            
            soup = BeautifulSoup(item,'lxml')

            bonus_list=[]
            holder = soup.div.findAll('div', class_ = 'Aw')
            
            for item in holder:
                for description in item.div.div:
                    for line in description.findAll('li'):
                        if (':' in line.text) and ('Chance for one of the following' in line.text):
                            if '%' in line.text:
                                big_chance=line.findAll('div')
                                numbr=len(big_chance)
                                chan=int(line.text.split()[0][:-1])
                                for i in big_chance:
                                    bonus_list.append(str(round(chan/numbr, 2))+'%','Chance of',i.text)
                            else:
                                big_chance=line.findAll('div')
                                numbr=len(big_chance)
                                for i in big_chance:
                                    bonus_list.append(str(round(1/numbr*100, 2))+'%','Chance of',i.text)

                        if (':' in line.text) and ('Chance of' in line.text):
                            big_chance=line.findAll('div')
                            chan=line.text.split()[0]
                            for i in big_chance:
                                bonus_list.append(chan,'Chance of',i.text)
                        bonus_list.append(line.text)
                        
            match1 = soup.div.find('div', class_='A1')
            name = match1.find('a', class_='A5').text
            item_data[count][1].append([name,bonus_list])
              
        count += 1
    with open('ItemData.pkl', 'wb') as fid:
        pickle.dump(item_data, fid)



def LoadData():
    with open('ItemData.pkl', 'rb') as fid:
        item_data = pickle.load(fid)
    return item_data
            
def Check(search,percent,sortby):
    item_data=LoadData()
    for category in item_data:
        print('\n',category[0],'\n'+'-'*15+'\n')
        items=[]
        for item in category[1]:
            uh=bonus_digester(item[1],item[0],search,percent,sortby)
            if uh!=None:
                items.append(uh)
        for duh in sorted(items)[::-1]:
            print(duh[1],', \"'+duh[2]+'\"')
            
Check('Chance of Piercing Retaliation',1,'value')       
#core()
    
