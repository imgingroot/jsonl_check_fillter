import json
import os
import logging
import argparse
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterator, *args, **kwargs):
        return iterator

logging.basicConfig(filename='json_check.log', level=logging.INFO)


def recursive_parse_jsonl_files(input_path):
    # 遍历目录及子目录查找 jsonl 文件
    for root, dirs, files in os.walk(input_path):
        for file_name in files:
            if file_name.endswith('.jsonl'):
                input_file = os.path.join(root, file_name)
                checked_file = os.path.join(root, f"{file_name}.checked")
                err_file = os.path.join(root, f"{file_name}.err")
                try:
                    logging.info(f"Parsing jsonl files: {input_file}")
                    parse_jsonl_file(input_file, checked_file, err_file)
                except Exception as e:
                    logging.exception(f"Error occurred while processing the file: {input_file}. Exception: {e}")


def parse_jsonl_file(input_file, checked_file, err_file):
    checked_set = set()
    with open(input_file, 'r') as f, open(checked_file, 'w') as c, open(err_file, 'w') as ef:
        for line in tqdm(f):
            try:
                line = line.strip()
                line_hash = hash(line)
                if line_hash in checked_set:
                    continue
                json.loads(line)
                c.write(line + "\n")
                checked_set.add(line_hash)
            except Exception as e:
                logging.error(f"Error occurred while parsing {input_file} at line: {line}. Exception: {e}")
                ef.write(line + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse jsonl files')
    parser.add_argument('input_path', type=str, help='input path to recurse')
    args = parser.parse_args()

    recursive_parse_jsonl_files(args.input_path)
    logging.info("Finished parsing all jsonl files in the input path")
