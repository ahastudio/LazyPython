from lazy import lazy, ChainEffect, Effect, print

@lazy
def sum(a, b):
    return a + b


def mul(a):
    @lazy
    def lazy_mul(b):
        return a * b
    return lazy_mul


def test_lazy_sum():
    sum_effect = sum(1, 2)

    assert isinstance(sum_effect, Effect)

    assert sum_effect.excute() == 1 + 2
    assert not sum_effect.excute() == 1 + 3


def test_effect_chain():
    sum_effect = sum(1, 2)
    print_effect = sum_effect.flatMap(print)

    assert isinstance(print_effect, ChainEffect)
    
    sum_effect = sum(4, 1)
    print_effect = sum_effect << print

    assert isinstance(print_effect, ChainEffect)


def test_lazy_one_multiplex():
    multiplexer = mul(2)
    sum_effect = sum(1, 2)
    result_effect = sum_effect\
        .flatMap(multiplexer)

    assert isinstance(result_effect, ChainEffect)
    assert result_effect.excute() == 3 * 2


def test_lazy_multiplex():
    multiplexer = mul(2)
    sum_effect = sum(1, 2)

    result_effect = sum_effect\
        .flatMap(multiplexer)\
        .flatMap(multiplexer)\
        .flatMap(multiplexer)


    assert isinstance(result_effect, ChainEffect)
    assert result_effect.excute() == 3 * 2 * 2 * 2


def test_lazy_maps():
    sum_effect = sum(1, 2)
    result = sum_effect\
        .map(lambda x: x + 1)\
        .map(lambda x: x + 1)\
        .map(lambda x: x + 1)\
        .excute()
    assert result == 1 + 2 + 1 + 1 + 1

def test_lazy_one_multiplex():
    multiplexer = mul(2)
    sum_effect = sum(1, 2)
    chain_effect = sum_effect\
        .flatMap(multiplexer)\
        .flatMap(multiplexer)\
        .map(lambda x: x - 4)

    assert chain_effect.excute() == (3 * 2 * 2) - 4