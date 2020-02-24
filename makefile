addon_xml := addon.xml

# Collect information to build as sensible package name
name = $(shell xmllint --xpath 'string(/addon/@id)' $(addon_xml))
version = $(shell xmllint --xpath 'string(/addon/@version)' $(addon_xml))
date_time_str = $(shell date +"%Y_%m_%d_%H_%M_%S")

zip_name = $(name)-$(version)-local-$(date_time_str).zip
include_files = main.py addon.xml LICENSE.txt README.md resources/ hbogolib/
include_paths = $(patsubst %,$(name)/%,$(include_files))
zip_dir = $(name)/

all: clean test zip

clean:
	@find . -name '*.pyc' -type f -delete
	@find . -name '*.pyo' -type f -delete
	@find . -name __pycache__ -type d -delete
	@find . -name '.DS_Store' -type f -delete
	@rm -rf .pytest_cache/ .tox/
	@rm -f *.log
	@rm -f *.zip
	@echo "Cleaning done..."

test: sanity

sanity: flake8 mypy kodi

flake8:
	@echo "Starting flake8 test"
	@flake8 . --ignore E501,N801,N802,N803,N806 --statistics --count

mypy:
	@echo "Starting mypy test"
	@mypy . --no-incremental --cache-dir=/dev/null

kodi: clean
	@echo "Starting official kodi-addon-checker"
	@kodi-addon-checker --branch=leia
	@rm -f *.log

zip: clean
	@echo "Building Kodi add-on ZIP: $(zip_name)..."
	@rm -f ../$(zip_name)
	cd ..; zip -r $(zip_name) $(include_paths)
	@echo "Done."
