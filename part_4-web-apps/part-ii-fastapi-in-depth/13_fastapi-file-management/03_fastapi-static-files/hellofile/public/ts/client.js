"use strict";
/* Note that you may want to use Browserify if you plan to use TS modules */
console.log(`Everything's perfectly all right now. We're fine. We're all fine here now, thank you. How are you?`);
const indeterminateCheckbox = getValidatedHtmlElement('#indeterminateCheckbox');
indeterminateCheckbox.indeterminate = true;
function getValidatedHtmlElement(htmlSelector) {
    const elem = document.querySelector(htmlSelector);
    if (!elem) {
        console.log(`ERROR: ${htmlSelector} was not found in the HTML`);
        throw new Error(`Missing element ${htmlSelector} in HTML`);
    }
    return elem;
}
//# sourceMappingURL=client.js.map