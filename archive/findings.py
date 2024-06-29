import pandas as pd
import plotnine as p9
from plotnine import ggplot, aes
import seaborn as sns

import helper

data = helper.load_all()
locals().update(data)

# CTN-0027: Starting Treatment with Agonist Replacement Therapies (START)
# https://ctnlibrary.org/protocol/ctn0027/


# This study demonstrated no evidence of liver damage
# during the initial 6 months of treatment with either BUP or MET,
# providing further encouragement to physicians to use buprenorphine
# as an effective treatment option for opioid addiction.

# liver damage measured by transaminase levels

all_drugs
everybody

randomization
rbs
sex

# CTN-0030: Prescription Opiate Abuse Treatment Study (POATS)
# https://ctnlibrary.org/protocol/ctn0030/

# Prescription opioid–dependent patients are most likely to reduce opioid use
# during buprenorphine-naloxone treatment.
# However, if tapered off buprenorphine-naloxone,
# even after 12 weeks of treatment,
# the likelihood of an unsuccessful outcome is high,
# even in patients receiving counseling in addition to standard medical management.

all_drugs
detox
everybody
first_survey
randomization
rbs
screening_date
tlfb  # self reported drug use, who what when
treatment  # doses of study drug administed to each patient each day, injection is 1,else mg

uds  # urine drug screening, patient, drug, and study day detected


drug_what_when = tlfb.groupby(["when", "what"]).count().reset_index()

drug_what_when.what.unique()

drug_usage_opioids = drug_what_when.loc[drug_what_when.what == "Opioid"]

drug_usage_opioids = drug_usage_opioids.merge(
    randomization[["who", "treatment"]], on="who"
)

(
    ggplot(drug_usage_opioids, aes(x="when", y="who", color="treatment"))
    + p9.geom_line()
    + p9.geom_vline(aes(xintercept=0))
    + p9.xlim(drug_what_when.when.min(), 7 * (12 + 10))
)

# CTN-0051: Extended-Release Naltrexone vs. Buprenorphine for Opioid Treatment (X:BOT)
# https://ctnlibrary.org/protocol/ctn0051/

# Participants randomized to XR-NTX had a substantial induction hurdle:
# fewer successfully initiated XR-NTX than BUP-NX,
# resulting in a higher rate of 24-week relapse events for the XR-NTX group.
# Among participants successfully inducted to treatment,
# however, 24-week relapse events were similar across study groups.
# Self-reported opioid craving was initially less with XR-NTX than with BUP-NX (p=0.0012),
# then converged by week 24 (p=0.20).
# With the exception of mild-to-moderate XR-NTX injection site reactions,
# treatment-emergent adverse events including overdose
# did not differ between treatment groups.

# In this population,
# it is more difficult to initiate patients to XR-NTX than to BUP-NX,
# and this negatively affected overall relapse.
# However, once initiated, both medications were equally safe and effective.

randomization.treatment.value_counts()

randomization.loc[randomization.treatment.isin(["Inpatient NR-NTX", ""])]
