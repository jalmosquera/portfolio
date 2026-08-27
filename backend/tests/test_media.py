from django.urls import resolve


def test_media_files_are_routed_before_the_admin_catch_all():
    match = resolve('/media/projects/example.svg')

    assert match.func.__name__ == 'serve'
