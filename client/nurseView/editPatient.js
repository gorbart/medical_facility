import { Patient } from "../api/apiClient.js";

var url = "http://127.0.0.1:8000";
var patient = new Patient(url);

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const myId = urlParams.get('id')
if (myId != null){
    patient.get_one_patient(myId)
        .then(editingPatient =>{
            fillFieldsWithPatientData(editingPatient);
        })
        .catch((err) => console.log(err));
}
else{
    location.href = "nursePatientView.html"
}


function fillFieldsWithPatientData(editingPatient){
    document.getElementById("idname").value = editingPatient['name'];
    document.getElementById("idsurname").value = editingPatient['surname'];
    document.getElementById("idemail").value = editingPatient['email'];
    document.getElementById("idphone").value = editingPatient['phone_number'];
}

function savePatientData(){
    const myForm = document.forms['editForm'];
    const name = myForm['name'].value;
    const surname = myForm['surname'].value;
    const email = myForm['email'].value;
    const phone = myForm['phone'].value;
    var newPatient ={
        "name": name,
        "surname": surname,
        "email": email,
        "phone_number": phone,
    }
    console.log(newPatient);
    patient.update_patient_data(myId, newPatient);
}

window.savePatientData = savePatientData;