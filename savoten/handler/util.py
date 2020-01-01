import copy
import json
from datetime import datetime

from savoten.domain import Candidate, Event, EventItem, Period, User


# Domainの自作classをjsonエンコードする際の処理
# json.dumpsやjsonifyで使用
class DomainEncoder(json.JSONEncoder):
    _domain_class_tuple = (Event, EventItem, User, Candidate, Period)

    def default(self, obj):
        # Datetime型についてもjson化の際の定義が必要なのでその記述
        # PeriodクラスのメンバにDatetime型がいる
        if isinstance(obj, datetime):
            return obj.isoformat()
        # Domainで定義する自作classのjsonエンコード定義
        # 自作classのメンバにさらに自作classが入れ子になっていることがあるが
        # 子のclassについても再起的に呼ばれ、すべてjsonになって戻ってくる
        if isinstance(obj, self._domain_class_tuple):
            new_obj = copy.deepcopy(obj)
            return self._encode_obj_to_dict(new_obj)
        return super(DomainEncoder, self).default(obj)

    def _encode_obj_to_dict(self, obj):
        obj_dict = vars(obj)
        return self._strip_key_head_underbar(obj_dict)

    # 変数名の頭にアンダーバーがあれば一律で外す
    # private変数で定義されている変数の頭のアンダーバーを外す意図
    def _strip_key_head_underbar(self, obj_dict):
        for key in obj_dict:
            if key.startswith('_'):
                stripped_key = key.lstrip('_')
                obj_dict[stripped_key] = obj_dict.pop(key)
        return obj_dict
