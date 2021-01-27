import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { interval, Subscription } from 'rxjs';
import { ToastrService } from 'ngx-toastr';
import { CustomToast } from './custom.toast';

import { HttpClient } from '@angular/common/http';

import {formatDate } from '@angular/common';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})


export class HomeComponent implements OnInit {

  constructor(private apiService: ApiService, private toastService: ToastrService, private http: HttpClient) { }
  subscription: Subscription;
  textarea;


  ngOnInit(): void {
    // const source = interval(500);
    // this.subscription = source.subscribe(val => this.checkSocket());
    this.checkSocket();
    this.textarea = <HTMLInputElement>document.getElementById('log');

  }

  clearDatabase() {
    this.apiService.sendHttpQuery('DELETE FROM solar_sensor').subscribe(data => {
      console.log('Database cleared');
      this.newConsoleLog("Database cleared");
		});
  }

  checkSocket() {
    this.apiService.getAlarm().subscribe(data => {
      this.parseData(data);
    });
  }

  showAlert(text) {
    this.toastService.warning(text, "ALERT", {
      timeOut: 4000, progressBar: true, closeButton: true, tapToDismiss: false, positionClass: 'toast-bottom-right',
    });
  }

  parseData(data) {
	  //console.log(data);
    if (data["alert_message"] != "All normal") {
      if (data["alert_message"].startsWith("Alarma automatica")){
        this.showAlert(data["alert_message"]);
        this.newConsoleLog(data["alert_message"]);
      } else if (data["alert_message"].startsWith("Alarma manual"))
        this.showToast(data["alert_message"], data["alert_message"]);
    }
    //console.log('Notification message: ');
    //console.log(data["notification_message"]);
    if(data["notification_message"] != "All normal"){
      // console.log('Writing log');
      //this.textarea.value += data["notification_message"];
      //this.textarea.value += "\n";
      this.newConsoleLog(data["notification_message"]);
    }
  }

  newConsoleLog(data) {

    let currentDate = new Date();

    const cValue = formatDate(currentDate, 'hh:mm:ss', 'en-US');
    this.textarea.value += "[" + cValue + "] ";
    this.textarea.value += data;
    this.textarea.value += "\n";
  }

  sendCustomAlarm() {
    if (confirm("Send alarm to the boat?")) {
      this.apiService.sendCustomAlarm();
      this.newConsoleLog("New custom alarm sent");
      /**this.apiService.sendCustomAlarm().subscribe(
        data => {
          console.log("Alarm sent");
        },
        error => {
          console.log(error);
      });*/
    }
  }


  showToast(text, action) {

    var message = text + "<br/><a (click)='test(0)' class='btn btn-danger mr-2'>Send Alarm</a><a (click)=\"test(0)\" type='button' class='btn btn-warning'>Ignore Alarm</a>";
    this.toastService.info(text, "ALERT", {
      timeOut: 13000,
      disableTimeOut: false,
      tapToDismiss: false,
      closeButton: true,
      enableHtml: true,
      progressBar: true,
      toastComponent: CustomToast
    }).onAction.subscribe(x => {
      if (x == "send") {
        //console.log("Enviar alarma manual")
        this.apiService.sendAction(action);
        this.newConsoleLog("New manual alarm sent");
        /**this.apiService.sendAction(action).subscribe(
              data => {
                console.log("Alarm sent");
              },
              error => {
                console.log(error);
        });*/
      }
    });
  }

  clearLog() {
    this.textarea.value = '';
  }


  ngOnDestroy() {
    //this.subscription.unsubscribe();
  }

}
