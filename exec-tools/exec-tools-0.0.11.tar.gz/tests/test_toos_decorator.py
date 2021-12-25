from exectools import RunTime
import time


@RunTime.run_time(show_short_result=10)
def test_run_time_res(sleep=1):
    time.sleep(sleep)
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


@RunTime.loop_time(show_short_result=10)
def test_loop_while_res(sleep=1):
    time.sleep(sleep)
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


@RunTime.loop_time(loop_times=2, show_short_result=10)
def test_loop_range_res(sleep=1):
    time.sleep(sleep)
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


if __name__ == '__main__':
    pass
    # test_run_time_res()
    test_loop_while_res()
    # test_loop_range_res()
