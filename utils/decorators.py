import functools
import timeit
from aoc2020.utils.log.base import get_logger

logger = get_logger(__name__)


def timer(func):
    @functools.wraps(func)
    def timer_wrapper(*args, **kwargs):
        start = timeit.default_timer()

        result = func(*args, **kwargs)

        elapsed = timeit.default_timer() - start
        logger.info(f"Completed {func.__name__} in {elapsed:4f} seconds.")

        return result

    return timer_wrapper
