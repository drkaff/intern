import autocomplete_light
from pygments.lexers import get_all_lexers
from pygments.lexers import get_lexer_by_name


class OsAutocomplete(autocomplete_light.AutocompleteListBase):
    LEXERS = [item for item in get_all_lexers() if item[1]]
    LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
    choices = []
    for item in LANGUAGE_CHOICES:
        choices.append(item[0])

autocomplete_light.register(OsAutocomplete)
