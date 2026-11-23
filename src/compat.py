"""factor_analyzer 0.5 calls sklearn's check_array(force_all_finite=...), which newer
scikit-learn renamed to ensure_all_finite. Import this module before using factor_analyzer."""
import factor_analyzer.factor_analyzer as _fa
from sklearn.utils import check_array as _check_array


def _patched(*args, **kwargs):
    if "force_all_finite" in kwargs:
        kwargs["ensure_all_finite"] = kwargs.pop("force_all_finite")
    return _check_array(*args, **kwargs)


_fa.check_array = _patched
