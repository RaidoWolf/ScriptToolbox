function FiniteStateMachine (states, transitions) {

    states = typeof states !== 'undefined' ? states : [];
    transitions = typeof transitions !== 'undefined' ? transitions : [];

    if (!Array.isArray(states)) {
        console.warn('FiniteStateMachine constructor failed: states must be an array.');
        return null;
    }

    if (!Array.isArray(transitions)) {
        console.warn('FiniteStateMachine constructor failed: transitions must be an array.');
        return null;
    }

    this.states = {}; // we don't want to overwrite the prototype...
    for (var i = 0; i < states.length; ++i) {

        if (states[i] instanceof FSMState) {
            if (!(states[i].key in this.states)) {
                this.states[states[i].key] = states[i];
            } else {
                console.warn('FiniteStateMachine constructor: all state keys must be unique.');
            }
        } else {
            console.warn('FiniteStateMachine constructor: contents of states array must be instances of FSMState.');
        }

    }

    for (var j = 0; j < transitions.length; ++j) {

        if (transitions[j] instanceof FSMTransition) {
            this.transitions.push(transitions[j]);
        } else {
            console.warn('FiniteStateMachine constructor: contents of transitions array must be instances of FSMTransition.');
        }

    }

    this.data = {};

}

FiniteStateMachine.prototype.switchTo = function (stateKey, data) {

    if (!(stateKey in this.states)) {
        console.warn('FiniteStateMachine.switchTo() failed: Requested state does not exist.');
    }

    // no state has ever run, so any valid state can now
    if (this.currentState === null) {

        this.states[stateKey].onStart(this, data, this.currentState); // tell new state it's starting
        this.currentState = stateKey;

        return true;

    }

    // check for a valid transition from current state to the new one
    for (var i = 0; i < this.transitions.length; ++i) {

        if (this.transitions[i].from === this.currentState && this.transitions[i].to === stateKey) {

            this.states[this.currentState].onEnd(this, data, stateKey); // tell current state it's ending
            this.transitions[i].callback(this, data); // run transition callback
            this.states[stateKey].onStart(this, data, this.currentState); // tell new state it's starting
            this.currentState = stateKey;

            return true;

        }

    }

    return false; // no transitions ever got matched, so we never returned

};

FiniteStateMachine.prototype.currentState = null;
FiniteStateMachine.prototype.states = {};
FiniteStateMachine.prototype.transitions = [];
FiniteStateMachine.prototype.data = null;

function FSMState (key, onStart, onEnd) {

    if (typeof key === 'string') {
        this.key = key;
    } else {
        if (typeof key === 'undefined') {
            console.warn('FSMState constructor: key must be set.');
        } else {
            console.warn('FSMState constructor: key must be a string.');
        }
    }

    if (typeof onStart === 'function') {
        this.onStart = onStart;
    } else {
        if (typeof onStart!== 'undefined') {
            console.warn('FSMState constructor: onStart callback must be a function.');
        }
    }

    if (typeof onEnd === 'function') {
        this.onEnd = onEnd;
    } else {
        if (typeof onEnd !== 'undefined') {
            console.warn('FSMState constructor: onStart callback must be a function.');
        }
    }

    this.data = {};

}

FSMState.prototype.key = null;
FSMState.prototype.onStart = function (fsm, data, prevState) {};
FSMState.prototype.onEnd = function (fsm, data, nextState) {};
FSMState.prototype.data = null;

function FSMTransition (fromKey, toKey, callback) {

    if (typeof fromKey === 'string') {
        this.from = fromKey;
    } else {
        if (typeof fromKey === 'undefined') {
            console.warn('FSMTransition constructor: from key must be set.');
        } else {
            console.warn('FSMTransition constructor: from key must be a string.');
        }
    }

    if (typeof toKey === 'string') {
        this.to = toKey;
    } else {
        if (typeof toKey === 'undefined') {
            console.warn('FSMTransition constructor: to key must be set.');
        } else {
            console.warn('FSMTransition constructor: to key must be a string.');
        }
    }

    if (typeof callback === 'function') {
        this.callback = callback;
    } else {
        if (typeof callback !== 'undefined') {
            console.warn('FSMTransition constructor: callback must be a function.');
        }
    }

    this.data = {};

}

FSMTransition.prototype.from = null;
FSMTransition.prototype.to = null;
FSMTransition.prototype.callback = function (fsm, data) {};
FSMTransition.prototype.data = null;
