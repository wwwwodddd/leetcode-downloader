# leetcode-downloader
Download all your LeetCode**CN** and LeetCode**US** submissions

下载你的所有力扣**中国**和力扣**美国**的提交记录

## Usage
`lccn.py` 需要 `requests`，`lcus.py` 需要 `selenium`。

`lccn.py` requires `requests`, `lcus.py` requires `selenium`.

```
$ python3 lccn.py
Username: input_your_username
Password: input_your_password
$ python3 lcus.py
Username: input_your_username
Password: input_your_password
```

The result will be in the folder `Accepted`(only latest accepted) and `yyyymmdd_hhmmss`(date and time, all submissions)

结果将保存在文件夹 `Accepted`(最近正确提交) 和 `yyyymmdd_hhmmss`(日期时间，所有提交)
