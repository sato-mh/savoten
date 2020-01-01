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
            return vars(obj)
        return super(DomainEncoder, self).default(obj)
