import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Socket } from 'ngx-socket-io';
import { map } from 'rxjs/operators';

const baseUrl = 'http://solarboat.ddns.net:5001/';
const influxUrl = 'http://solarboat.ddns.net:8086/query?db=SolarBoat';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient, private socket: Socket) { }

  sendMessage(msg: string, topic: string) {
    this.socket.emit(topic, msg);
  }

  getAlarm() {
    return this.socket
      .fromEvent("ALARMA")
      .pipe(map((data) => data));
  }

  sendAction(message) {
    return this.sendMessage(message, "SEND_ACTION");
  }

  sendCustomAlarm() {
    return this.sendMessage("custom alarm", "CUSTOM_ACTION");
  }

  clearDatabase() {
    return this.sendMessage("Clear Database", "CLEAR_DATABASE");
  }

  sendHttpQuery(query: string) {
    return this.http.get(influxUrl + '&q=' + query);
  }


}
