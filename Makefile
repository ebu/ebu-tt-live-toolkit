.PHONY: docs

init:
	pip install -r requirements.txt
	pyxbgen --binding-root=./ebu_tt_live/bindings -m __init__ --schema-root=./ebu_tt_live/xsd1.1/ -r -u ebutt_live.xsd

test:
	python setup.py test
