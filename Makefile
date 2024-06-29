@PHONY: app
app:
	python -m shiny run --port 54321 --reload --reload-excludes skimpy.html app.py
	# http://127.0.0.1:54321

@PHONY: setup
setup:
	pip freeze | xargs pip uninstall -y
	pip install prompt-toolkit==3.0.36 ipython==7.34.0 shiny ipykernel faicons
	pip install pandas plotnine seaborn great_tables
	pip install altair shinywidgets plotly
	pip install skimpy

	Rscript -e "install.packages(c('public.ctn0094data', 'readr'), repos = 'https://cloud.r-project.org/')"

	make snapshot

@PHONY: snapshot
snapshot:
	pip freeze > requirements.txt

@PHONY: app_data
app_data:
	Rscript data/01-get_data.R
