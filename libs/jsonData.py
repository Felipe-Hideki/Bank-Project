import json
from collections.abc import Sequence

class _data(Sequence):
    def __getitem__(self, data: str) -> str:
        return self._data[data]
    
    def __len__(self):
        return len(self._data)

    def as_dict(self) -> dict:
        return dict(self._data)

    def __init__(self, dictionary: dict = None):
        if dictionary is not None:
            self._data = dict(dictionary)

class _json:
    def get_json(self) -> str:
        return self._json_data
    
    def __init__(self):
        super().__init__()
        self._json_data = None

    def extract(self) -> dict[str]:
        return json.loads(self._json_data)

class login_data(_data):
    def __init__(self, login: str = None, psk: str = None, id = None, dictionary: dict = None) -> None:
        self._data = {"login":login, "psk":psk, "id":id}
        super().__init__(dictionary)
        
class client_data(_data):
    def __init__(self, name: str = None, money: float = None ,dictionary: dict = None) -> None:
        self._data = {"name":name, "money":money}
        super().__init__(dictionary)
    
class client_json(_json):
    def __init__(self, data: client_data):
        super().__init__()
        self._json_data = json.dumps(data.as_dict())

class login_json(_json):
    def __init__(self, data: login_data):
        super().__init__()
        self._json_data = json.dumps(data.as_dict())