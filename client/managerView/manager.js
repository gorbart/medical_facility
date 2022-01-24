import { Doctor } from "../api/apiClient.js";

var url = "http://127.0.0.1:8000";
var doctor = new Doctor(url);

var tBody = document.getElementById("tableBody");

doctor.get_doctor_list()
    .then(doctors => {
        for (const singleDoctor of doctors){
    
            var row = document.createElement("tr");
            tBody.appendChild(row);
        
            var name = document.createElement("th");
            name.innerText=singleDoctor['name'];
            row.appendChild(name);
            
            var surname = document.createElement("th");
            surname.innerText=singleDoctor['surname'];
            row.appendChild(surname);
            
            var email = document.createElement("th");
            email.innerText=singleDoctor['email'];
            row.appendChild(email);
            
            var phone = document.createElement("th");
            phone.innerText=singleDoctor['phone_number'];
            row.appendChild(phone);

            var Specialties = document.createElement("th");
            // console.log(singleDoctor['specialties'].toString());
            Specialties.innerText=singleDoctor['specialties'] != null ? singleDoctor['specialties'].toString() : null;
            row.appendChild(Specialties);

            var actions = document.createElement("th");
            row.appendChild(actions);
            var delButton = document.createElement("button");
            delButton.innerText = "delete"
            delButton.addEventListener("click",function(){
                deleteDoctor(singleDoctor['id']);
            } , false);
            delButton.className="smallButt";
            actions.appendChild(delButton);
            var edit = document.createElement("a");
            edit.innerText = "edit";
            edit.href = "editDoctor.html?id="+singleDoctor['id'];
            edit.className = "linkInTable"
            actions.appendChild(edit);
        };
        
    })
    .catch((err) => console.log(err));


function addDoctor(){
    location.href = "addDoctor.html"
}

function deleteDoctor(str){
    doctor.delete_doctor_data(str)
    location.reload();
}

window.addDoctor = addDoctor;