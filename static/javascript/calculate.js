const button = document.getElementById("button");

var real = document.getElementById("real_number");
var imaginary = document.getElementById("imaginary_number");
var zoom = document.getElementById("zoom");
var iterations = document.getElementById("iterations");

var image = document.getElementById("mandlebrot");

button.onclick = () => {
    console.log(real.value);
    
}

button.addEventListener("click", function(){
    
    
    fetch("http://127.0.0.1:5000/calculate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({"real": real.value, "imaginary": imaginary.value, "zoom": zoom.value, "iterations": iterations.value})
    }).then(async response => {
        if(response.ok){
            response.text().then(async result => {
                image.src = "data:image/png;base64, " + result
                return
            })
        }
        throw new Error('Request failed!');
    }, networkError => {
        console.log(networkError.message);
    })
});
