from savoten import domain


def test_init_event_with_correct_args():
    args = {
        'name': 'user_name',
        'email': 'user_email@example.com',
        'permission': 100
    }
    domain.User(**args)
