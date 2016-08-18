User input producer
===================

The user input producer is composed of a user interface written in javascript, the user interface is defined in the file `ebu_tt_live/ui/user_input_producer/user_input_producer.html`. It works with Javascript, JQuery_ and nunjucks_.

Demo
----

To test the user input producer, setup the environment as indicated in the `README.md` file at the root of the project. Then launch the ``ebu-user-input-consumer`` script and open the `ui/user_input_producer/user_input_producer.html` file in your browser. Click on the ``Connect`` button on the HTML page; the default URL should work: if you changed it in the `ebu_tt_live/script/ebu-user-input-consumer.py` file, then enter your custom URL, just be careful that the carriage uses websocket. If you have not already created a sequence, then create one with the corresponding button, set its options and select it in the dropdown box that allows you to choose a sequence identifier. 

There are three ways of sending documents :
    * `Send document on click on "Send" button` will issue a new document each time you clik the "Send" button.
    * `Send document on scheduled time` replaces the "Send" button by an input box and a "Schedule" button. You have two options, using a "local" clock, which is the time of your computer or using a "media" clock, which is a clock starting at `00:00:00.0` when you click on "Synchronize" button. Times have to be entered using `hh:mm:ss` format in the "Scheduled time" input. When you click on "Schedule" the current document state is set to be sent at the given time. You can now change any field to schedule a new document without waiting.
    * `Send documents asynchronously` will send a new document every `x` seconds, taking your modifications on-the-go.

You can type subtitle's text in the `Subtitles text` box. Each time a new document is being sent it should be logged by the ``ebu-user-input-consumer`` script.

.. _JQuery: https://jquery.com/
.. _nunjucks: https://mozilla.github.io/nunjucks/


