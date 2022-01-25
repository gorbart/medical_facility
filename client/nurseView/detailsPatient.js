import { Patient } from "../api/apiClient.js";

var url = "http://127.0.0.1:8000";
var patient = new Patient(url);

const myId = new URLSearchParams(window.location.search).get('id')
var diseaseTable = document.getElementById("diseaseTable");
var medicineTable = document.getElementById("medicneTable");

patient.get_one_patient(myId)
    .then(myPatient => {
        let diseasesHist = myPatient.disease_history
        for (let i=0; i<diseasesHist.length;i++){
            //na relacyjnej bazie mozna to posortowac,bedzie latwiej
            var row = document.createElement("tr");
            diseaseTable.appendChild(row);

            var disease = document.createElement("th");
            disease.innerText=diseasesHist[i]['name'];
            row.appendChild(disease);

            var date = document.createElement("th");
            let wholeDate = new Date(diseasesHist[i]['date']);
            let formatedDate = wholeDate.getDate() + "." + (parseInt(wholeDate.getMonth())+1).toString() + "." + wholeDate.getFullYear(); 
            date.innerText = formatedDate;
            row.appendChild(date);
        }

        let medicineTaken = myPatient.medicine_taken
        for (let i=0; i<medicineTaken.length;i++){
            let from = new Date(medicineTaken[i]['date'])
            let fromFormatedDate = from.getDate() + "." + (parseInt(from.getMonth())+1).toString() + "." + from.getFullYear(); 
                
            for(let j=0; j<medicineTaken[i].medicines.length; j++){
                //na relacyjnej bazie mozna to posortowac,bedzie latwiej
                var row = document.createElement("tr");
                medicineTable.appendChild(row);

                var medicine = document.createElement("th");
                medicine.innerText=medicineTaken[i].medicines[j]['name'];
                row.appendChild(medicine);

                var dateFrom = document.createElement("th");
                dateFrom.innerText = fromFormatedDate;
                row.appendChild(dateFrom);


                var until = document.createElement("th");
                let wholeDate = new Date(medicineTaken[i].medicines[j]['until']);
                let formatedDate = wholeDate.getDate() + "." + (parseInt(wholeDate.getMonth())+1).toString() + "." + wholeDate.getFullYear(); 
                until.innerText = formatedDate;
                row.appendChild(until);
            }
        }
        
    })
    .catch((err) => console.log(err));

function addMedicine(){
    location.href = "addMedicine.html?id="+ myId;
}

function addDisease(){
    location.href = "addDisease.html?id="+ myId;
}

window.addMedicine = addMedicine;
window.addDisease = addDisease;