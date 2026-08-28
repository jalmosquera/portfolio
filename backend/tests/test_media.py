from django.urls import resolve
from django.test import RequestFactory
from django.views.static import serve


def test_media_files_are_routed_before_the_admin_catch_all():
    match = resolve('/media/projects/example.svg')

    assert match.func.__name__ == 'serve'


def test_webp_media_uses_image_content_type(tmp_path):
    (tmp_path / 'example.webp').write_bytes(b'webp')

    response = serve(RequestFactory().get('/media/example.webp'), 'example.webp', document_root=tmp_path)

    assert response['Content-Type'] == 'image/webp'
