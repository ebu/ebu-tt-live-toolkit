.PHONY: docs

init:
	pip install --upgrade -r requirements.txt
	pyxbgen --binding-root=./ebu_tt_live/bindings -m __init__ --schema-root=./ebu_tt_live/xsd1.1/ -r -u ebutt_live.xsd
	npm install nunjucks
	node_modules/nunjucks/bin/precompile ebu_tt_live/ui/user_input_producer/template/user_input_producer_template.xml > ebu_tt_live/ui/user_input_producer/template/user_input_producer_template.js

make initnpm:
	npm install nunjucks

template:
	node_modules/nunjucks/bin/precompile ebu_tt_live/ui/user_input_producer/template/user_input_producer_template.xml > ebu_tt_live/ui/user_input_producer/template/user_input_producer_template.js

test:
	python setup.py test

docs:
	python setup.py build_sphinx
