import os
import json
import time
import datetime
import requests
import getpass

requests.packages.urllib3.disable_warnings() # avoid warning

leetcodecn_address = 'https://leetcode.cn/'
login_adress = leetcodecn_address + 'accounts/login/'
submissions_url = leetcodecn_address + 'submissions/'
lang2extension = {'cpp': 'cpp', 'python3': 'py'}

username = input('Username: ') # change this to username
password = getpass.getpass() # change this to password

yyyymmdd_hhmmss = datetime.datetime.today().strftime('%Y%m%d_%H%M%S') # log folder name

def login():
    client = requests.session()
    client.get(login_adress, verify=False)
    para = {'login': username, 'password': password}
    result = client.post(login_adress, data=para, headers={'Referer': login_adress})
    assert result.ok
    return client

def download_submission(submission_id, client):
    print('download_submission', submission_id)
    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
    }   
    para = {'operationName': 'mySubmissionDetail', 'variables': {'id': submission_id},
            'query': "query mySubmissionDetail($id: ID!) {  submissionDetail(submissionId: $id) {    id    code    runtime    memory    statusDisplay    timestamp    lang    passedTestCaseCnt    totalTestCaseCnt    sourceUrl    question {      titleSlug      title      translatedTitle      questionId      __typename    }    ... on GeneralSubmissionNode {      outputDetail {        codeOutput        expectedOutput        input        compileError        runtimeError        lastTestcase        __typename      }      __typename    }    __typename  }}"
            }

    time.sleep(1)
    response = client.post(leetcodecn_address + 'graphql/', data=json.dumps(para), headers=headers)
    result = response.json()
    return result

def main():
    print('Logging in')
    client = login()
    offset = 0
    accepted_titleSlug = set()
    os.makedirs('Accepted', exist_ok=True)
    while True:
        print("offset", offset)
        submissions_url = leetcodecn_address + 'api/submissions/?offset=' + str(offset) + "&limit=20&lastkey="
        response = client.get(submissions_url, verify=False)
        result = response.json()
        if 'submissions_dump' not in result:
            break
        for submission in result['submissions_dump']:
            result = download_submission(submission['id'], client)
            # print(json.dumps(result, indent=4, ensure_ascii=False))
            titleSlug = result['data']['submissionDetail']['question']['titleSlug']
            lang = result['data']['submissionDetail']['lang']
            submission_time = result['data']['submissionDetail']['timestamp']
            folder_path = 'lccn_%s/%s' % (username, titleSlug)
            json_path = '%s/%s.json' % (folder_path, submission_time)
            if os.path.exists(json_path):
                return
            os.makedirs(folder_path, exist_ok=True)
            json.dump(result, open(json_path, 'w'), indent=4, ensure_ascii=False)
            if result['data']['submissionDetail']['statusDisplay'] == 'Accepted' and titleSlug not in accepted_titleSlug:
                accepted_titleSlug.add('titleSlug')
                with open('Accepted/%s.%s' % (titleSlug, lang2extension.get(lang, lang)), 'w') as fout:
                    fout.write(result['data']['submissionDetail']['code'])
        offset += 20

if __name__ == '__main__':
    main()
