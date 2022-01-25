import { Doctor } from "../api/apiClient.js";

var url = "http://127.0.0.1:8000";
var doctor = new Doctor(url);

async function createDoctor(){
    
    const myForm = document.forms['creatingForm'];
    const name = myForm['name'].value;
    const surname = myForm['surname'].value;
    const email = myForm['email'].value;
    const phone = myForm['phone'].value;
    // const specialities = myForm['specialities'].value;
    const specArr = [];
    let selectField = document.forms[0].specialities;
    for (let i=0; i<selectField.options.length;i++){
        if(selectField.options[i].selected){
            specArr.push(selectField.options[i].value);
        }
    }
    var newDoctor ={
        "name": name,
        "surname": surname,
        "email": email,
        "phone_number": phone
    }
    console.log(specArr);
    console.log(newDoctor)
    await doctor.add_doctor_data(newDoctor, specArr);
}
window.createDoctor = createDoctor;