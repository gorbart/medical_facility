import { Doctor } from "../api/apiClient.js";

var url = "http://127.0.0.1:8000";
var doctor = new Doctor(url);

var specArr = null;
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const myId = urlParams.get('id')
if (myId != null){
    doctor.get_one_doctor(myId)
        .then(response => {
            return JSON.parse(response);
        })
        .then(editingDoctor =>{
            fillFieldsWithDoctorData(editingDoctor);
        })
        .catch((err) => console.log(err));
}
else{
    location.href = "manager.html"
}


function fillFieldsWithDoctorData(editingDoctor){
    document.getElementById("idname").value = editingDoctor['name'];
    document.getElementById("idsurname").value = editingDoctor['surname'];
    document.getElementById("idemail").value = editingDoctor['email'];
    document.getElementById("idphone").value = editingDoctor['phone_number'];
    //wychodze z założenia ze nie można stracic specjalności, więc nie wyswietlam tych ktore mial zapisane,
    //jezeli uzytkownik wybierze jakas specjalnosc dodatkowa to po prostu sie doda, jak nie wybierze nic,
    //to pozostanie bez zmian
    specArr = editingDoctor['specialties'];
}

function saveDoctorData(){
    const myForm = document.forms['editForm'];
    const name = myForm['name'].value;
    const surname = myForm['surname'].value;
    const email = myForm['email'].value;
    const phone = myForm['phone'].value;
    console.log(specArr);
    let selectField = document.forms[0].Specialities;
    for (let i=0; i<selectField.options.length;i++){
        if(selectField.options[i].selected){
            specArr.push(selectField.options[i].value);
        }
    }
    console.log(specArr);
    var newDoctor ={
        "name": name,
        "surname": surname,
        "email": email,
        "phone_number": phone,
        "specialties": specArr
    }
    console.log(newDoctor);
    doctor.update_doctor_data(myId, newDoctor);
}

window.saveDoctorData = saveDoctorData;