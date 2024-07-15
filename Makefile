@PHONY: app
app:
	python -m shiny run --port 54321 --reload app.py
	# http://127.0.0.1:54321

@PHONY: setup
setup:
	pip freeze | xargs pip uninstall -y
	pip install prompt-toolkit==3.0.36 ipython==7.34.0 shiny shinyswatch ipykernel faicons pyarrow
	pip install pandas plotnine seaborn great_tables
	pip install shinywidgets plotly
	pip install rsconnect-python

	Rscript -e "install.packages(c('public.ctn0094data', 'readr'), repos = 'https://cloud.r-project.org/')"

	make snapshot

@PHONY: snapshot
snapshot:
	pip freeze > requirements.txt

@PHONY: setup_connect
setup_connect:
	rsconnect add \
		--api-key $(POSIT_TEAM_PUB_KEY) \
		--server $(POSIT_TEAM_PUB_SERVER) \
		--name demo_posit_team_connect

@PHONY: deploy
deploy:
	rsconnect deploy shiny -n demo_posit_team_connect ./

@PHONY: app_data
app_data:
	Rscript data/01-get_data.R
