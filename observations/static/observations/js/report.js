(function() {
    var map;
    var initial_bounds = [
        [49.674000000000049, -14.015517000000013],
        [61.061000000000064, 2.091911700000002]
    ];
    
    function updateMap() {
        var postcode = $("#postcode").val();
        $.getJSON(GEOCODE_URL, {postcode: postcode, full: true}, function(data) {
            console.log(data);
        })
    }
    
    $(function() {
        map = L.map("map").fitBounds(initial_bounds);
        
        L.tileLayer(
            'http://{s}.tile.cloudmade.com/{api_key}/997/256/{z}/{x}/{y}.png',
            {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
                maxZoom: 18,
                api_key: CLOUDMADE_API_KEY
            }
        ).addTo(map);
        
        $("#updatemap").click(updateMap);
    })
})();