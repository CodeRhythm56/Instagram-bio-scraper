from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import pandas as pd
import time
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--window-size=1920,1080')
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
 
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser,15)
attempts=0
df = pd.read_csv('oterobar.csv',encoding='utf-8')
refresh = False
for x in range(150,len(df)): #len(df)
    while True:
        try:
            username=df.iloc[x]['username']
            if not refresh:
                browser.get(f"https://insta-stories-viewer.com/{username}/")
            refresh=False
           
            #attempts at waiting till the bio loads
            #html = browser.find_element(By.XPATH, '/html/body/section/div[2]/div/div[2]/div[2]/div')
            #html = browser.find_element(By.CLASS_NAME, 'profile__description')
            #html = browser.find_element(By.CSS_SELECTOR, 'body > section > div.center > div > div.profile__header > div.profile__header-right > div')
            #htmlofpfp = wait.until_not(EC.visibility_of("""<img class="profile__avatar-pic" src="/static/images/no-avatar.png">"""))
            #htmlofnopfp = wait.until_not(EC.all_of(browser.find_element(By.XPATH,'/html/body/section/div[2]/div/div[2]/div[1]/div/div[1]/img').text=="/static/images/no-avatar.png"))
            #htmlofnopfp=wait.until_not(EC.all_of(EC.visibility_of(browser.find_element(By.LINK_TEXT,"/static/images/no-avatar.png"))))
            #htmlofstat = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/section/div[2]/div/div[2]/div[1]/div/div[1]/img')))
            # htmlofpfp = wait.until((EC.visibility_of(browser.find_element(By.XPATH, '/html/body/section/div[2]/div/div[2]/div[1]/div/div[1]/img'))))
            # htmlofnopfp = wait.until_not(EC.element_attribute_to_include((By.XPATH,'/html/body/section/div[2]/div/div[2]/div[1]/div/div[1]/img'),"/static/images/no-avatar.png"))
            #htmlofnoopfp = wait.until(EC.invisibility_of_element(EC.element_attribute_to_include((By.XPATH,'/html/body/section/div[2]/div/div[2]/div[1]/div/div[1]/img'),"/static/images/no-avatar.png")))
            wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/section/div[2]/div/div[2]/div[2]/ul/li[3]/span')))
            wait.until(lambda browser: browser.find_element(*(By.XPATH,'/html/body/section/div[2]/div/div[2]/div[2]/ul/li[3]/span')).text != "0") #following != 0, genius move
            time.sleep(0.1)
 
            html = browser.find_element(By.XPATH, '/html/body/section/div[2]/div/div[2]/div[2]/div')
            bio = html.text
            if bio =="":
                df.loc[df['username'] == username, 'biography'] = "<Empty>"
                #print("<Empty>")
            else:
                df.loc[df['username']==username,'biography']=bio
                #print(bio)
            df.to_csv("oterobar.csv",index=False)
            print("Success! for ",x+1,"th user")
            attempts=0
 
        except IndexError:
            print("Possible deleted account.")
            break
        except TimeoutException:
            print("Refreshing... user:",username)
            attempts=attempts+1
            if attempts>8:
                attempts=0
                print(f"Too many attempts: skipping{username}")
                browser.get_screenshot_as_file(f"{username}.png")
                break
            browser.get_screenshot_as_file("Screenshot.png")
            refresh = True
            browser.refresh()
            continue
 
        # except Exception as e:
        #     print("Error: ",e)
        #     print("Error! Retrying in 5 seconds.....")
        #     time.sleep(5)
        #     continue
        break
 
browser.quit()
 

