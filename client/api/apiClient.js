import { postData, deleteData, putData, urlSearchParams } from "./base";

export class Patient {
  constructor(baseURL = "http://127.0.0.1:8000") {
    if (baseURL.endsWith("/")) {
      this.baseURL = baseURL + "patients/";
    } else {
      this.baseURL = baseURL + "/patients/";
    }
  }
  async get_patient_list() {
    const response = await fetch(this.baseURL);
    return response.json();
  }
  async add_patient_data(patient = {}) {
    return postData(this.baseURL, patient);
  }
  async get_one_patient(patient_id = "") {
    const url = urlSearchParams(this.baseURL, { patient_id: patient_id });
    const response = await fetch(url);
    return response.json();
  }
  async update_patient_data(patient_id = "", patient = {}) {
    return putData(this.baseURL, patient, { patient_id: patient_id });
  }
  async add_medicine(patient_id = "", medicine_data = {}) {
    return putData(this.baseURL + "add_medicine/", medicine_data, {
      patient_id: patient_id,
    });
  }
  async add_disease(patient_id = "", disease_data = {}) {
    putData(this.baseURL + "add_disease/", disease_data, {
      patient_id: patient_id,
    });
  }
  async delete_patient_data(patient_id = "") {
    deleteData(this.baseURL, { patient_id: patient_id });
  }
}

export class User {
  constructor(baseURL = "http://127.0.0.1:8000") {
    if (baseURL.endsWith("/")) {
      this.baseURL = baseURL + "users/";
    } else {
      this.baseURL = baseURL + "/users/";
    }
  }
  async get_one_user(user_id = "") {
    const url = urlSearchParams(this.baseURL, { user_id: user_id });
    const response = await fetch(url);
    return response.json();
  }
  async get_user_list() {
    const response = await fetch(this.baseURL);
    return response.json();
  }
  async log_in(login = "", password = "") {
    const url = urlSearchParams(this.baseURL, {
      login: login,
      password: password,
    });
    const response = await fetch(url);
    return response.json();
  }
  async add_user_data(patient = {}) {
    return postData(this.baseURL, patient);
  }
  async update_user_data(user_id = "", user = {}) {
    return putData(this.baseURL, user, { user_id: user_id });
  }
  async delete_user_data(user_id = "") {
    return deleteData(this.baseURL, { user_id: user_id });
  }
}

export class Doctor {
  constructor(baseURL = "http://127.0.0.1:8000") {
    if (baseURL.endsWith("/")) {
      this.baseURL = baseURL + "doctors/";
    } else {
      this.baseURL = baseURL + "/doctors/";
    }
  }
  async get_doctors_with_specialty(doctor_specialty = "") {
    const url = urlSearchParams(this.baseURL + "specialty/", {
      doctor_specialty: doctor_specialty,
    });
    const response = await fetch(url);
    return response.json();
  }
  async get_one_doctor(doctor_id = "") {
    const url = urlSearchParams(this.baseURL + "one/", {
      doctor_id: doctor_id,
    });
    const response = await fetch(url);
    return response.json();
  }
  async get_doctor_list() {
    const response = await fetch(this.baseURL);
    return response.json();
  }
  async add_doctor_data(doctor = {}) {
    return postData(this.baseURL, doctor);
  }
  async update_doctor_data(doctor_id = "", doctor = {}) {
    return putData(this.baseURL, doctor, { doctor_id: doctor_id });
  }
  async add_time_period(doctor_id = "", time_period = {}) {
    return putData(this.baseURL + "add_time_period/", time_period, {
      doctor_id: doctor_id,
    });
  }
  async add_appointment(doctor_id = "", appointment = {}) {
    return putData(this.baseURL + "add_appointment/", appointment, {
      doctor_id: doctor_id,
    });
  }
  async delete_doctor_data(doctor_id = "") {
    return deleteData(this.baseURL, { doctor_id: doctor_id });
  }
}
