import pathlib as pl

import pandas as pd

# load all the data from the data/ directory into environment -----

data_pl = pl.Path("data")
data_pl_path = list(data_pl.glob("*.csv"))
data = {f.stem: pd.read_csv(f) for f in data_pl_path}
assert len(data) == 20
locals().update(data)

# table 1 -----

demographics.shape

demographics.groupby(["is_male"])[["is_male"]].count().T
demographics.age.describe()
demographics.groupby(["is_hispanic"])[["is_hispanic"]].count().T
demographics.groupby(["race"])[["race"]].count().T
demographics.groupby(["education"])[["education"]].count()
demographics.groupby(["marital"])[["marital"]].count()
demographics.groupby(["job"])[["job"]].count()
demographics.groupby(["is_living_stable"])[["is_living_stable"]].count()

## table 1 patient splits can be broken down by combining with the everybody table

demo_everybody = demographics.merge(everybody, on="who")

demo_everybody.groupby("project").agg("count").T

# table 2 -----

uds.what.value_counts().rename_axis("Drug").reset_index(name="Count")


# table 3 -----

psychiatric.drop(columns="who").apply(lambda x: x.value_counts(dropna=False))

#
