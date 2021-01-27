import { Component, OnInit, Inject, Injectable, NgZone, PLATFORM_ID, Renderer2, ElementRef } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { interval, Subscription } from 'rxjs';
import { ApiService } from '../api.service';



@Component({
	selector: 'app-altura-panel',
	templateUrl: './altura-panel.component.html',
	styleUrls: ['./altura-panel.component.scss']
})
export class AlturaPanelComponent implements OnInit {

	private subscription: Subscription;
	datos: any = [{
		name: "Height",
		series: []
	}];


	interval = '10m';

	private influxQuery = 'SELECT height FROM solar_sensor WHERE time > now() - '

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
	yAxisLabel = 'Height (cm)';

	private lastQueryTime;

	colorScheme = {
		domain: ['#0aa7db']
	};

	// line, area
	autoScale = true;

	constructor(private apiService: ApiService,private _renderer: Renderer2,private _el: ElementRef) { }


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
					let altura = values[index][1];
					this.datos[0].series.push({ name: date, value: altura });
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
					let altura = values[index][1];
					this.datos[0].series.push({ name: date, value: altura });
				}
			}
			this.datos = [...this.datos];
		});
	}

	showCustomInterval(time: String) {
		console.log(time);
		this.datos[0].series = [];
		this.getInitialInfluxData(time);
	}

}
