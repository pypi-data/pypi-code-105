

from ._utils import experimental
from ._utils import has_dependency
from ._utils import requires


# external dependencies go here (i.e. those not in standard library)
if has_dependency("sklearn"):
    import sklearn
    import sklearn.datasets
    import sklearn.preprocessing

if has_dependency("pandas"):
    import pandas as pd

if has_dependency("numpy"):
    import numpy as np
# end of external dependencies


# TODO: expose it externally?
@experimental
@requires("numpy", "pandas", "sklearn")
def generate_dummy_classification_data(
        n_samples=10_000,
        target_name="label",
        random_state=None,
        ):
    """
    Generate dummy dataset using sklearn.datasets.make_classification.
    """
    from sklearn.preprocessing import MinMaxScaler
    n_features = 20  # maybe add configurability in the future

    data = sklearn.datasets.make_classification(
        n_samples=n_samples,
        n_features=n_features,
        random_state=random_state,
    )

    data[0][:, 10:20] = MinMaxScaler().fit_transform(data[0][:, 10:20])

    df = pd.DataFrame(data=data[0], columns=[f"f{idx}" for idx in range(n_features)], copy=False)
    df[target_name] = data[1]
    del data  # no longer needed

    # create some integer features
    for num, idx in enumerate(range(10, 15)):
        df[f"f{idx}"] = (df[f"f{idx}"] * (1.5 + 3 * num)).astype(np.int32)

    # create some string features
    words_lookup = [
        "foo", "bar", "baz", "qux", "quux", "quuz", "corge", "grault",
        "garply", "waldo", "fred", "plugh", "xyzzy", "thud",
    ]

    for num, idx in enumerate(range(15, 20)):
        df[f"f{idx}"] = (df[f"f{idx}"] * (1.5 + 3 * num)).astype(np.int32)
        df[f"f{idx}"] = df[f"f{idx}"].apply(lambda x: words_lookup[x % len(words_lookup)])

    return df


# IDEA: load_iris
# IDEA: fetch_uci_ml(name: str)?
#   * UCI ML Credit Card dataset
#   * ...
