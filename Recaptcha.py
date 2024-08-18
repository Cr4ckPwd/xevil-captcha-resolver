import requests
import time
#API key and site key
api_key = '2b8c9292ea263ff1479ca8fef38f9d6f'
site_key = 'Data-sitekey'
page_url = 'Page-url'

def solve_recaptcha():
	try:
		# Create task
		create_task_url = "http://api.pushon.me/createTask"
		create_task_payload = {
			"clientKey": api_key,
			"task": {
				"type": "RecaptchaV2TaskProxyless",
				"websiteURL": page_url,
				"websiteKey": site_key
			}
		}
		create_task_response = requests.post(create_task_url, json=create_task_payload)
		create_task_response.raise_for_status()  # Check for HTTP errors
		create_task_data = create_task_response.json()
		print(create_task_data)

		if "taskId" not in create_task_data:
			raise Exception("Failed to create task: 'taskId' not found in response")

		task_id = create_task_data["taskId"]

		# Get task result
		get_task_result_url = "http://api.pushon.me/getTaskResult"
		get_task_result_payload = {
			"clientKey": api_key,
			"taskId": task_id
		}

		while True:
			get_task_result_response = requests.post(get_task_result_url, json=get_task_result_payload)
			get_task_result_response.raise_for_status()  # Check for HTTP errors
			get_task_result_data = get_task_result_response.json()
			print(get_task_result_data)

			if get_task_result_data["status"] == "ready":
				return get_task_result_data["solution"]["gRecaptchaResponse"]
			elif get_task_result_data["status"] == "processing":
				time.sleep(5)
			else:
				raise Exception("Failed to resolve captcha: " + get_task_result_data.get("error", "Unknown error"))

	except requests.RequestException as e:
		print(f"HTTP Request failed: {e}")
	except Exception as e:
		print(f"An error occurred: {e}")

# Run the function to solve reCAPTCHA
solve_recaptcha()