import requests
import time

api_key = 'API_KEY'
base64_image = 'IMAGE_BASE64'
img_instructions = 'Image instructions'

def solve_base64_captcha():
	while True:
		# Send request to solve base64 captcha
		multipart_data = {
			'key': (None, api_key),
			'method': (None, 'base64'),
			'body': (None, base64_image),
			'imginstructions': (None, img_instructions),
			'recaptcha': (None, '1')
		}
		
		response = requests.post('http://2captcha.com/in.php', files=multipart_data)
		if response.status_code == 200 and 'OK|' in response.text:
			print(response.text)
			captcha_id = response.text.split('|')[1]
		else:
			print('Failed to submit captcha')
			continue

		# Check result
		result = None
		while not result:
			time.sleep(5)
			res = requests.get(f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}')
			if res.status_code == 200 and 'OK|' in res.text:
				print(res.text)
				return result
			elif 'CAPCHA_NOT_READY' in res.text:
				print('Captcha not ready yet')
			elif 'ERROR_CAPTCHA_UNSOLVABLE' in res.text:
				print('Captcha unsolvable, requesting again...')
				break
			else:
				print('Failed to get captcha result')
				break

# Run the function to solve base64 captcha and print the result token
result_token = solve_base64_captcha()
if result_token:
	print(result_token)