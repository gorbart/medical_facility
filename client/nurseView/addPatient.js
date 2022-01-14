import { Patient } from "../api/apiClient.js";

var url = "http://127.0.0.1:8000";
var patient = new Patient(url);

async function createPatient(){
    
    const myForm = document.forms['creatingForm'];
    const name = myForm['name'].value;
    const surname = myForm['surname'].value;
    const email = myForm['email'].value;
    const phone = myForm['phone'].value;
    var newPatient ={
        "name": name,
        "surname": surname,
        "email": email,
        "phone_number": phone
    }
    console.log(newPatient);
    await patient.add_patient_data(newPatient);
}
window.createPatient = createPatient;