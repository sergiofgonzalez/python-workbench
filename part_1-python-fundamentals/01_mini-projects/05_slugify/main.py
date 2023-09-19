from slugify import slugify, SLUG_OK


def get_slug(text):
    SLUG_OK = '-'

    return slugify(text, ok=SLUG_OK, only_ascii=True)


print(get_slug("78Bän...g (bang) -_~ Compañía"))
