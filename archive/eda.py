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

pd.DataFrame(demographics.is_male.value_counts(dropna=False)).T

demographics.is_male.isnull().mean()


import pandas as pd
import plotly.express as px

# Example DataFrame
data = {"A": [1, 2, None, 4], "B": [None, 2, 3, 4], "C": [1, None, None, 4]}
df = pd.DataFrame(data)

data = {"A": [1, 2, None, 4, None, None]}
df = pd.DataFrame(data)

# Step 1: Calculate the proportion of missing values for each column
missing_proportion = df.isnull().mean().reset_index()
missing_proportion.columns = ["column", "proportion"]

# Step 2: Create a horizontal bar graph using Plotly
fig = px.bar(missing_proportion, x="proportion", y="column", orientation="h")

# Customize the layout to remove additional elements and axis labels
fig.update_layout(
    title=None,
    xaxis=dict(
        range=[0, 1],
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
        title=None,
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
        title=None,
    ),
    showlegend=False,
    margin=dict(l=0, r=0, t=0, b=0),
)

fig


px_missing(demographics, "who")
