#!/usr/bin/env python3
import os

from vdaf_poc.test_utils import gen_test_vec_for_vdaf

from vdaf_prio3_l1_bound_sum import Prio3L1BoundSum

TEST_VECTOR_PATH = os.environ.get(
    "TEST_VECTOR_PATH",
    "../test_vec/",
)


if __name__ == "__main__":
    ctx = b"some application"
    vdaf_test_vec_path = TEST_VECTOR_PATH + "/vdaf/"

    num_shares = 2
    prio = Prio3L1BoundSum(2, 10, 8, 9)
    measurements = [
        list(range(10)),
        [255, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 255],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1] * 10,
    ]
    gen_test_vec_for_vdaf(
        vdaf_test_vec_path,
        prio,
        None,
        ctx,
        measurements,
        0,
    )
