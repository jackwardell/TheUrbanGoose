import os

os.environ["GOOSE_ENV"] = GOOSE_ENV = "production"
os.environ["USERNAME"] = USERNAME = "hello"
os.environ["PASSWORD"] = PASSWORD = "world"


def _get_csrf_from_form(html):
    input_tag = html.split('<div class="form-group">')[1].split(
        "</div>", maxsplit=1
    )[0]
    value = input_tag[input_tag.find("value=") :]
    token = value.split('"')[1]
    # check its a long string
    assert len(token) > 80
    return token
