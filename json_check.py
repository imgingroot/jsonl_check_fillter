#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 修复github的meta爬虫因早期代码bug导致的数据问题
# author:water,esbatmop
# 用法：python json_check.py meta数据目录
import json
import os
import logging
import argparse
import jsonlines
import traceback

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterator, *args, **kwargs):
        return iterator

logging.basicConfig(filename='json_check.log', level=logging.INFO)


# 找出目标jsonl文件，重命名成jsonl.raw，调用清洗函数
def recursive_parse_jsonl_files(input_path):
    # 遍历目录及子目录查找 jsonl 文件
    for root, dirs, files in os.walk(input_path):
        for file_name in files:
            if file_name.endswith('.jsonl'):
                input_file = os.path.join(root, file_name)
                raw_file = os.path.join(root, f"{file_name}.raw")
                checked_file = os.path.join(root, file_name)
                err_file = os.path.join(root, f"{file_name}.err")
                # 打印解析日志信息
                logging.info(f"Parsing jsonl files: {input_file}")
                # 重命名 jsonl 文件为 raw 文件，以便备份
                os.rename(input_file, raw_file)
                # 根据文件名，判断文件中id范围
                file_without_extension = os.path.splitext(file_name)[0]
                id_start, id_end = file_without_extension.split('-')
                # 清洗单个 jsonl 文件
                parse_jsonl_file(int(id_start), int(id_end), raw_file, checked_file, err_file)


# 清洗单个jsonl
def parse_jsonl_file(id_start, id_end, input_file, checked_file, err_file):
    checked_set = set()
    with open(input_file, 'r', encoding='utf-8') as f, \
            jsonlines.open(checked_file, 'w') as c, \
            open(err_file, 'w', encoding='utf-8') as ef:
        for line in tqdm(f.readlines()):
            try:
                # 如有报错，证明json格式不正确，写入error文件
                json_data = json.loads(line.strip())
                if isinstance(json_data, str):
                    json_data = json.loads(json_data)
                # 如果json中没有id,则写入error文件
                id = json_data['id']
                # 如果id重复了，则跳过
                if id in checked_set:
                    continue
                # 记录每个id
                checked_set.add(id)
                # 写入文件
                if id_start <= id < id_end:
                    c.write(json_data)
                else:
                    ef.write("out range:" + line + "\n")
            except Exception as e:
                logging.error(f"Error occurred while parsing {input_file} at line: {line}. Exception: {e}")
                logging.error(traceback.format_exc())
                ef.write(line + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse jsonl files')
    parser.add_argument('input_path', type=str, help='input path to recurse')
    args = parser.parse_args()
    recursive_parse_jsonl_files(args.input_path)
    logging.info("Finished parsing all jsonl files in the input path")
