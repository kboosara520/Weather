function currentCity() {
    document.body.style.backgroundImage = 'none';
    document.body.innerHTML = '';
    link = document.querySelector('#my-location');

    function success(position) {
        
        let lat = position.coords.latitude;
        let lon = position.coords.longitude;
        console.log(lat)
        console.log(lon)

        window.location.href = '/city?lat=' + lat + '&lon=' + lon;
    }

    function error() {
        window.location.herf = 'javascript:void(0)';
    }

    navigator.geolocation.getCurrentPosition(success, error);
}