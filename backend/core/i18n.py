from django.conf import settings


def request_language(request):
    supported = {code for code, _label in settings.LANGUAGES}
    requested = request.query_params.get("language") if request else None
    if not requested and request:
        requested = request.headers.get("Accept-Language", "").split(",", 1)[0]
    language = (requested or settings.PARLER_DEFAULT_LANGUAGE_CODE).split("-", 1)[0].lower()
    return language if language in supported else settings.PARLER_DEFAULT_LANGUAGE_CODE


class LocalizedRepresentationMixin:
    localized_fields = {}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        language = request_language(self.context.get("request"))

        for field, relation_name in self.localized_fields.items():
            content = getattr(instance, relation_name, None)
            if content:
                data[field] = content.safe_translation_getter(
                    field,
                    language_code=language,
                    any_language=True,
                ) or data.get(field)
        return data
