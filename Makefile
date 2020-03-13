addon_xml := addon.xml
export CDPATH=.

# Collect information to build as sensible package name
name = $(shell xmllint --xpath 'string(/addon/@id)' $(addon_xml))
version = $(shell xmllint --xpath 'string(/addon/@version)' $(addon_xml))
date_time_str = $(shell date +"%Y_%m_%d_%H_%M_%S")
git_branch = $(shell git rev-parse --abbrev-ref HEAD)
git_hash = $(shell git rev-parse --short HEAD)
zip_file_o = $(name)-$(git_branch)-$(git_hash).zip

zip_name_leia = $(name)-$(version)-leia.zip
zip_name_matrix = $(name)-$(version)-matrix.zip
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
	@echo "Starting official kodi-addon-checker for both leia and matrix+"
	# make sure the ABI is set for leia
	@perl -i -pe's/<import addon=\"xbmc.python\" version=\"3.0.0\" \/>/<import addon=\"xbmc.python\" version=\"2.26.0\" \/>/g' addon.xml
	@kodi-addon-checker --branch=leia
	@rm -f *.log
	#switch to ABI 3
	@perl -i -pe's/<import addon=\"xbmc.python\" version=\"2.26.0\" \/>/<import addon=\"xbmc.python\" version=\"3.0.0\" \/>/g' addon.xml
	@kodi-addon-checker --branch=matrix
	@rm -f *.log
	# switch back to 2.75 ABI
	@perl -i -pe's/<import addon=\"xbmc.python\" version=\"3.0.0\" \/>/<import addon=\"xbmc.python\" version=\"2.26.0\" \/>/g' addon.xml


zip: clean
	@echo "Building Kodi add-on ZIPs: $(zip_name)..."
	@rm -f *.zip
	@perl -i -pe's/<import addon=\"xbmc.python\" version=\"3.0.0\" \/>/<import addon=\"xbmc.python\" version=\"2.26.0\" \/>/g' addon.xml
	cd ..; zip -r $(zip_name_leia) $(include_paths)
	@perl -i -pe's/<import addon=\"xbmc.python\" version=\"2.26.0\" \/>/<import addon=\"xbmc.python\" version=\"3.0.0\" \/>/g' addon.xml
	cd ..; zip -r $(zip_name_matrix) $(include_paths)
	@perl -i -pe's/<import addon=\"xbmc.python\" version=\"3.0.0\" \/>/<import addon=\"xbmc.python\" version=\"2.26.0\" \/>/g' addon.xml
	@echo "Done."

git-zip: clean
	@echo "Building Kodi add-on ZIP from last commit on branch $(git_branch): $(zip_file_o)"
	@git archive -v --format zip --prefix=$(name)/ --worktree-attributes -9 -o ../$(zip_file_o) HEAD
	@echo "Done."

abi-leia: clean
	@perl -i -pe's/<import addon=\"xbmc.python\" version=\"3.0.0\" \/>/<import addon=\"xbmc.python\" version=\"2.26.0\" \/>/g' addon.xml

abi-matrix: clean
	@perl -i -pe's/<import addon=\"xbmc.python\" version=\"2.26.0\" \/>/<import addon=\"xbmc.python\" version=\"3.0.0\" \/>/g' addon.xml
