import pickle,os

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
            print("The programme struggled with -",i,item)

def LoadData():
    with open('ItemData.pkl', 'rb') as fid:
        item_data = pickle.load(fid)
    return item_data
            
def Check(search,nsearch='',percent=1,sortby='value'):
    item_data=LoadData()
    for category in item_data:
        print('\n',category[0],'\n'+'-'*15+'\n')
        items=[]
        for item in category[1]:
            uh=bonus_digester(item[1],item[0],search,percent,sortby,nsearch)
            if uh!=None:
                items.append(uh)
        for duh in sorted(items)[::-1]:
            print('    '+duh[1],', \"'+duh[2]+'\"')

def Main():
    search = input("    Enter words you are looking for : ")
    print()
    nsearch = input("    Enter words you want to omit : ")
    print()
    percent = input("""    Enter:

    1 - if you look for stat like: +30% Health
    
    0 - if you look for stat like: 300 Health
    
    : """)
    print()
    sortby = input("""    Enter:

    value - to sort by value

    chance - to sort by chance
    
    : """)
    print()
    Check(search,nsearch,percent,sortby)
    return 0

os.system('mode con: cols=100 lines=1000')
print("""\n      Be aware that you may experience problems with the programme,
      most common being that some information may not appear,
      depending on whether you use value or chance to sort.\n""")
while True:
    Main()
    print('\nPress any key to search again, or enter \'q\' to leave.\n')
    if (input()=='q'):
        break


    
