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

	make snapshot

@PHONY: snapshot
snapshot:
	pip freeze > requirements.txt
