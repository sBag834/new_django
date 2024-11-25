from django import template
import re

register = template.Library()

BAD_WORDS = ['редиска', 'безумное', 'госсуверенитета']

@register.filter
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Фильтр 'censor' может применяться только к строкам.")

    def replace_bad_word(match):
        word = match.group(0)
        return word[0] + '*' * (len(word) - 1)

    pattern = r'\b(' + '|'.join(BAD_WORDS) + r')\b'

    return re.sub(pattern, replace_bad_word, value, flags=re.IGNORECASE)