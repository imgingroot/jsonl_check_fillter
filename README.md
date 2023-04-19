# jsonl_check_fillter

检查jsonl文件是否可被解析，并把可解析的行和解析出错的行分别输出到两个文件

 **使用**：
```
python3 json_check.py /path/jsonl/ 
```

支持按照属性过滤清洗数据：
```
python3 json_check.py /path/jsonl/ --property "id > 100" "id < 106"
```
以上命令会把json中 id > 100 and id < 106 的记录保留，其他记录放入err中。目前只是4种运算符 > 、< 、!= 、== ，其中大小判断为数值，等于判断为字符串，也可以增加字符串包含或正则处理。 **一定要按照这个写法，空格不能多也不能少 ^_^  "id > 10000000" **

**输入**：需要解析的jsonl文件目录（会递归遍历） 

**输出**：在jsonl文件同目录输出文件:
 - .jsonl.checked (验证通过的行) 
 - .jsonl.err (验证失败的行)

执行日志在 json_check.log

需要将jsonl.checked覆盖回jsonl可以使用下面的linux命令
```
find /path/to/a -type f -name "*.jsonl.checked" -exec sh -c 'mv "$0" "${0%.*}"' {} \;
```
需要把所有的err文件移动，可以使用：
```
find /path/to/a -type f -name "*.jsonl.err" -exec mv {} ./ \;
```
