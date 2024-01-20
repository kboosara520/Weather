let button = document.querySelector('#save');

async function updateSavedList() {
    let savedButton = document.querySelector('#saved_list')
    let toggleSavedButton = document.querySelector('#toggle_button')
    let response = await fetch('/saved_cities');
    let cities = await response.json();
    let html = '';

    if (cities.length == 0) {
        toggleSavedButton.disabled = true;
    } else {
        for (let i in cities) {
            let name = cities[i].name;
            let state = cities[i].state;
            let country = cities[i].country;
    
            if (state === null) {
                string = name + ', ' + country;
            }
            else {
                string = name + ', ' + state + ', ' + country;
            }
            console.log(string);
    
            let id = cities[i].city_id.toString();
    
            html += `<a class="list-group-item" href="/city?id=${id}"><li class="dropdown-item">${string}</li></a>`
        }
        savedButton.innerHTML = html;
        toggleSavedButton.disabled = false;
    }
}

button.addEventListener('click', async function() {
    if (button.classList.contains('btn-light')) {
        fetch(`/save?city_id=${button.value}`)
            .then(response => {
                if (response.ok) {
                    button.classList.remove('btn-light');
                    button.classList.add('btn-dark');
                    button.innerHTML = "Unsave";
                    updateSavedList();
                } else {
                    console.log("error1");
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
        console.log("Save");
    } else if (button.classList.contains('btn-dark')) {
        fetch(`/unsave?city_id=${button.value}`)
            .then(response => {
                if (response.ok) {
                    button.classList.remove('btn-dark');
                    button.classList.add('btn-light');
                    button.innerHTML = "Save";
                    updateSavedList();
                } else {
                    console.log("error1");
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
        console.log("Unsave");
    } else {
        console.log("error");
    }
});