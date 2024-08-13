import requests
import time

api_key = '604c824d4fdc49bc453729100bfde8cc'
site_key = '4c672d35-0701-42b2-88c3-78380b0db560'
page_url = 'https://discord.com/register'

def solve_hcaptcha():
	while True:
		# Send request to solve hCaptcha
		response = requests.post('https://2captcha.com/in.php', data={
			'key': api_key,
			'method': 'hcaptcha',
			'sitekey': site_key,
			'pageurl': page_url
		})

		if response.status_code == 200 and 'OK|' in response.text:
			captcha_id = response.text.split('|')[1]
			print(f'Captcha ID: {captcha_id}')
		else:
			print('Failed to submit captcha')
			continue

		# Check result
		result = None
		while not result:
			time.sleep(5)
			res = requests.get(f'https://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}')
			if res.status_code == 200 and 'OK|' in res.text:
				result = res.text.split('|')[1]
				if result == 'ERROR_CAPTCHA_UNSOLVABLE':
					print('Captcha unsolvable, requesting again...')
					break
				print(f'Captcha solved: {result}')
				return result
			elif 'CAPCHA_NOT_READY' in res.text:
				print('Captcha not ready yet')
			else:
				print('Failed to get captcha result')
				break

# Run the function to solve hCaptcha
solve_hcaptcha()