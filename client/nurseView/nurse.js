import { Doctor } from "../api/apiClient.js";

var url = "http://127.0.0.1:8000";
var doctor = new Doctor(url);

var tBody = document.getElementById("tableBody");

function showView(filter){
    doctor.get_doctor_list()
    .then(doctors => {
        tBody.innerHTML = ''
        
        for (const singleDoctor of doctors){
            if(filter != null && filter != "All"){
                if(singleDoctor['specialties'] == null){
                    continue
                }
                let tmp = singleDoctor['specialties'].indexOf(filter)
                if(tmp == -1){
                    console.log(filter)
                    continue
                }
            }
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
            Specialties.innerText=singleDoctor['specialties'] != null ? singleDoctor['specialties'].toString() : null;
            row.appendChild(Specialties);

            var actions = document.createElement("th");
            row.appendChild(actions);
            var details = document.createElement("a");
            details.innerText = "appointments";
            details.href = "scheduleDoctor.html?id="+singleDoctor['id'];
            details.className = "linkInTable"
            actions.appendChild(details);
            
            var addSchedule = document.createElement("a");
            addSchedule.innerText = " schedules";
            addSchedule.href = "addSchedule.html?id="+singleDoctor['id'];
            addSchedule.className = "linkInTable"
            actions.appendChild(addSchedule);
        };
        
    })
    .catch((err) => console.log(err));

}
showView(null)

function patientsView(){
    location.href = "nursePatientView.html"
}

function Filtr(){
    var select = document.getElementById('myFilter');
    var value = select.options[select.selectedIndex].value;
    showView(value)
    
}

window.patientsView = patientsView;

window.Filtr = Filtr;