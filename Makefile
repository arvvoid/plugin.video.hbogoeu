# At the moment Kodi 18.x Leia is the stable release and and the code
# after operations will always return to those defaults.
# List of intended operations (most common):
#	make			    This will run all checks and create Zip for both Leia and Matrix
#	make test			Will run just test for Leia
#	make test-multi		Will run test for both Leia and Matrix
#	make test-light		Run just basic python sanity tests
#	make kodi-all		Will run Kodi add-on cheker for both Leia and Matrix
#	make kodi-leia		Will run Kodi add-on cheker for Leia
#	make kodi-matrix	Will run Kodi add-on cheker for Matrix
#	make zip			Will make zip for both Leia and Matrix
#	make zip-leia		Will make zip just for Leia
#	make zip-matrix		Will make zip just for Matrix
#	make git-zip		Will make zip from last commit
#	make abi-leia		Will edit addon.xml for Leia
#	make abi-matrix		Will edit addon.xml for Matrix
#	make test-language-sync		Will check if language files are in sync
#	make test-language-maintained	Will inform of status of translations
#
#	This can both be used localy or from CI (Travis, GitHub Actions, ecc...)
#	make sure all dependency are installed
#
#	Depending on the system used you need to install
#	libxml2-utils    (on Ubuntu/Debian sudo apt -y install libxml2-utils)
#	gettext			 (on Ubuntu/Debian sudo apt -y install gettext)
#	python -m pip install --upgrade pip
#	python -m pip install --upgrade pip
#	pip install -r requirements.txt
#	pip install kodi-addon-checker
#

addon_xml := addon.xml
TRANSLATION_DIR = ./resources/language/
TRANSLATION_POT = ./resources//language/resource.language.en_gb/strings.po

# Collect information
name = $(shell xmllint --xpath 'string(/addon/@id)' $(addon_xml))
name_for_show = $(shell xmllint --xpath 'string(/addon/@name)' $(addon_xml))
provider = $(shell xmllint --xpath 'string(/addon/@provider-name)' $(addon_xml))
provider_srch := $(subst +,\+,$(provider))
version = $(shell xmllint --xpath 'string(/addon/@version)' $(addon_xml))
version := $(subst +matrix.1,,$(version))
version_matrix := $(version)+matrix.1
version_matrix_srch := $(version)\+matrix.1
date_time_str = $(shell date +"%Y_%m_%d_%H_%M_%S")
git_branch = $(shell git for-each-ref --format='%(objectname) %(refname:short)' refs/heads | awk "/^$$(git rev-parse HEAD)/ {print \$$2}")
git_hash = $(shell git rev-parse --short HEAD)
zip_file_o = $(name)-$(git_branch)-$(git_hash).zip

zip_name_leia = $(name)-$(version)-leia.zip
zip_name_matrix = $(name)-$(version)-matrix.zip
include_files = main.py addon.xml LICENSE.txt README.md resources/ hbogolib/ libs/
include_paths = $(patsubst %,$(name)/%,$(include_files))
zip_dir = $(name)/

all: clean test-multi zip

clean:
	@find . -name '*.pyc' -type f -delete
	@find . -name '*.pyo' -type f -delete
	@find . -name __pycache__ -type d -delete
	@find . -name '.DS_Store' -type f -delete
	-@rm -rf .pytest_cache/ .tox/
	-@rm -f *.log
	-@rm -f *.zip
	@echo "Cleaning done..."

test: sanity

test-multi: sanity-multi

sanity: flake8 mypy kodi

test-light: flake8 mypy

sanity-multi: flake8 mypy kodi-all

abi-leia: clean
	@echo "Switch version and xbmc.python to Leia"
	@perl -i -pe's/<addon id=\"$(name)\" name=\"$(name_for_show)\" provider-name=\"$(provider_srch)\" version=\"$(version_matrix_srch)\">/<addon id=\"$(name)\" name=\"$(name_for_show)\" provider-name=\"$(provider)\" version=\"$(version)\">/g' addon.xml
	@perl -i -pe's/<import addon=\"xbmc.python\" version=\"3.0.0\" \/>/<import addon=\"xbmc.python\" version=\"2.26.0\" \/>/g' addon.xml

abi-matrix: clean
	@echo "Switch version and xbmc.python to Matrix"
	@perl -i -pe's/<addon id=\"$(name)\" name=\"$(name_for_show)\" provider-name=\"$(provider_srch)\" version=\"$(version)\">/<addon id=\"$(name)\" name=\"$(name_for_show)" provider-name=\"$(provider)\" version=\"$(version_matrix)\">/g' addon.xml
	@perl -i -pe's/<import addon=\"xbmc.python\" version=\"2.26.0\" \/>/<import addon=\"xbmc.python\" version=\"3.0.0\" \/>/g' addon.xml

flake8:
	@echo "Starting flake8 test"
	@flake8 . --ignore E501,N801,N802,N803,N806 --statistics --count

mypy:
	@echo "Starting mypy test"
	@mypy --no-incremental --cache-dir=/dev/null .

kodi: kodi-leia

kodi-leia: abi-leia
	@echo "Starting official kodi-addon-checker for Leia ($(git_hash))"
	@kodi-addon-checker --branch=leia
	-@rm -f *.log

kodi-matrix: abi-matrix
	@echo "Starting official kodi-addon-checker for matrix on branch $(git_branch) ($(git_hash))"
	@kodi-addon-checker --branch=matrix
	-@rm -f *.log
	@echo "Switch version and xbmc.python to Leia"
	@perl -i -pe's/<addon id=\"$(name)\" name=\"$(name_for_show)\" provider-name=\"$(provider_srch)\" version=\"$(version_matrix_srch)\">/<addon id=\"$(name)\" name=\"$(name_for_show)\" provider-name=\"$(provider)\" version=\"$(version)\">/g' addon.xml
	@perl -i -pe's/<import addon=\"xbmc.python\" version=\"3.0.0\" \/>/<import addon=\"xbmc.python\" version=\"2.26.0\" \/>/g' addon.xml

kodi-all: kodi-leia kodi-matrix

test-language-sync:
	@echo "Test if all language files are sync properly"
	@for f in $(shell ls ${TRANSLATION_DIR} -I "*.en_gb"); do echo "TESTING $${f}:";msgcmp --use-fuzzy --use-untranslated ${TRANSLATION_DIR}$${f}/strings.po ${TRANSLATION_POT};if [ $$? -eq 0 ]; then echo " OK\n"; else exit 1; fi done

test-language-maintained:
	@echo "Test all maintained language files, INFORMATIVE: "
	-@for f in $(shell ls ${TRANSLATION_DIR} -I "*.en_gb"); do echo "TESTING $${f}:";msgcmp ${TRANSLATION_DIR}$${f}/strings.po ${TRANSLATION_POT};if [ $$? -eq 0 ]; then echo " OK\n"; else echo "\n"; fi done
	@echo "Done."

zip: zip-leia zip-matrix
	@echo "Made Kodi add-on ZIPs: $(zip_name_leia) and $(zip_name_matrix) from $(git_branch) ($(git_hash))..."

zip-leia: abi-leia
	@cd ..; zip -r $(zip_name_leia) $(include_paths)

zip-matrix: abi-matrix
	@cd ..; zip -r $(zip_name_matrix) $(include_paths)
	@echo "Switch version and xbmc.python to Leia"
	@perl -i -pe's/<addon id=\"$(name)\" name=\"$(name_for_show)\" provider-name=\"$(provider_srch)\" version=\"$(version_matrix_srch)\">/<addon id=\"$(name)\" name=\"$(name_for_show)\" provider-name=\"$(provider)\" version=\"$(version)\">/g' addon.xml
	@perl -i -pe's/<import addon=\"xbmc.python\" version=\"3.0.0\" \/>/<import addon=\"xbmc.python\" version=\"2.26.0\" \/>/g' addon.xml

git-zip: clean
	@echo "Building Kodi add-on ZIP from last commit on branch $(git_branch) ($(git_hash)): $(zip_file_o)"
	@git archive -v --format zip --prefix=$(name)/ --worktree-attributes -9 -o ../$(zip_file_o) HEAD
	@echo "Done."