import logging
import math
import scipy.stats
import statsmodels.stats.proportion


LOGGING_FORMAT = "%(levelname)s:%(filename)s:%(lineno)s-%(funcName)s: %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_min_sample_size_to_estimate_success_rate(
    success_rate: float,
    error_margin: float,
    significance_level: float
) -> int:
    logger.debug(
        "Started; \n"
        f"\t success_rate= {success_rate} \n"
        f"\t error_margin= {error_margin} \n"
        f"\t significance_level= {significance_level}"
    )

    def cdf(n, m):
        rv = scipy.stats.binom(n, success_rate)
        return rv.cdf(m)
    
    n_begin, n_end = 1, 10**4
    while n_begin < n_end:
        n = (n_begin + n_end) // 2

        left_boundary = math.ceil((success_rate - error_margin)*n)
        right_boundary = math.floor((success_rate + error_margin)*n)

        significance_level_ = cdf(n, right_boundary) - cdf(n, left_boundary)
        if significance_level_ <= significance_level:
            n_begin = n + 1
        else:
            n_end = n
    
    return n_begin


def get_conf_int(
    success_rate: float,
    num_trials: int,
    confidence_level: float
) -> tuple[float, float]:
    # logger.debug(
    #     "Started; \n"
    #     f"\t success_rate= {success_rate} \n"
    #     f"\t num_trials= {num_trials} \n"
    #     f"\t confidence_level= {confidence_level}"
    # )
    
    method = "wilson"
    num_success = math.ceil(num_trials * success_rate)
    alpha = 1 - confidence_level
    
    conf_int_low, conf_int_upp = statsmodels.stats.proportion.proportion_confint(num_success, num_trials, alpha=alpha, method=method)
    logger.debug(f"conf_int= {[conf_int_low, conf_int_upp]}")
    
    return conf_int_low, conf_int_upp


def get_min_num_trials(
    success_rate: float,
    error_margin: float,
    confidence_level: float
) -> int:
    logger.debug(
        "Started; \n"
        f"\t success_rate= {success_rate} \n"
        f"\t error_margin= {error_margin} \n"
        f"\t confidence_level= {confidence_level}"
    )

    n_begin, n_end = 1, 10**4
    while n_begin < n_end:
        n = (n_begin + n_end) // 2
        conf_int_low, conf_int_upp = get_conf_int(success_rate, n, confidence_level)
        
        # if conf_int_upp - conf_int_low > error_margin:
        max_margin = max(success_rate - conf_int_low, conf_int_upp - success_rate)
        if max_margin > error_margin:
            n_begin = n + 1
        else:
            n_end = n
    
    return n_begin


if __name__ == "__main__":
    # success_rate = 0.9
    # num_trials = 100
    # confidence_level = 0.95
    # get_conf_int(success_rate, num_trials, confidence_level)

    """
    success_rate = 0.9
    ## 1
    min_num_trials = get_min_num_trials(
        success_rate,
        error_margin = 0.1,
        confidence_level = 0.95
    )
    logger.info(f"min_num_trials= {min_num_trials}")

    ## 2
    min_num_trials = get_min_num_trials(
        success_rate,
        error_margin = 0.15,
        confidence_level = 0.95
    )
    logger.info(f"min_num_trials= {min_num_trials}")
    """

    confidence_level = 0.95
    # for success_rate in [0.85, 0.90, 0.95]:
    for success_rate in [0.75]:
        for error_margin in [0.05, 0.10, 0.15]:
            min_num_trials = get_min_num_trials(
                success_rate,
                error_margin,
                confidence_level
            )
            logger.info(f"min_num_trials= {min_num_trials}")


    # significance_level = 0.99
    # for success_rate in [0.75, 0.85]:
    #     for error_margin in [0.07]:
    #         min_sample_size = get_min_sample_size_to_estimate_success_rate(
    #             success_rate,
    #             error_margin,
    #             significance_level
    #         )

    #         logger.info(f"min_sample_size= {min_sample_size}")
