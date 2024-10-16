from vdaf_poc.field import Field128
from vdaf_poc.flp_bbcggi19 import FlpBBCGGI19
from vdaf_poc.vdaf_prio3 import Prio3
from vdaf_poc.xof import XofTurboShake128

from flp_l1_bound_sum import L1BoundSum


class Prio3L1BoundSum(Prio3[list[int], list[int], Field128]):
    ID = 0xFFFF0000  # TODO: select algorithm ID
    xof = XofTurboShake128
    VERIFY_KEY_SIZE = xof.SEED_SIZE

    # Name of the VDAF, for use in test vector filenames.
    test_vec_name = "Prio3L1BoundSum"

    def __init__(self, shares: int, length: int, bits: int, chunk_length: int):
        flp = FlpBBCGGI19[list[int], list[int], Field128](
            L1BoundSum(Field128, length, bits, chunk_length)
        )
        super().__init__(shares, flp, 1)
