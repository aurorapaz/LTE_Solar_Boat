import { Component, OnInit, Inject, Injectable, NgZone, PLATFORM_ID, Renderer2, ElementRef } from '@angular/core';
import { interval, Subscription } from 'rxjs';
import { ApiService } from '../api.service';


// amCharts imports
import * as am4core from '@amcharts/amcharts4/core';
import * as am4charts from '@amcharts/amcharts4/charts';
import am4themes_animated from '@amcharts/amcharts4/themes/animated';
import am4themes_dark from "@amcharts/amcharts4/themes/dark";

@Component({
	selector: 'app-imu-panel',
	templateUrl: './imu-panel.component.html',
	styleUrls: ['./imu-panel.component.scss']
})

@Injectable({ providedIn: 'root' })
export class ImuPanelComponent implements OnInit {


	private subscription: Subscription;
	datos: any = [{
		name: "Pitch",
		series: []
	}, {
		name: "Roll",
		series: []
	}];


	private influxQuery = 'SELECT pitch, roll FROM solar_sensor WHERE time > now() - '

	//view: any[] = [1100, 400];
	single: any[];
	multi: any[];

	// options
	showXAxis = true;
	showYAxis = true;
	gradient = false;
	showLegend = true;
	showXAxisLabel = true;
	xAxisLabel = 'Time';
	showYAxisLabel = true;
	yAxisLabel = 'Pitch&Roll Angles (deg)';

	private lastQueryTime;

	colorScheme = {
		domain: ['#5AA454', '#A10A28', '#C7B42C', '#AAAAAA']
	};

	// line, area
	autoScale = false;

	interval = '10m';

	constructor(private apiService: ApiService, private _renderer: Renderer2, private _el: ElementRef) { }


	ngOnInit() {
		this.getInitialInfluxData();
		const source = interval(1000);
		this.subscription = source.subscribe(val => this.getNewInfluxData());
	}

	onSelect(event) {
		console.log(event);
	}

	private getInitialInfluxData(time: String = '10m') {
		this.lastQueryTime = new Date().getTime();
		this.apiService.sendHttpQuery(this.influxQuery + time).subscribe(data => {
			if (data["results"][0]["series"] != undefined) {
				var values = data["results"][0]["series"][0]["values"];
				for (var index = 0; index < values.length; index++) {
					let date = new Date(values[index][0]);
					let pitch = values[index][1];
					let roll = values[index][2];
					this.datos[0].series.push({ name: date, value: pitch });
					this.datos[1].series.push({ name: date, value: roll });
				}
			}
			this.datos = [...this.datos];
		});

	}

	private getNewInfluxData() {
		let currentTime = new Date().getTime();
		let milliSecondsBetweenQueries = Math.abs((currentTime - this.lastQueryTime));
		this.lastQueryTime = currentTime;
		this.apiService.sendHttpQuery(this.influxQuery + milliSecondsBetweenQueries + 'ms').subscribe(data => {
			if (data["results"][0]["series"] != undefined) {
				var values = data["results"][0]["series"][0]["values"];
				for (var index = 0; index < values.length; index++) {
					let date = new Date(values[index][0]);
					let pitch = values[index][1];
					let roll = values[index][2];
					this.datos[0].series.push({ name: date, value: pitch });
					this.datos[1].series.push({ name: date, value: roll });
				}
			}
			this.datos = [...this.datos];
		});
	}

	showCustomInterval(time: String) {
		console.log(time);
		this.datos[0].series = [];
		this.datos[1].series = []
		this.getInitialInfluxData(time);
	}

}
