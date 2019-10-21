import pytest

from savoten.domain import Candidate, User
from savoten.repository.memory import CandidateRepository
from tests.util import get_public_vars

user_args = {
    'name': 'test_user',
    'email': 'test_user@test.com',
    'permission': 100
}
user = User(**user_args)


class TestSave:

    def setup_method(self):
        self.repository = CandidateRepository()

    @pytest.mark.parametrize('candidate', [Candidate(user)])
    def test_succeeds_when_candidate_has_no_id(self, candidate):
        self.repository.save(candidate)
        assert get_public_vars(
            self.repository.candidates[1]) == get_public_vars(candidate)

    @pytest.mark.parametrize(
        'candidate, updated_candidate',
        [(Candidate(user), Candidate(user, id=1, description='updated'))])
    def test_update_succeeds_when_candidate_has_id(self, candidate,
                                                   updated_candidate):
        self.repository.save(candidate)
        self.repository.save(updated_candidate)
        assert get_public_vars(
            self.repository.candidates[1]) == get_public_vars(updated_candidate)

    @pytest.mark.parametrize('candidate, event_item_id',
                             [(Candidate(user, id=1), 1)])
    def test_save_succeeds_when_given_event_item_id(self, candidate,
                                                    event_item_id):
        self.repository.save(candidate, event_item_id)
        assert set(self.repository.event_item_id_to_candidate_map[event_item_id]
                  ) == set([candidate])


class TestDelete:

    @classmethod
    def setup_class(cls):
        cls.repository = CandidateRepository()
        cls.repository.candidates[1] = Candidate(user, id=1)

    @pytest.mark.parametrize('candidate', [Candidate(user, id=1)])
    def test_succeeds_when_target_candidate_exists(self, candidate):
        self.repository.delete(candidate)

    @pytest.mark.parametrize('candidate', [Candidate(user, id=100)])
    def test_return_value_error_when_target_candidate_does_not_exist(
            self, candidate):
        with pytest.raises(ValueError):
            assert self.repository.delete(candidate)

    @pytest.mark.parametrize('candidate', [Candidate(user, id=None)])
    def test_return_value_error_when_given_candidate_id_is_none(
            self, candidate):
        with pytest.raises(ValueError):
            assert self.repository.delete(candidate)


class TestFindById:

    @classmethod
    def setup_class(cls):
        cls.repository = CandidateRepository()
        cls.repository.candidates[1] = Candidate(user, id=1)

    def test_return_candidate_when_target_id_exists(self):
        assert get_public_vars(
            self.repository.find_by_id(1)) == get_public_vars(
                self.repository.candidates[1])

    def test_return_none_when_target_id_does_not_exist(self):
        assert self.repository.find_by_id(100) is None


class TestFindByEventItemId:

    @classmethod
    def setup_class(cls):
        cls.repository = CandidateRepository()
        cls.test_candidates = [Candidate(user, id=i) for i in range(1, 5)]
        event_item_id = 1
        cls.repository.event_item_id_to_candidate_map[
            event_item_id] = cls.test_candidates

    def test_return_candidates_when_target_event_ids_candidate_exists(self):
        set(self.repository.find_by_event_item_id(1)) == set(
            self.test_candidates)

    def test_return_none_when_target_event_item_ids_candidates_does_not_exists(
            self):
        assert self.repository.find_by_id(100) is None


class TestFindAll:

    @classmethod
    def setup_class(cls):
        cls.repository = CandidateRepository()
        cls.test_candidates = [Candidate(user, id=i) for i in range(1, 5)]
        for candidate in cls.test_candidates:
            cls.repository.candidates[candidate.id] = candidate

    def test_return_all_candidate(self):
        assert set(self.repository.find_all()) == set(self.test_candidates)
