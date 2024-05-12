from pathlib import Path


def path_log_file(file_name):
    return str(Path(__file__).parent.parent.joinpath(f'logs/{file_name}'))


def path_json_scheme(file_name):
    return str(Path(__file__).parent.parent.joinpath(f'scheme/{file_name}'))


def relative_from_root(path: str):
    from pathlib import Path
    return Path(__file__).parent.parent.joinpath(path).absolute().__str__()