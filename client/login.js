import { Patient, Doctor, User } from "./api/apiClient.js";

var url = "http://127.0.0.1:8000";
var user = new User(url);
var type = new URLSearchParams(window.location.search).get('type')
console.log(type)
function authorisation(response){
  console.log(response);
  if (type == "admin"){
    location.href = "admin.html"
  }
  else if (type == "manager"){
    location.href = "manager.html"
  }
  else if (type == "nurse"){
    location.href = "nurse.html"
  }
}
//sytuacja niepoprawnego logowania nie zostala jeszcze obsluzona
async function authentication(){
  const myForm = document.forms['myForm'];
  const login = myForm['login'].value;
  const password = myForm['password'].value;
  user.log_in(login, password, type)
    .then((response) => {
      authorisation(response);
    })
    .catch((err) => {
      console.log(err);
     // alert('Entered login or password are incorrect');
    });
}




window.authentication = authentication;
      // authorisation(response);




    
