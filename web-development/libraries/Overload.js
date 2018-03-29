//jshint esversion: 6

class OverloadArgument {

    constructor (types, classes) {

        if (!Array.isArray(types)) {
            console.warn('Failed: OverloadArgument types must be array.');
            return null;
        }

        if (!Array.isArray(classes)) {
            console.warn('Failed: OverloadArgument classes must be array.');
            return null;
        }

        this._types = types;
        this._classes = classes;

    }

    get types () {
        return typeof this._types !== 'undefined' ? this._types : [];
    }

    get classes () {
        return typeof this._classes !== 'undefined' ? this._classes : [];
    }

}

class OverloadOption {

    constructor (args, callback) {

        if (!Array.isArray(args)) {
            console.warn('Failed: OverloadOption args must be array.');
            return null;
        }

        for (let i = 0; i < args.length; ++i) {
            if (!((typeof args[i] === 'object') && (args[i] instanceof OverloadArgument))) {
                console.warn('Failed: OverloadOption args must be instances of OverloadArgument.');
                return null;
            }
        }

        this._args = args;

    }

    get args () {
        return typeof this._args !== 'undefined' ? this._args : [];
    }

}

class Overload {

    constructor (overloads) {

        this._overloads = [];

        if (typeof overloads !== 'undefined') {

            if (Array.isArray(overloads)) {

                for (let i = 0; i < overloads.length; ++i) {
                    if (!(overloads[i] instanceof OverloadOption)) {
                        console.warn('Failed: Overload overloads must be instances of OverloadOption.');
                        return null;
                    }
                }

                this._overloads = overloads;

            } else {

                console.warn('Failed: Overload overloads must be array.');
                return null;

            }

        }

    }

    overload (overload) {

        if (!(overload instanceof OverloadOption)) {
            console.warn('Failed: Overload overloads must be instances of OverloadOption.');
            return false;
        }

        this._overloads.push(overload);

        return true;

    }

    call () {

        for (let i = this._overloads.length; i > 0; --i) {

            let thisOverload = this._overloads[i];

            for (let j = 0; j < this._overloads[i].args.length; ++j) {

                let overloadArg = this._overloads[i].args[j];
                let calledArg = typeof arguments[j] !== 'undefined' ? arguments[j] : null;

                if (!overloadedArg.types.includes(typeof calledArg)) {
                    break;
                }

                if (typeof calledArg === 'object') {

                    let caught = false;

                    for (let i = 0; i < overloadedArg.classes.length; ++i) {
                        if (
                            typeof window[overloadedArg.classes[i]] === 'function' &&
                            calledArg instanceof overloadedArg.classes[i]
                        ) {
                            caught = true;
                        }
                    }

                    if (!caught) {
                        break;
                    }

                    return thisOverload.callback.apply(null, arguments);

                }

            }
        }

    }

    get overloads () {
        return typeof this._overload !== 'undefined' ? this._overload : [];
    }

}
