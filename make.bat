@echo off
set HERE=%cd%

IF NOT EXIST %HERE%\env (
virtualenv env
)

REM Make sure we are in an active virtualenv
IF NOT DEFINED VIRTUAL_ENV (
call env\Scripts\activate
)

call pip install --upgrade -r requirements.txt

python %HERE%\env\Scripts\pyxbgen --binding-root=ebu_tt_live/bindings -m __init__ -r -u file:///%HERE%/ebu_tt_live/xsd1.1/ebutt_live.xsd

call npm install nunjucks
call node_modules/nunjucks/bin/precompile ebu_tt_live/ui/user_input_producer/template/user_input_producer_template.xml > ebu_tt_live/ui/user_input_producer/template/user_input_producer_template.js
