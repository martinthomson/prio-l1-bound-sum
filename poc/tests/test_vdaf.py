from vdaf_poc.test_utils import TestVdaf

from vdaf_prio3_l1_bound_sum import Prio3L1BoundSum


class TestPrio3SumVec(TestVdaf):
    def test(self) -> None:
        prio3 = Prio3L1BoundSum(2, 4, 3, 3)
        self.run_vdaf_test(
            prio3,
            None,
            [
                [7, 0, 0, 0],
                [0, 0, 0, 7],
                [0, 0, 0, 0],
                [1, 2, 2, 2],
                [0, 1, 0, 0],
            ],
            [8, 3, 2, 9],
        )
