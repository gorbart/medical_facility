import { Patient } from "../api/apiClient.js";

var url = "http://127.0.0.1:8000";
var patient = new Patient(url);

var tBody = document.getElementById("tableBody");

patient.get_patient_list()
    .then(response => {
        return JSON.parse(response);
    })
    .then(patients => {
        for (const singlePatient of patients){
    
            var row = document.createElement("tr");
            tBody.appendChild(row);
        
            var name = document.createElement("th");
            name.innerText=singlePatient['name'];
            row.appendChild(name);
            
            var surname = document.createElement("th");
            surname.innerText=singlePatient['surname'];
            row.appendChild(surname);
            
            var email = document.createElement("th");
            email.innerText=singlePatient['email'];
            row.appendChild(email);
            
            var phone = document.createElement("th");
            phone.innerText=singlePatient['phone_number'];
            row.appendChild(phone);

            var actions = document.createElement("th");
            row.appendChild(actions);

            var edit = document.createElement("a");
            edit.innerText = "edit";
            edit.href = "editPatient.html?id="+singlePatient['_id'].$oid;
            edit.className = "linkInTable";
            actions.appendChild(edit);

            var delButton = document.createElement("button");
            delButton.innerText = "delete"
            delButton.addEventListener("click",function(){
                deletePatient(singlePatient['_id'].$oid);
            } , false);
            delButton.className="smallButt";
            actions.appendChild(delButton);
            
            var details = document.createElement("a");
            details.innerText = "details";
            details.href = "detailsPatient.html?id="+singlePatient['_id'].$oid;
            details.className = "linkInTable";
            details.id = "detailPatientLink";
            actions.appendChild(details);
        };
        
    })
    .catch((err) => console.log(err));

function deletePatient(str){
    patient.delete_patient_data(str)
    location.reload();
}

function mainView(){
    location.href = "nurse.html"
}

function addPatient(){
    location.href = "addPatient.html"
}

window.mainView = mainView;
window.addPatient = addPatient;