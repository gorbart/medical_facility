import { Patient, Doctor, User } from "./api/apiClient.js";

var url = "http://127.0.0.1:8000";
var user = new User(url);

function authorisation(response){
  var id = response[0];
  var type = response[1];
  if (type == 0){
    location.href = "admin.html"
  }
  else if (type == 1){
    location.href = "manager.html"
  }
  else if (type == 2){
    location.href = "nurseDoctors.html"
  }
  else{
    alert('Entered login or password are incorrect');
  }
}

function authentication(){
  const myForm = document.forms['myForm'];
  const login = myForm['login'].value;
  const password = myForm['password'].value;
  console.log(login);
  const login_return = user
    .log_in(login, password)
    .then((response) => {
        authorisation(response);
    })
    .catch((err) => console.log(err));
}





    
