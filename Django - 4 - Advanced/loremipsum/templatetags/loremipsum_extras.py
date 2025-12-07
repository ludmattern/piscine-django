from django import template

register = template.Library()


@register.filter
def switch_lang_code(path, language):
    """
    Replaces the language prefix in the path with the given language code.
    Also attempts to replace the language prefix in the 'next' query parameter if present.
    """
    if language == "fr":
        # Switching to French: replace /en/ with /fr/
        return path.replace("/en/", "/fr/")
    elif language == "en":
        # Switching to English: replace /fr/ with /en/
        return path.replace("/fr/", "/en/")
    return path
