

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
 *  Inline editable forms interactivitiy.
 */
const Inlines = (function() {

    // @todo; Improve the deletion behavior (no redirects plz)
    // @todo; Instead of hide/show, use a transition, if possible
    
    EDITABLE = '.Form-EDIT';
    READ = '.Form-READ';
    ADDED = '.Form-ADD'
    
    function edit(btn) {
        if (btn.classList.contains('active')) {
            // Allow toggling back
            // (maybe the form is really big and Cancel is too far below)
            restore_all();
            return;
        }
        
        restore_all();
        btn.classList.add('active') // Leave the button in active state
        li = _find_ancestor(btn, 'li');
        li.querySelectorAll(EDITABLE).forEach(_show);
    }
    function add_line(btn) {
        if (btn.classList.contains('active')) {
            restore_all();
            return;
        }
        restore_all();
        btn.classList.add('active');
        ul = _find_ancestor(btn, 'dl').querySelector('ul');
        add = ul.querySelector(ADDED).cloneNode(true);
        _show(add)
        ul.appendChild(add);
    }
    function restore_all() {
        // Restore all buttons from forced active states
        document.querySelectorAll('.active').forEach(function(btn) {
            btn.classList.remove('active');
        })

        // Hide any `edit` and `add` views
        document.querySelectorAll(EDITABLE + ',' + ADDED)
            .forEach(_hide);
    }

    // Escape to cancel
    document.addEventListener('keydown', function(e) {
        if (e.key == "Escape") {
            restore_all();
        }
    });

    public_api = {
        'edit': edit,
        'add_line': add_line,
        'restore_all': restore_all
    };
    return public_api;
})()


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
    return public_api;
})();


var calendar_widget = (function CalendarWidget() {

    // Formatting to/from django
    function django_encode(date) {
        var month = '' + (date.getMonth() + 1);
        var day = '' + date.getDate();
        var year = '' + date.getFullYear();
        // Pad with zeroes
        if (month.length == 1) month = '0' + month;
        if (day.length == 1) day = '0' + day;
        return [year, month, day].join('-')
    }
    function django_decode(date_string) {
        var comps = date_string.split('-');
        // @todo; Make decoding dates in JS a bit more robust
        return new Date(
            comps[0],      // year
            comps[1] - 1,  // month
            comps[2]       // day
        );
    }

    // Utility functions
    function copy_of(node) {
        const CLONE_CHILDREN = true;
        var copy = node.cloneNode(CLONE_CHILDREN);
        copy.id = '';  // Copy can't have the ID
        return copy;
    };
    function capitalize(str) {
        return str.charAt(0).toUpperCase() + str.substring(1);
    };

    

    // Find the inputs viable for widgeting
    const INPUT_SELECTOR = 'input[type="text"].dateinput.form-control';
    const INPUTS = document.querySelectorAll(INPUT_SELECTOR);
    if (INPUTS.length == 0) {
        console.info("Calendar widget; No inputs for widget found.");
        return;
    }

    // Grab HTML templates
    const WrapperTemplate = document.getElementById('Calendar-Template');
    const RowTemplate = document.getElementById('CalendarRow-Template');
    const ItemTemplate = document.getElementById('CalendarItem-Template');
    const MonthTemplate = document.getElementById('CalendarMonth-Template');
    if (!WrapperTemplate || !RowTemplate ||
        !ItemTemplate || !MonthTemplate) {
        console.error("Calendar widget; " +
                      "Templates not found, inputs won't use calendars.");
        console.error(WrapperTemplate, RowTemplate,
                      ItemTemplate, MonthTemplate);
        return;
    }

    
    INPUTS.forEach(function init_input(input) {
        
        const InitialDate = django_decode(input.value);
        var CurrentlyDisplayed = null;  // Set when switching

        setTimeout(function() {  // Defer to the end
            force_select_date(InitialDate);
        }, 1);
        
        // Element construction
        var Wrapper = null;
        (function construct_calendar_skeleton() {
            
            Wrapper = copy_of(WrapperTemplate);
            input.parentNode.appendChild(Wrapper);
            
            // Weekdays header
            const weekdays = Wrapper.querySelector('.calendar__weekdays');
            DAYS.forEach(function(translated_day_name) {
                const day = copy_of(ItemTemplate);
                weekdays.appendChild(day);
                var first_few = translated_day_name.substring(0, 2);
                day.innerHTML = capitalize(first_few);
            });

            // Month switching events
            const prev_btn = Wrapper.querySelector('button.Prev-Month');
            prev_btn.addEventListener('click', function() {
                var new_date = new Date(CurrentlyDisplayedMonth);  // Clone
                new_date.setMonth(CurrentlyDisplayedMonth.getMonth() - 1);
                switch_to_month(new_date);
            });
            const next_btn = Wrapper.querySelector('button.Next-Month');
            next_btn.addEventListener('click', function() {
                var new_date = new Date(CurrentlyDisplayedMonth);  // Clone
                new_date.setMonth(CurrentlyDisplayedMonth.getMonth() + 1);
                switch_to_month(new_date);
            });
        })();
        
        function switch_to_month(date_obj) {

            // Internal value
            CurrentlyDisplayedMonth = new Date(date_obj);  // Clone date
            CurrentlyDisplayedMonth.setDate(1);  // Just in case...
            
            // Switch the calendar heading
            Wrapper.querySelector('.Top-Date')
                .innerHTML =
                capitalize(MONTHS[date_obj.getMonth()]) + ' ' +
                date_obj.getFullYear();

            // Find the corresponding month
            var wraps = Wrapper.querySelectorAll('.Month-Wrap');
            var show_month = (function find_wrap_for_month(date) {
                var found = null;
                wraps.forEach(function(wrap) {
                    if (wrap.dataset.month == date.getMonth()) {
                        found = wrap;
                        // break;  // Can't `break` out of a function!
                    }
                });
                return found;
            })(date_obj);

            // Construct the wanted month if it doesn't exist
            if (show_month === null) {
                show_month = construct_month(date_obj); 
            }

            // Show only the month that we want to see  @todo; With effects
            wraps.forEach(function(wrap) {
                if (wrap == show_month) {
                    wrap.classList.remove('d-none');
                } else {
                    wrap.classList.add('d-none');
                }
            });

            return show_month;  // Return the month we've decided to show
        };

        function force_select_date(date) {
            // Get the month with the date, (maybe create) and display it
            var shown_month = switch_to_month(date);

            // Find the button that corresponds with the date and click it
            var dates = shown_month.querySelectorAll('.Date');
            dates.forEach(function(date_elem) {
                var data_attr = date_elem.dataset;
                if (date.getFullYear() == data_attr.year &&
                    date.getMonth() == data_attr.month &&
                    date.getDate() == data_attr.day
                   ) {
                    date_elem.click();  // Trigger the click event
                }
            });
        }
        
        function construct_month(date_obj) {
            const month_wrap = Wrapper.querySelector('.calendar__months');
            
            const Month = copy_of(MonthTemplate);
            month_wrap.appendChild(Month);
            Month.dataset.month = date_obj.getMonth();
            

            // Padding out the months' starting day
            
            const month_starts_at_day = (function(date) {
                const first_day = new Date(
                    date.getFullYear(), date.getMonth(), 1);
                var american_format = first_day.getDay();
                if (american_format == 0) {
                    return 6;  // Sunday fix
                }
                return american_format - 1;
            })(date_obj);
            
            var row_i = 0;  // How filled is the current row
            var current_row = copy_of(RowTemplate);
            
            current_row.innerHTML = '';
            Month.appendChild(current_row);

            
            for (var day=0; day < month_starts_at_day; day++) {
                current_row.appendChild(copy_of(ItemTemplate));
                row_i += 1;
            }

            
            // Actual days in the currently viewed month
            
            const days_in_this_month = (function(date) {
                const last_day = new Date(
                    date.getFullYear(),
                    date.getMonth() + 1,  // Next month
                    0  // 0th day wraps and gets last day of previous month
                );
                return last_day.getDate();
            })(date_obj);
            const today_day_index = (function(date) {
                var today_date = new Date();
                if (date.getFullYear() === today_date.getFullYear()) {
                    if (date.getMonth() === today_date.getMonth()){
                        return today_date.getDate();
                    }
                }
                return -1;  // Today is not in current month
            })(date_obj);
            
            for (var day=0; day < days_in_this_month; day++) {
                
                // Break line of days before writing Monday
                var is_new_week = (row_i == 7);
                if (is_new_week) {
                    current_row = copy_of(RowTemplate);
                    Month.appendChild(current_row);
                    is_new_week = false;
                    row_i = 0;
                }
                
                const new_day = copy_of(ItemTemplate);
                new_day.innerHTML = (day + 1) + '';
                new_day.classList.add('Date', 'btn', 'big');
                
                // Save date into the HTML attributes
                const data_attr = new_day.dataset;
                data_attr.day = day + 1;
                data_attr.month = date_obj.getMonth();
                data_attr.year = date_obj.getFullYear();

                // Click events for choosing the date
                new_day.addEventListener('click', function() {

                    const selected_date = (function(day_button) {
                        const data_attr = day_button.dataset;
                        return django_encode(new Date(
                            data_attr.year, data_attr.month, data_attr.day
                        ));
                    })(this);
                    
                    const input = (function(calendar) {
                        // Find nearest input element
                        const widget_parent = calendar.parentNode;
                        return widget_parent.querySelector('input');
                    })(Wrapper);

                    input.value = selected_date;

                    // Toggle the selected item classes
                    Wrapper.querySelectorAll('.SELECTED_DAY')
                        .forEach(function(el) {
                            el.classList.remove('SELECTED_DAY', 'btn-primary');
                        });
                    this.classList.add('SELECTED_DAY', 'btn-primary');
                    
                });
                
                // Highlight today, if viewing the correct month
                if (today_day_index > 0) {
                    const is_today = ((day + 1) === today_day_index);
                    if (is_today) {
                        new_day.style.boxShadow =
                            '0px 0px 0px 3px hsla(205, 100%, 50%, 0.5)';
                    }
                }
                
                current_row.appendChild(new_day);
                row_i += 1;
            }

            
            // Padding out the end
            
            for (var day=row_i; day < 7; day++) {
                current_row.appendChild(copy_of(ItemTemplate));
            }


            // Return the created month
            return Month;
        }
    });
    
})();

