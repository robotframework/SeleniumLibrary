import shutil
import subprocess
import sys
from pathlib import Path
from typing import List

STUB_FILES = Path('./stub_files')
SRC = Path('src/SeleniumLibrary/')
STUB_INIT_FILE = '__init__.pyi'


def get_sl_keywords():
    sys.path.insert(0, str(SRC.parent))
    try:
        from SeleniumLibrary import SeleniumLibrary
        sl = SeleniumLibrary()
        return sl.keywords
    except Exception as error:
        raise error
    finally:
        sys.path.pop(0)


def generate_init_stub():
    Path(SRC / STUB_INIT_FILE).unlink(missing_ok=True)
    shutil.rmtree(STUB_FILES, ignore_errors=True)
    rc = subprocess.run(['stubgen', '-o', STUB_FILES, SRC])
    if rc.returncode != 0:
        print(rc.stdout)
        print('Generation of stubb files failed.')
        sys.exit(rc.returncode)


def copy_init_sub() -> Path :
    init = STUB_FILES / 'SeleniumLibrary' / STUB_INIT_FILE
    Path(SRC / STUB_INIT_FILE).unlink(missing_ok=True)
    init_stub_path = Path(SRC / STUB_INIT_FILE)
    init.rename(init_stub_path)
    return init_stub_path


def read_kw_stub_files() -> List[str]:
    lines = []
    for file in Path(STUB_FILES / 'SeleniumLibrary' / 'keywords').glob('*.pyi'):
        lines.extend(file.read_text().splitlines())
    return lines


def append_keywords_to_stub(init_stub: Path, stub_lines: List[str], sl_keywords: List[str]):
    kw_sub_lines = []
    for kw in sl_keywords:
        if ' ' in kw:
            kw = kw.lower().replace(' ', '_')
        if kw == 'page_should_contain_checkbox':
            print(kw)
        kw_sub_lines.append(find_kw_stub_lines(kw, stub_lines))
    kw_sub_lines.sort()
    with init_stub.open('a') as init_file:
        init_file.write('\n'.join(kw_sub_lines))
        init_file.write('\n')


def find_kw_stub_lines(kw: str, stub_lines: List[str]):
    for line in stub_lines:
        if f'def {kw}(self' in line:
            if 'page_should_contain_checkbox' == kw:
                print(line)
            return line


if __name__ == '__main__':
    sl_keywords = get_sl_keywords()
    generate_init_stub()
    init_stub = copy_init_sub()
    stub_lines = read_kw_stub_files()
    append_keywords_to_stub(init_stub, stub_lines, sl_keywords)
