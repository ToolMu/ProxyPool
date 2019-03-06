import json
import yaml
from copy import deepcopy
from collections import MutableMapping


class Config:

    @staticmethod
    def from_json(file_name):
        """从json文件中读取配置"""
        with open(file_name, 'r', encoding="utf8") as f:
            read_data = json.loads(f.read())

        return ReadDict(read_data)

    @staticmethod
    def from_yaml(file_name):
        """从yaml文件中读取配置"""
        with open(file_name, 'r', encoding="utf8") as f:
            read_data = yaml.load(f.read())

        return ReadDict(read_data)

    @staticmethod
    def from_dict(obj):
        return ReadDict(obj)
    
    @staticmethod
    def from_center(url, which):
        """设想的远程获取配置文件  胖客户机，瘦服务器？"""
        pass


class ReadDict:
    def __init__(self, content):
        if isinstance(content, dict):
            self._content = deepcopy(content)
        else:
            raise ValueError("Content Type Error! Content Must Dict!")
    
    def __getitem__(self, opt_name):
        """提供解析 a.b.c 键的能力 -> Obj['a.b.c']"""
        result = self._content

        for opt in opt_name.split('.'):
            result = result[opt]
        
        return result


if __name__ == "__main__":
    # config = Config.from_yaml("config.yaml")
    # print(config['name'])
    # print(config['side.url'])
    # config = Config.from_json("config.json")
    # print(config['name.na'])
    data = {"na": {"me": "OK"}}
    config = Config.from_dict(data)
    print(config["na.me"])
