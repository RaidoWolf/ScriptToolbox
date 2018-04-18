// ==UserScript==
// @name         TSI Notifier
// @namespace    com.vault86.tsinotifier
// @version      1.0.0
// @description  A script that routinely checks TSI for work, and notifies if any is available.
// @author       Alexander Barber <dangerbarber@gmail.com>
// @match        *://*.mytitlesourceconnection.com/Vendor/AppraiserQueue/*
// @grant        none
// ==/UserScript==

TSINOTIFIER_NOTIFICATION_REQUIRE_INTERACTION = true; //notifications stick around until closed
TSINOTIFIER_REFRESH_TIME = 5; //seconds to wait after refreshing without any luck
TSINOTIFIER_DEAD_TIME = 30; //seconds to wait after notifying about new jobs
TSINOTIFIER_CONTROLLER_HEIGHT = 2; //how many buttons tall can the controller be
TSINOTIFIER_CHECK_DELAY = 1; //how many seconds to wait after page load before checking for appraisals

/**
 * An object representing a notification
 * @param {string} title The title of the notification
 * @param {string} text  The body of the notification
 */
TsiNotifierNotification = function (title, text) {

    title = typeof title === 'string' ? title : 'Notification';
    text = typeof text === 'string' ? text : '';

    this.title = title;
    this.text = text;

};

TsiNotifierNotification.prototype.type = 'TsiNotifierNotification'; //this is to verify that the data is an instance of this class

/**
 * An object representing a button on the controller
 * @param {string}   text    The text to display on the button
 * @param {function} onclick The function to execute when the button is clicked
 */
TsiNotifierControllerButton = function (text, onclick) {

    text = typeof text === 'string' ? text : 'button';
    onclick = typeof onclick === 'function' ? onclick : function(){};

    this.text = text;
    this.onclick = onclick;

};

TsiNotifierControllerButton.prototype.type = 'TsiNotifierControllerButton'; //this is to verify that the data is an instance of this class

/**
 * An object representing the controller
 * @type {Object}
 */
TsiNotifierController = {

    columns: [],
    controllerWrapperSelector: '#tsinotifier-controller-wrapper',
    controllerSelector: '#tsinotifier-controller',

    /**
     * Initialize the controller
     * @return {boolean} True. It'll return true.
     */
    init: function () {

        // remove any existing controllers that may have been created
        $(TsiNotifierController.controllerWrapperSelector).remove();

        // append the wrapper element to the DOM
        $('body').append(
            '<div id="tsinotifier-controller-wrapper" style="position:fixed;top:0;left:80px;z-index:0118999;">' +
            '</div>'
        );

        return true;

    },

    /**
     * Add a button to the controller
     * @param {object} button An instance of TsiNotifierControllerButton
     */
    addButton: function (button) {

        // check if a new column needs to be added
        if (
            TsiNotifierController.columns.length === 0 ||
            TsiNotifierController.columns[TsiNotifierController.columns.length - 1].length >= TSINOTIFIER_CONTROLLER_HEIGHT
        ) {
            // add a new column
            TsiNotifierController.columns.push([]);
        }

        // append the button to the last column
        TsiNotifierController.columns[TsiNotifierController.columns.length - 1].push(button);

        // render the controller
        TsiNotifierController.render();

        return true;

    },

    /**
     * Render the controller and put it in the DOM
     * @return {object} An instance of a jQuery element representing the controller table
     */
    render: function () {

        // create a new controller table
        var controller = '<table id="tsinotifier-controller">';

        // iterate for every row
        for (var i = 0; i < TSINOTIFIER_CONTROLLER_HEIGHT; i++) {
            // create a new row
            controller += '<tr>';
            // iterate for every column
            for (var j = 0; j < TsiNotifierController.columns.length; j++) {
                // check if column has a corresponding element at this row
                if (TsiNotifierController.columns[j].length >= i + 1) {
                    // create a new cell and put the button element inside of it
                    controller += '<td>';
                    controller += '<button class="tsinotifier-controller-button" id="tsinotifer-controller-' + j + '-' + i + '">' + TsiNotifierController.columns[j][i].text + '</button>';
                    controller += '</td>';
                } else { // column doesn't have an element at this row...
                    // create an empty cell
                    controller += '<td></td>';
                }
            }
            //close the new row
            controller += '</tr>';
        }

        // close the new controller table
        controller += '</table>';

        // remove any existing controller table
        $(TsiNotifierController.controllerSelector).remove();

        // insert the new controller table
        $(TsiNotifierController.controllerWrapperSelector).append(controller);

        // initialize event listeners for when buttons are clicked, and map them to their onclick function
        $('.tsinotifier-controller-button').on('click', function (e) {
            var j = parseInt($(e.target).attr('id').substring(22, 23));
            var i = parseInt($(e.target).attr('id').substring(24, 25));
            TsiNotifierController.columns[j][i].onclick();
        });

        // return a copy of the jQuery object for the controller table
        return $(TsiNotifierController.controllerSelector);

    }

};

/**
 * An object representing the countdown timer
 * @type {Object}
 */
TsiNotifierCountdown = {

    timeout: undefined,

    /**
     * Initialize the countdown timer
     * @return {boolean} True. It'll return true.
     */
    init: function () {

        // remove existing countdown timers
        $('#tsinotifier-coundown-wrapper').remove();

        // append the countdown timer wraper and countdown elements
        $('body').append(
            '<div id="tsinotifier-countdown-wrapper" style="position:fixed;top:0;left:0;z-index:0118999;">' +
                '<span id="tsinotifier-countdown" style="color:#000000;font-size:36pt;line-height:1em;">' +
                '</span>' +
            '</div>'
        );

        return true;

    },

    /**
     * Cancel the countdown timer
     * @return {boolean} True. It'll return true.
     */
    cancel: function () {

        // cancel the countdown timeout
        if (typeof TsiNotifierCountdown.timeout !== 'undefined') {
            clearTimeout(TsiNotifierCountdown.timeout);
        }

        // reset the timer display to 0
        TsiNotifierCountdown.setCountdown('0');

        return true;

    },

    /**
     * Start the countdown timer at the given number of seconds. Don't do this more than once until the timer runs out.
     * @param  {int|string} seconds The number of seconds from which to start the timer
     * @return {boolean}            True. It'll return true.
     */
    countdownFrom: function (seconds) {

        // set the countdown display to the number of seconds
        TsiNotifierCountdown.setCountdown(seconds);

        // if the timer still has time, decrement the time in 1 second (recursion)
        if (seconds > 0) {
            TsiNotifierCountdown.timeout = setTimeout(function () {
                TsiNotifierCountdown.countdownFrom(seconds - 1);
            }, 1000);
        }

        return true;

    },

    /**
     * Set the countdown timer display to the given number.
     * @param  {int|string} seconds The number of seconds to display
     * @return {boolean}            True. It'll return true.
     */
    setCountdown: function (seconds) {

        // get the countdown element
        var countdown = $('#tsinotifier-countdown');

        // check if the countdown exists
        if ($(countdown).length) {
            //set the countdown display to the given number of seconds
            $(countdown).text(seconds);
        } else {
            // initialize the countdown elements and try again (recursion)
            TsiNotifierCountdown.init();
            TsiNotifierCountdown.setCountdown(seconds);
        }

    }

};

/**
 * An object representing the TSI Notifier subsystem
 * @type {Object}
 */
TsiNotifier = {

    /**
     * Check if notifications are allowed, and if not, ask for them
     * @return {boolean} True if notifications are allowed, false if they've been denied
     */
    askForNotifications: function () {

        // check if notification API support is available
        if (typeof Notification !== 'undefined') {

            // check if we need to ask for notification permission
            if (Notification.permission !== 'granted') {

                // ask for permission to send desktop notifications
                Notification.requestPermission().then(function (permission) {

                    // check if user is being stubborn and denied our request
                    if (permission !== 'granted') {
                        // damn son, we just got SHUT DOWN!
                        alert('If you do not agree to notifications, TSI Notifier will not work. Please refresh the page and agree.');
                        return false;
                    } else {
                        return true;
                    }

                });

            } else {
                return true;
            }

        } else {
            // no notification API support
            console.log('ERROR: Cannot send notification. Notification API does not exist.');
            alert('TSI Notifier requires a modern browser with Notification API support. Please consider downloading the latest version of Firefox.');
            return false;
        }

    },

    /**
     * Check if any appraisals are available, if they are, notify. Also initializes the menu and handles page refreshes.
     * @return {boolean} True. It'll return true.
     */
    checkAppraisals: function () {

        // get our element of interest (and setup a place to store the data)
        var assignmentsBadge = $('[data-queue-count=APPRASSIGNMENTS]');
        var assignmentCount = '0';

        // check that the assignments badge actually exists
        if ($(assignmentsBadge).length) {
            // get the number from the badge
            assignmentCount = $(assignmentsBadge).text();
        }

        // check if there are no assignments...
        if (assignmentCount === '0') {
            // tough luck, let's try again

            // start a countdown timer for time before another refresh
            TsiNotifierCountdown.countdownFrom(TSINOTIFIER_REFRESH_TIME);

            // refresh the page after the refresh delay
            var retryTimeout = setTimeout(function () {
                location.reload();
            }, TSINOTIFIER_REFRESH_TIME * 1000);

        } else { //or if there are...
            // these are truly exciting times.

            // send that notification about the available appraisals.
            var notification = TsiNotifier.notify(new TsiNotifierNotification('New Appraisal(s)', 'There are '+assignmentCount+' appraisals available.'));

            // start a countdown timer for the time until the notification is considered dead (and the page refreshes)
            TsiNotifierCountdown.countdownFrom(TSINOTIFIER_DEAD_TIME);

            // refresh the page after the dead time runs out
            var deadTimeout = setTimeout(function () {
                notification.close();
                location.reload();
            }, TSINOTIFIER_DEAD_TIME * 1000);

        }

        // initialize the controller
        TsiNotifierController.init();

        // add a start button
        TsiNotifierController.addButton(new TsiNotifierControllerButton('start', function () {
            // refresh the page (restarts all scripts)
            location.reload();
        }));

        // add a stop button
        TsiNotifierController.addButton(new TsiNotifierControllerButton('stop', function () {
            // cancel the retry timeout
            if (typeof retryTimeout !== 'undefined') {
                clearTimeout(retryTimeout);
            }
            // cencel the dead timeout
            if (typeof deadTimeout !== 'undefined') {
                clearTimeout(deadTimeout);
            }
            // cancel the countdown timer
            TsiNotifierCountdown.cancel();
        }));

        return true;

    },

    /**
     * Send a notification to the desktop
     * @param  {object} notification An instance of TsiNotifierNotification representing the notification to send
     * @return {object|boolean}      either an instance of Notification on success, or false on failure
     */
    notify: function (notification) {

        // check if the browser supports the notification API
        if (typeof Notification !== 'undefined') {

            // check if we have permission to send notifications
            if (Notification.permission === 'granted') {

                // check that the passed notification is actually a properly formatted notification
                if (notification.type === 'TsiNotifierNotification') {

                    // send the notification to the browser! YAY!
                    var actualNotification = new Notification(notification.title, {
                        body: notification.text,
                        lang: 'EN', // language is english
                        vibrate: [300,100,100,100,300,100,100,100], // this is a vibrate pattern with a long buzz, short buzz, long buzz, short buzz
                        requireInteraction: TSINOTIFIER_NOTIFICATION_REQUIRE_INTERACTION // whether to lock the notification on the desktop until the user closes
                    });

                    //return the notification object
                    return actualNotification;

                } else {
                    // what you talkin 'bout Willis?
                    console.log('ERROR: Attempted to send notification that was not an instance of TsiNotifierNotification.');
                }

            } else {

                // request permission to send notifications
                Notification.requestPermission().then(function (permission) {

                    // check if user actually accepted our request
                    if (permission === 'granted') {
                        TsiNotifier.notify(notification);
                    } else {
                        // ok, fine, I don't even want to help you!
                        console.log('ERROR: Cannot send notification. Notification permission not granted.');
                        alert('If you do not agree to notifications, TSI Notifier will not work.');
                        return false;
                    }

                });

            }

        } else {
            // no notification API support
            console.log('ERROR: Cannot send notification. Notification API does not exist.');
            alert('TSI Notifier requires a modern browser with Notification API support. Please consider downloading the latest version of Firefox.');
            return false;
        }

    }

};

// wait for the document to be ready for modification
$(document).ready(function () {

    // request permission to send notifications (if necessary)
    if (TsiNotifier.askForNotifications()) {

        // wait a moment to ensure that the page fully loads
        setTimeout(function () {
            // check if any appraisals are available (and if so, notify)
            TsiNotifier.checkAppraisals();
        }, TSINOTIFIER_CHECK_DELAY * 1000);

    }

});
