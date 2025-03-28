# Instagram scraper
This script scrapes the bio of instagram accounts
This was a part of a personal project and my script evolved and i landed on this.
## Evolution
### 1. Using instaloader library
This did not work because instagram had frequent rate limits for my big list of usernames
### 2. Using requests
This would utilize a third party website to scrape the bio. I noticed that anonymous story viewer lets you view instagram stories as well as they show username, followers and followings, and biography.
I would `get request` this website.com/username to get the html which had the biography. It worked for a few usernames but, it turns out for a newer usernames it would need to load the information 
and after it gets the information, the javascript updates the webpage. So i was getting a skeleton of the webpage from the `get request` without any information as it requests the very first html.
I thought, if found a way to let the website load I might pull it off.
### 3. Using phantom.js
I came across a fourm that mentioned that for a dynamic website `requests` fail and I had to switch to `phantom.js`. I tried this approach but once again i kept recieving empty biography, perhaps the information still hadnt loaded.
### 4. Using webdriver
I finally switched to webdriver, It would fix the issue of letting the website load before i scraped the information, however, i thought webdriver takes a long time to get the data compared to simply requesting it. I used selenium and after a very long time i eventually found a way to wait till the information fully loaded. This was a challange because some users dont have biography and there was no way to differentiate if they actually dont have the information or has it not loaded. The answer lied in following list. I had gotten the usernames from followers list of a massive account which meant that all these accounts had atleast 1 following. I simply waited for the site till the followings was no longer 0.
The problem was, even thoough its headless, it still takes time. This approach worked, I still had issues with rate limits but it was not as bad (prbl because the website owner had accounted for this issue). 
This is the script which this repo is about.
### 5. Using websocket
I had to find out how the website was requesting for the users information. If i can replicate it, i can get the information directly without needing to load the website. After further investigation i realized, the site was communicating to a server via websocket and the information was handded after handshake. This was the first time i was introduced to websocket and how handshakes worked in this site.
the handshake
