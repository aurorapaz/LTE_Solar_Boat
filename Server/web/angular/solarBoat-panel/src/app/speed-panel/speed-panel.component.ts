import { Component, OnInit } from '@angular/core';
import { interval, Subscription } from 'rxjs';
import { ApiService } from '../api.service';


@Component({
  selector: 'app-speed-panel',
  templateUrl: './speed-panel.component.html',
  styleUrls: ['./speed-panel.component.css']
})
export class SpeedPanelComponent implements OnInit {

  private influxQuery = 'SELECT speed FROM solar_sensor ORDER BY DESC LIMIT 1'
  private subscription: Subscription;

  datos: any[] = [{
    "name": "Speed",
    "value": 0
  }];
  view: any[] = [500, 400];
  legend: boolean = true;
  legendPosition: string = 'below';

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    const source = interval(0);
    this.subscription = source.subscribe(val => this.getNewInfluxData());
  }

  private getNewInfluxData() {
    this.apiService.sendHttpQuery(this.influxQuery).subscribe(data => {
      if (data["results"][0]["series"] != undefined) {
        var values = data["results"][0]["series"][0]["values"];
        for (var index = 0; index < values.length; index++) {
          let date = new Date(values[index][0]);
          let speed = values[index][1];
          this.datos[0].value = speed ;
        }
      }
      this.datos = [...this.datos];
    });
  }

}
