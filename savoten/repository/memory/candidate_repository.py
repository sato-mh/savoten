from savoten.domain import CandidateRepositoryInterface


class CandidateRepository(CandidateRepositoryInterface):

    def __init__(self):
        self.candidates = {}
        self.id = 0

        # 本来DBテーブルに記録するevent_item_idとcandidateの関係を、on_memoryの間だけ代替するdict
        # key: event_item_id, value: [candidate]で記載
        # on_memoryの間だけ使用する　DB仕様では不要
        self.event_item_id_to_candidate_map = {}

    def save(self, candidate, event_item_id=None):
        if candidate.id is None:
            candidate.id = self._get_new_id()
        self.candidates[candidate.id] = candidate

        # event_itemとの所属関係の処理
        # on_memoryからDB仕様にする時に書き換えが必要
        if event_item_id:
            if self.event_item_id_to_candidate_map.get(event_item_id, None):
                self.event_item_id_to_candidate_map[event_item_id].append(
                    candidate)
            else:
                self.event_item_id_to_candidate_map[event_item_id] = [candidate]

        return candidate

    def delete(self, candidate):
        if candidate.id is None or candidate.id not in self.candidates:
            raise ValueError("error!")

        self.candidates.pop(candidate.id)

        # event_itemとの所属関係の処理
        # on_memoryからDB仕様にする時に書き換えが必要
        for registed_candidates in self.event_item_id_to_candidate_map.values():
            for registed_candidate in registed_candidates:
                if candidate.id == registed_candidate.id:
                    registed_candidates.remove(registed_candidate)

    def find_by_id(self, id):
        return self.candidates.get(id, None)

    def find_by_event_item_id(self, event_item_id):
        return self.event_item_id_to_candidate_map.get(event_item_id, None)

    def find_all(self):
        return self.candidates.values()

    def _get_new_id(self):
        self.id = self.id + 1
        return self.id
