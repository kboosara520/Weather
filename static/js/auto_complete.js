let input = document.querySelector('input');
input.addEventListener('input', async function() {
    let city = input.value.replace(/ /g, '');

    console.log(city);

    let response = await fetch('/search?city=' + city);

    console.log(response);

    let cities = await response.json();

    console.log(cities);

    let html = '';

    for (let index in cities) {
        let name = cities[index].name;
        let state = cities[index].state;
        let country = cities[index].country;

        if (state === null) {
            string = name + ', ' + country;
        }
        else {
            string = name + ', ' + state + ', ' + country;
        }

        console.log(string);
        let id = cities[index].city_id.toString();

        html += '<a class="list-group-item list-group-item-action no-border" href="/city?id=' + id + '">' + string + '</a>'
    }

    document.querySelector('#selections').innerHTML = html;
});