import { Doctor } from "../api/apiClient.js";

var url = "http://127.0.0.1:8000";

function Schedule() {
    this.doctor = new Doctor(url)
    this.myId = new URLSearchParams(window.location.search).get('id')
    this.date = null
    this.until = null
    this.workingHours = []
    this.butt1 = document.getElementById("buttPeriod");
    this.butt2 = document.getElementById("buttWH");
    this.butt3 = document.getElementById("buttCreate");
    this.addEventListeners()
}

Schedule.prototype.addEventListeners = function(){
    this.butt1.addEventListener("click", this.addTimePeriod.bind(this));
    this.butt2.addEventListener("click", this.addWorkingHour.bind(this));
    this.butt3.addEventListener("click", this.createSchedule.bind(this));
}
  
Schedule.prototype.addTimePeriod = function(){
    var now = new Date()
    var dateFrom = document.getElementById("periodFrom");
    this.date = new Date(dateFrom.value)
    var dateUntil = document.getElementById("periodUntil");
    this.until = new Date(dateUntil.value)
    if(this.date.getTime() < now.getTime() || this.date.getTime()>this.until.getTime()){
        this.date = null
        this.until = null
        alert("Entered data are incorect. Dates cannot be past, and Time period from should be earlier than time period until ")
    }
    else{
        dateFrom.value = null
        dateUntil.value = null
    }
}

Schedule.prototype.addWorkingHour = function(){
    var input1 = document.getElementById("day")
    var input2 = document.getElementById("startWork")
    var input3 = document.getElementById("endWork")
    var day = new Date(input1.value);
    var now = new Date()
    var start = input2.value;
    var end = input3.value;
    var startingWork = new Date(day.getFullYear(), day.getMonth(), day.getDate(), start[0] + start[1], start[3]+start[4])
    var endingWork = new Date(day.getFullYear(), day.getMonth(), day.getDate(), end[0] + end[1], end[3]+end[4])
    
    if(startingWork.getTime() < now.getTime() || startingWork.getTime()>endingWork.getTime()){
        alert("Entered data are incorect. Dates cannot be past, and Doctor should start his work before he ends it")
    }
    else{
        this.workingHours.push({
            "date" : startingWork, 
            "until" : endingWork
        })
        input1.value = null
        input2.value = null
        input3.value = null
    }
}

Schedule.prototype.createSchedule = async function (){
    for (let i=0; i<this.workingHours.length;i++){
        if(this.workingHours[i].date.getTime() < this.date.getTime() ||
         this.workingHours[i].until.getTime() > this.until.getTime()){
            this.workingHours.splice(i,1)
         }
    }
    for (let i=0; i<this.workingHours.length;i++){
        let mainWH = this.workingHours[i]
        for (let j=i+1; j<this.workingHours.length;j++){
            let iteratedWH = this.workingHours[j]
            //sprawdzam czy ten sam dzien
            if(mainWH.date.getDate() == iteratedWH.date.getDate()){
                //sprawdzam czy sie jedno zawarte w drugim
                if(mainWH.date.getTime() < iteratedWH.date.getTime() && 
                mainWH.until.getTime() > iteratedWH.until.getTime()){
                    this.workingHours.splice(j,1)
                }
                else if(mainWH.date.getTime() > iteratedWH.date.getTime() && 
                mainWH.until.getTime() < iteratedWH.until.getTime()){
                    this.workingHours.splice(i,1)
                }
                //sprawdzam czy sie przeplata
                else if(mainWH.until.getTime() > iteratedWH.date.getTime() && 
                    mainWH.date.getTime() < iteratedWH.date.getTime()){
                    this.workingHours[i].until = this.workingHours[j].until;
                    this.workingHours.splice(j,1)
                }
                else if (iteratedWH.until.getTime() > mainWH.date.getTime() &&
                iteratedWH.date.getTime() < mainWH.date.getTime()){
                    this.workingHours[i].date = this.workingHours[j].date;
                    this.workingHours.splice(j,1)
                }

            }
        }
        if(this.workingHours[i].date.getTime() < this.date.getTime() ||
         this.workingHours[i].until.getTime() > this.until.getTime()){
            this.workingHours.splice(i,1)
         }
    }

    let newSchedule = {
        "date": this.date,
        "until": this.until,
        "workingHours": this.workingHours
    }
    console.log(newSchedule)
    await this.doctor.add_time_period(this.myId, newSchedule);
}

var schedule = new Schedule();