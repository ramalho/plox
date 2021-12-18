import sys
import readline  # enable readline for input()

import parser

def main(args: list[str]) -> None:
    if len(args) == 0:
        run_prompt()
    elif len(args) == 1:
        run_file(args[0])
    else:
        print('Usage: lox.py [script]')
        sys.exit(64)


def run_file(path: str) -> None:
    with open(path) as fp:
        source = fp.read()
    _run(source)
    if had_error:
        sys.exit(65)


def run_prompt() -> None:
    while True:
        try:
            line = input('> ')
        except EOFError:
            break
        _run(line)
        had_error = False

 
def _run(source: str):
    scanner = parser.Scanner(source)
    for token in scanner.scan_tokens():
        print(token)


def error(line: int, message: str):
    _report(line, '', message)


def _report(line: int, where: str, message: str):
    print(f'[line {line}] Error {where}: {message}')
    had_error = True


if __name__ == '__main__':
    had_error = False
    main(sys.argv[1:])
