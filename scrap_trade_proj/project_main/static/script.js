

/**
 * Find first ancestor that matches the selector provided
 */
function _find_ancestor(el, selector_criteria) {
    while (! el.matches('body')) {
        console.log(el.classList);
        el = el.parentElement;
        if (el.matches(selector_criteria))
            return el;
    }
    return null;
}


function _show(el) { el.classList.remove('d-none'); }
function _hide(el) { el.classList.add('d-none'); }
