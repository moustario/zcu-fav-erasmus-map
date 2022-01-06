postUniversity = () => {
    let payload = {
        properties: {},
        geometry: {}
    };
    let properties = document.getElementById('uni-properties').children;
    let geometry = document.getElementById('uni-geometry').children;

    for (index in properties) {
        let prop = properties[index]
        if (!isNaN(prop)) break;

        let key = prop.children[0].innerHTML;
        let value = prop.children[1].value;
        payload.properties[key] = value;
    }

    for (index in geometry) {
        let geo = geometry[index]
        if (!isNaN(geo)) break;

        let key = geo.children[0].innerHTML;
        let value = geo.children[1].value;
        payload.geometry[key] = value;
    }
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/euc/" + payload.properties.EUC, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify((payload)));
}

document.getElementById("btn-save").addEventListener("click", postUniversity);