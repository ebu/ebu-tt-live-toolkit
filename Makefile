.PHONY: docs

init:
	pip install --upgrade -r requirements.txt
	pyxbgen --binding-root=./ebu_tt_live/bindings -m __init__ --schema-root=./ebu_tt_live/xsd/ -r -u ebutt_all.xsd
ifeq ("$(wildcard node_modules)","")
	npm install nunjucks
else 
	npm update nunjucks
endif
	node_modules/nunjucks/bin/precompile ebu_tt_live/ui/user_input_producer/template/user_input_producer_template.xml > ebu_tt_live/ui/user_input_producer/template/user_input_producer_template.js

initnpm:
ifeq ("$(wildcard node_modules)","")
	npm install nunjucks
else 
	npm update nunjucks
endif

template:
	node_modules/nunjucks/bin/precompile ebu_tt_live/ui/user_input_producer/template/user_input_producer_template.xml > ebu_tt_live/ui/user_input_producer/template/user_input_producer_template.js

test:
	python setup.py test

docs:
	python setup.py build_sphinx
