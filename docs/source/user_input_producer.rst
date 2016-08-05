User input producer
===================

The user input producer is composed of a user interface written in javascript, the user interface is defined in the file `ebu_tt_live/ui/user_input_producer/user_input_producer.html`. It works with Javascript, JQuery_ and nunjucks_.

Demo
----

To test the user input producer, setup the environment as indicated in the `README.md` file at the root of the project. Then launch the ``ebu-user-input-consumer`` script and open the `ui/user_input_producer/user_input_producer.html` file in your browser. Click on the ``Connect`` button on the HTML page; the default URL should work: if you changed it in the `ebu_tt_live/script/ebu-user-input-consumer.py` file, then enter your custom URL, just be careful that the carriage uses websocket. If you have not already created a sequence then create one with the corresponding button and select it in the dropdown box that allows you to choose a sequence identifier. Then setup the options as you want and start typing text in the `Subtitle content` box. Each time you click the `Submit` button you should see a new document being sent with the text in the edit box, which is received and logged in the terminal running the ``ebu-user-input-consumer`` script.

.. _JQuery: https://jquery.com/
.. _nunjucks: https://mozilla.github.io/nunjucks/


