import { User } from "../api/apiClient.js";

var url = "http://127.0.0.1:8000";
var user = new User(url);

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const myLogin = urlParams.get('login')
const myUserType = urlParams.get('userType')
if (myLogin != null && myUserType != null){
    user.get_one_user(myLogin, myUserType)
        .then(editingUser =>{
            fillFieldsWithUserData(editingUser);
        })
        .catch((err) => console.log(err));
}
else{
    location.href = "admin.html"
}


function fillFieldsWithUserData(editingUser){
    document.getElementById("idname").value = editingUser['name'];
    document.getElementById("idsurname").value = editingUser['surname'];
    document.getElementById("idemail").value = editingUser['email'];
    document.getElementById("idphone").value = editingUser['phone_number'];
    document.getElementById("selector").value = myUserType;
    document.getElementById("idlogin").value = editingUser['login'];
    document.getElementById("idpassword").value = editingUser['password'];
}

function saveUserData(){
    const myForm = document.forms['editForm'];
    const name = myForm['name'].value;
    const surname = myForm['surname'].value;
    const email = myForm['email'].value;
    const phone = myForm['phone'].value;
    const type = myForm['type'].value;
    const login = myForm['login'].value;
    const password = myForm['password'].value;
    var newUser ={
        "name": name,
        "surname": surname,
        "email": email,
        "phone_number": phone,
        "login": login,
        "password": password,
        "user_type": type
    }
    user.update_user_data(myLogin, myUserType, newUser);
}

window.saveUserData = saveUserData;