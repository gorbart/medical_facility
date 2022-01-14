import { Patient } from "../api/apiClient.js";

var url = "http://127.0.0.1:8000";

function Medicine() {
    this.patient = new Patient(url)
    this.myId = new URLSearchParams(window.location.search).get('id')
    this.date = null
    this.MedcinesArr = []
    this.butt1 = document.getElementById("buttDate");
    this.butt2 = document.getElementById("buttMedicine");
    this.butt3 = document.getElementById("buttCreate");
    this.addEventListeners()
}

Medicine.prototype.addEventListeners = function(){
    this.butt1.addEventListener("click", this.setDate.bind(this));
    this.butt2.addEventListener("click", this.addMedicine.bind(this));
    this.butt3.addEventListener("click", this.createMedicinesTaken.bind(this));
}
  
Medicine.prototype.setDate = function(){
    var date = document.getElementById("date");
    this.date = new Date(date.value)
    date.value=null;
}

Medicine.prototype.addMedicine = function(){
    var medicineInput = document.getElementById("medicine")
    var untilInput = document.getElementById("until")
    let untilDate = new Date(untilInput.value)
    if(this.date == null){
        alert("Please enter Date from, first")
    }
    else{
        if(this.date.getTime() > untilDate.getTime()){
            alert("Entered data are incorect. Dates of starting supplementation of medicine should be earlier than ending supplementation")
        }
        else{
            this.MedcinesArr.push({
                "name" : medicineInput.value, 
                "until" : untilDate
            })
            medicineInput.value = null
            untilInput.value = null
        }
    }
}

Medicine.prototype.createMedicinesTaken = async function (){

    let newMedicineHist = {
        "date": this.date,
        "medicines": this.MedcinesArr
    }
    await this.patient.add_medicine(this.myId, newMedicineHist);
}

var medicine = new Medicine();