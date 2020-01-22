

/**
 * Find first ancestor that matches the selector provided
 */
function _find_ancestor(el, selector_criteria) {
    while (! el.matches('body')) {
        el = el.parentElement;
        if (el.matches(selector_criteria))
            return el;
    }
    return null;
}


function _show(el) { el.classList.remove('d-none'); }
function _hide(el) { el.classList.add('d-none'); }




/**
 *  Login form interactivity. 
 */
const login = (function() {
    
    const USE_ESCAPE_SHORTCUT = true;
    
    const LOGIN_POPUP_ID = 'LOGIN_POPUP';
    const get_popup_element = function() {
        var el = document.getElementById(LOGIN_POPUP_ID);
        return el;
    }

    
    const show_popup = function() {
        var el = get_popup_element();
        if (el == null) {
            console.error(
                "Login popup doesn't exist, redirecting to form."
            );
            window.location.href = LOGIN_PAGEURL;
            return
        }
        
        _show(el);  // @todo; Show the login form with some effects

        if (!USE_ESCAPE_SHORTCUT) {
            document.addEventListener('keydown', function(e) {
                if (e.key == "Escape") {
                    close_popup();
                }
            });
        }
        
        focus_first_field();
    };

    const focus_first_field = function() {
        get_popup_element()
            .querySelectorAll('input[type=text]')[0]
            .focus();
    }
    
    const close_popup = function() {
        var el = get_popup_element();
        if (el == null) return;
        
        _hide(el);
    }

    
    const is_hidden = function() {
        // @todo; Make toggling the form less dependent on _show() and _hide()
        var el = get_popup_element();
        return el.classList.contains('d-none');
    };
    const toggle_popup = function() {
        var el = get_popup_element();
        if (is_hidden()) {
            _show(el);
        } else {
            _hide(el);
        }
    }

    // Toggle popup on Esc key
    if (USE_ESCAPE_SHORTCUT) {
        document.addEventListener('keydown', function(e) {
            if (get_popup_element() == null) {
                return  // Prevents the redirect in show_popup
            }
            
            if (e.key == "Escape") {
                toggle_popup();
                if (!is_hidden()) {
                    focus_first_field();
                }
            }
        });
    }

    // Allow dismissing popup by clicking the background
    // ..We can't just use an onclick on the bg element because
    //   the event would trigger on sub-elements as well.
    document.addEventListener('click', function(e) {
        var clicked = e.target;
        if (clicked.id == 'LOGIN_POPUP_BACKGROUND') {
            close_popup();
        }
    });

    
    const public_api = {
        'show_popup': show_popup,
        'close_popup': close_popup
    }
    return public_api
})()
