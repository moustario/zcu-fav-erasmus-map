var mymap = L.map('mapid').setView([55, 20], 4);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mymap);

var markers = L.markerClusterGroup();

// Coloring of point characters of departments
function getColor(d) {
    return d == 'KIV' ? 'green' :
        d == 'KMA' ? "blue" :
        d == 'KGM' ? "yellow" :
        d == 'KKY' ? "black" :
        d == 'KME' ? "purple" :
        d == 'KFY' ? "red" :
        "#ff7f00";
}

// Population info DIV information from geojson by properties feature.properties
function onEachFeature(feature, layer) {
    layer.katedra = feature.properties.katedra;
    let popupContent = feature.properties['Name of institute (EN)'];
    popupContent += "</br> <b>EUC : </b>" + feature.properties['EUC'];
    popupContent += "</br> <b>City : </b>" + feature.properties['City'];
    popupContent += "</br> <b>Language : </b>" + feature.properties['Language of Instruction 1'];
    popupContent += "</br> <b>Level : </b>" + feature.properties['Student Mobility for Studies - Level'];
    popupContent += "</br> <a href=" + feature.properties['ECTSWebsite'] + ">Website</a>";
    popupContent += "</br> <a href=/euc/" + feature.properties['EUC'].split('.').join('-') + ">More Information</a>";
    layer.bindPopup(popupContent);
}

// point layer with all departments styled according to the colors defined above
var body = L.geoJson(geobody, {
    pointToLayer: (feature, latlng) => {
        return L.circleMarker(latlng, {
            radius: 8,
            fillColor: getColor(feature.properties.katedra),
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        });
    },
    onEachFeature: onEachFeature
});
body.addTo(markers);


// display the legend in the map at the top right
var legend = L.control({ position: 'topright' });
legend.onAdd = function(mymap) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = ['KIV', 'KMA', 'KGM', 'KKY', 'KME', 'KFY'],
        labels = [],
        labels2 = ['KIV: Katedra informatiky a výpočetní techniky', 'KMA: Katedra matematiky', 'KGM: Katedra geomatiky', 'KKY: Katedra kybernetiky', 'KME: Katedra mechaniky', 'KFY: Katedra fyziky'];

    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            labels.push(
                '<i class="circle" style="background:' + getColor(grades[i]) + '"></i>' + (grades[i] ? labels2[i] : '+'));
    }

    div.innerHTML = labels.join('<br>');
    return div;
};
legend.addTo(mymap);


// Button to show all departments on the map
document.getElementById("vsechny").addEventListener("click", addVsechny);

function addVsechny() {
    markers.addLayer(body);
    mymap.setView([55, 20], 4);
    elements.forEach(faculty => {
        document.getElementById(faculty).checked = true;
    })
};


// Binding faculty button to display on map
elements = ["kiv", "kma", "kgm", "kky", "kme", "kfy"];
elements.forEach(faculty => {
    document.getElementById(faculty).addEventListener("click", () => {

        if (document.getElementById(faculty).checked) {
            var fac = L.geoJson(geobody, {
                filter: (feature, layer) => {
                    return feature.properties.katedra == faculty.toUpperCase();
                },
                pointToLayer: (feature, latlng) => {
                    return L.circleMarker(latlng, {
                        radius: 8,
                        fillColor: getColor(feature.properties.katedra),
                        color: "#000",
                        weight: 1,
                        opacity: 1,
                        fillOpacity: 0.8
                    });
                },
                onEachFeature: onEachFeature
            });
            markers.addLayer(fac);
        } else {
            odebrat({}, faculty.toUpperCase());
        }
    })
});

// on load every check box is ticked
elements.forEach(faculty => {
    document.getElementById(faculty).checked = true;
});

// Button to remove all departments from the map
document.getElementById("nic").addEventListener("click", odebrat);

function odebrat(event, filter = "none") {
    mymap.eachLayer((layer) => {
        if (filter != "none") {
            if (layer.katedra == filter) {
                markers.removeLayer(layer);
                document.getElementById(filter.toLocaleLowerCase()).checked = false;
            }
        } else {
            markers.removeLayer(layer);
            elements.forEach(faculty => {
                document.getElementById(faculty).checked = false;
            })
        }
    });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(mymap);
    mymap.setView([55, 20], 4);
};

// Marker cluster handling
mymap.addLayer(markers);

// adding scale to map
L.control.scale({
    metric: true,
    imperial: false,
}).addTo(mymap);