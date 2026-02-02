import pytest
from tests.utils import Parser

def test_parser_0():
    source = 'struct S { int x; int y; };\nvoid main() {\n    if (i) {\n    x = x + y;\n    return x;\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_1():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_2():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_3():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_4():
    source = 'struct S { int x; int y; };\nvoid main() {\n    while (z - 1) {\n    i = 1;\n}\n    while (x / y) {\n    z = i + x;\n    return y - y;\n    for (int z = 0; z < 10; z = z + 1) {\n    while (z) {\n    y - i;\n    i = 0 - 1;\n    int y;\n}\n    int z;\n    for (int z = 0; z < 10; z = z + 1) {\n    z = 10;\n}\n    for (int i = 0; i < 10; i = i + 1) {\n    0;\n    return 1 - z;\n}\n}\n    switch (z) {\n    case 0:\n        break;\n    default:\n        break;\n}\n}\n    x--;\n    for (int i = 0; i < 10; i = i + 1) {\n    int x;\n    if (y * 2) {\n    switch (z) {\n    case 2:\n        break;\n    default:\n        break;\n}\n    z = z;\n}\n    while (x) {\n    switch (1) {\n    case 0:\n        break;\n    default:\n        break;\n}\n    if (i) {\n    x = 10;\n}\n    y = 10;\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_5():
    source = 'void main() {\n    return 0;\n    for (int z = 0; z < 10; z = z + 1) {\n    switch (y) {\n    case 1:\n        break;\n    default:\n        break;\n}\n    while (i) {\n    int x;\n    int y;\n}\n    x = y - 0;\n    switch (i / 2) {\n    case 1:\n        break;\n    default:\n        break;\n}\n}\n    return y;\n    for (int z = 0; z < 10; z = z + 1) {\n    for (int i = 0; i < 10; i = i + 1) {\n    x = 1 + i;\n}\n    return 10;\n    y--;\n    switch (y + x) {\n    case 0:\n        break;\n    default:\n        break;\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_6():
    source = 'struct S { int x; int y; };\nvoid main() {\n    for (int i = 0; i < 10; i = i + 1) {\n    return x - 2;\n    int i;\n    if (0 / 10) {\n    return i + x;\n    while (x) {\n    return x;\n}\n}\n    y = y;\n}\n    return y - x;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_7():
    source = 'void main() {\n    if (1) {\n    if (z * 10) {\n    x = y + i;\n    if (z) {\n    int y;\n    y--;\n    y - 0;\n}\n    x = 0;\n}\n    if (1) {\n    if (10) {\n    int x;\n    return x + 1;\n    z = 10;\n}\n    for (int x = 0; x < 10; x = x + 1) {\n    int y;\n}\n}\n}\n    int z;\n    y++;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_8():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_9():
    source = 'void main() {\n    return 1;\n    for (int y = 0; y < 10; y = y + 1) {\n    x - 1;\n    for (int y = 0; y < 10; y = y + 1) {\n    x / i;\n    return 1 * i;\n    return i;\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_10():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_11():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_12():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_13():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_14():
    source = 'struct S { int x; int y; };\nvoid main() {\n    x++;\n    for (int z = 0; z < 10; z = z + 1) {\n    for (int x = 0; x < 10; x = x + 1) {\n    return x / x;\n    return 2 + 1;\n    while (y) {\n    z--;\n    2;\n    return 0;\n}\n    for (int x = 0; x < 10; x = x + 1) {\n    1 / 10;\n    return 10;\n    x = 1 + i;\n}\n}\n    if (i) {\n    int x;\n    return y / 2;\n}\n    return 10 / i;\n}\n    2;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_15():
    source = 'struct S { int x; int y; };\nvoid main() {\n    int y;\n    i = 10;\n    while (2 / z) {\n    switch (i * 10) {\n    case 1:\n        break;\n    case 2:\n        break;\n    default:\n        break;\n}\n    z = 0;\n    while (y - z) {\n    for (int y = 0; y < 10; y = y + 1) {\n    int i;\n    return 10 / x;\n}\n    return 2 + 2;\n}\n    switch (2 / i) {\n    case 2:\n        break;\n    default:\n        break;\n}\n}\n    switch (10 + 2) {\n    case 2:\n        break;\n    default:\n        break;\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_16():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_17():
    source = 'void main() {\n    int i;\n    int x;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_18():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_19():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_20():
    source = 'void main() {\n    while (10) {\n    while (0 / 0) {\n    switch (1) {\n    case 0:\n        break;\n    default:\n        break;\n}\n}\n    return x;\n    int y;\n}\n    return z;\n    return 10;\n    y = 0 * z;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_21():
    source = 'struct S { int x; int y; };\nvoid main() {\n    x = 2 / i;\n    y = 0;\n    x = 2 * y;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_22():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_23():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_24():
    source = 'void main() {\n    switch (0) {\n    case 10:\n        break;\n    default:\n        break;\n}\n    switch (i + 0) {\n    case 10:\n        break;\n    case 2:\n        break;\n    default:\n        break;\n}\n    switch (1 + 10) {\n    case 10:\n        break;\n    default:\n        break;\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_25():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_26():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_27():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_28():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_29():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_30():
    source = 'struct S { int x; int y; };\nvoid main() {\n    for (int i = 0; i < 10; i = i + 1) {\n    switch (0) {\n    case 10:\n        break;\n    case 0:\n        break;\n    default:\n        break;\n}\n    return i * 1;\n}\n    switch (10 * 0) {\n    case 10:\n        break;\n    case 2:\n        break;\n    default:\n        break;\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_31():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_32():
    source = 'struct S { int x; int y; };\nvoid main() {\n    y = i;\n    switch (0) {\n    case 2:\n        break;\n    case 0:\n        break;\n    default:\n        break;\n}\n    return z * x;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_33():
    source = 'void main() {\n    int z;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_34():
    source = 'void main() {\n    int z;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_35():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_36():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_37():
    source = 'struct S { int x; int y; };\nvoid main() {\n    switch (10 + x) {\n    case 0:\n        break;\n    default:\n        break;\n}\n    y - y;\n    for (int y = 0; y < 10; y = y + 1) {\n    switch (x + i) {\n    case 2:\n        break;\n    case 10:\n        break;\n    default:\n        break;\n}\n    return y - i;\n    x;\n    for (int i = 0; i < 10; i = i + 1) {\n    if (x) {\n    i++;\n    z = 2;\n}\n    y = 0;\n    z;\n    if (0) {\n    int i;\n    z--;\n    return x;\n    return 0 + y;\n}\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_38():
    source = 'struct S { int x; int y; };\nvoid main() {\n    int y;\n    switch (10 + 10) {\n    case 2:\n        break;\n    case 1:\n        break;\n    default:\n        break;\n}\n    while (1 * y) {\n    while (10 * 2) {\n    switch (0) {\n    case 2:\n        break;\n    default:\n        break;\n}\n}\n    while (2) {\n    switch (1) {\n    case 0:\n        break;\n    case 1:\n        break;\n    default:\n        break;\n}\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_39():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_40():
    source = 'struct S { int x; int y; };\nvoid main() {\n    i--;\n    x = z;\n    if (2) {\n    return 10;\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_41():
    source = 'struct S { int x; int y; };\nvoid main() {\n    if (2 / 10) {\n    switch (z) {\n    case 10:\n        break;\n    default:\n        break;\n}\n    z = 1 * x;\n}\n    if (10 - 10) {\n    while (2 / 1) {\n    return i / x;\n    while (10) {\n    return 10;\n    int y;\n    y / x;\n    i = y;\n}\n}\n    switch (1) {\n    case 2:\n        break;\n    case 10:\n        break;\n    default:\n        break;\n}\n    for (int z = 0; z < 10; z = z + 1) {\n    int x;\n    return i + 2;\n    x = z * x;\n    int z;\n}\n    int z;\n}\n    while (2 - i) {\n    y;\n    for (int y = 0; y < 10; y = y + 1) {\n    0 / 0;\n    int i;\n    if (z) {\n    return 0 / 0;\n}\n    switch (10) {\n    case 1:\n        break;\n    case 10:\n        break;\n    default:\n        break;\n}\n}\n    y = 1 * 0;\n    int i;\n}\n    if (x) {\n    if (1) {\n    return z + x;\n    if (10) {\n    0;\n}\n}\n    while (z - z) {\n    if (z) {\n    return 1 + 10;\n    int y;\n    i = y / x;\n}\n    if (y) {\n    i--;\n    int y;\n    return 1;\n    x = 0 / y;\n}\n    0;\n}\n    switch (z) {\n    case 0:\n        break;\n    default:\n        break;\n}\n    for (int i = 0; i < 10; i = i + 1) {\n    for (int y = 0; y < 10; y = y + 1) {\n    int i;\n    return x * i;\n    return i * y;\n    x--;\n}\n    if (i) {\n    return i;\n}\n    int x;\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_42():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_43():
    source = 'struct S { int x; int y; };\nvoid main() {\n    return i;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_44():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_45():
    source = 'void main() {\n    y++;\n    int y;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_46():
    source = 'void main() {\n    while (z) {\n    int y;\n    for (int x = 0; x < 10; x = x + 1) {\n    switch (10) {\n    case 2:\n        break;\n    case 0:\n        break;\n    default:\n        break;\n}\n}\n    return 0;\n}\n    switch (2 / y) {\n    case 0:\n        break;\n    default:\n        break;\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_47():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_48():
    source = 'struct S { int x; int y; };\nvoid main() {\n    0;\n    while (0 / 2) {\n    y = 10 - 2;\n}\n    while (2 / y) {\n    for (int z = 0; z < 10; z = z + 1) {\n    while (z) {\n    int x;\n    int x;\n    return 1;\n    x = y / 1;\n}\n    for (int x = 0; x < 10; x = x + 1) {\n    x++;\n    i = y;\n    x--;\n}\n    return x * x;\n}\n    z--;\n    while (z) {\n    for (int x = 0; x < 10; x = x + 1) {\n    int x;\n    i = 10 * z;\n}\n    while (0) {\n    int x;\n    y = y;\n    i--;\n}\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_49():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_50():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_51():
    source = 'void main() {\n    z = 0 + i;\n    for (int x = 0; x < 10; x = x + 1) {\n    return i - 0;\n}\n    if (y + 10) {\n    i * y;\n    for (int x = 0; x < 10; x = x + 1) {\n    int i;\n    z = 2 / 0;\n    i = 1;\n    z++;\n}\n    for (int x = 0; x < 10; x = x + 1) {\n    for (int i = 0; i < 10; i = i + 1) {\n    return 1 - 1;\n}\n    i;\n}\n    while (z - y) {\n    if (i) {\n    x = 10;\n    return 1 * z;\n}\n    switch (10) {\n    case 10:\n        break;\n    default:\n        break;\n}\n}\n}\n    if (x * y) {\n    switch (0 + y) {\n    case 0:\n        break;\n    case 0:\n        break;\n    default:\n        break;\n}\n    for (int i = 0; i < 10; i = i + 1) {\n    switch (10) {\n    case 2:\n        break;\n    default:\n        break;\n}\n}\n    y * y;\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_52():
    source = 'struct S { int x; int y; };\nvoid main() {\n    switch (0 / 2) {\n    case 1:\n        break;\n    case 2:\n        break;\n    default:\n        break;\n}\n    while (1) {\n    while (2) {\n    if (z) {\n    int y;\n    i++;\n    int z;\n}\n    for (int z = 0; z < 10; z = z + 1) {\n    int i;\n    0 - i;\n}\n    while (10) {\n    y = y;\n    1;\n}\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_53():
    source = 'void main() {\n    10;\n    int i;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_54():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_55():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_56():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_57():
    source = 'void main() {\n    return 10 / 0;\n    for (int i = 0; i < 10; i = i + 1) {\n    return 0;\n    int i;\n}\n    while (y) {\n    y = 10 - 2;\n    y = 1 + 2;\n    int i;\n}\n    while (2) {\n    while (x) {\n    z = z;\n    int z;\n    switch (10) {\n    case 10:\n        break;\n    default:\n        break;\n}\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_58():
    source = 'struct S { int x; int y; };\nvoid main() {\n    if (z) {\n    z = 0;\n    x = 2;\n    switch (x - z) {\n    case 0:\n        break;\n    default:\n        break;\n}\n    if (x * i) {\n    y + 2;\n    switch (1) {\n    case 10:\n        break;\n    default:\n        break;\n}\n    if (x) {\n    int z;\n    x = z + 1;\n    10 - z;\n}\n    i = 0;\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_59():
    source = 'struct S { int x; int y; };\nvoid main() {\n    int z;\n    if (10 * x) {\n    if (x * 0) {\n    while (2) {\n    return 1 - 10;\n    return 0 + 2;\n    int i;\n    z = y + 1;\n}\n}\n    if (10 / z) {\n    while (10) {\n    z++;\n}\n    i = z + z;\n    switch (y) {\n    case 1:\n        break;\n    default:\n        break;\n}\n    return 1 / x;\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_60():
    source = 'void main() {\n    while (y - 1) {\n    while (i + x) {\n    switch (0) {\n    case 0:\n        break;\n    case 2:\n        break;\n    default:\n        break;\n}\n    switch (10) {\n    case 2:\n        break;\n    default:\n        break;\n}\n}\n    return z;\n    i = 10;\n    z = y * 0;\n}\n    i + i;\n    x * 1;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_61():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_62():
    source = 'struct S { int x; int y; };\nvoid main() {\n    for (int i = 0; i < 10; i = i + 1) {\n    for (int x = 0; x < 10; x = x + 1) {\n    while (y) {\n    return z - z;\n    return y;\n    z = z;\n    0 + 0;\n}\n    return z * y;\n}\n    1;\n    int x;\n    x = i / x;\n}\n    switch (2) {\n    case 2:\n        break;\n    case 10:\n        break;\n    default:\n        break;\n}\n    if (y + z) {\n    for (int i = 0; i < 10; i = i + 1) {\n    return z * 1;\n    while (2) {\n    i / y;\n    y++;\n}\n    x = 2 / i;\n    z++;\n}\n    i--;\n    if (x + 2) {\n    return 1;\n    int x;\n    if (10) {\n    2;\n    z = 2 * x;\n    return i;\n    x--;\n}\n    switch (y) {\n    case 0:\n        break;\n    case 1:\n        break;\n    default:\n        break;\n}\n}\n    for (int z = 0; z < 10; z = z + 1) {\n    while (z) {\n    return x;\n    int y;\n}\n    while (10) {\n    y = 1 - 2;\n    i--;\n    return 1;\n    0 + 10;\n}\n    if (i) {\n    return 2;\n}\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_63():
    source = 'struct S { int x; int y; };\nvoid main() {\n    y = 10;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_64():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_65():
    source = 'void main() {\n    for (int i = 0; i < 10; i = i + 1) {\n    10 / 1;\n}\n    z--;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_66():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_67():
    source = 'struct S { int x; int y; };\nvoid main() {\n    if (0) {\n    return 1 / 1;\n    if (y / 2) {\n    x--;\n    z = 0 / i;\n    return 0 - y;\n}\n    return x;\n}\n    return x;\n    i = 10 + z;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_68():
    source = 'struct S { int x; int y; };\nvoid main() {\n    switch (0 + y) {\n    case 1:\n        break;\n    case 2:\n        break;\n    default:\n        break;\n}\n    return z;\n    for (int y = 0; y < 10; y = y + 1) {\n    for (int i = 0; i < 10; i = i + 1) {\n    if (x) {\n    0 / 10;\n}\n    z++;\n}\n}\n    z = 10;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_69():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_70():
    source = 'void main() {\n    return 2;\n    for (int z = 0; z < 10; z = z + 1) {\n    for (int x = 0; x < 10; x = x + 1) {\n    z++;\n    int z;\n}\n}\n    for (int y = 0; y < 10; y = y + 1) {\n    if (0 + 0) {\n    return y;\n    switch (0) {\n    case 1:\n        break;\n    case 10:\n        break;\n    default:\n        break;\n}\n    z = i - z;\n}\n    switch (2 / i) {\n    case 10:\n        break;\n    default:\n        break;\n}\n    return 10;\n    while (y) {\n    return z;\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_71():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_72():
    source = 'struct S { int x; int y; };\nvoid main() {\n    i = 10;\n    i++;\n    switch (x - y) {\n    case 0:\n        break;\n    case 10:\n        break;\n    default:\n        break;\n}\n    int i;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_73():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_74():
    source = 'struct S { int x; int y; };\nvoid main() {\n    int z;\n    for (int y = 0; y < 10; y = y + 1) {\n    for (int z = 0; z < 10; z = z + 1) {\n    switch (z) {\n    case 10:\n        break;\n    case 0:\n        break;\n    default:\n        break;\n}\n    while (y) {\n    return i;\n    int x;\n}\n    if (10) {\n    return i;\n    return z * i;\n    int x;\n    return i;\n}\n    return y;\n}\n    int i;\n}\n    int y;\n    int i;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_75():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_76():
    source = 'struct S { int x; int y; };\nvoid main() {\n    if (1) {\n    return z - 2;\n    if (x - 2) {\n    int z;\n    for (int z = 0; z < 10; z = z + 1) {\n    return 0;\n    return 10;\n    y = z / x;\n    return z / i;\n}\n    if (i) {\n    int i;\n    x;\n    x++;\n}\n    return 10;\n}\n    return 0 + i;\n}\n    return 10;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_77():
    source = 'struct S { int x; int y; };\nvoid main() {\n    return 0 / 10;\n    while (0 * 10) {\n    i = i * 1;\n    for (int x = 0; x < 10; x = x + 1) {\n    2 * z;\n    return i / i;\n}\n    switch (10 - 1) {\n    case 2:\n        break;\n    case 10:\n        break;\n    default:\n        break;\n}\n    z + x;\n}\n    x = 2;\n    z;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_78():
    source = 'struct S { int x; int y; };\nvoid main() {\n    while (10) {\n    int x;\n    for (int x = 0; x < 10; x = x + 1) {\n    if (0) {\n    return y;\n}\n}\n    y = i;\n    if (0 / y) {\n    for (int i = 0; i < 10; i = i + 1) {\n    z = x;\n    int i;\n}\n    for (int i = 0; i < 10; i = i + 1) {\n    int x;\n    x = 2 * y;\n    int y;\n    i = x + 0;\n}\n    int y;\n}\n}\n    while (i) {\n    for (int x = 0; x < 10; x = x + 1) {\n    1 / z;\n    z = y;\n    for (int y = 0; y < 10; y = y + 1) {\n    z++;\n}\n}\n    if (10 - 1) {\n    for (int y = 0; y < 10; y = y + 1) {\n    int z;\n    x = 0;\n    i = 2;\n    x++;\n}\n    int z;\n    switch (z) {\n    case 2:\n        break;\n    case 0:\n        break;\n    default:\n        break;\n}\n    y = 10 / y;\n}\n}\n    int x;\n    while (1) {\n    int z;\n    for (int i = 0; i < 10; i = i + 1) {\n    return 2;\n}\n    0 * 10;\n    2;\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_79():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_80():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_81():
    source = 'void main() {\n    return i / y;\n    x--;\n    while (1 / 1) {\n    z++;\n    switch (0 / i) {\n    case 1:\n        break;\n    case 10:\n        break;\n    default:\n        break;\n}\n    while (0 / 1) {\n    return x;\n}\n    switch (y / 10) {\n    case 10:\n        break;\n    default:\n        break;\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_82():
    source = 'void main() {\n    if (2) {\n    i = 2 / x;\n    while (y) {\n    while (z) {\n    return 2 + x;\n}\n    z = i;\n}\n    switch (1) {\n    case 10:\n        break;\n    case 10:\n        break;\n    default:\n        break;\n}\n    int i;\n}\n    z = y + z;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_83():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_84():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_85():
    source = 'void main() {\n    switch (1 + 0) {\n    case 10:\n        break;\n    default:\n        break;\n}\n    int x;\n    int z;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_86():
    source = 'struct S { int x; int y; };\nvoid main() {\n    2 / i;\n    for (int y = 0; y < 10; y = y + 1) {\n    for (int i = 0; i < 10; i = i + 1) {\n    return 2 / x;\n}\n    return 0;\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_87():
    source = 'struct S { int x; int y; };\nvoid main() {\n    while (i / y) {\n    switch (1) {\n    case 10:\n        break;\n    case 10:\n        break;\n    default:\n        break;\n}\n    while (z * y) {\n    while (y) {\n    1;\n    i = z / 2;\n}\n    y++;\n}\n    switch (10 + 1) {\n    case 1:\n        break;\n    case 1:\n        break;\n    default:\n        break;\n}\n}\n    int i;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_88():
    source = 'struct S { int x; int y; };\nvoid main() {\n    switch (10 - y) {\n    case 10:\n        break;\n    case 10:\n        break;\n    default:\n        break;\n}\n    int y;\n    if (0) {\n    if (10) {\n    x = 1 + 10;\n    return y - 0;\n    int i;\n    if (1) {\n    return i;\n}\n}\n    return 2 - z;\n}\n    return x;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_89():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_90():
    source = 'void main() {\n    if (y - 2) {\n    if (z) {\n    y--;\n    switch (2) {\n    case 2:\n        break;\n    default:\n        break;\n}\n}\n}\n    for (int i = 0; i < 10; i = i + 1) {\n    i = 1 / 10;\n}\n    while (y) {\n    while (2) {\n    for (int y = 0; y < 10; y = y + 1) {\n    z--;\n    i = x + y;\n    return y;\n    i = x / i;\n}\n    y--;\n}\n    z = y * z;\n    int i;\n    if (2) {\n    x = 10;\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_91():
    source = 'struct S { int x; int y; };\nvoid main() {\n    switch (y / z) {\n    case 0:\n        break;\n    default:\n        break;\n}\n    switch (y + y) {\n    case 1:\n        break;\n    default:\n        break;\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_92():
    source = 'void main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_93():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_94():
    source = 'struct S { int x; int y; };\nvoid main( { }'
    parser = Parser(source)
    result = parser.parse()
    assert result != 'success'

def test_parser_95():
    source = 'struct S { int x; int y; };\nvoid main() {\n    z++;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_96():
    source = 'void main() {\n    return y;\n    1 / 1;\n    y - 0;\n    int z;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_97():
    source = 'struct S { int x; int y; };\nvoid main() {\n    if (i) {\n    for (int x = 0; x < 10; x = x + 1) {\n    switch (1) {\n    case 0:\n        break;\n    default:\n        break;\n}\n    while (z) {\n    return z / y;\n    int x;\n    int z;\n    x = 2;\n}\n}\n    if (2 / y) {\n    if (y) {\n    int y;\n    z = y * 2;\n    x = y;\n}\n    for (int x = 0; x < 10; x = x + 1) {\n    int z;\n    x = z;\n    int y;\n    return 0 - 1;\n}\n}\n    x++;\n    while (0 + 0) {\n    switch (10) {\n    case 2:\n        break;\n    case 0:\n        break;\n    default:\n        break;\n}\n}\n}\n    y--;\n    x = x;\n    int x;\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_98():
    source = 'struct S { int x; int y; };\nvoid main() {\n    while (z - x) {\n    return i / 1;\n    if (1) {\n    int y;\n}\n    return 2;\n    i = 0 * y;\n}\n    switch (0) {\n    case 2:\n        break;\n    default:\n        break;\n}\n    if (10) {\n    switch (x) {\n    case 1:\n        break;\n    default:\n        break;\n}\n    for (int x = 0; x < 10; x = x + 1) {\n    while (x) {\n    int i;\n    i;\n    return x - 0;\n}\n    x = 2;\n}\n    while (y + z) {\n    x = z - 0;\n    if (1) {\n    i--;\n    x = z;\n    int y;\n    int y;\n}\n    switch (y) {\n    case 2:\n        break;\n    case 10:\n        break;\n    default:\n        break;\n}\n    while (i) {\n    z++;\n    int y;\n    1;\n    x = 1;\n}\n}\n}\n    for (int x = 0; x < 10; x = x + 1) {\n    if (x) {\n    switch (10) {\n    case 0:\n        break;\n    default:\n        break;\n}\n    y = x;\n    int y;\n    1 + 0;\n}\n    x = i;\n    switch (y + 10) {\n    case 0:\n        break;\n    default:\n        break;\n}\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'

def test_parser_99():
    source = 'struct S { int x; int y; };\nvoid main() {\n    for (int i = 0; i < 10; i = i + 1) {\n    for (int i = 0; i < 10; i = i + 1) {\n    while (i) {\n    i++;\n    int y;\n}\n    if (10) {\n    return y;\n    y--;\n    y = 2;\n    i--;\n}\n}\n}\n    while (0 - x) {\n    return 0;\n    int i;\n    while (z) {\n    return 0;\n}\n}\n    int y;\n    for (int z = 0; z < 10; z = z + 1) {\n    1 + 1;\n    0 - 10;\n}\n}'
    parser = Parser(source)
    result = parser.parse()
    assert result == 'success'
