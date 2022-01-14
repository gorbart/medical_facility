import { User } from "../api/apiClient.js";

var url = "http://127.0.0.1:8000";
var user = new User(url);

var tBody = document.getElementById("tableBody");

user.get_user_list()
    .then(response => {
        return JSON.parse(response);
    })
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
            if (type == 0){  
                typeCell.innerText="Admin";
            }
            else if (type == 1){
                typeCell.innerText="Manager";
            }
            else if (type == 2){
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
            delButton.addEventListener("click",function(){
                deleteUser(singleUser['_id'].$oid);
            } , false);
            delButton.className="smallButt";
            actions.appendChild(delButton);
            var edit = document.createElement("a");
            edit.innerText = "edit";
            edit.href = "editUser.html?id="+singleUser['_id'].$oid;
            edit.className = "linkInTable"
            actions.appendChild(edit);
        };
        
    })
    .catch((err) => console.log(err));


function addUser(){
    location.href = "addUser.html"
}

function deleteUser(str){
    user.delete_user_data(str)
    location.reload();
}

window.addUser = addUser;