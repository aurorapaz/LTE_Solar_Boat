import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

const baseUrl = 'http://localhost:5000/';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  getSpeedStatus() {
    var speedLimits = {
      speed_manual: "25",
      speed_automatic: "10",
      speed_warning: "20"
    };

    return this.http.post(baseUrl + "speedStatus",speedLimits)
  }

  getHeigthStatus() {
    var heigthLimits = {
      heigth_manual: "200",
      heigth_automatic: "300"
    };

    return this.http.post(baseUrl + "heigthStatus",heigthLimits);
  }

  getRollStatus() {
    var rollLimits = {
      roll_manual: "20",
      roll_automatic: "30"
    };

    return this.http.post(baseUrl + "rollStatus", rollLimits);
  }

  getPitchStatus() {
    var pitchLimits = {
      pitch_manual: "20",
      pitch_automatic: "30"
    };

    return this.http.post(baseUrl + "pitchStatus",pitchLimits);
  }

  sendAction(message){
    var payload = {"message": message};
    return this.http.post(baseUrl + "sendAction",payload);
  }

  sendCustomAlarm() {
    return this.http.get(baseUrl + "sendCustomAlarm");
  }

}
