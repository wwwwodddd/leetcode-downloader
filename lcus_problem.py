import urllib3
import json
import re

def get_csrftoken():
    http = urllib3.PoolManager()
    r = http.request(
        'GET',
        'https://leetcode.com/problemset/all/',
        redirect=False
    )
    if r.status != 302:
        raise RuntimeError('Fail to get csrftoken! status: %d, data: %s' % (r.status, r.data))
    match_obj = re.search('csrftoken=(\S+); ', r.headers['Set-Cookie'])
    if match_obj:
        return match_obj.group(1)
    else:
        raise RuntimeError('Fail to parse csrftoken from headers! headers: %s' % r.headers)

def fetch_problems(csrftoken, limit=50):
    http = urllib3.PoolManager()
    cookie = 'csrftoken=%s' % csrftoken
    data = {
        'query': 'query problemsetQuestionList($categorySlug:String,$limit:Int,$skip:Int,$filters:QuestionListFilterInput){problemsetQuestionList:questionList(categorySlug:$categorySlug limit:$limit skip:$skip filters:$filters){total:totalNum questions:data{acRate difficulty freqBar frontendQuestionId:questionFrontendId isFavor paidOnly:isPaidOnly status title titleSlug topicTags{name id slug}hasSolution hasVideoSolution}}}',
        'variables': {
            'categorySlug': '',
            'skip': 0,
            'limit': limit,
            'filters': {},
        },
    }
    encoded_data = json.dumps(data).encode('utf-8')
    r = http.request(
        'POST',
        'https://leetcode.com/graphql/',
        body=encoded_data,
        headers={
            'Content-Type': 'application/json',
            'cookie': cookie,
        },
    )
    if r.status != 200:
        raise RuntimeError('Fail to fetch problems! status: %d, data: %s' % (r.status, r.data))
    response_content = json.loads(r.data)
    return response_content

def main():
    print('Now try get csrftoken...')
    csrftoken = get_csrftoken()
    print('Got csrftoken %s.' % csrftoken)

    response_content = fetch_problems(csrftoken)
    total_count = response_content['data']['problemsetQuestionList']['total']

    response_content = fetch_problems(csrftoken, total_count)
    problems_list = response_content['data']['problemsetQuestionList']['questions']
    print('len(problems_list)', len(problems_list))
    with open('lcus_problem.json', 'w') as fout:
        json.dump(problems_list, fout, indent=4)

if __name__ == '__main__':
    main()
