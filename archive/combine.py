import pandas as pd
import plotnine as p9
from plotnine import ggplot, aes

import helper

data = helper.load_all()
locals().update(data)

# ctn-30 with the double randomization is causing an issue.
# so we'll remove those people with double 'which' values in the randomization
rand_which_2 = randomization.loc[randomization.which == 2, "who"].unique()
randomization1 = randomization.loc[~randomization.who.isin(rand_which_2)]
# check that the which value is only 1
assert (randomization1.which == 1).all()

# https://ctn-0094.github.io/public.ctn0094data/

# study and randomization

demo_rand = pd.merge(
    demographics,
    randomization,
    how="inner",  # keep only patients with randomization information,
    # there are 1068 "who"s with no randomization
    on=["who"],
)

demographics.shape
randomization.shape
demo_rand.shape

# treatment: The amount of drugs received on a day.
# Value is 1 for injections and mg otherwise

# treatment_ = treatment.loc[treatment.who == 3560]
# rand_ = randomization.loc[randomization.who == 3560]

# rand_treat_ = treatment_.merge(
#     rand_,
#     how = "inner",
#     on = ["who", "when"],
#     indicator=True
# )


rand1_treat = randomization1.merge(treatment, how="inner", on=["who"]).rename(
    columns={"when_x": "when_start", "when_y": "when"}
)

rand1_treat[rand1_treat.who == 3554]


treatment.shape
randomization1.shape
rand1_treat.shape


# self reported drug use
tlfb  # self reported drug use

tlfb1 = tlfb.loc[~tlfb.who.isin(rand_which_2)]


drug_what_when = tlfb1.groupby(["when", "what"]).count().reset_index()

drug_what_when.what.unique()

drug_usage_opioids = drug_what_when.loc[drug_what_when.what == "Opioid"]

drug_usage_opioids = drug_usage_opioids.merge(
    randomization1[["who", "treatment"]], on="who"
)


visit = visit.assign(
    has_reason_missed=lambda df_: df_.filter(like="is_")
    .notna()
    .any(axis="columns")
)

visit.what.value_counts(dropna=False)

visit_missed_counts = (
    visit.groupby(["who", "when", "has_reason_missed"])
    .size()
    .reset_index(name="count")
)

# there are 66 different types of "visit" types
visit.visit.value_counts()

# each person day and visit type has 1 value,
# 1 observation has 2 somewhere
visit.groupby(["who", "when", "visit"]).size().value_counts()

# demo_rand_treat_visit = demo_rand_treat.merge(
#     visit, how="outer", on=["who", "when"]
# )

# visit.shape
# demo_rand_treat_visit.shape

# demo_rand_treat_visit.columns

# make a dashboard showing the current patient visit and completions
visit

visit.is_no_note.value_counts()

visit.filter(like="is_", axis="columns").apply(lambda x: x.isna())

visit.filter(like="is_", axis="columns").isna().sum(axis=1)


visit.isnull().any(axis=1)


visit.has_reason_missed.value_counts()


# DASHBOARD -----

# value box showing percentage

total_visits = visit_missed_counts["count"].sum()
has_reason_missed = visit_missed_counts.loc[
    visit_missed_counts.has_reason_missed == True
]["count"].sum()

# pct of all visits with reason missed
pct_visit_missed_reason = has_reason_missed / total_visits

# self reported drug use for patents in the study of interest

(
    ggplot(drug_usage_opioids, aes(x="when", y="who", color="treatment"))
    + p9.geom_line()
    + p9.geom_vline(aes(xintercept=0))
    + p9.theme_bw()
)

import altair as alt

line = (
    alt.Chart(drug_usage_opioids)
    .mark_line()
    .encode(x="when", y="who", color="treatment", tooltip=["when", "who"])
)

# Create the vertical line at x=0
vertical_line = (
    alt.Chart(pd.DataFrame({"when": [0]}))
    .mark_rule(color="red")
    .encode(x="when:Q")
)

chart = line + vertical_line
chart.interactive()
chart.display()


# help with figuring out data order


demo_rand = pd.merge(
    demographics,
    randomization1,
    how="inner",  # keep only patients with randomization information,
    # there are 1068 "who"s with no randomization
    on=["who"],
)

demographics.shape
randomization.shape
demo_rand.shape

demo_rand_treat = pd.merge(
    demo_rand, treatment, how="inner", on=["who", "when"]
)
demo_rand_treat.shape

demo_rand_treat_visit = pd.merge(
    demo_rand_treat, visit, how="inner", on=["who", "when"]
)
demo_rand_treat_visit.shape


demo_rand_treat_visit_tlfb = pd.merge(
    demo_rand_treat_visit, tlfb, how="inner", on=["who", "when"]
)
