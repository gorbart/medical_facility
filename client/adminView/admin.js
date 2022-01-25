import { User } from "../api/apiClient.js";

var url = "http://127.0.0.1:8000";
var user = new User(url);

var tBody = document.getElementById("tableBody");

user.get_user_list()
    .then(users => {
        for (const singleUser of users){
    
            var row = document.createElement("tr");
            tBody.appendChild(row);
        
            var name = document.createElement("th");
            name.innerText=singleUser['name'];
            row.appendChild(name);
            
            var surname = document.createElement("th");
            surname.innerText=singleUser['surname'];
            row.appendChild(surname);
            
            var email = document.createElement("th");
            email.innerText=singleUser['email'];
            row.appendChild(email);
            
            var phone = document.createElement("th");
            phone.innerText=singleUser['phone_number'];
            row.appendChild(phone);
            
            var typeCell = document.createElement("th");
            var type = singleUser['user_type'];
            if (type == "UserType.ADMIN"){  
                typeCell.innerText="Admin";
            }
            else if (type == "UserType.MANAGER"){
                typeCell.innerText="Manager";
            }
            else if (type == "UserType.NURSE"){
                typeCell.innerText="Nurse";
            }
            row.appendChild(typeCell);
        
            var login = document.createElement("th");
            login.innerText=singleUser['login'];
            row.appendChild(login);
            
            var password = document.createElement("th");
            password.innerText=singleUser['password'];
            row.appendChild(password);
            
            
            var actions = document.createElement("th");
            row.appendChild(actions);
            var delButton = document.createElement("button");
            delButton.innerText = "delete"
            var userType = null
            if(singleUser['user_type'] == "UserType.NURSE"){
                userType = "nurse"
            }
            else if (singleUser['user_type']== "UserType.ADMIN"){
                userType = "admin"
            }
            else if (singleUser['user_type']== "UserType.MANAGER"){
                userType = "manager"
            }
            delButton.addEventListener("click",function(){
                deleteUser(singleUser['login'], userType);
            } , false);
            delButton.className="smallButt";
            actions.appendChild(delButton);
            var edit = document.createElement("a");
            edit.innerText = "edit";
            edit.href = "editUser.html?login="+singleUser['login'] + "&" + "userType=" + userType;
            edit.className = "linkInTable"
            actions.appendChild(edit);
        };
        
    })
    .catch((err) => console.log(err));


function addUser(){
    location.href = "addUser.html"
}

function deleteUser(login, type){
    user.delete_user_data(login, type)
    location.reload();
}

window.addUser = addUser;