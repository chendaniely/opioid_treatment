<!-- text used in the application for the about tab-->

De-Identified data from the
[CTN-0094: Individual Level Predictive Modeling of Opioid Use Disorder Treatment Outcome](https://ctnlibrary.org/protocol/ctn0094/).
Original data source from:

<https://ctn-0094.github.io/public.ctn0094data/>

For reporting simplicity,
this application does not use patients from the second randomization.

## Datasets

The dataset descriptions can be found in the
[original data package repository](https://ctn-0094.github.io/public.ctn0094data/reference/index.html).
Not all data in the package is used in this application.

A quick description of the data used in this repository and select relevant column information (taken from data repository).

- `demographics`: Patient demographics
- `everybody`: Everybody with any data
    - `project`: CTN project number: 27, 30, 51
- `randomization`: Treatment randomization data. CTN-30 has two randomization events.
    - `treatment`: Prescribed treatment: Inpatient BUP, Inpatient NR-NTX, Methadone, Outpatient BUP, Outpatient BUP + EMM, Outpatient BUP + SMM
    - `which`: randomization indicator, has values 1 and 2 (for CTN-30)
- `tlfb`: Timeline flowback. Self-reported drug use.
    - Drugs grouped as opioids: Codeine, Fentanyl, Hydrocodone, Merperidine, Oxycodone, Oxymorphone, Propoxyphene
    - `what`: drug used: Alcohol, Amphetamine, Analgesic, Antibiotic, Antidepressant, Antiemetic, Antihistamine, Antipsychotic, Benadryl, Benzodiazepine, Buprenorphine, Caffeine, Cathinones, Clonidine, Cocaine, Dextromethorphan, Ghb, Hallucinogen, Heroin, Inhalant, K2, Kratom, Mdma/Hallucinogen, Methadone, Methylphenidate, Muscle Relaxant, Opioid, Pcp, Pseudoephedrine, Sedatives, THC, Unknown
- `treatment`: Amount of study drug per day
- `uds`: Urine drug screening.
    - `what`: Name of drug idemtified: Alcohol, Amphetamine, Benzodiazepine, Buprenorphine, Cocaine, Mdma/Hallucinogen, Methadone, Opioid, Sedatives, Thc
- `visit`: Patient planned visit data. Not all appointments were kept.
    - Contains indicators for known reasons for a missed appointment
