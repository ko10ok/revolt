from typing import List, Tuple

import pytest
from baby_steps import then, when, given

from revolt.utils.list_combinator import make_list_combinations, Pair, ErrStack


@pytest.mark.parametrize("base, sub, expected", [
    (
        [1, 2, 3],
        [1, 2, 3],
        [[Pair(1, 1), Pair(2, 2), Pair(3, 3)]]
    ),
    (
        [1, 1, 1],
        [1, 1],
        []
    ),
    (
        [1, 1],
        [1, 1, 1],
        []
    ),
    (
        [1, 2, ...],
        [1, 2, 3],
        [[Pair(1, 1), Pair(2, 2), Pair(..., 3), Pair(..., None)]]
    ),
    (
        [..., 1, 2],
        [3, 1, 2],
        [[Pair(..., 3), Pair(..., None), Pair(1, 1), Pair(2, 2)]]
    ),
    (
        [..., 1, ...],
        [1, 1],
        [
            [Pair(..., 1), Pair(..., None), Pair(1, 1), Pair(..., None)],
            [Pair(..., None), Pair(1, 1), Pair(..., 1), Pair(..., None)],
        ]
    ),
    (
        [..., 1, ...],
        [1, 1, 1],
        [
            [Pair(..., 1), Pair(..., 1), Pair(..., None), Pair(1, 1), Pair(..., None)],
            [Pair(..., 1), Pair(..., None), Pair(1, 1), Pair(..., 1), Pair(..., None)],
            [Pair(..., None), Pair(1, 1), Pair(..., 1), Pair(..., 1), Pair(..., None)],
        ]
    ),
    (
        [1],
        [1, ...],
        []
    ),
    (
        [1],
        [..., 1],
        []
    ),
    (
        [1],
        [..., 1, ...],
        []
    ),
    (
        [..., 1, ..., 1, ...],
        [1, 1],
        [
            [Pair(..., None), Pair(1, 1), Pair(..., None), Pair(1, 1), Pair(..., None)],
        ]
    ),
    (
        [..., 1, 2, 3, 4, ..., 5, 6, 7, 8, ...],
        [1, 2, 3, 4, 5, 6, 7, 8],
        [
            [Pair(..., None),
             Pair(1, 1), Pair(2, 2), Pair(3, 3), Pair(4, 4),
             Pair(..., None),
             Pair(5, 5), Pair(6, 6), Pair(7, 7), Pair(8, 8),
             Pair(..., None)],
        ]
    ),
    (
        [..., 1, ..., 1, ...],
        [1, 1, 1],
        [
            [Pair(..., 1), Pair(..., None), Pair(1, 1), Pair(..., None), Pair(1, 1),
             Pair(..., None)],
            [Pair(..., None), Pair(1, 1), Pair(..., 1), Pair(..., None), Pair(1, 1),
             Pair(..., None)],
            [Pair(..., None), Pair(1, 1), Pair(..., None), Pair(1, 1), Pair(..., 1),
             Pair(..., None)],
        ]
    ),
    (
        [..., 1, ..., 1, ...],
        [..., 1, ..., 1, ...],
        [
            [
                Pair(..., ...),
                Pair(..., None),
                Pair(1, 1),
                Pair(..., ...),
                Pair(..., None),
                Pair(1, 1),
                Pair(..., ...),
                Pair(..., None)
            ]
        ]
    ),
    (
        [..., 1, 2, ..., 3, ...],
        [..., 1, 2, 3, ...],
        [
            [
                Pair(..., ...),
                Pair(..., None),
                Pair(1, 1),
                Pair(2, 2),
                Pair(..., None),
                Pair(3, 3),
                Pair(..., ...),
                Pair(..., None)
            ]
        ]
    ),
    (
        [..., 1, 2, ..., 3, ...],
        [..., 1, ..., 2, 3, ...],
        []
    ),
    (
        [..., 1, ...],
        [..., 1, ..., 1, ...],
        [
            [
                Pair(..., ...),
                Pair(..., None),
                Pair(1, 1),
                Pair(..., ...),
                Pair(..., 1),
                Pair(..., ...),
                Pair(..., None)
            ],
            [
                Pair(..., ...),
                Pair(..., 1),
                Pair(..., ...),
                Pair(..., None),
                Pair(1, 1),
                Pair(..., ...),
                Pair(..., None)
            ],
        ]
    ),
    (
        [..., 1, ..., 1, ...],
        [..., 1, ..., 1, ..., 1, ...],
        [
            [
                Pair(..., ...),
                Pair(..., None),
                Pair(1, 1),
                Pair(..., ...),
                Pair(..., 1),
                Pair(..., ...),
                Pair(..., None),
                Pair(1, 1),
                Pair(..., ...),
                Pair(..., None)
            ],
            [
                Pair(..., ...),
                Pair(..., 1),
                Pair(..., ...),
                Pair(..., None),
                Pair(1, 1),
                Pair(..., ...),
                Pair(..., None),
                Pair(1, 1),
                Pair(..., ...),
                Pair(..., None)
            ],
            [
                Pair(..., ...),
                Pair(..., None),
                Pair(1, 1),
                Pair(..., ...),
                Pair(..., None),
                Pair(1, 1),
                Pair(..., ...),
                Pair(..., 1),
                Pair(..., ...),
                Pair(..., None)
            ],
        ]
    ),
])
def test_list_combinator(base: List, sub: List, expected: List[Tuple[Tuple]]):
    with given:
        stack = ErrStack()

    with given:
        comparator = lambda x, y: x == y

    with when:
        res = list(make_list_combinations(base, sub, stack, comparator=comparator))

    with then:
        for item in expected:
            assert item in res

    with then:
        for item in res:
            assert item in expected

    with then:
        assert len(res) == len(expected)
