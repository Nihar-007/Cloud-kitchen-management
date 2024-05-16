const getLocation = () => {
    fetch("https://ipapi.co/json")
        .then((res) => res.json())
        .then((data) => {
            console.log(data)
            const des = document.getElementById("ip");
            des.innerHTML = `Latitude: ${data.latitude} Longitude: ${data.longitude}`;
        });
    fetch("https://api.bigdatacloud.net/data/client-ip")
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
        const des = document.getElementById("ip");
        des.innerHTML = `IPV4: ${data.ipString}`;
        let ip = data.ipString
        console.log(typeof ip)
        $.ajax({
        url : '/home',
        method : 'POST',
        data : {ip : ip},
        success : function(result){
            console.log("Success")
        }
        });
    });
};