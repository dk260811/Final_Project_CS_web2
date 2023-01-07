//$('.datepicker').datepicker({
//    inline: true
//  });

//flatpickr("input[type=datetime-local]", {});

document.addEventListener('DOMContentLoaded', function() {
    
    

    if (window.location.pathname == '/') {
        const datePicker = document.querySelector('#try-date');
        
        datePicker.addEventListener('click', function() {
            // do something when a nav-link is clicked
            show_availability()
        });
    }

    else {
        // code to execute when on the desired URL
        load_observation();
        /*
        const links = document.querySelectorAll('a[href="/trainingdays/"]');
        for (const link of links) {
            link.addEventListener('click', function() {
            // The link with the desired URL has been clicked, so you can execute your code here
            // Your code goes here
            load_observation();
            });
        }*/
            
        const navLinks = document.querySelectorAll('.nav-link');

        navLinks.forEach(function(navLink) {
            navLink.addEventListener('click', function() {
                // do something when a nav-link is clicked
                change_day(navLink)
            });
        });

        document.querySelector('#edit').addEventListener('click', editObservation);
        document.querySelector('#show').addEventListener('click', saveObservation);
    
    
    }

    
});

function show_availability() {
    
    console.log('show_availability');

    var start_date_missing_input = document.getElementById("start-train").value;
    var end_date_missing_input = document.getElementById("emd-train").value;
    var datecompstart = new Date(start_date_missing_input);
    var datecompend = new Date(end_date_missing_input);
    if (start_date_missing_input === "" || end_date_missing_input === "") {
        document.getElementById("error").innerHTML = "Error: No input provided";

    } else if ( datecompstart.getTime() >= datecompend.getTime() ) {
        document.getElementById("error").innerHTML = "Stard date can't be later then end date";
    } else {
        document.getElementById("error").innerHTML = "";

        console.log(datecompstart);
        console.log(datecompend);
        //const navLinks = document.querySelectorAll('.nav-link');
        class_ids = document.querySelectorAll('#class_id');

        //let list_availables = [];
        //let count = 0;
        let start = []
        let end = []
        let class_id_value = []
        class_ids.forEach(function(class_id) {

            startdate = document.querySelector('#start-train');
            enddate = document.querySelector('#emd-train');
            //class_id = document.querySelector('#class_id');
            //let class_id_value_ele = class_id.getAttribute("href");
            let class_id_value_ele = class_id.innerHTML;
            console.log(class_id_value_ele);

            start_date = startdate.value;
            end_date = enddate.value;
            datelist = [start_date, end_date];

            //console.log(startdate.value);
            //console.log(enddate.value);
            //console.log(csrfToken);
            //console.log(class_id_value);

            let start_ele = start_date.match(/\d+/g);
            let end_ele = end_date.match(/\d+/g);

            start.push(start_ele)
            end.push(end_ele)
            class_id_value.push(class_id_value_ele)
        
        });

        console.log(start);
        console.log(end);
        console.log(class_id_value);

        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        
        fetch('/available', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                startdate: start,
                enddate: end,
                class_id: class_id_value,
                })
            })
            .then(response => response.json())
            .then(result => {
                // Print result
                console.log(result);
                console.log(result.message[0]);
                avails = document.querySelectorAll('#avail');
                idpicks = document.querySelectorAll('#class_id');
                let count = 0;
                avails.forEach(function(avail) {
                    avail.innerHTML = result.message[count];
                    /*
                    if (result.message[count] === "True"){
                        idpicks[count].setAttribute("href", "/{{ class_room.id }}");
                    } else {
                        idpicks[count].removeAttribute("href", "/{{ class_room.id }}");
                    }*/
                        
                    count = count + 1;
                });
                
                //document.querySelector(`#${class_id_value.substring(1)}availability`).innerHTML = result.message;
                //document.querySelector(`#1availability`).innerHTML = result.message;
                //if (result === "True"){
                //    list_availables.push(1);
                //}else{
                //    list_availables.push(0);
                //}
                //console.log(document.querySelectorAll(`#${class_id_value.substring(1)}`));
                //document.querySelectorAll(`#${class_id_value.substring(1)}`).innerHTML = result;
                //const output = result;    
            });
                //document.querySelector(`#${class_id_value.substring(1)}availability`).innerHTML = result.message;

        /*
        console.log(list_availables[1]);
        console.log(list_availables);
        console.log([1,2,3]);

        let count = 0;
        avails = document.querySelectorAll('#availability');
        console.log(avails[1]);
        console.log(avails[2]);
        console.log(avails[3]);

        avails.forEach(function(avail) {
            avail.innerHTML = list_availables[count];
            count = count + 1;
        });

        list_availables.forEach(function(list_available) {
            avails[count].innerHTML = list_available;
            console.log(list_available);
            count = count + 1;
        });*/

        //console.log(output[0]);
        }
}

function load_observation() {
  
    view_blocks = document.querySelectorAll("#post-view");
    view_blocks.forEach(function(view_block) {
        view_block.style.display = 'block';
    });
    edit_blocks = document.querySelectorAll("#edit-view");
    edit_blocks.forEach(function(edit_block) {
        edit_block.style.display = 'none';
    });

    document.querySelector("#show").style.display = 'none';
    document.querySelector("#edit").style.display = 'block';
    //document.querySelector("#PDF").style.display = 'block';
    
}

async function change_day(navLink) {

    console.log('change post');
    
    const navLinkId = navLink.getAttribute('id');
    console.log(navLinkId);

    const navLinks = document.getElementsByClassName('nav-link');

    var url = location.pathname;
    url = url.slice(1, );
    //const lastIndex = url.lastIndexOf('/');
    //const index = url.slice(0, lastIndex).last
    //const endOfUrl = url.substring(url.indexOf('/') + 1);
    const startIndex = url.indexOf('/');
    const endIndex = url.lastIndexOf('/');
    const between = url.substring(startIndex+1, endIndex);

    //console.log(between);

    const form = document.querySelector('#csrf_token');
    const csrfToken = form.value;
    console.log(csrfToken);
    let j = 0;
    for (let i = 4; i < navLinks.length; i++) {
        console.log(navLinks[i]);
        if (navLinks[i].id === navLinkId){
            //if (i === navLinks.length - 1){
            //    j = 999
            //}
            console.log('this is page');
            console.log(between);
            console.log("this is day");
            console.log(j);

            const response = await fetch(`/trainingdays/${between}/${j}`, {
                method: 'GET'
            });

            const html = await response.text();
            //document.body.innerHTML = html;
            
            history.pushState({}, "", `/trainingdays/${between}/${j}`);
            document.body.innerHTML = html;

            const script = document.createElement("script");
            script.src = "/static/training_scheduling/inbox.js";
            document.body.appendChild(script);
            load_observation();
            location.reload(true);

            break
        }

        j = j + 1;
    }
}

function editObservation() {
    view_blocks = document.querySelectorAll("#post-view");
    view_blocks.forEach(function(view_block) {
        view_block.style.display = 'none';
    });
    edit_blocks = document.querySelectorAll("#edit-view");
    edit_blocks.forEach(function(edit_block) {
        edit_block.style.display = 'block';
    });
    document.querySelector("#edit").style.display = 'none';
    document.querySelector("#show").style.display = 'block';
    //document.querySelector("#PDF").style.display = 'none';
    
}

function saveObservation() {

    list_of_ids = []

    var cells = document.querySelectorAll("td:nth-child(5)");

    for (var i = 0; i < cells.length; i++) {
        var value = cells[i].innerHTML;
        //console.log(value);
        list_of_ids.push(value)
    }

    //console.log(list_of_ids.slice(list_of_ids.length/2));
    list_of_ids = list_of_ids.slice(list_of_ids.length/2)

    list_of_inputs = []

    var inputs = document.querySelectorAll("table input");
    CSFR_token = inputs[0].value;
    console.log(CSFR_token);
    var j = 0;
    var list = [];
    for (var i = 2; i < inputs.length; i++) {

        var value = inputs[i].value;
        if (j === 0) {
            if (inputs[i].checked) {
                //console.log('The checkbox is checked.');
                value = 'True'
            } else {
                //console.log('The checkbox is not checked.');
                value = 'False'
            }
            //inputs[i].checked = false;
        };  
        list.push(value);
        //console.log(value);
        //console.log(i);
        
        j = j + 1;

        if (j === 4) {
            list_of_inputs.push(list);
            j = 0;
            list = []; 
        };
        
    };
    //console.log(list_of_inputs);
    console.log(list_of_ids);
    console.log(list_of_inputs);

    fetch('/changeobs', {
        method: 'POST',
        headers: {
            'X-CSRFToken': CSFR_token,
            'Content-Type': 'application/json'
          },
        body: JSON.stringify({ 
            list_of_ids: list_of_ids,
            list_of_inputs: list_of_inputs,
            })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);
        });
    
    location.reload();
    view_blocks = document.querySelectorAll("#post-view");
    view_blocks.forEach(function(view_block) {
        view_block.style.display = 'block';
    });

    edit_blocks = document.querySelectorAll("#edit-view");
    edit_blocks.forEach(function(edit_block) {
        edit_block.style.display = 'none';
    });

    document.querySelector("#show").style.display = 'none';
    document.querySelector("#edit").style.display = 'block';
    document.querySelector("#PDF").style.display = 'block';
    
}
