from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionconfig:
    root_dir: Path
    source_url: str
    local_data_file: Path
    unzip_directory: Path

@dataclass(frozen=True)
class Datavalidationconfig:
    root_dir: Path
    status_file: str
    all_required_files: list


@dataclass(frozen=True)
class Datatransformationconfig:
    root_dir: Path
    data_path: Path
    data_path_test: Path
    tokenizer_name: Path