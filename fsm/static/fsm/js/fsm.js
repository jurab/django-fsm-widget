function fsm_get_index(list, value) {
    // Older versions of IE don't support indexOf, so I'm using a custom one.
    for (var i = 0, j = list.length; i < j; i++) {
        if (list[i] === value) {
            return i;
        }
    }
    return -1;
}


function fsm_update_selected_values(selected_id, base) {
    // Update the list of values of the currently selected objects using the
    // selected_id <select> field.
    var options = fsm_get_all(selected_id);
    window[base + '_selected_values'] = [];
    for(var i = 0; i < options.length; i++) {
        window[base + '_selected_values'].push(options[i].value);
    }
}


function fsm_update_submit(base) {
    // Updated the list of objects to be submitted on POST using the list
    // of objects chosen by the user contained in the _to field.
    var submit_select = document.getElementById(base + '_submit');
    var options = fsm_get_all(base + "_to");
    fsm_clear_select(submit_select);
    for(var i = 0; i < options.length; i++) {
        submit_select.add(fsm_create_option(options[i].text, options[i].value, true));
    }
}

function fsm_filter(input_id) {
    // Apply filter terms to list of choices via ajax call.
    var input = document.getElementById(input_id);
    var input_data = input.value;
    var base_id = input_id.replace('_input', '');

    // Get the url for the specific field. This allows for multiple fields in
    // the same form, all using unique urls.
    var ajax_url = window[base_id + '_url'] + '?filter=' + input_data;


    var from_element = input.parentElement.parentElement.getElementsByTagName('select')[0];

    // Wait a few seconds after input to filter. This gives the user
    // a chance to finish what they're typing before the query is sent.
    if(this.timer) {
        clearTimeout(this.timer);
    }
    var pause_interval = 1000;
    this.timer = setTimeout(function() {
        fsm_ajax(ajax_url, fsm_load_options, from_element);
    }, pause_interval);
}

function fsm_load_options(text, select) {
    // Insert a list of options from a json object into the
    // choices <select>.
    fsm_clear_select(select);

    var json_data = JSON.parse(text, function (key, value) {
        var type;
        if (value && typeof value === 'object') {
            type = value.type;
            if (typeof type === 'string' && typeof window[type] === 'function') {
                return new (window[type])(value);
            }
        }
        return value;
    });

    // Nearly all the fields have an id 'id_somethingDescriptive'. Since
    // we know 'select' is the 'id_from' by removing the from we can figure
    // out the base 'id' value.
    var base_id = select.id.slice(0,-5);
    var to_element_id = base_id + '_to';
    fsm_update_selected_values(to_element_id, base_id);

    for(var i in json_data) {
        if(fsm_get_index(window[base_id + '_selected_values'], i) == -1) {
            select.add(fsm_create_option(json_data[i], i, false));
        }
    }

    fsm_update_submit(base_id);
}


function fsm_clear_select(select) {
    // Remove all the options from a select.
    select.innerHTML = "";
}


function fsm_move(from, to, base) {
    // Move an option from one select to another, and update the list of
    // objects that will be submitted on POST.
    var selected = fsm_get_selected(from);
    for(var i = 0; i < selected.length; i++) {
        fsm_move_element(to, selected[i]);
    }
    fsm_update_submit(base);
}


function fsm_move_all(from, to, base) {
    // Move all options from one select to another, and update the list of
    // objects that will be submitted on POST.
    var options = fsm_get_all(from);
    for(var i = 0; i < options.length; i++) {
        fsm_move_element(to, options[i]);
    }
    fsm_update_submit(base);
}


function fsm_get_selected(from) {
    // Gets a list of selected options in a <select>.
    var selected = [];
    var from_element = document.getElementById(from);

    for(var i = 0; i < from_element.options.length; i++) {
        if(from_element.options[i].selected) {
            selected.push(from_element.options[i]);
        }
    }
    return selected;
}


function fsm_get_all(from) {
    // Gets a list of all options in a <select> regardless of selection
    // status.
    var options = [];
    var from_element = document.getElementById(from);

    for(var i = 0; i < from_element.options.length; i++) {
        options.push(from_element.options[i]);
    }

    return options;
}


function fsm_move_element(to, option) {
    // Moves a specific option to a specified <select>.
    var to_element = document.getElementById(to);
    var new_option = fsm_create_option(option.text, option.value, false);
    to_element.add(new_option);
    option.parentNode.removeChild(option);
}

function fsm_ajax(url, callback, target_element) {
    // Sends ajax request for choices filtered on a specified value.
    // Shamelessly copied from http://stackoverflow.com/a/18324384
    var xmlhttp;
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
            callback(xmlhttp.responseText, target_element);
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}


function fsm_create_option(text, value, selected) {
    // Creates a new <option> using the specified text and value.
    // Option will be marked as selected if selected===true.

    var new_option = document.createElement("option");
    new_option.text = text;
    new_option.value = value;

    if(selected) {
        new_option.setAttribute('selected', 'selected');
    }

    return new_option
}