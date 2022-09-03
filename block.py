import json
from pathlib import Path
import hashlib

BLOCKS_DIR = Path('./blocks/')


def get_hash(filename: str):
    with open(Path(BLOCKS_DIR, filename), 'rb') as file:
        content = file.read()
    return hashlib.md5(content).hexdigest()


def get_list_files() -> list:
    return sorted(int(filepath.name) for filepath in list(BLOCKS_DIR.iterdir()))


def create_first_block():
    first_data = {
        'from': 'Sasha_K1990',
        'to': 'AlexQwerty',
        'amount': 250,
        'hash': None
    }
    with open(Path(BLOCKS_DIR, '0'), 'w') as file:
        json.dump(first_data, file, indent=4)


def find_last_block() -> str:
    list_files = get_list_files()
    try:
        block_name = list_files[-1]
    except IndexError:
        block_name = '0'
        create_first_block()
    return str(block_name)


def write_block(_from: str, to: str, amount: str, prev_hash=''):
    last_file = find_last_block()
    prev_hash = get_hash(last_file)
    data = {
        'from': _from,
        'to': to,
        'amount': int(amount),
        'hash': prev_hash
    }

    block_name = str(int(find_last_block()) + 1)
    with open(Path(BLOCKS_DIR, block_name), 'w') as file:
        json.dump(data, file, indent=4)


def check_integrity() -> list:
    files = get_list_files()
    result = []
    for file in files[1:]:
        content = open(Path(BLOCKS_DIR, str(file)))
        hash = json.load(content)['hash']
        prev_file = str(file - 1)
        actual_hash = get_hash(prev_file)
        if hash == actual_hash:
            res = 'ok'
        else:
            res = 'corrupted'
        result.append({'block': prev_file, 'result': res})

    return result


def main():
    print(check_integrity())
    # write_block()


if __name__ == '__main__':
    main()
