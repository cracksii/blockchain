import json
import hashing


class Base:
    def get_dict(self):
        raise NotImplementedError()

    def get_json(self, *args, **kwargs):
        return json.dumps(self.get_dict(), *args, **kwargs)

    def get_hash(self):
        return hashing.hash(self.get_json())
