# jsonl_check_fillter

检查jsonl文件是否可被解析，并把可解析的行和解析出错的行分别输出到两个文件
使用：
```
python3 json_check.py /path/jsonl/
```

输入：需要解析的jsonl文件目录（会递归遍历）
输出：在jsonl文件同目录输出 .jsonl.checked (验证通过的行) 和 .jsonl.err (验证失败的行)

执行日志在 json_check.log

需要将jsonl.checked覆盖回jsonl可以使用下面的linux命令
```
find /path/to/a -type f -name "*.jsonl.checked" -exec sh -c 'mv "$0" "${0%.*}"' {} \;
```
需要把所有的err文件移动，可以使用：
```
find /path/to/a -type f -name "*.json.err" -exec mv {} ./ \;
```
