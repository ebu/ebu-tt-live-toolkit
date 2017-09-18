.PHONY: docs uiclean uibuild template initnpm uicopy

all: init ui
	
init:
	pip install --upgrade -r requirements.txt
	pyxbgen --binding-root=./ebu_tt_live/bindings -m __init__ --schema-root=./ebu_tt_live/xsd/ -r -u ebutt_all.xsd

initnpm:
ifeq ("$(wildcard node_modules)","")
	npm install nunjucks
else 
	npm update nunjucks
endif

test:
	python setup.py test

docs:
	python setup.py build_sphinx

bindings:
	pyxbgen --binding-root=./ebu_tt_live/bindings -m __init__ --schema-root=./ebu_tt_live/xsd/ -r -u ebutt_all.xsd

ui: uiclean uibuild
	
uiclean:
ifneq ("$(wildcard docs/build/ui/.)","")
	rm -R docs/build/ui
endif
	
uibuild: template uicopy
	
template: initnpm
	node_modules/nunjucks/bin/precompile ebu_tt_live/ui/user_input_producer/template/user_input_producer_template.xml > ebu_tt_live/ui/user_input_producer/template/user_input_producer_template.js
	node_modules/nunjucks/bin/precompile ebu_tt_live/ui/user_input_producer/template/live_message_template.xml > ebu_tt_live/ui/user_input_producer/template/live_message_template.js

uicopy:
	mkdir -p docs/build/ui
	cp -R ebu_tt_live/ui/user_input_producer docs/build/ui/
	cp -R ebu_tt_live/ui/test docs/build/ui/
	cp -R ebu_tt_live/ui/assets docs/build/ui/user_input_producer/
	cp -R ebu_tt_live/ui/assets docs/build/ui/test/
		
