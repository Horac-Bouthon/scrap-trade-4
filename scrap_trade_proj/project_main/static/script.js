

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

function _copy_of(node) {
    const CLONE_CHILDREN = true;
    var copy = node.cloneNode(CLONE_CHILDREN);
    copy.id = '';  // Copy can't have the same ID as the original
    return copy;
}

function _replace_all(str, a, b) {
    return str.replace(new RegExp(a, 'g'), b);
}


const Alerts = (function init_alerts() {

    // On load; Display all the alerts with effect
    // by adding the `shown` class.
    // Time out the initial display to get the user's
    // attention better + deferring needed for display effects.
    setTimeout(function display_all() {
        document.querySelectorAll('.alert').forEach(display);
    }, 300);
    
    function display(mesg) {
        // Ignore templates
        if (mesg.id == 'AlertTemplate') { return; }
        
        // Hook up the close button when displaying
        var close_button = mesg.querySelector('button');
        close_button.addEventListener('click', hide_handler);
                
        // Show by adding the class
        mesg.classList.add('shown');
        
        // @todo; [optional] Auto-close alerts after a set time?? 
    }
    
    function hide_handler(ev) {
        var button = this;
        var alert = _find_ancestor(button, '.alert');
        alert.classList.remove('shown');
        setTimeout(function shrink_to_nothing() {
            alert.style =
                'overflow: hidden;' +
                'height: 0;' +
                'margin: 0 !important;' +
                'padding: 0 !important;';
        }, 300);  // Make sure we're hiding after transition finished
    }


    // Alerts at runtime
    
    var Wrapper = document.querySelector('.Alert-Wrap');
    var AlertTemplate = document.getElementById('AlertTemplate');
    function add_new(message, type) {
        if (!AlertTemplate) {
            console.error('Alerts; Template for new alert not found');
            return;
        }
        if (!Wrapper) {
            console.error('Alerts; We have nowhere to put the alert.');
            return;
        }

        var new_alert = _copy_of(AlertTemplate);
        var text = new_alert.querySelector('.Alert-Text');
        var button = new_alert.querySelector('.Alert-Close');
        [new_alert, text, button].forEach(function fill_types(el) {
            el.className = _replace_all(el.className, 'TEMPLATE', type);
        });
        
        text.innerHTML = message;
        
        Wrapper.appendChild(new_alert);
        
        return new_alert;
    }
    
    function add_and_show(message, type) {    
        var new_alert = add_new(message, type);
        
        setTimeout(function() {  // defer
            display(new_alert);
        }, 1);
    }

    // Public API
    return {
        add: add_new,
        show: display,
        add_and_show: add_and_show,
    };
})();

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
    function django_encode(date, type) {
        var year = '' + date.getFullYear();
        var month = '' + (date.getMonth() + 1);  // JS month is 0-based
        var day = '' + date.getDate();
        var hours = '' + date.getHours();
        var minutes = '' + date.getMinutes();
        var Date = [year, zeropad(month), zeropad(day)].join('-');
        var Time = [zeropad(hours), zeropad(minutes)].join(':');
        var Datetime = [Date, Time].join(' ');
        var types = { 'date': Date, 'time': Time, 'datetime': Datetime };
        return types[type];
    }
    function django_decode(date_string) {
        if (date_string.trim().length == 0) {
            return null;
        }
        
        var datetime = date_string.split(' ');
        var date_comps = datetime[0].split('-');
        if (datetime.length == 1) {
            return new Date(
                date_comps[0],      // year
                date_comps[1] - 1,  // month
                date_comps[2]       // day
            );
        } else {
            var time_comps = datetime[1].split(':');
            return new Date(
                date_comps[0],      // year
                date_comps[1] - 1,  // month
                date_comps[2],      // day
                time_comps[0],      // hour
                time_comps[1]       // minute
            );
        }
    }
    function zeropad(number) {
        var str = '' + number;
        if (str.length == 1) { return ('0' + str); }
        else { return (str); }
    }
    
    // Utility functions
    function capitalize(str) {
        return str.charAt(0).toUpperCase() + str.substring(1);
    }

    

    // Find the inputs viable for widgeting
    const DATETIME_SELECTOR = 'input[type="text"].datetimeinput.form-control';
    const DATE_SELECTOR = 'input[type="text"].dateinput.form-control';
    const Inputs = document.querySelectorAll(DATETIME_SELECTOR + ', ' +
                                             DATE_SELECTOR);
    if (Inputs.length == 0) {
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
    
    
    Inputs.forEach(function init_input(input) {

        const INPUT_TYPE = (function() {
            if (input.classList.contains('dateinput')) { return 'date'; }
            else { return 'datetime'; }
        })();
        
        const InitialDate = django_decode(input.value, INPUT_TYPE);
        var CurrentlyDisplayedMonth = null;  // Set when switching
        
        // Element construction, immediatelly
        var Wrapper = construct_calendar_skeleton();
        init_time_events();

        // Defer selecting the loaded date to the end
        setTimeout(function() {
            // Create current month, select loaded date
            force_select_date(InitialDate, input);
            // Update the time fields, if possible
            init_time_fields(InitialDate);
        }, 1);

        
        function init_time_fields(date) {
            // Don't init non-datetimes
            if (INPUT_TYPE !== 'datetime') { return; }
            // If date wasn't initiated at load, fill in the current time
            if (date === null) { 
                date = new Date();
            }

            // Copy over the initial values
            const hours = Wrapper.querySelector('input[name=hours]');
            const mins = Wrapper.querySelector('input[name=minutes]');
            hours.value = zeropad(date.getHours());
            mins.value = zeropad(date.getMinutes());
        }
        
        function init_time_events() {
            // Add time-setting event listeners
            var minutes_and_hours = Wrapper.querySelectorAll(
                'input[name=minutes], input[name=hours]');
            minutes_and_hours.forEach(function(time_element) {
                
                time_element.addEventListener('click', update_input);
                time_element.addEventListener('keydown', update_input);
            });
            
            function update_input() {
                // Timed out so that it won't clash with builtin functionality
                setTimeout(function() {
                    // Clamp the hours and minutes before setting them
                    const hours = Wrapper.querySelector('input[name=hours]');
                    const mins = Wrapper.querySelector('input[name=minutes]');
                    hours.value = zeropad(
                        clamp(
                            parseInt(hours.value), hours.min, hours.max
                        ) || hours.value);
                    mins.value = zeropad(
                        clamp(
                            parseInt(mins.value), mins.min, mins.max
                        ) || mins.value);
                    // Decode the current time, modify hrs and mins
                    var current_date = django_decode(input.value, INPUT_TYPE);
                    if (current_date === null) {
                        // If date in field isn't valid, pick today as date
                        // and select it in the calendar visibly.
                        current_date = new Date();
                        force_select_date(current_date, input);
                    }
                    input.value = django_encode(new Date(
                        current_date.getFullYear(),
                        current_date.getMonth(),
                        current_date.getDate(),
                        hours.value, mins.value
                    ), INPUT_TYPE);
                }, 1);
            }
            function clamp(value, min, max) {
                if (value <= min) { return min; }
                else if (value > max) { return max; }
                else { return value; }
            }
        }


        function construct_calendar_skeleton() {
            
            var wrap = _copy_of(WrapperTemplate);
            input.parentNode.appendChild(wrap);
            
            // Weekdays header
            const weekdays = wrap.querySelector('.calendar__weekdays');
            DAYS.forEach(function(translated_day_name) {
                const day = _copy_of(ItemTemplate);
                weekdays.appendChild(day);
                var first_few = translated_day_name.substring(0, 2);
                day.innerHTML = capitalize(first_few);
            });

            // Month switching events
            const prev_btn = wrap.querySelector('button.Prev-Month');
            prev_btn.addEventListener('click', function() {
                var new_date = new Date(CurrentlyDisplayedMonth);  // Clone
                new_date.setMonth(CurrentlyDisplayedMonth.getMonth() - 1);
                switch_to_month(new_date, input);
            });
            const next_btn = wrap.querySelector('button.Next-Month');
            next_btn.addEventListener('click', function() {
                var new_date = new Date(CurrentlyDisplayedMonth);  // Clone
                new_date.setMonth(CurrentlyDisplayedMonth.getMonth() + 1);
                switch_to_month(new_date, input);
            });

            // Display time section, if needed
            var Time = wrap.querySelector('section.calendar__time');
            if (INPUT_TYPE !== 'datetime')
                Time.classList.add('d-none');

            return wrap;
        }
        
        function force_select_date(date, input) {
            if (date === null) {
                // Date wasn't filled in by the backend, so we shouldn't
                // fill it at the start.
                // ...Maybe it's supposed to not be filled in, we can't know
                switch_to_month(null, input);
                
            } else {
                // Get the month with the date, (maybe create) and display it
                var shown_month = switch_to_month(date, input);

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
        }
        
        function switch_to_month(date_obj, input) {
            
            // Switch the calendar heading, modify the internal value
            if (date_obj === null) {
                CurrentlyDisplayedMonth = new Date();  // Set to now
            } else {
                // Modify the internal value
                CurrentlyDisplayedMonth = new Date(date_obj);  // Clone date
                CurrentlyDisplayedMonth.setDate(1);  // Just in case...
            }
            
            // In case we don't get a valid date object, 
            Wrapper.querySelector('.Top-Date')
                .innerHTML =
                capitalize(MONTHS[CurrentlyDisplayedMonth.getMonth()]) + ' ' +
                CurrentlyDisplayedMonth.getFullYear();
            
            // Find the corresponding month
            var wraps = Wrapper.querySelectorAll('.Month-Wrap');
            var show_month = (function find_wrap_for_month(date) {
                var found = null;
                wraps.forEach(function(wrap) {
                    if (wrap.dataset.month == date.getMonth()) {
                        found = wrap;
                    }
                });
                return found;
            })(CurrentlyDisplayedMonth);

            // Construct the wanted month if it doesn't exist
            if (show_month === null) {
                show_month = construct_month(CurrentlyDisplayedMonth, input); 
            }
            
            // Show only the month that we want to see  @todo; With effects
            wraps.forEach(function(wrap) {
                if (wrap == show_month) {
                    wrap.classList.remove('d-none');
                } else {
                    wrap.classList.add('d-none');
                }
            });

            // Return the month we've decided to show
            return show_month;
        }
        
        function construct_month(date_obj, input) {
            
            const month_wrap = Wrapper.querySelector('.calendar__months');
            const Month = _copy_of(MonthTemplate);
            month_wrap.appendChild(Month);

            // Remember month in the HTML for later
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
            var current_row = _copy_of(RowTemplate);
            Month.appendChild(current_row);
            
            for (var day=0; day < month_starts_at_day; day++) {
                current_row.appendChild(_copy_of(ItemTemplate));
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
            
            for (var day=0; day < days_in_this_month; day++) {
                
                // Break line of days before writing Monday
                var is_new_week = (row_i == 7);
                if (is_new_week) {
                    current_row = _copy_of(RowTemplate);
                    Month.appendChild(current_row);
                    is_new_week = false;
                    row_i = 0;
                }
                
                const new_day = _copy_of(ItemTemplate);
                new_day.innerHTML = (day + 1) + '';
                new_day.classList.add('Date', 'btn', 'big');
                
                // Save date into the HTML attributes
                const data_attr = new_day.dataset;
                data_attr.day = day + 1;
                data_attr.month = date_obj.getMonth();
                data_attr.year = date_obj.getFullYear();
                function get_datestring_from_button(day_button) {
                    var current_time = django_decode(input.value, INPUT_TYPE);
                    if (current_time === null) current_time = new Date();
                    const btn_date = day_button.dataset;
                    return django_encode(new Date(
                        btn_date.year, btn_date.month, btn_date.day,
                        current_time.getHours(), current_time.getMinutes()
                    ), INPUT_TYPE);
                }
                
                // Click events for choosing the date
                new_day.addEventListener('click', function() {

                    // Set the original input's value
                    input.value = get_datestring_from_button(this);

                    // Toggle the selected item classes
                    Wrapper.querySelectorAll('.SELECTED_DAY')
                        .forEach(function(el) {
                            el.classList.remove('SELECTED_DAY', 'btn-primary');
                        });
                    this.classList.add('SELECTED_DAY', 'btn-primary');
                    
                });
                
                // Highlight today, if viewing the correct month
                const today_day_index = (function(date) {
                    var today_date = new Date();
                    if (date.getFullYear() === today_date.getFullYear()) {
                        if (date.getMonth() === today_date.getMonth()){
                            return today_date.getDate();
                        }
                    }
                    return -1;  // Today is not in current month
                })(date_obj);
                if (today_day_index > 0) {
                    const is_today = ((day + 1) === today_day_index);
                    if (is_today) {
                        new_day.style.boxShadow =
                            '0px 0px 0px 3px hsla(205, 100%, 50%, 0.5)';
                    }
                }

                // Add the day into the row, keep track of days in the row
                current_row.appendChild(new_day);
                row_i += 1;
            }

            
            // Padding out the end
            
            for (var day=row_i; day < 7; day++) {
                current_row.appendChild(_copy_of(ItemTemplate));
            }


            // Return the created month
            return Month;
        }
    });
    
})();

