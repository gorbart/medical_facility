import { User } from "../api/apiClient.js";

var url = "http://127.0.0.1:8000";
var user = new User(url);

async function createUser(){

    const myForm = document.forms['creatingForm'];
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
    await user.add_user_data(newUser);
}


window.createUser = createUser;