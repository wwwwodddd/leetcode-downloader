# -*- coding: utf-8 -*-
#/usr/bin/env python3
"""
这是一个将力扣中国(leetcode-cn.com)上的【个人提交】的submission自动爬到本地并push到github上的爬虫脚本。
请使用相同目录下的config.json设置 用户名，密码，本地储存目录等参数。
致谢@fyears， 本脚本的login函数来自https://gist.github.com/fyears/487fc702ba814f0da367a17a2379e8ba
原仓库地址：https://github.com/JiayangWu/LeetCodeCN-Submissions-Crawler
如果爬虫失效的情况，请在原仓库提出issue。
"""
import os
import json
import time
import datetime
import requests

#~~~~~~~~~~~~以下是无需修改的参数~~~~~~~~~~~~~~~~·
requests.packages.urllib3.disable_warnings() #为了避免弹出一万个warning，which is caused by 非验证的get请求

leetcode_url = 'https://leetcode-cn.com/'

sign_in_url = leetcode_url + 'accounts/login/'
submissions_url = leetcode_url + 'submissions/'

yyyymmdd_hhmmss = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')

def login(): # 本函数修改自https://gist.github.com/fyears/487fc702ba814f0da367a17a2379e8ba，感谢@fyears
    client = requests.session()
    client.encoding = "utf-8"
    # try:
    #     client.get(sign_in_url, verify=False)
    #     login_data = {'login': config['username'], 'password': config['password']}
    #     result = client.post(sign_in_url, data = login_data, headers = dict(Referer = sign_in_url))
    #     assert result.ok
    # except:
    #     print ("Login failed! Wait till next round!")
    #     assert False
    return client

def downloadQuestion(titleSlug, client):
    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
    }   
    param = {'operationName': 'questionData',
            'variables': {'titleSlug': titleSlug},
            'query': 'query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    questionFrontendId    categoryTitle    boundTopicId    title    titleSlug    content    translatedTitle    translatedContent    isPaidOnly    difficulty    likes    dislikes    isLiked    similarQuestions    contributors {      username      profileUrl      avatarUrl      __typename    }    langToValidPlayground    topicTags {      name      slug      translatedName      __typename    }    companyTagStats    codeSnippets {      lang      langSlug      code      __typename    }    stats    hints    solution {      id      canSeeDetail      __typename    }    status    sampleTestCase    metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    envInfo    book {      id      bookName      pressName      source      shortDescription      fullDescription      bookImgUrl      pressImgUrl      productUrl      __typename    }    isSubscribed    isDailyQuestion    dailyRecordStatus    editorType    ugcQuestionId    style    exampleTestcases    jsonExampleTestcases    __typename  }}'
            }

    param_json = json.dumps(param)
    time.sleep(1)
    response = client.post("https://leetcode-cn.com/graphql/", data = param_json, headers = headers)
    result = response.json()
    # print(json.dumps(result, indent=4, ensure_ascii=False))
    json.dump(result, open('%s/%s.json' % (yyyymmdd_hhmmss, titleSlug), 'w'), indent=4, ensure_ascii=False)

def downloadproblemsetQuestionList(skip, client):
    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
    }   
    param = {'operationName': 'problemsetQuestionList',
            'variables': {'categorySlug': '', 'filters': {}, 'limit': 100, 'skip': skip},
            'query': '    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {  problemsetQuestionList(    categorySlug: $categorySlug    limit: $limit    skip: $skip    filters: $filters  ) {    hasMore    total    questions {      acRate      difficulty      freqBar      frontendQuestionId      isFavor      paidOnly      solutionNum      status      title      titleCn      titleSlug      topicTags {        name        nameTranslated        id        slug      }      extra {        hasVideoSolution        topCompanyTags {          imgUrl          slug          numSubscribed        }      }    }  }}    '
            }

    param_json = json.dumps(param)
    time.sleep(3)
    response = client.post("https://leetcode-cn.com/graphql/", data = param_json, headers = headers)
    result = response.json()
    # print(json.dumps(result['data']['problemsetQuestionList'], indent=4, ensure_ascii=False))
    return result['data']['problemsetQuestionList']['questions']

def main():
    print('Logging in')
    client = login()
    skip = 0

    # os.makedirs(yyyymmdd_hhmmss)

    problems_list = []
    while True:
        print("skip", skip)
        problems = downloadproblemsetQuestionList(skip, client)
        print(skip, len(problems))
        if len(problems) == 0:
            break
        problems_list += problems
        skip += 100
    print('len(problems_list)', len(problems_list))
    with open('lccn_problem.json', 'w') as fout:
        json.dump(problems_list, fout, indent=4, ensure_ascii=False)

    # problems_list = json.load(open('problems_list.json'))
    # for (iprob, problem) in enumerate(problems_list):
    #     print(problem['titleSlug'], iprob, len(problems_list), problem['paidOnly'])
    #     if problem['paidOnly']:
    #         downloadQuestion(problem['titleSlug'], client)

if __name__ == '__main__':
    main()
