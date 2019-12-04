(function() {(window.nunjucksPrecompiled = window.nunjucksPrecompiled || {})["ebu_tt_live/ui/user_input_producer/template/user_input_producer_template.xml"] = (function() {
function root(env, context, frame, runtime, cb) {
var lineno = 0;
var colno = 0;
var output = "";
try {
var parentTemplate = null;
output += "<?xml version=\"1.0\" ?>\n<tt:tt\n        ebuttp:sequenceIdentifier=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "sequence_identifier"), env.opts.autoescape);
output += "\"\n        ebuttp:sequenceNumber=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "sequence_number"), env.opts.autoescape);
output += "\"\n        ttp:timeBase=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "time_base"), env.opts.autoescape);
output += "\"\n      ";
if(runtime.contextOrFrameLookup(context, frame, "clock_mode")) {
output += "\n        ttp:clockMode=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "clock_mode"), env.opts.autoescape);
output += "\"\n      ";
;
}
output += "\n      ";
if(runtime.contextOrFrameLookup(context, frame, "time_base") == "smpte") {
output += "\n        ttp:frameRate=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "frame_rate"), env.opts.autoescape);
output += "\"\n        ttp:frameRateMultiplier=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "frm_numerator"), env.opts.autoescape);
output += " ";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "frm_denominator"), env.opts.autoescape);
output += "\"\n        ttp:markerMode=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "marker_mode"), env.opts.autoescape);
output += "\"\n        ttp:dropMode=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "drop_mode"), env.opts.autoescape);
output += "\"\n      ";
;
}
output += "\n      ";
if(runtime.contextOrFrameLookup(context, frame, "authors_group_identifier")) {
output += "\n        ebuttp:authorsGroupIdentifier=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "authors_group_identifier"), env.opts.autoescape);
output += "\"\n      ";
;
}
output += "\n      ";
if(runtime.contextOrFrameLookup(context, frame, "authors_group_control_token")) {
output += "\n        ebuttp:authorsGroupControlToken=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "authors_group_control_token"), env.opts.autoescape);
output += "\"\n      ";
;
}
output += "\n        xml:lang=\"en-GB\"\n        xmlns:ebuttm=\"urn:ebu:tt:metadata\"\n        xmlns:ebuttp=\"urn:ebu:tt:parameters\"\n        xmlns:ebutts=\"urn:ebu:tt:style\"\n        xmlns:tt=\"http://www.w3.org/ns/ttml\"\n        xmlns:tts=\"http://www.w3.org/ns/ttml#styling\"\n        xmlns:ttp=\"http://www.w3.org/ns/ttml#parameter\"\n        xmlns:xml=\"http://www.w3.org/XML/1998/namespace\">\n  <tt:head>\n    <tt:metadata>\n      <ebuttm:documentMetadata/>\n    </tt:metadata>\n    <tt:styling>\n      <tt:style xml:id=\"styleP\" tts:color=\"rgb(255, 255, 255)\"  ebutts:linePadding=\"0.5c\" tts:fontFamily=\"sansSerif\" />\n      <tt:style xml:id=\"styleSpan\" tts:backgroundColor=\"rgb(0, 0, 0)\"/>\n    </tt:styling>\n    <tt:layout>\n      <tt:region xml:id=\"bottomRegion\" tts:origin=\"14.375% 60%\" tts:extent=\"71.25% 24%\" tts:displayAlign=\"after\" tts:writingMode=\"lrtb\" tts:overflow=\"visible\" />\n    </tt:layout>\n  </tt:head>\n  <tt:body\n  ";
if(runtime.contextOrFrameLookup(context, frame, "body_begin")) {
output += "\n    begin=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "body_begin"), env.opts.autoescape);
output += "\"\n  ";
;
}
output += "\n  ";
if(runtime.contextOrFrameLookup(context, frame, "body_end")) {
output += "\n    end=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "body_end"), env.opts.autoescape);
output += "\"\n  ";
;
}
output += "\n  ";
if(runtime.contextOrFrameLookup(context, frame, "dur")) {
output += "\n    dur=\"";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "dur"), env.opts.autoescape);
output += "\"\n  ";
;
}
output += "\n  >\n    <tt:div region=\"bottomRegion\">\n      <tt:p xml:id=\"p1\" style=\"styleP\"><tt:span style=\"styleSpan\">";
output += runtime.suppressValue(runtime.contextOrFrameLookup(context, frame, "body_content"), env.opts.autoescape);
output += "</tt:span></tt:p>\n    </tt:div>\n  </tt:body>\n</tt:tt>\n";
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

