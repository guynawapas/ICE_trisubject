const queryString = window.location.search;

const urlParams = new URLSearchParams(queryString);

const image_url = urlParams.get('img');
console.log(image_url);

const div_image = document.getElementById('image');
var img = document.createElement("img");
img.setAttribute("id","data");
img.setAttribute("src",image_url);
div_image.appendChild(img);

