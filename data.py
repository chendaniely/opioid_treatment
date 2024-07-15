import math
from pathlib import Path
import subprocess

from great_tables import GT
import pandas as pd
from skimpy import skim
import skimpy as sk


def no_ctn30(data, who_ctn30):
    return data.loc[~data.who.isin(who_ctn30)]


def roundup(x):
    return math.ceil(x / 10.0) * 10


# run data code and call R, if needed

data_directory = Path("./data")
csv_files = list(data_directory.glob("*.csv"))
if not csv_files:
    try:
        print("RUNNING R CODE TO DOWNLOAD DATA")
        subprocess.run(["Rscript", "data/01-get_data.R"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the R script: {e}")
else:
    print("CSV files found in ./data")


# load data -----

randomization = pd.read_csv("data/randomization.csv")
everybody = pd.read_csv("data/everybody.csv")
treatment = pd.read_csv("data/treatment.csv")
uds = pd.read_csv("data/uds.csv")
tlfb = pd.read_csv("data/tlfb.csv")
visit = pd.read_csv("data/visit.csv")
demographics = pd.read_csv("data/demographics.csv")

# do not use the CTN-30 patient data with 2 randomization points

rand_which_2 = randomization.loc[randomization.which == 2, "who"].unique()

# subset data so we're not using any CTN-30 randomization 2 data-----

randomization = no_ctn30(randomization, rand_which_2)
assert (randomization.which == 1).all()

everybody = no_ctn30(everybody, rand_which_2)
treatment = no_ctn30(treatment, rand_which_2)
uds = no_ctn30(uds, rand_which_2)
tlfb = no_ctn30(tlfb, rand_which_2)
visit = no_ctn30(visit, rand_which_2)
demographics = no_ctn30(demographics, rand_which_2)

# process data -----


# data for drug use counts

drug_what_when = (
    tlfb.groupby(["when", "what"])["who"]
    .count()
    .reset_index()
    .rename(columns={"what": "drug", "who": "count"})
)

drug_randomization = tlfb.merge(
    randomization[["who", "treatment"]], on=["who"], how="outer"
)

total_drug_over_study = (
    drug_randomization.groupby(["when", "treatment", "what"])["who"]
    .count()
    .reset_index()
)

total_drug_over_study_opioids = total_drug_over_study.loc[
    total_drug_over_study.what == "Opioid"
]

# data for urine test drug use counts

urine_drug_usage = (
    uds.merge(randomization[["who", "treatment"]], on=["who"], how="outer")
    .groupby(["when", "treatment", "what"])["who"]
    .count()
    .reset_index()
)

urine_drug_usage_opioid = urine_drug_usage.loc[
    urine_drug_usage.what == "Opioid"
]

# visit and missing visit

visit = visit.assign(
    has_reason_missed=lambda df_: df_.filter(like="is_")
    .notna()
    .any(axis="columns")
)

# visit_missed_counts = (
#     visit.groupby(["who", "when", "has_reason_missed"])
#     .size()
#     .reset_index(name="count")
# )

# total_visits = visit_missed_counts["count"].sum()
# has_reason_missed = visit_missed_counts.loc[
#     visit_missed_counts.has_reason_missed == True
# ]["count"].sum()

# demo_everybody = demographics.merge(everybody, on="who")
# demo_everybody_stats = demo_everybody.groupby("project").agg("count").T

visit_miss_14 = visit[["who", "is_missing_14_consecutive"]]
visit_miss_14 = visit_miss_14.loc[
    ~visit_miss_14.is_missing_14_consecutive.isna()
]

num_visit_miss_14 = len(visit_miss_14.who.unique())

# Overview page values -----

patient_count = len(randomization.who.unique())

max_y_for_plot = (
    roundup(
        max(
            total_drug_over_study_opioids.who.max(),
            urine_drug_usage_opioid.who.max(),
        )
    )
    + 10
)

# great_table -----

drug_0_50_diff = (
    total_drug_over_study.loc[total_drug_over_study.when.isin([0, 50])]
    .pivot_table(index=["treatment", "what"], columns=["when"], values="who")
    .reset_index()
)
drug_0_50_diff.columns = drug_0_50_diff.columns.map(str)
drug_0_50_diff.columns.name = None

drug_0_50_diff = (
    drug_0_50_diff.assign(
        pct_change=lambda df_: (df_["50"] - df_["0"]) / df_["0"]
    )
    .sort_values(["pct_change", "treatment", "what"], axis="index")
    .reset_index(drop=True)
    .dropna()
    .drop(columns=["0", "50"])
    .rename(
        columns={
            "treatment": "Treatment",
            "what": "Drug",
            "pct_change": "Change",
        }
    )
)

gt = (
    GT(drug_0_50_diff)
    .fmt_percent(columns="Change", decimals=2)
    .tab_header(
        title="Percent Change in Self-Reported Drug Use",
        subtitle="Comparing Study Day 0 and Day 50",
    )
    .tab_source_note(
        source_note="Note: Not all drugs have a recording on day 50"
    )
)


# interactive filter data

data_choices = {
    "demographics": "Demographics",
    "everybody": "Everybody",
    "randomization": "Randomization",
    "treatment": "Treatment",
    "uds": "Urine Drug Screening Results",
    "tlfb": "Self-Reported Drug Use (tlfb)",
    "visit": "Visit",
}

data_dict = {
    "demographics": demographics,
    "everybody": everybody,
    "randomization": randomization,
    "treatment": treatment,
    "uds": uds,
    "visit": visit,
    "tlfb": tlfb,
}

merge_keys = {
    "demographics": ["who"],
    "everybody": ["who"],
    "randomization": ["who", "when"],
    "treatment": ["who", "when"],
    "visit": ["who", "when"],
    "uds": ["who", "when"],
    "tlfb": ["who", "when"],
}

desired_join_order = [
    "demographics",
    "everybody",
    "randomization",
    "treatment",
    "visit",
    "uds",
    "tlfb",
]

data_filter_options = {
    "demographics": demographics.columns.to_list(),
    "everybody": everybody.columns.to_list(),
    "randomization": randomization.columns.to_list(),
    "treatment": treatment.columns.to_list(),
    "uds": uds.columns.to_list(),
    "tlfb": tlfb.columns.to_list(),
    "visit": visit.columns.to_list(),
}

# About markdown data ----

with open("about.md", "r") as f:
    about_markdown = f.read()
