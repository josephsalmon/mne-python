# Authors: Yousra Bekhti <yousra.bekhti@gmail.com>
#          Mark Wronkiewicz <wronk@uw.edu>
#
# License: BSD (3-clause)

import numpy as np
from scipy.linalg import norm

# TODO: Add more localization accuracy functions. For example, distance between
#       true dipole position (in simulated stc) and the centroid of the
#       estimated activity.


def _check_stc(stc1, stc2):
    """Helper for checking that stcs are compatible"""
    if stc1.data.shape != stc2.data.shape:
        raise ValueError('Data in stcs must have the same size')
    if np.all(stc1.times != stc2.times):
        raise ValueError('Times of two stcs must match.')


def source_estimate_quantification(stc1, stc2, metric='rms', src=None):
    """Helper function to calculate matrix similarities.

    Parameters
    ----------
    stc1 : SourceEstimate
        First source estimate for comparison
    stc2 : SourceEstimate
        First source estimate for comparison
    metric : str
        Metric to calculate. 'rms', 'rms_normed', 'corr', 'distance_err',
        'weighted_distance_err', ...
    src : None | list of dict
        The source space. The default value is None. It must be provided when
        using those metrics: "distance_err", "weighted_distance_err"

    Returns
    -------
    score : float | array
        Calculated metric

    Notes
    -----
    Metric calculation has multiple options:
        rms: Root mean square of difference between stc data matrices.
        cosine: Normalized correlation of all elements in stc data matrices.
        distance_err: Distance between most active dipoles.
        weighted_distance_err: Distance between most active dipoles weighted by
            difference in activity.
    """
    known_metrics = ['rms', 'cosine', 'distance_err',
                     'weighted_distance_err']
    if metric not in known_metrics:
        raise ValueError('metric must be a str from the known metrics: '
                         '"rms", "cosine", "distance_err", '
                         '"weighted_distance_err" or "..."')

    if metric in ['distance_err', 'weighted_distance_err'] and src is None:
        raise ValueError('The source space src is needed when using '
                         '"distance_err" or "weighted_distance_err"')

    # This is checking that the datas are having the same size meaning
    # no comparison between distributed and sparse can be done so far.
    _check_stc(stc1, stc2)
    data1, data2 = stc1.data, stc2.data

    # Calculate root mean square difference between two matrices
    if metric == 'rms':
        return np.sqrt(np.mean((data1 - data2) ** 2))

    # Calculate correlation coefficient between matrix elements
    elif metric == 'cosine':
        score = (np.correlate(data1.flatten(), data2.flatten()) /
                 (norm(data1) * norm(data2)))
        return 1 - score
