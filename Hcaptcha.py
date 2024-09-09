import requests
import time

api_key = '2b8c9292ea263ff1479ca8fef38f9d6f'
site_key = 'c0421d06-b92e-47fc-ab9a-5caa43c04538'
page_url = 'https://2captcha.com/demo/hcaptcha'

def solve_hcaptcha():
    while True:
        # Send request to create a task for solving hCaptcha using 2Captcha API v2
        response = requests.post('http://api.pushon.me/createTask', json={
            'clientKey': api_key,
            'task': {
                'type': 'HCaptchaTaskProxyless',
                'websiteURL': page_url,
                'websiteKey': site_key
            }
        })

        if response.status_code == 200 and response.json().get('errorId') == 0:
            task_id = response.json().get('taskId')
            print(f'Task ID: {task_id}')
        else:
            print('Failed to create task')
            continue

        # Check result
        result = None
        while not result:
            time.sleep(5)
            res = requests.post('http://api.pushon.me/getTaskResult', json={
                'clientKey': api_key,
                'taskId': task_id
            })
            if res.status_code == 200:
                res_json = res.json()
                if res_json.get('status') == 'ready':
                    result = res_json.get('solution').get('gRecaptchaResponse')
                    print(f'Captcha solved: {result}')
                    return result
                elif res_json.get('status') == 'processing':
                    print('Captcha not ready yet')
                else:
                    print('Failed to get captcha result')
                    break
            else:
                print('Failed to get captcha result')
                break

# Run the function to solve hCaptcha
solve_hcaptcha()