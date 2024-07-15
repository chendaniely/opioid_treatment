# Introduction to public.ctn0094data: De-Identified Data from the CTN-0094 Protocol
# https://ctn-0094.github.io/public.ctn0094data/

# remotes::install_github("CTN-0094/public.ctn0094data")
# install.packages(c("readr", "public.ctn0094data"))

library(public.ctn0094data)
library(readr)

write_csv(public.ctn0094data::all_drugs, "data/all_drugs.csv")
write_csv(public.ctn0094data::asi, "data/asi.csv")
# no days dataset in package
write_csv(public.ctn0094data::demographics, "data/demographics.csv")
write_csv(public.ctn0094data::detox, "data/detox.csv")
write_csv(public.ctn0094data::everybody, "data/everybody.csv")
write_csv(public.ctn0094data::fagerstrom, "data/fagerstrom.csv")
write_csv(public.ctn0094data::first_survey, "data/first_survey.csv")
write_csv(public.ctn0094data::pain, "data/pain.csv")
write_csv(public.ctn0094data::psychiatric, "data/psychiatric.csv")
write_csv(public.ctn0094data::randomization, "data/randomization.csv")
write_csv(public.ctn0094data::rbs, "data/rbs.csv")
write_csv(public.ctn0094data::rbs_iv, "data/rbs_iv.csv")
write_csv(public.ctn0094data::screening_date, "data/screening_date.csv")
write_csv(public.ctn0094data::sex, "data/sex.csv")
write_csv(public.ctn0094data::tlfb, "data/tlfb.csv")
write_csv(public.ctn0094data::treatment, "data/treatment.csv")
write_csv(public.ctn0094data::uds, "data/uds.csv")
write_csv(public.ctn0094data::visit, "data/visit.csv")
write_csv(public.ctn0094data::withdrawal, "data/withdrawal.csv")
write_csv(public.ctn0094data::withdrawal_pre_post, "data/withdrawal_pre_post.csv")
