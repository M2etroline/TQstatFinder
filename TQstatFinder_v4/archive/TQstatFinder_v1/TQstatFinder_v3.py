from selenium import webdriver
from bs4 import BeautifulSoup
import pickle,time

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

def get_sets():
    chrome_path = r'C:\Users\to0dl\Documents\driver\chromedriver.exe'
    driver = webdriver.Chrome(chrome_path)
    driver.get('https://tq-db.net/en/set')
    time.sleep(10)
    all_items=[['set'],[]]
    grid = driver.find_element_by_xpath("""//*[@id="app"]/div/div[2]/div[2]/main/div""")
    items = grid.find_elements_by_class_name("v")   
    for item in items:
        soup = BeautifulSoup(item.get_attribute('innerHTML'),'lxml')
        name=soup.div.div.div.text
        lines = item.find_elements_by_class_name("A7")
        for c in range(len(lines)):
            soup = BeautifulSoup(lines[c].get_attribute('innerHTML'),'lxml')
            sett = soup.div.text
            match1 = soup.find('ul')
            listt = match1.findAll('li')
            bonus_list=[]
            for li in range(len(listt)):
                if li == 0:
                    temp_name=name+' '+sett
                else:
                    bonus_list.append(listt[li].text)
            all_items[1].append([temp_name,bonus_list])
    return all_items
        

    #return all_items_data,[len(all_items),len(all_items_data)]
    
def get_items(link):

    chrome_path = r'C:\Users\to0dl\Documents\driver\chromedriver.exe'
    driver = webdriver.Chrome(chrome_path)
    driver.get('https://www.tq-db.net'+link)
    time.sleep(10)
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

def bonus_digester(bonus_list,item,name,percent,sortby,nsearch):
    for ass in bonus_list:
        splat=ass.split()
        lesplat=len(splat)
        try:
            if set(name.split()).issubset(splat) and (not any(item in splat for item in nsearch.split())):
                count=0
                inumlist=[]
                for i in range(lesplat):
                    if '%' in splat[i]:
                        splat[i] = splat[i][:-1]
                    if ('+' in splat[i]):
                        splat[i] = splat[i][1:]                        
                    try:
                        a=float(splat[i])
                        count+=1
                        inumlist.append(i)
                    except:
                        a=1
                #print(count,splat)
                if sortby == 'chance':
                    return [float(splat[inumlist[0]]),ass,item]
                if sortby == 'value':
                    if '~' in ass:
                        if percent == 0:
                            if count == 2:
                                return [(float(splat[inumlist[0]])+float(splat[inumlist[1]]))/2,ass,item]
                    else:
                        if count == 1:
                            if percent == 1:
                                if '%' in ass.split()[0]:
                                    return [float(splat[inumlist[0]]),ass,item]
                            else:
                                if '%' not in ass.split()[0]:
                                    return [float(splat[inumlist[0]]),ass,item]
                        if count == 2:
                            if percent == 1:
                                if '%' in ass.split()[0]:
                                    if 'Chance' not in ass:
                                        return [float(splat[inumlist[0]]),ass,item]
                                    else:
                                        if '%' in ass.split()[inumlist[1]]:
                                            return [float(splat[inumlist[1]]),ass,item]
                            else:
                                if '%' not in ass.split()[0]:
                                    if 'Chance' not in ass: 
                                        return [float(splat[inumlist[0]]),ass,item]
                                    else:
                                        return [float(splat[inumlist[1]]),ass,item]
                        
        except:
            print(i,item)


def core():

    item_data=[]

    item_data.append(get_sets())

    count=1
    
    for link in get_links():
        
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
                            if '%' in line.text.split()[0]:
                                big_chance=line.findAll('div')
                                numbr=len(big_chance)
                                try:
                                    chan=int(line.text.split()[0][:-1])
                                except:
                                    print(line.text.split())
                                for i in big_chance:
                                    bonus_list.append(str(round(chan/numbr, 2))+'%'+' Chance of '+i.text)
                            else:
                                big_chance=line.findAll('div')
                                numbr=len(big_chance)
                                for i in big_chance:
                                    bonus_list.append(str(round(1/numbr*100, 2))+'%'+' Chance of '+i.text)

                        elif (':' in line.text) and ('Chance of' in line.text):
                            big_chance=line.findAll('div')
                            chan=line.text.split()[0]
                            for i in big_chance:
                                bonus_list.append(chan+' Chance of '+i.text)
                        else:
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
            
def Check(search,nsearch,percent,sortby):
    item_data=LoadData()
    for category in item_data:
        print('\n',category[0],'\n'+'-'*15+'\n')
        items=[]
        for item in category[1]:
            uh=bonus_digester(item[1],item[0],search,percent,sortby,nsearch)
            if uh!=None:
                items.append(uh)
        for duh in sorted(items)[::-1]:
            print(duh[1],', \"'+duh[2]+'\"')
            
#Check('Reduction to Enemy\'s Health','',1,'value')       
core()

    
