var PointerUtil = {

    getClientCoordFromEvent: function (e) {

        switch (e.type) {

            case 'touchstart':
            case 'touchmove':
            case 'touchend':
            case 'touchcancel':
                return PointerUtil.getTouchClientCoordsFromEvent(e)[0];

            default:
                return PointerUtil.getMouseClientCoordFromEvent(e);

        }

    },

    getTouchClientCoordsFromEvent: function (e) {

        var output = [];

        for (var i = 0; i < e.originalEvent.touches.length; ++i) {
            output.push({
                x: e.originalEvent.touches[i].pageX - window.scrollX,
                y: e.originalEvent.touches[i].pageY - window.scrollY
            });
        }

        return output;

    },

    getMouseClientCoordFromEvent: function (e) {

        return {
            x: e.pageX - window.scrollX,
            y: e.pageY - window.scrollY
        };

    },

    pointerOverElement: function (e, element) {

        var coord = getPointerCoord(e);
        return PointerUtil.coordOverElement(coord, element);

    },

    coordOverElement: function (coord, element) {

        if (typeof jQuery !== 'undefined' && element instanceof jQuery) {
            elementRect = $(element).get(0).getBoundingClientRect();
        } else {
            elementRect = element.getBoundingClientRect();
        }

        if (
            elementRect.left < coord.x &&
            elementRect.right > coord.x &&
            elementRect.top < coord.y &&
            elementRect.bottom > coord.x
        ) {
            return true;
        } else {
            return false;
        }

    }

};
