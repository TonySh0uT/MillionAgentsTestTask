
class EmailMasker:
    def __init__(self, email: str, mask: str = 'x'):
        self.email = email
        self.mask = mask

    def do_masking(self):
        username, domain = self.email.split('@', 1)
        masked_email = f'{self.mask * len(username)}@{domain}'
        return masked_email


class PhoneMasker:
    def __init__(self, phone_number: str, mask: str = 'x', num_masking_numbers: int = 3):
        self.phone_number = phone_number
        self.mask = mask
        self.num_masking_numbers = num_masking_numbers

    def do_masking(self):
        chars = list(self.phone_number.strip())
        chars.reverse()
        masked_nums = 0
        result = list()
        for char in chars:
            if masked_nums == self.num_masking_numbers or char.isspace():
                result.append(char)
            else:
                result.append(self.mask)
                masked_nums += 1
        result.reverse()
        return ' '.join(''.join(result).split())


class SkypeMasker:
    def __init__(self, skype_string: str, mask: str = 'x'):
        self.skype_string = skype_string
        self.mask = mask

    def do_mask(self):
        # Простой вариант вида skype:alex.max
        if self.skype_string.startswith("skype:"):
            return "skype:" + self.mask * 3

        # Вариант со ссылкой вида href=\"skype:alex.max?call\">skype</a>"
        if self.skype_string.startswith('<a href="skype:') and self.skype_string.endswith('">skype</a>'):
            start = len('<a href="skype:')
            end = self.skype_string.index('?call">skype</a>')
            masked_username = self.mask * 3
            return f'{self.skype_string[:start]}{masked_username}{self.skype_string[end:]}'
        return self.skype_string