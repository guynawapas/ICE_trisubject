const queryString = window.location.search;

const urlParams = new URLSearchParams(queryString);

const amount = urlParams.get('amount');


const div_amount = document.getElementById('amount');
var img = document.createElement("p");
img.setAttribute("id","data");
img.innerHTML = amount;
div_amount.appendChild(img);

