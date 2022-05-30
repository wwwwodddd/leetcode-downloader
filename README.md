# leetcode-downloader
Download all your LeetCode**CN** and LeetCode**US** submissions

下载你的所有力扣**中国**和力扣**美国**的提交记录

Download all problems info

下载所有问题信息

## Usage
`lccn_submission.py` requires `requests`, `lcus_submission.py` requires `selenium`.

`lccn_problem.py` downloads LCCN problem list, `lcus_problem.py` downloads LCUS problem list.

`lccn_submission.py` 需要 `requests`，`lcus_submission.py` 需要 `selenium`。

`lccn_problem.py` 下载 LCCN 题目列表，`lcus_problem.py` 下载 LCUS 题目列表。

```
$ python3 lccn_submission.py
Username: input_your_username
Password: input_your_password
$ python3 lcus_submission.py
Username: input_your_username
Password: input_your_password
$ python3 lccn_problem.py
$ python3 lcus_problem.py
```

The result will be saved in the folder `lccn_username` 和 `lcus_username`(all submissions, all information, json format)

结果将保存在文件夹 `lccn_username` 和 `lcus_username`（所有提交，所有信息，json 格式）

Only incremental submissions will be downloaded, existing submissions will be skipped.

只会下载增量提交，已有提交会被跳过。

The latest accepted submissions will be saved in `Accepted`.

最近正确提交会保存在 `Accepted`。

All problems info will be saved in `lccn_problem.json` and `lcus_problem.json`.

所有问题信息会被保存在 `lccn_problem.json` 和 `lcus_problem.json`。
