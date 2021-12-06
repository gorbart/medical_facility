Wszystkie funkcje zwracają response.json() otrzymane z api więc wartość zwracana przez funkcje to gotowy do użycia obiekt JSON

Można korzystać w ten sposób:
```javascript
import { Patient, Doctor, User } from "./api/apiClient.js";
//następnie
var url = "http://127.0.0.1:8000"; // <== domyślna wartość dla url
var doctor = new Doctor(url);
var patient = new Patient(url);
var user = new User(url);

//potem można używać:

const doctor_list = doctor
  .get_doctor_list()
  .then((response) => {
    zrob_cos(response);
  })
  .catch((err) => console.log(err));
```

Aby można było tak tego używać i chrome wiedział o co chodzi to trzeba to dołączyć do html w taki sposób:
```html
    <script type="module" src="./main.js"></script>
```