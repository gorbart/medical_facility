import { Patient } from "../api/apiClient.js";

var url = "http://127.0.0.1:8000";

function Disease() {
    this.patient = new Patient(url)
    this.myId = new URLSearchParams(window.location.search).get('id')
    this.date = null
    this.Diseases = null
    this.butt1 = document.getElementById("buttDate");
    this.butt2 = document.getElementById("buttDisease");
    this.butt3 = document.getElementById("buttCreate");
    this.addEventListeners()
}

Disease.prototype.addEventListeners = function(){
    this.butt1.addEventListener("click", this.setDate.bind(this));
    this.butt2.addEventListener("click", this.addDisease.bind(this));
    this.butt3.addEventListener("click", this.createDiseaseHistory.bind(this));
}
  
Disease.prototype.setDate = function(){
    var date = document.getElementById("date");
    this.date = new Date(date.value)
    date.value=null;
}

Disease.prototype.addDisease = function(){
    var diseaseInput = document.getElementById("disease")
    this.Diseases = diseaseInput.value
    diseaseInput.value=null;
}

Disease.prototype.createDiseaseHistory = async function (){

    let newDiseaseHist = {
        "date": this.date,
        "name": this.Diseases
    }
    console.log(newDiseaseHist)
    await this.patient.add_disease(this.myId, newDiseaseHist);
}

var disease = new Disease();