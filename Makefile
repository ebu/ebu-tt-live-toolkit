.PHONY: docs

init:
	pip install --upgrade -r requirements.txt
	pyxbgen --binding-root=./ebu_tt_live/bindings/ebutt_live -m __init__ --schema-root=./ebu_tt_live/xsd/ebutt_live -r -u ebutt_live.xsd
	pyxbgen --binding-root=./ebu_tt_live/bindings/ebutt_d -m __init__ --schema-root=./ebu_tt_live/xsd/ebutt_d -r -u ebutt_d.xsd
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
