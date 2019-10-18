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


@pytest.fixture(scope='function')
def setup_repository():
    candidate_repository = CandidateRepository()
    yield (candidate_repository)
    del (candidate_repository)


class TestSave:

    @pytest.mark.parametrize('candidate', [Candidate(user)])
    def test_succeeds_when_candidate_has_no_id(self, candidate,
                                               setup_repository):
        candidate_repository = setup_repository
        candidate_repository.save(candidate)
        assert get_public_vars(
            candidate_repository.candidates[1]) == get_public_vars(candidate)

    @pytest.mark.parametrize('candidate', [Candidate(user, id=3)])
    def test_update_succeeds_when_candidate_has_id(self, candidate,
                                                   setup_repository):
        candidate_repository = setup_repository
        candidate_repository.save(candidate)
        candidate.name = 'updated_name'
        candidate_repository.save(candidate)
        assert get_public_vars(
            candidate_repository.candidates[3]) == get_public_vars(candidate)

    @pytest.mark.parametrize('candidate, event_item_id',
                             [(Candidate(user, id=1), 1)])
    def test_save_succeeds_when_given_event_item_id(self, candidate,
                                                    event_item_id,
                                                    setup_repository):
        candidate_repository = setup_repository
        candidate_repository.save(candidate, event_item_id)
        assert set(candidate_repository.
                   event_item_id_to_candidate_map[event_item_id]) == set(
                       [candidate])


class TestDelete:

    @pytest.mark.parametrize('candidate', [Candidate(user, id=1)])
    def test_succeeds_when_target_candidate_exists(self, candidate,
                                                   setup_repository):
        candidate_repository = setup_repository
        candidate_repository.candidates[1] = candidate
        candidate_repository.delete(candidate)

    @pytest.mark.parametrize('candidate', [Candidate(user, id=1)])
    def test_return_value_error_when_target_candidate_does_not_exist(
            self, candidate, setup_repository):
        candidate_repository = setup_repository
        with pytest.raises(ValueError):
            assert candidate_repository.delete(candidate)

    @pytest.mark.parametrize('candidate', [Candidate(user, id=1)])
    def test_return_value_error_when_given_candidate_id_is_none(
            self, candidate, setup_repository):
        candidate_repository = setup_repository
        candidate_repository.candidates[1] = candidate
        candidate.id = None
        with pytest.raises(ValueError):
            assert candidate_repository.delete(candidate)


class TestFindById:

    @pytest.mark.parametrize('candidate', [Candidate(user, id=1)])
    def test_return_candidate_when_target_id_exists(self, candidate,
                                                    setup_repository):
        candidate_repository = setup_repository
        candidate_repository.candidates[1] = candidate
        found_candidate = candidate_repository.find_by_id(1)
        assert get_public_vars(found_candidate) == get_public_vars(
            candidate_repository.candidates[1])

    def test_return_none_when_target_id_does_not_exist(self, setup_repository):
        candidate_repository = setup_repository
        found_candidate = candidate_repository.find_by_id(100)
        assert found_candidate is None


class TestFindByEventItemId:

    @pytest.mark.parametrize('candidate', [Candidate(user, id=1)])
    def test_return_candidates_when_candidate_with_target_event_item_id_exists(
            self, candidate, setup_repository):
        candidate_repository = setup_repository
        candidate_repository.candidates[1] = candidate

        found_candidate = candidate_repository.find_by_id(1)
        assert get_public_vars(found_candidate) == get_public_vars(
            candidate_repository.candidates[1])

    def test_return_none_when_candidates_with_target_event_item_id_does_not_exists(
            self, setup_repository):
        candidate_repository = setup_repository
        found_candidate = candidate_repository.find_by_id(100)
        assert found_candidate is None


class TestFindAll:

    def test_return_all_candidate(self, setup_repository):
        candidate_repository = setup_repository
        added_candidates = []
        for id in range(1, 5):
            candidate = Candidate(user, id)
            candidate_repository.candidates[id] = candidate
            added_candidates.append(candidate)
        found_candidates = candidate_repository.find_all()
        assert set(found_candidates) == set(added_candidates)
