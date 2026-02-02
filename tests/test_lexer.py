import pytest
from tests.utils import Tokenizer
from lexererr import ErrorToken, IllegalEscape, UncloseString

def test_lexer_0():
    source = 'struct S { int x; int y; };\nvoid main() {\n    for (int i = 0; i < 10; i = i + 1) {\n    for (int i = 0; i < 10; i = i + 1) {\n    while (i) {\n    i++;\n    int y;\n}\n    if (10) {\n    return y;\n    y--;\n    y = 2;\n    i--;\n}\n}\n}\n    while (0 - x) {\n    return 0;\n    int i;\n    while (z) {\n    return 0;\n}\n}\n    int y;\n    for (int z = 0; z < 10; z = z + 1) {\n    1 + 1;\n    0 - 10;\n}\n}'
    tokenizer = Tokenizer(source)
    print(tokenizer.get_tokens_as_string())
    with pytest.raises(ErrorToken):
        tokenizer.get_tokens_as_string()
