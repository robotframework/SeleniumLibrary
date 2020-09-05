from SeleniumLibrary.utils import is_noney

TRUTHY = ["foo", " ", 1, 2.3, True, [1], "True", {"k": "v"}]


def test_is_noney():
    for item in [None, "None", "NONE", "none"]:
        assert is_noney(item)
    for item in TRUTHY + [False, 0, "False", "", [], {}, ()]:
        assert is_noney(item) is False
