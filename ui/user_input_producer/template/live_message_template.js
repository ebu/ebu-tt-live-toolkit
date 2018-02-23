(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["ebu_tt_live/ui/user_input_producer/template/live_message_template.xml"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = null;
var colno = null;
var output = "";
try {
var parentTemplate = null;
output += "<?xml version=\"1.0\" ?>\n<ebuttlm:message\n        ebuttp:sequenceIdentifier=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "sequence_identifier"), env.opts.autoescape);
output += "\"\n        xmlns:ebuttp=\"urn:ebu:tt:parameters\"\n        xmlns:ebuttlm=\"urn:ebu:tt:livemessage\" >\n    <ebuttlm:header>\n      ";
if(runtime.contextOrFrameLookup(context, frame, "sender")) {
output += "\n        <ebuttlm:sender>";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "sender"), env.opts.autoescape);
output += "</ebuttlm:sender>\n      ";
;
}
output += "\n      ";
if(runtime.contextOrFrameLookup(context, frame, "recipient")) {
output += "\n      ";
frame = frame.push();
var t_3 = runtime.contextOrFrameLookup(context, frame, "recipient");
if(t_3) {t_3 = runtime.fromIterator(t_3);
var t_2 = t_3.length;
for(var t_1=0; t_1 < t_3.length; t_1++) {
var t_4 = t_3[t_1];
frame.set("item", t_4);
frame.set("loop.index", t_1 + 1);
frame.set("loop.index0", t_1);
frame.set("loop.revindex", t_2 - t_1);
frame.set("loop.revindex0", t_2 - t_1 - 1);
frame.set("loop.first", t_1 === 0);
frame.set("loop.last", t_1 === t_2 - 1);
frame.set("loop.length", t_2);
output += "\n        <ebuttlm:recipient>";
output += runtime.suppressValue(t_4, env.opts.autoescape);
output += "</ebuttlm:recipient>\n      ";
;
}
}
frame = frame.pop();
output += "\n      ";
;
}
output += "\n        <ebuttlm:type>authorsGroupControlRequest</ebuttlm:type>\n    </ebuttlm:header>\n    <ebuttlm:payload>";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "payload"), env.opts.autoescape);
output += "</ebuttlm:payload>\n</ebuttlm:message>";
if(parentTemplate) {
parentTemplate.rootRenderFunc(env, context, frame, runtime, cb);
} else {
cb(null, output);
}
;
} catch (e) {
  cb(runtime.handleError(e, lineno, colno));
}
}
return {
root: root
};

})();
})();

