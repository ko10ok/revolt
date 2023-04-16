from typing import List, NamedTuple, Any

from district42.utils import is_ellipsis


class Pair(NamedTuple):
    l: Any
    r: Any

    def __repr__(self):
        return f'{self.l} ~ {self.r}'


def list_combine(base: List, sub: List) -> List:
    ...


# # (1, ...)(1, 1)(1, 2)  # F (1, 3) (1, ...) (1, ...) (2, ...) (3, ...) (4, ...) (..., ...)
# # (1, ...)(1, 1)(1, 2)(1, 3)(1, ...)(1, ...)(2, ...)(3, ...)(4, ...)(..., ...)
#
# print('==========================')
# print(list_combine([..., 1, ...], [..., 1, ..., 2, ...]))
# print(list_combine([..., 1, ...], [..., 1, ..., 2, 1, ...]))
# # print(list_combine([..., 1, ..., 2, ...], [..., 1, ..., 2, ...]))
#
# print('==========================')
# print(schema_list_combine([..., 1, ...], [..., 1, ..., 1, ...]))
#
# sys.exit()
#
# print(list_combine([..., 1, 2, 3, ...], [1, 2, 3]))
# print(list_combine([..., 1, 2, 3, ...], [..., 1, 2, 3, ...]))
# print(list_combine([..., 1, 2, ..., 3, ...], [..., 1, 2, 3, ...]))
# print(list_combine([..., 1, 2, ..., 3, ...], [..., 1, 2, ..., 3, ...]))
# print(list_combine([..., 1, 2, ..., 3, ...], [..., 1, ..., 2, 3, ...]))


# NOPE!
# a' = partitions(a)        # [ ..., ( [1, 2, 3], [4, 5] ), ...]
# b' = partitions(b)        # [ ..., ( [1, 2], [3, 4, 5] ), ...]
# foreach a' => a'':
#    foreach b' => b'':
#       vary_pairs_2_lists(a''' with b''')
#          ( [1,2,3], [4,5] ) - ( [1,2], [3, 4, 5] )

# fillout ( [1,2,3], [4,5], I ) - ( [1,2], [3, 4, 5], None )
#         ( [1,2,3], [4,5], None ) - ( [1,2], [3, 4, 5], I ) to len == len
# ( I* if I ) or ( None if no I )

# filterout () with element []-[]: len != len


# tokenizing
# [..., 1,2,3,... ,1,2,3,4,...] -> [..., sub[1,2,3],... ,sub[1,2,3,4], ...]
# split from ... : [...], sub[1,2,3], [...] ,sub[1,2,3,4], [...]
# vary non [...]:
#   [...], partitions(sub[1,2,3]) as A, [...] ,partitions(sub[1,2,3,4]) as B, [...] :  AxB cases
#
# NOPE


# [..., 1,2,3,... ,1,2,3,4,...] -> [..., 1] [,2,] [3,...], [... ,1],[2,3],[4,...]

# [6, 1, 2, 3, 4, 5, 6, 7]
# [6, 1] [2] [3,


class MappingError(NamedTuple):
    stack: List
    msg: str
    base: List
    sub: List


class ErrStack:
    def __init__(self):
        self.errors = []

    def snapshot_error(self, state, msg, a, b):
        self.errors += [MappingError(state, msg, a, b)]


def make_list_combinations(pattern, sub, err_stack, seq=None, comparator=None) -> List[List[Pair]]:
    # print('new: ', pattern, sub, stack.state())
    if seq is None:
        seq = []

    if pattern == [] and sub == []:
        yield seq

    sub_idx = 0
    pattern_idx = 0

    if pattern:
        pattern_item = pattern[pattern_idx]
        if is_ellipsis(pattern_item):
            # skip "..."
            yield from make_list_combinations(
                pattern[pattern_idx + 1:],
                sub[sub_idx:],
                err_stack,
                seq + [Pair(..., None)],
                comparator
            )

            # with "..."
            if sub:
                yield from make_list_combinations(
                    pattern[pattern_idx:],
                    sub[sub_idx + 1:],
                    err_stack,
                    seq + [Pair(..., sub[sub_idx])],
                    comparator
                )
        else:
            if len(sub) == 0:
                err_stack.snapshot_error(
                    seq,
                    'substitution exhausted while pattern not done',
                    pattern,
                    sub
                )
                # print('wrong: sub exhausted while: pattern not ready: ', pattern, sub)
                return

            assert comparator, f'Can\'t compare {pattern_item} with {sub[sub_idx]}'
            # change to substitution via .apply() and ... handling
            if not comparator(pattern_item, sub[sub_idx]):
                err_stack.snapshot_error(
                    seq,
                    f'unordered substitution: item {sub[sub_idx]} with next {pattern_item}',
                    pattern,
                    sub
                )
                # print('wrong: ', pattern_item, ' != ', sub[sub_idx])
                return

            if is_ellipsis(sub[sub_idx]):
                # skip "..."
                yield from make_list_combinations(
                    pattern[pattern_idx:],
                    sub[1:],
                    err_stack,
                    seq + [Pair(..., ...)],
                    comparator
                )

                # with "..."
                # if pattern:
                #     yield from make_list_combinations(
                #         pattern[pattern_idx + 0:],
                #         sub,
                #         err_stack,
                #         seq + [Pair(pattern[0], sub[0])]
                #     )

            yield from make_list_combinations(
                pattern[pattern_idx + 1:],
                sub[sub_idx + 1:],
                err_stack,
                seq + [Pair(pattern_item, sub[sub_idx])],
                comparator
            )
