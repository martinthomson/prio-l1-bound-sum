from vdaf_poc.field import Field64, Field96, Field128, NttField
from vdaf_poc.flp_bbcggi19 import FlpBBCGGI19
from vdaf_poc.test_utils import TestFlpBBCGGI19

from flp_l1_bound_sum import L1BoundSum


class TestL1BoundSum(TestFlpBBCGGI19):
    def run_encode_truncate_decode_with_ntt_fields_test(
            self,
            measurements: list[list[int]],
            length: int,
            bits: int,
            chunk_length: int) -> None:
        for field in [Field64, Field96, Field128]:
            l1boundsum = L1BoundSum[NttField](
                field,
                length,
                bits,
                chunk_length,
            )
            self.assertEqual(l1boundsum.field, field)
            self.assertTrue(isinstance(l1boundsum, L1BoundSum))
            self.run_encode_truncate_decode_test(
                FlpBBCGGI19(l1boundsum),
                measurements,
            )

    def test_with_fields(self) -> None:
        # L1BoundSum with length = 4, bits = 3, chunk length = 3.
        self.run_encode_truncate_decode_with_ntt_fields_test(
            [
                [7, 0, 0, 0],
                [0, 0, 0, 7],
                [1, 2, 2, 1],
                [2, 1, 2, 2],
                [5, 2, 0, 0],
                [0, 0, 0, 0],
            ],
            4,
            3,
            3,
        )

    def test_valid(self) -> None:
        valid = L1BoundSum(Field128, 4, 3, 3)
        flp = FlpBBCGGI19(valid)
        self.run_flp_test(
            flp,
            [
                (flp.encode([7, 0, 0, 0]), True),
                (flp.encode([0, 0, 0, 7]), True),
                (flp.encode([2, 2, 2, 1]), True),
                (flp.encode([0, 0, 0, 0]), True),
                (flp.encode([2, 2, 2, 0]), True),
                (flp.encode([1, 0, 2, 0]), True),
            ],
        )

    def test_invalid(self) -> None:
        field = Field128
        length = 4
        bits = 3
        valid = L1BoundSum(field, length, bits, 3)
        flp = FlpBBCGGI19(valid)
        self.run_flp_test(
            flp,
            [
                (
                    field.encode_into_bit_vector(7, bits)
                    + field.encode_into_bit_vector(0, bits)
                    + field.encode_into_bit_vector(0, bits)
                    + field.encode_into_bit_vector(0, bits)
                    + field.encode_into_bit_vector(6, bits),
                    False,
                ),
                (
                    [field(2)]
                    + [field(0)] * 11
                    + field.encode_into_bit_vector(2, bits),
                    False,
                ),
                (
                    [
                        # first vector element: 2
                        field(0),
                        field(1),
                        field(0),
                        # rest of vector elements: 0
                        field(0),
                        field(0),
                        field(0),
                        field(0),
                        field(0),
                        field(0),
                        field(0),
                        field(0),
                        field(0),
                        # improperly encoded weight
                        field(2),
                        field(0),
                        field(0),
                    ],
                    False,
                ),
            ],
        )
