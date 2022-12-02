import yaml


class YamlUtil:

    def __init__(self, file_path):
        self._yaml_path = file_path

    @property
    def read(self):
        with open(self._yaml_path, encoding='utf-8') as f:
            return yaml.safe_load(f)

    def write_a(self, write_data):
        with open(self._yaml_path, 'a', encoding='utf-8') as f:
            yaml.safe_dump(write_data, f, allow_unicode=True)

    def write_w(self, write_data):
        with open(self._yaml_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(write_data, f, allow_unicode=True)
