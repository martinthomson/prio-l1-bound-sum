from typing import Any, Optional, TypeVar, cast

from vdaf_poc.field import NttField
from vdaf_poc.flp_bbcggi19 import Mul, ParallelSum, Valid

F = TypeVar("F", bound=NttField)


class L1BoundSum(Valid[list[int], list[int], F]):
    EVAL_OUTPUT_LEN = 2
    length: int
    bits: int
    chunk_length: int
    field: type[F]

    def __init__(self,
                 field: type[F],
                 length: int,
                 bits: int,
                 chunk_length: int):
        """
        Instantiate the `L1BoundSum` circuit for measurements with
        `length` elements, each in the range `[0, 2^bits)`, and with
        a maximum L1 norm of `2^bits - 1`.
        """
        self.field = field
        self.length = length
        self.bits = bits
        self.chunk_length = chunk_length
        self.GADGETS = [ParallelSum(Mul(), chunk_length)]
        self.GADGET_CALLS = [
            ((length + 1) * bits + chunk_length - 1) // chunk_length
        ]
        self.MEAS_LEN = (length + 1) * bits
        self.OUTPUT_LEN = length
        self.JOINT_RAND_LEN = self.GADGET_CALLS[0]

    def eval(
            self,
            meas: list[F],
            joint_rand: list[F],
            num_shares: int) -> list[F]:
        range_check = self.field(0)
        shares_inv = self.field(num_shares).inv()
        for i in range(self.GADGET_CALLS[0]):
            r = joint_rand[i]
            r_power = r
            inputs: list[Optional[F]]
            inputs = [None] * (2 * self.chunk_length)
            for j in range(self.chunk_length):
                index = i * self.chunk_length + j
                if index < len(meas):
                    meas_elem = meas[index]
                else:
                    meas_elem = self.field(0)

                inputs[j * 2] = r_power * meas_elem
                inputs[j * 2 + 1] = meas_elem - shares_inv

                r_power *= r

            range_check += self.GADGETS[0].eval(
                self.field,
                cast(list[F], inputs),
            )

        observed_weight = self.field(0)
        for i in range(self.length):
            observed_weight += self.field.decode_from_bit_vector(
                meas[i * self.bits:(i + 1) * self.bits]
            )
        weight_position = self.length * self.bits
        claimed_weight = self.field.decode_from_bit_vector(
            meas[weight_position:weight_position + self.bits]
        )
        weight_check = observed_weight - claimed_weight

        return [range_check, weight_check]

    def encode(self, measurement: list[int]) -> list[F]:
        encoded = []
        for val in measurement:
            encoded += self.field.encode_into_bit_vector(
                val,
                self.bits,
            )
        encoded += self.field.encode_into_bit_vector(
            sum(measurement),
            self.bits,
        )
        return encoded

    def truncate(self, meas: list[F]) -> list[F]:
        truncated = []
        for i in range(self.length):
            truncated.append(self.field.decode_from_bit_vector(
                meas[i * self.bits: (i + 1) * self.bits]
            ))
        return truncated

    def decode(
            self,
            output: list[F],
            _num_measurements) -> list[int]:
        return [x.as_unsigned() for x in output]

    def test_vec_set_type_param(self, test_vec: dict[str, Any]) -> list[str]:
        test_vec['length'] = self.length
        test_vec['bits'] = self.bits
        test_vec['chunk_length'] = self.chunk_length
        return ['length', 'bits', 'chunk_length']
