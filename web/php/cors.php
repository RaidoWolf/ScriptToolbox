<?php

/**
 * enable_cors function
 * ====================
 *
 * Sends CORS header to allow asynchronous requests from JavaScript
 * on modern browsers without violating security measures.
 *
 * NOTE: Must be executed before content is printed to client.
 *
 * @return boolean - true (success), false (failure)
 */
function enable_cors () {
    //try to send CORS header (must not have sent html)
    if (header("Access-Control-Allow-Origin: *")) {
        //success
        return true;
    } else {
        //failure (content has probably already been sent, try output buffering)
        return false;
    }
}

?>
