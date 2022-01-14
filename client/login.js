import { Patient, Doctor, User } from "./api/apiClient.js";

var url = "http://127.0.0.1:8000";
var user = new User(url);

function authorisation(response){
  console.log(response);
  var id = response['id'];
  var type = response['user_type'];
  if (type == 0){
    location.href = "admin.html"
  }
  else if (type == 1){
    location.href = "manager.html"
  }
  else if (type == 2){
    location.href = "nurse.html"
  }
  else{
    alert('Entered login or password are incorrect');
  }
}

async function authentication(){
  const myForm = document.forms['myForm'];
  const login = myForm['login'].value;
  const password = myForm['password'].value;
  user.log_in(login, password)
    .then(response => {
      return JSON.parse(response);
    })
    .then((response) => {
      authorisation(response);
    })
    
    .catch((err) => console.log(err));
}




window.authentication = authentication;
      // authorisation(response);




    
