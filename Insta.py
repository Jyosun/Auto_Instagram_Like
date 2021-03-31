import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from random import randint

random_wait_min = 7
random_wait_max = 9

random_next_min = 1
random_next_max = 5

refresh_count = 40
onetime_count = 45

like_count = 0;

tag = ['#Like']
comment_list = ['PLZ LIKE ME BACK']

comment_flag = True

follow_flag = True
follow_count = 0

options = webdriver.ChromeOptions()
options.add_argument("lang=ko_KR")

browser = webdriver.Chrome("C:\\ChromeDriver\\chromedriver.exe", chrome_options=options) # Download the chrome driver and enter the address
browser.get('https://www.instagram.com/?hl=ko')
browser.maximize_window()
time.sleep(2)

# Login
browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys('My_ID') # Enter your ID
browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys('My_Password') # Enter your Password
browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
time.sleep(3)
browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
time.sleep(2)
browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
time.sleep(2)

# Searching with tag
time.sleep(1)
search = browser.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
search.send_keys(tag)

# Entering Top-Level Search Results
time.sleep(3)
search.send_keys(Keys.RETURN)
search.send_keys(Keys.RETURN)

prev_url = browser.current_url

time.sleep(3)

# Moving to next post
def nextFeed():
     time.sleep(2)
     nextFeed = browser.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.EfHg9 > div > div > a._65Bje.coreSpriteRightPaginationArrow')
     nextFeed.click() 

for b in range(refresh_count):
    
    # Selecting the first post among the most recent posts
    time.sleep(5)
    feed = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[3]/div[3]/a')
    feed.send_keys(Keys.ENTER)
    nextFeed()

    for a in range(onetime_count):
        # Pressing Like Button
        time.sleep(randint(random_wait_min,random_wait_max))
        try:
            like_list = browser.find_elements_by_xpath('//article//section/span/button')
            likeBtnTxt = browser.find_elements_by_class_name('_8-yf5 ')
        
            like_pass = False

            for i in range ( len ( likeBtnTxt ) ) :
                if likeBtnTxt[i].get_attribute("aria-label") == 'Unlike' :
                    like_pass = True
                    print(likeBtnTxt[i].get_attribute("aria-label"), "Pass like")
                    break

            if like_pass == False :
                like_list[0].click()
                like_count += 1
                print ("like count = ", like_count)
                refresh_err = 0

                # Leaving a comment
                try : 
                    comment = browser.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[3]/div/form/textarea')
                except : 
                    try :
                        comment = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[3]/div/form/textarea')
                    except :
                        print ("exception in Comment")
                        break 

                comment_content = comment_list[randint(0,len(comment_list)-1)]

                ac = ActionChains(browser)
                ac.move_to_element(comment)
                ac.click()
                ac.pause(3)
                ac.send_keys(comment_content)
                ac.pause(1)
                ac.send_keys(Keys.ENTER)
                ac.perform()

                print ("Comment Sucess ", comment_content)

                # Following
                try : 
                    follow = browser.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[2]/button')
                except : 
                    try :
                        follow = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button')
                    except :
                        print ("exception in Follow")
                        break 
                            
                if follow.text == 'Follow':
                    follow.send_keys(Keys.ENTER)

                time.sleep(2)

                if follow.text == 'Following':
                    follow_count += 1
                    print ("Follow Sucess", follow_count)

        except :
            print("exception!")

        # Moving to next feed
        for b in range(randint(random_next_min,random_next_max)):
            nextFeed()

    browser.get(prev_url)
    print ("refresh!")