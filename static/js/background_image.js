document.addEventListener('DOMContentLoaded', function() {

    let currentTime = new Date().getHours();

    if (currentTime >= 5 && currentTime < 7) 
    {
        src = "url('/static/images/dawn_sky.jpg')";
    }
    else if (currentTime >= 7 && currentTime < 17) 
    {
        src = "url('/static/images/day_sky.jpeg')";
    }
    else if (currentTime >= 17 && currentTime < 19) 
    {
        src = "url('/static/images/dusk_sky.jpg')";
    }
    else 
    {
        src = "url('/static/images/night_sky.jpg')";
    }     
    document.body.style.backgroundImage = src;
});