$(document).ready(function() {

    var sequence_numbers = {};
    var all_sequences = {};
    var interval_send = null;
    var scheduled_send_media_clock_offset = null;
    var interval_running_clock = null;

    if (typeof(Storage) === "undefined") {
        window.alert("You are using an old browser that does not allow to save data between session. Do not reload this page or you will lose your defined sequences.");
    }


    // Get data from local storage if it exists (we retain some data, like existing sequences and sequence numbers
    // on page reload. Also works when the browser is closed and reopened.
    if (localStorage.sequence_selector) {
        $("#sequence-selector").html(localStorage.sequence_selector);
    }
    if (localStorage.all_sequences) {
        all_sequences = JSON.parse(localStorage.all_sequences);
    }
    if (localStorage.sequence_numbers) {
        sequence_numbers = JSON.parse(localStorage.sequence_numbers);
    }


    /********************************************************** Options to show or not depending on other options and general purpose functions****************************/

    function stopResetRunningClock() {
        //$("#running-clock").empty();
        if (interval_running_clock != null) {
            clearInterval(interval_running_clock);
            interval_running_clock = null;
        }
    }

// NOTE: Some of the code below includes handling of SMPTE time base, which was removed from version 1.0 of the specification.

    function handleTimeBaseDependingOptions() {
        var selected_time_base = $("#time-base-selector").val();
        if (selected_time_base == "clock") {
            $("#clock-mode-span").show();
            $("#smpte-attributes-span").hide();
        } else if (selected_time_base == "smpte") {
            $("#clock-mode-span").hide();
            $("#smpte-attributes-span").show();
        } else {
            $("#clock-mode-span").hide();
            $("#smpte-attributes-span").hide();
        }
    }

    handleTimeBaseDependingOptions();

    function handleSequenceSelected() {
        var sequence_identifier = $("#sequence-selector").val();
          if (sequence_identifier) {
            if (all_sequences[sequence_identifier]) {
              var authors_group_control_token = all_sequences[sequence_identifier]["authors_group_control_token"];
              if (authors_group_control_token) {
                  $("#ag-token-input").html(authors_group_control_token);
              } else {
                  $("#ag-token-input").empty();
              }
            }
            else {
              // Sometimes we find that an invalid sequence identifier was
              // selected, so let's fix that...
              $("#ag-token-input").empty();
              $("#sequence-selector").empty();
            }
          }
    }

    handleSequenceSelected();

    function handleSendingTypeDependingOptions() {
        var sending_type = $("input[name=sending-type-radio-input]:checked").val();
        if (sending_type == "scheduled_send") {
            $("#scheduled-time-span").show();
            $("#scheduled-send-setup-div").show();
            $("#asynchronous-send-setup-div").hide();
            $("#running-clock").show();
            $("#submit-subtitle-button").hide();
            $("#schedule-subtitle-button").show();
        } else if (sending_type == "asynchronous_send") {
            $("#scheduled-time-span").hide();
            $("#scheduled-send-setup-div").hide();
            $("#asynchronous-send-setup-div").show();
            $("#submit-subtitle-button").hide();
            $("#schedule-subtitle-button").hide();
            stopResetRunningClock();
        } else {
            $("#scheduled-time-span").hide();
            $("#scheduled-send-setup-div").hide();
            $("#asynchronous-send-setup-div").hide();
            $("#schedule-subtitle-button").hide();
            $("#submit-subtitle-button").show();
            stopResetRunningClock();
        }
    }

    handleSendingTypeDependingOptions();


    function handleScheduledSendSetupDependingOptions() {
        var selected_clock_type = $("#scheduled-send-clock-selector").val();
        stopResetRunningClock();
        if (selected_clock_type == "local") {
            $("#synchronize-media-clock-button").hide();
            $('#running-clock').show();
            $('#running-clock-media').hide();
            interval_running_clock = setInterval(updateRunningClockLocal, 500);
        } else {
            $("#synchronize-media-clock-button").show();
        }
    }

    handleScheduledSendSetupDependingOptions();

    function updateRunningClockMedia() {
      var diff = moment().diff(scheduled_send_media_clock_offset);
      var offset = moment(diff).format('HH:mm:ss');

      $('#running-clock-media').html(offset);
      setTimeout(updateRunningClockMedia, 500);
    }

    function updateRunningClockLocal() {
      var time = moment().format('HH:mm:ss');

      $('#running-clock').html(time);
      setTimeout(updateRunningClockLocal, 500);
    }

    /************************************************** Helper functions ******************************************/
    function notifyError(element, notification, fade_out) {
        element.css("color", "red");
        element.text(notification);
        if (fade_out)
        setTimeout(function() {
            element.text("");
        }, 3000);
    }

    function notifyWarning(element, notification, fade_out) {
        element.css("color", "orange");
        element.text(notification);
        if (fade_out)
        setTimeout(function() {
            element.text("");
        }, 3000);
    }

    function notifySuccess(element, notification, fade_out) {
        element.css("color", "green");
        element.text(notification);
        if (fade_out)
        setTimeout(function() {
            element.text("");
        }, 3000);
    }

    function hideNewSequenceDiv() {
        $("#new-sequence-div").hide();
        $("#create-new-sequence-button").show();
        // Clear input on cancel
        $("#new-sequence-identifier-input").val("");
        $("#new-sequence-notification-span").text("");
    }

    function createMessageListItem(message) {
        var clonedElement = $('#result-list .message-item-template').clone();
        clonedElement.find('.sender-value').text(
            message.getElementsByTagNameNS(
                'urn:ebu:tt:livemessage', 'header'
            )[0].getElementsByTagNameNS(
                'urn:ebu:tt:livemessage', 'sender'
            )[0].firstChild.nodeValue
        );
        clonedElement.find('.payload').text(
          message.getElementsByTagNameNS(
            'urn:ebu:tt:livemessage', 'payload'
          )[0].firstChild.nodeValue
        );

        clonedElement.removeClass('message-item-template');
        clonedElement.addClass('result-list-item');

        return clonedElement;
    }

    function createDocumentListItem(tt) {
        /* Clone template list item and fill in the details */
        var clonedElement = $('#result-list .doc-item-template').clone();
        clonedElement.find('.seqNum-value').text(
            tt.getAttributeNS('urn:ebu:tt:parameters', 'sequenceNumber')
        );
        clonedElement.find('.autGID-value').text(
            tt.getAttributeNS('urn:ebu:tt:parameters', 'authorsGroupIdentifier')
        );
        clonedElement.find('.autGCT-value').text(
            tt.getAttributeNS('urn:ebu:tt:parameters', 'authorsGroupControlToken')
        );
        clonedElement.removeClass('doc-item-template');
        clonedElement.addClass('result-list-item');

        return clonedElement;
    }

    function checkOnAir(tt) {
        if(tt.getAttributeNS(
            'urn:ebu:tt:metadata', 'authorsGroupSelectedSequenceIdentifier'
        ) == $("#sequence-selector").val()) {
            $('#on-air-span').addClass('selected');
        } else {
            $('#on-air-span').removeClass('selected');
        }
    }

    function createListItem(xmldata) {
        /* Parse XML to extract important handover information */
        var parser = new DOMParser();
        var parsedXml = parser.parseFromString(xmldata, "text/xml");
        var item = parsedXml.documentElement;
        var clonedElement = '';

        // Create 2 different list item types
        if (item.namespaceURI != 'urn:ebu:tt:livemessage') {
            clonedElement = createDocumentListItem(item);
            checkOnAir(item);
        } else {
            clonedElement = createMessageListItem(item);
        }

        clonedElement.data('xml', xmldata);

        $('#result-list').append(clonedElement);

        /* if over 10 items discard the oldest */
        $('#result-list .result-list-item').slice(0, -10).remove();
    }

    /******************************************* Websocket logic ***********************************************/

    var socket = {
        connected: false
    };

    function websocketOnError(e) {
        notifyError($("#websocket-notifications-span"), "Error: cannot connect to websocket server.", false);
        socket.connected = false;
        socket.websocket = null;
        $("#websocket-connect-button").show();
        $("#websocket-disconnect-button").hide();
    }

    function websocketOnOpen(e) {
        notifySuccess($("#websocket-notifications-span"), "Connected to websocket server", false);
        socket.connected = true;
        $("#websocket-connect-button").hide();
        $("#websocket-disconnect-button").show();
        socket.websocket.onclose = websocketOnClose;
    }

    function websocketOnClose(e) {
        notifyWarning($("#websocket-notifications-span"), "Connection to websocket server closed.", false);
        socket.connected = false;
        socket.websocket = null;
        $("#websocket-connect-button").show();
        $("#websocket-disconnect-button").hide();
    }

    function websocketOnMessage(e) {
        // We are not expecting any messages back - close the connection!
        socket.websocket.close();

        notifyError($('#subtitle-form-notification-div'), "Unexpected message from server!", false);
    }

    /* This part is the result monitoring connection */
    var subscribeSocket = {
        connected: false
    };

    function subWebsocketOnError(e) {

    }

    function subWebsocketOnOpen(e) {
        subscribeSocket.connected = true;
        subscribeSocket.websocket.onclose = subWebsocketOnClose;
        $('#subscribe-websocket-connect-button').text('Disconnect');
    }

    function subWebsocketOnMessage(e) {
        createListItem(e.data);
    }

    function subWebsocketOnClose(e) {
        subscribeSocket.connected = false;
        subscribeSocket.websocket = null;
        $('#subscribe-websocket-connect-button').text('Connect');
    }

    function connectResultFeed() {
        var sub_websocket_url = $("#subscribe-host-input").val() + "/" + fixedEncodeURIComponent($('#subscribe-sequence-input').val()) + "/subscribe";

        subscribeSocket.websocket = new WebSocket(sub_websocket_url);
        subscribeSocket.websocket.onerror = subWebsocketOnError;
        subscribeSocket.websocket.onopen = subWebsocketOnOpen;
        subscribeSocket.websocket.onmessage = subWebsocketOnMessage;
    }

    function disconnectResultFeed() {
        subscribeSocket.websocket.close();
    }



    /******************************************************** Page elements logic ***************************************/
    // Toggle the display of the form to create a new sequence.
    $("#create-new-sequence-button").click(function() {
        if ($("#new-sequence-div").css("display") == "none") {
            $("#new-sequence-div").show();
            $("#create-new-sequence-button").hide();
        }
    });

    // Cancel the creation of a new sequence.
    $("#cancel-new-sequence-button").click(function() {
        if (!($("#new-sequence-div").css("display") == "none")) {
            hideNewSequenceDiv();
        }
    });

    // Create a new sequence
    $("#validate-new-sequence-button").click(function() {
        if ($("#new-sequence-identifier-input").val() == "") {
            notifyError($("#new-sequence-notification-span"), "The sequence identifier cannot be empty", false);
        } else {
            var sequence = {};
            var sequence_identifier = $("#new-sequence-identifier-input").val();
            var authors_group_identifier = $("#ag-identifier-input").val();

            $("#sequence-selector")
              .append($("<option></option>")
              .attr("value", sequence_identifier)
              .text(sequence_identifier));

            if (authors_group_identifier) {
                sequence["authors_group_identifier"] = authors_group_identifier;
            }

            var time_base = $("#time-base-selector").val();
            sequence["time_base"] = time_base;

            if (time_base == "clock") {
                sequence["clock_mode"] = $("#clock-mode-selector").val();
            } else if (time_base == "smpte") {
                sequence["frame_rate"] = $("#frame-rate-input").val();
                sequence["frm_numerator"] = $("#frm-numerator-input").val();
                sequence["frm_denominator"] = $("#frm-denominator-input").val();
                sequence["marker_mode"] = $("#marker-mode-selector").val();
                sequence["drop_mode"] = $("#drop-mode-selector").val();
            }
            all_sequences[sequence_identifier] = sequence;
            sequence_numbers[sequence_identifier] = 1;
            if (typeof(Storage) !== "undefined") {
                localStorage.sequence_selector = $("#sequence-selector").html();
                localStorage.all_sequences = JSON.stringify(all_sequences);
                localStorage.sequence_numbers = JSON.stringify(sequence_numbers);
            }
            hideNewSequenceDiv();
            notifySuccess($("#new-sequence-notification-span"), "New sequence created", true);
        }
    });

    // Reset the whole page
    $("#reset-all").click(function() {
        $("#sequence-selector").html("");
        if (typeof(Storage) !== "undefined") {
            $("#subtitle-form-notification-div").text("");
            localStorage.clear();
            sequence_numbers = {};
            all_sequences = {};
        }
    });

    // Encoding function from https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent
    function fixedEncodeURIComponent(str) {
        return encodeURIComponent(str).replace(/[!'()*]/g, function(c) {
            return '%' + c.charCodeAt(0).toString(16);
        });
    }

    // websocket connection
    $("#websocket-connect-button").click(function() {
        if (socket.connected == false) {
            var websocket_url = $("#websocket-url-input").val() + "/" + fixedEncodeURIComponent($('#sequence-selector').val()) + "/publish";
            //console.log("WebSocket URL: ", websocket_url);
            socket.websocket = new WebSocket(websocket_url);
            // onclose hook is not set yet because we need to know if the connection has been established
            // and to get an error if not. However if onclose is defined it is called instead of onerror.
            // So we define onclose in the onopen hook.
            socket.websocket.onerror = websocketOnError;
            socket.websocket.onopen = websocketOnOpen;
            socket.websocket.onmessage = websocketOnMessage;
        }
    });

    // websocket disconnection
    $("#websocket-disconnect-button").click(function() {
        if (socket.connected == true) {
            socket.websocket.close();
        }
    });

    $('#subscribe-websocket-connect-button').click(function() {
        if (!subscribeSocket.connected) {
            $('#subscribe-websocket-connect-button').text('Connecting...');
            connectResultFeed();
        } else {
            disconnectResultFeed();
        }
    });

    $("#time-base-selector").change(handleTimeBaseDependingOptions);

    $("#sequence-selector").change(handleSequenceSelected);

    $("input[name=sending-type-radio-input]").click(function() {
        if ($(this).is(':checked')) {
            handleSendingTypeDependingOptions();
        }
    });

    $("#scheduled-send-clock-selector").change(handleScheduledSendSetupDependingOptions);

    $("#synchronize-media-clock-button").click(function() {
        scheduled_send_media_clock_offset = moment();
        stopResetRunningClock();
        $('#running-clock').hide();
        $('#running-clock-media').show();
        interval_running_clock = setInterval(updateRunningClockMedia, 500);
        notifySuccess($("#scheduled-send-status-span"), "Synchronized", true);
    });

    $("#asynchronous-send-start-button").click(function() {
        if (!interval_send) {
            var interval = parseFloat($("#asynchronous-send-interval-input").val());
            if (isNaN(interval) || interval <= 0) {
                notifyError($("#asynchronous-send-status-span"), "Empty, non-number, negative and 0 values are not allowed", false);
                return;
            }
            interval_send = setInterval(asyncSubmit, interval * 1000);
            notifySuccess($("#asynchronous-send-status-span"), "Running...", false);
        }
    });

    $("#asynchronous-send-stop-button").click(function() {
        if (interval_send) {
            clearInterval(interval_send);
            interval_send = null;
            $("#asynchronous-send-status-span").text("");
        }
    });

    nunjucks.configure({
        autoescape: false
    });

    function createTemplateDict() {
        var template_data = {};

        sequence_identifier = $("#sequence-selector").val();
        template_data["sequence_identifier"] = sequence_identifier;
        template_data["sequence_number"] = sequence_numbers[sequence_identifier];

        var time_base = all_sequences[sequence_identifier]["time_base"];
        var authors_group_identifier = all_sequences[sequence_identifier]["authors_group_identifier"];
        var authors_group_control_token = $('#ag-token-input').val();
        template_data["time_base"] = time_base;

        if (time_base == "clock") {
            template_data["clock_mode"] = all_sequences[sequence_identifier]["clock_mode"];
        } else if (time_base == "smpte") {
            template_data["frame_rate"] = all_sequences[sequence_identifier]["frame_rate"];
            template_data["frm_numerator"] = all_sequences[sequence_identifier]["frm_numerator"];
            template_data["frm_denominator"] = all_sequences[sequence_identifier]["frm_denominator"];
            template_data["marker_mode"] = all_sequences[sequence_identifier]["marker_mode"];
            template_data["drop_mode"] = all_sequences[sequence_identifier]["drop_mode"];
        }
        if (authors_group_identifier) {
            template_data["authors_group_identifier"] = authors_group_identifier;
        }
        if (authors_group_control_token) {
            template_data["authors_group_control_token"] = authors_group_control_token;
        }
        template_data["body_content"] = $("#subtitle-content-textarea").val().replace(/\r?\n|\r/g, "<tt:br/>");
        template_data["body_begin"] = $("#body-begin-input").val();
        template_data["body_end"] = $("#body-end-input").val();
        template_data["dur"] = $("#dur-input").val();
        return template_data;
    }

    function createHandoverMessageTemplateDict(request_message) {
        var template_data = {}

        template_data['sender'] = $("#sequence-selector").val();  // TODO: Change this to something more sensible
        template_data['sequence_identifier'] = $("#sequence-selector").val();
        template_data['recipient'] = [];  // TODO: This is probably not needed but part of message header
        template_data['payload'] = request_message;

        return template_data;
    }

    function renderHandoverMessageTemplate(template_data) {
        var rendered_document = nunjucks.render(
          'template/live_message_template.xml',
          template_data
        );
        return rendered_document;
    }

    function sendHandoverMessage(message_obj) {
        if (socket.connected) {
            socket.websocket.send(
                message_obj
            );
            return true;
        }
        return false;
    }

    function computeScheduledSendTimeout(media_offset = null) {
        var timeout = 0;
        // if the media offset is not set we suppose that we are running in local clock mode.
        if (media_offset == null) {
            var scheduled_time = new Date(Date.now());
            scheduled_time_input = $("#scheduled-time-input").val();
            var scheduled_time_parsed = scheduled_time_input.match(/(\d\d):(\d\d):(\d\d)/);
            if (scheduled_time_parsed != null) {
              scheduled_time.setHours(scheduled_time_parsed[1]);
              scheduled_time.setMinutes(scheduled_time_parsed[2]);
              scheduled_time.setSeconds(scheduled_time_parsed[3]);
              timeout = scheduled_time.getTime() - Date.now();
            }
        } else { // media offset is not null
            var scheduled_time = new Date(0).getTime();
            scheduled_time_input = $("#scheduled-time-input").val();
            var scheduled_time_parsed = scheduled_time_input.match(/(\d\d):(\d\d):(\d\d)/);
            if (scheduled_time_parsed != null) {
              scheduled_time += parseInt(scheduled_time_parsed[1]) * 3600000;
              scheduled_time += parseInt(scheduled_time_parsed[2]) * 60000;
              scheduled_time += parseInt(scheduled_time_parsed[3]) * 1000;
              timeout = scheduled_send_media_clock_offset + scheduled_time;
              timeout = timeout - Date.now();
            }
        }
        return timeout;
    }

    function submitDocument() {
        var sending_type = $("input[name=sending-type-radio-input]:checked").val();

        if (sending_type == "scheduled_send") {
            /* If we are using sheduled time to send documents we must actually compute a timeout
            * value which is the difference between the scheduled time and the current time.
            */
            var media_offset = null;
            var scheduled_send_clock_type = $("#scheduled-send-clock-selector").val();
            if (scheduled_send_clock_type == "media") {
              media_offset = scheduled_send_media_clock_offset;
            }

            var timeout = computeScheduledSendTimeout(media_offset);
            var template_data = createTemplateDict();
            var rendered_document = nunjucks.render(
              'template/user_input_producer_template.xml',
              template_data
            );

            setTimeout(renderSendDocument, timeout, rendered_document);
            notifySuccess($("#scheduled-confirmation-span"), "Scheduled...", true);
            sequence_numbers[sequence_identifier] += 1;
        } else {
            renderSendDocument();
            sequence_numbers[sequence_identifier] += 1;
        }
        localStorage.sequence_numbers = JSON.stringify(sequence_numbers);
    }

    function asyncSubmit() {
        var template_data = createTemplateDict();
        var rendered_document = nunjucks.render('template/user_input_producer_template.xml', template_data);
        renderSendDocument(rendered_document);
        sequence_numbers[sequence_identifier] += 1;
        localStorage.sequence_numbers = JSON.stringify(sequence_numbers);
    }

    function renderSendDocument(doc = null) {
        var template_data = createTemplateDict();
        var rendered_document = null;
        // If doc in not null then it was already rendered (needed for scheduled times : the document
        // has to be rendered when the sending is scheduled not at effective sending time.
        if (doc == null) {
          rendered_document = nunjucks.render('template/user_input_producer_template.xml', template_data);
        } else {
          rendered_document = doc;
        }

        if (socket.websocket) {
          socket.websocket.send(rendered_document);
        } else {
          notifyError($("#subtitle-form-notification-div"), "Error: there is no connection to the websocket server !", false);
        }
    }

    function sendDocument() {
        var sequence_identifier = $("#sequence-selector").val();
        if (sequence_identifier == null) {
            notifyError($("#subtitle-form-notification-div"), "The sequence identifier cannot be undefined. Please create a new sequence.", false);
        } else {
            submitDocument();
        }
    }

    $("#submit-subtitle-button").click(sendDocument);


    // keyboard shortcut: Enter, space and escape send a document, escape also clears the text box.
    // Enter, space and escape send a document only in "Send button" mode.
    // Escape always clears. Enter removes previous lines according to the max-lines setting, after sending.
    // Not tested in Safari
    $("#subtitle-content-textarea").keydown(function(evt) {
        var keyCode = evt.which;
        var isSendButton = document.getElementById('radio_send').checked;
        if (isSendButton) {
            if (keyCode == 13 || keyCode == 32 || keyCode == 27) {
                sendDocument();
            }
        }
        if (keyCode == 27) {
            // Escape clears the text area
            document.getElementById('subtitle-content-textarea').value = "";
        }
        if (keyCode == 13) {
            // Enter removes first lines according to max-lines
            var max_lines = $("#max-lines").val();
            var new_text_arr = $("#subtitle-content-textarea").val().split(/\r?\n|\r/);
            while (new_text_arr.length >= max_lines) {
                new_text_arr.shift();
            };
            $("#subtitle-content-textarea").val(new_text_arr.join('\r\n'));
        }
    });

    // In the special case that max-lines is 1 clear the text area on Enter key up otherwise
    // an extra unwanted carriage return line feed pair is added at the beginning.
    $("#subtitle-content-textarea").keyup(function(evt) {
        if (evt.which == 13 && $("#max-lines").val() == 1) {
          document.getElementById('subtitle-content-textarea').value = "";
        }
    });

    // Workaround for jquery val() stripping out carriage returns from text areas
    $.valHooks.textarea = {
        get: function(elem) {
            return elem.value.replace(/\r?\n/g, "\r\n");
        }
    };

    $('#result-view-div').on('click', '#result-view-pre', function(e) {
        $('#result-list').show();
        $('#result-view-pre').hide();
    });

    $('#result-list').on('click', '.result-list-item', function(e) {
        $('#result-list').hide();
        $('#result-view-pre').text($(e.currentTarget).data('xml'));
        $('#result-view-pre').show();
    });

    $('#submit-ag-control-request-button').click(function(e) {
        var message = $('#ag-control-request-input').val();

        var success = sendHandoverMessage(
            renderHandoverMessageTemplate(
                createHandoverMessageTemplateDict(message)
            )
        );

        if (success) {
            $('#ag-control-request-input').val('');
        }
    });

    $('#ag-control-request-input').keydown(function(evt) {
        var keyCode = evt.which;
        if (keyCode == 13) {
            $("#submit-ag-control-request-button").trigger('click');
        }
    });
});
