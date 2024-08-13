import requests
import time

api_key = 'API_KEY'
base64_image = 'IMAGE_BASE64'

def solve_base64_captcha():
	while True:
		# Create task
		create_task_url = "http://api.2captcha.com/createTask"
		create_task_payload = {
			"clientKey": api_key,
			"task": {
				"type": "ImageToTextTask",
				"body": base64_image
			}
		}
		
		response = requests.post(create_task_url, json=create_task_payload)
		if response.status_code == 200 and response.json().get('errorId') == 0:
			print(response.text)
			captcha_id = response.json().get('taskId')
		else:
			print('Failed to submit captcha')
			continue

		# Check result
		result = None
		while not result:
			time.sleep(5)
			get_task_result_url = "http://api.2captcha.com/getTaskResult"
			get_task_result_payload = {
				"clientKey": api_key,
				"taskId": captcha_id
			}
			res = requests.post(get_task_result_url, json=get_task_result_payload)
			if res.status_code == 200 and res.json().get('status') == 'ready':
				print(res.text)
				result = res.json().get('solution').get('text')
				return result
			elif res.json().get('status') == 'processing':
				print('Captcha not ready yet')
			elif res.json().get('errorId') != 0:
				print('Captcha unsolvable, requesting again...')
				break
			else:
				print('Failed to get captcha result')
				break

# Run the function to solve base64 captcha and print the result token
result_token = solve_base64_captcha()
if result_token:
	print(result_token)