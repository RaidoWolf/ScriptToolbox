<?php

function intToOrdinal ($int) {

    if (is_int($int)) {
        if ($int < 13) {
            switch ($int) {
                case 1:
                    return '1st';
                    break;
                case 2:
                    return '2nd';
                    break;
                case 3:
                    return '3rd';
                    break;
                default:
                    return "{$int}th";
                    break;
            }
        } else {
            $lastDigit = $int % 10;
            switch ($lastDigit) {
                case 1:
                    return "{$int}st";
                    break;
                case 2:
                    return "{$int}nd";
                    break;
                case 3:
                    return "{$int}rd";
                default:
                    return "{$int}th";
                    break;
            }
        }
    } else {
        trigger_error('intToOrdinal(): Argument must be an integer, but got '.gettype($int).'.');
        return false;
    }

}

?>
