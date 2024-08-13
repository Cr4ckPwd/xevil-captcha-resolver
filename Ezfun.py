import requests
import time

def resolve_funcaptcha(client_key, website_url, website_key):
	try:
		print("Starting funcaptcha resolution...")
		
		# Create task
		create_task_url = "https://api.ez-captcha.com/createTask"
		create_task_payload = {
			"clientKey": client_key,
			"task": {
				"websiteURL": website_url,
				"websiteKey": website_key,
				"type": "FuncaptchaTaskProxyless"
			}
		}
		print(f"Sending create task request to {create_task_url} with payload: {create_task_payload}")
		create_task_response = requests.post(create_task_url, json=create_task_payload)
		print(f"Create task response status code: {create_task_response.status_code}")
		print(f"Create task response content: {create_task_response.text}")
		create_task_response.raise_for_status()  # Check for HTTP errors
		create_task_data = create_task_response.json()
		print(f"Create task response JSON: {create_task_data}")
		
		if "taskId" not in create_task_data:
			raise Exception("Failed to create task: 'taskId' not found in response")
		
		task_id = create_task_data["taskId"]
		print(f"Task ID: {task_id}")

		# Get task result
		get_task_result_url = "https://api.ez-captcha.com/getTaskResult"
		get_task_result_payload = {
			"clientKey": client_key,
			"taskId": task_id
		}

		while True:
			print(f"Sending get task result request to {get_task_result_url} with payload: {get_task_result_payload}")
			get_task_result_response = requests.post(get_task_result_url, json=get_task_result_payload)
			print(f"Get task result response status code: {get_task_result_response.status_code}")
			print(f"Get task result response content: {get_task_result_response.text}")
			get_task_result_response.raise_for_status()  # Check for HTTP errors
			get_task_result_data = get_task_result_response.json()
			print(f"Get task result response JSON: {get_task_result_data}")
			
			if get_task_result_data["status"] == "ready":
				print("Captcha resolved successfully.")
				return get_task_result_data["solution"]["token"]
			elif get_task_result_data["status"] == "processing":
				print("Captcha is still processing. Waiting for 5 seconds...")
				time.sleep(5)
			else:
				raise Exception("Failed to resolve captcha: " + get_task_result_data.get("error", "Unknown error"))

	except requests.RequestException as e:
		print(f"HTTP Request failed: {e}")
	except Exception as e:
		print(f"An error occurred: {e}")

# Khai báo các biến
client_key = "cc16c71d96d14e94b80d47f3dfe7b7cf261159"
website_url = "https://demo.arkoselabs.com/"
website_key = "DF9C4D87-CB7B-4062-9FEB-BADB6ADA61E6"

# Gọi hàm và in kết quả
print("Calling resolve_funcaptcha function...")
token = resolve_funcaptcha(client_key, website_url, website_key)
if token:
	print("Captcha token:", token)
else:
	print("Failed to get captcha token")