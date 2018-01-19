function touchProxy (element) {

    element = typeof element === 'undefined' ? document : element;

    if (typeof jQuery === 'function' && element instanceof jQuery) {
        element = jQuery(element).get(0);
    }

    var simulate = function (type, element) {

        var simulatedEvent = document.createEvent('MouseEvent');

        simulatedEvent.initMouseEvent(
            type,
            true,
            true,
            window,
            1,
            element.screenX,
            element.screenY,
            element.clientX,
            element.clientY,
            false,
            false,
            false,
            false,
            0, // left
            null
        );

        element.target.dispatchEvent(simulatedEvent);

    };

    var touchProxyCallback = function (ev) {

        var touches = ev.changedTouches;
        var first = touches[0];
        var type = '';

        switch (ev.type) {

            case 'touchstart':
                simulate("mouseover", first);
                simulate("mousedown", first);
                break;

            case 'touchmove':
                simulate("mouseover", first);
                simulate("mousemove", first);
                break;

            case 'touchend':
                simulate("mouseup", first);
                break;

            default:
                return;

        }

        ev.preventDefault();

    };

    element.addEventListener("touchstart", touchProxyCallback, true);
    element.addEventListener("touchmove", touchProxyCallback, true);
    element.addEventListener("touchend", touchProxyCallback, true);
    element.addEventListener("touchcancel", touchProxyCallback, true);

}
