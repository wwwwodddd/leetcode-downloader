import os
import json
import time
import datetime
import sys
import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

yyyymmdd_hhmmss = datetime.datetime.today().strftime('%Y%m%d_%H%M%S') # log folder name

lang2extension = {'cpp' : 'cpp', 'java' : 'java', 'python' : 'py', 'python3' : 'py', 'c' : 'c', 'csharp' : 'cs', 'javascript' : 'js', 'ruby' : 'rb', 'swift' : 'swift', 'golang' : 'go', 'scala' : 'scala', 'kotlin' : 'kt', 'rust' : 'rs', 'mysql' : 'sql', 'bash' : 'sh'}

username = input('Username: ') # change this to username
password = getpass.getpass() # change this to password

#selenium configurations
chromeOptions = webdriver.ChromeOptions()
prefs = {'safebrowsing.enabled': 'false'}
chromeOptions.add_experimental_option('prefs',prefs)
chromedriver = 'chromedriver'
driver = webdriver.Chrome(executable_path=chromedriver, options=chromeOptions)

#user agent configurations
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)    Chrome/41.0.2228.0 Safari/537.36'

# Login
driver.get('https://leetcode.com/accounts/login/')
time.sleep(3)

print('Try to input username')
already_present = driver.find_element(by=By.NAME, value='login').get_attribute('value')
for i in range(len(already_present)+1):
	driver.find_element(by=By.NAME, value='login').send_keys(Keys.BACKSPACE)
driver.find_element(by=By.NAME, value='login').send_keys(username)
time.sleep(1)

print('Try to input password')
already_present = driver.find_element(by=By.NAME, value='password').get_attribute('value')
for i in range(len(already_present)+1):
	driver.find_element(by=By.NAME, value='password').send_keys(Keys.BACKSPACE)
driver.find_element(by=By.NAME, value='password').send_keys(password)
time.sleep(1)

driver.find_element(by=By.ID,value='signin_btn').click()
time.sleep(5)

try:
	err_msg = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/p').text
	if 'CAPTCHA' in err_msg:
		input('Help me input the CAPTCHA, and press ENTER')
		driver.find_element(by=By.XPATH, value="//button[@class='btn__2FMG fancy-btn__CYhs primary__3S2m light__3zR9 btn__1eiM btn-md__3VAX ']").click()
		# You may increase below timer to 10 if you have slow internet connection.
		time.sleep(5)
		err_msg = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/div/div[2]/div/div/div/p').text
	if 'username' in err_msg:
		print('Wrong username and/or password')
		print('Exiting...')
		sys.exit()
except Exception as e:
	print('Login Successful')
	# You may increase below timer to 10 if you have slow internet connection.
	time.sleep(5)

time.sleep(3)
accepted_title_slug = set()
os.makedirs('Accepted', exist_ok=True)
leetcodecn_address = 'https://leetcode.com/'

def main():
	offset = 0
	while True:
		print('offset', offset)
		submissions_url = leetcodecn_address + 'api/submissions/?offset=' + str(offset) + '&limit=20&lastkey='
		driver.get(submissions_url)
		time.sleep(6)
		result = json.loads(driver.find_element(by=By.TAG_NAME, value='body').text)
		# print(json.dumps(result, indent=4, ensure_ascii=False))
		if 'submissions_dump' not in result or len(result['submissions_dump']) == 0:
			break
		for submission in result['submissions_dump']:
			title_slug = submission['title_slug']
			lang = submission['lang']
			submission_time = submission['timestamp']
			folder_path = 'lcus_%s/%s' % (username, title_slug)
			json_path = '%s/%s.json' % (folder_path, submission_time)
			if os.path.exists(json_path):
				return
			os.makedirs(folder_path, exist_ok=True)
			json.dump(submission, open(json_path, 'w'), indent=4, ensure_ascii=False)
			if submission['status_display'] == 'Accepted' and title_slug not in accepted_title_slug:
				accepted_title_slug.add(title_slug)
				with open('Accepted/%s.%s' % (title_slug, lang2extension.get(lang, lang)), 'w') as fout:
					fout.write(submission['code'])
		offset += 20

main()
driver.close()
