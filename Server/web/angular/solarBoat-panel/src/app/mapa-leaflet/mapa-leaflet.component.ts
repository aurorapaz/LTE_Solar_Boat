import { Component, OnInit, Injectable } from '@angular/core';
import { interval, Subscription } from 'rxjs';
import { ApiService } from '../api.service';
import * as L from 'leaflet';
import { ViewEncapsulation } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';


@Component({
	selector: 'app-mapa-leaflet',
	templateUrl: './mapa-leaflet.component.html',
	styleUrls: ['./mapa-leaflet.component.css'],
	encapsulation: ViewEncapsulation.None,
})

@Injectable({ providedIn: 'root' })
export class MapaLeafletComponent implements OnInit {

	private map;
	private subscription: Subscription;
	interval = '10m';
	custom = false;


	range = new FormGroup({
		start: new FormControl(),
		end: new FormControl()
	});

	track: boolean = false;

	constructor(private apiService: ApiService) { }
	ngOnInit() {
		const source = interval(3000);
		this.subscription = source.subscribe(val => this.getInfluxData());
		this.addToPage();
	}

	getInfluxData() {
		this.apiService.sendHttpQuery(`SELECT latitude, longitude FROM solar_sensor  where time > now() - ${this.interval}`).subscribe(data => {
			this.processResponse(data);
		});
	}


	processResponse(data) {
		var positionList = [];

		var values = data["results"][0]["series"][0]["values"];
		for (var index = 0; index < values.length; index++) {
			var position = {
				"latitude": values[index][1],
				"longitude": values[index][2]
			}
			if (position["latitude"]!= 0 && position["longitude"]!= 0)
				positionList.push(position);
		}

		this.fill(positionList);
	}



	addToPage() {
		var streets = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
			maxZoom: 18,
			attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
				'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
			id: 'mapbox/streets-v11',
			tileSize: 512,
			zoomOffset: -1
		});

		var CartoDB_DarkMatter = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
			attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
			subdomains: 'abcd',
			maxZoom: 19
		});

		var googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
			maxZoom: 20,
			subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
		});

		var googleHybrid = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
			maxZoom: 20,
			subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
		});

		var baseMaps = {
			"Grayscale": CartoDB_DarkMatter,
			"Satellite": googleSat,
			"Hybrid": googleHybrid,
			"Streets": streets
		};


		this.map = L.map('mapContainer', {
			layers: [streets, CartoDB_DarkMatter]
		});

		L.control.layers(baseMaps).addTo(this.map);

		this.map.setView(new L.LatLng(42.23282, -8.72264), 10);


		// L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		// 	maxZoom: 18,
		// 	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
		// 		'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		// 	id: 'mapbox/streets-v11',
		// 	tileSize: 512,
		// 	zoomOffset: -1
		// }).addTo(this.map);

	}

	fill(positionList) {

		this.clearMap();

		var linePoints = [];
		for (var index = 0; index < positionList.length; index++) {
			var newPoint = new L.LatLng(
				positionList[index].latitude,
				positionList[index].longitude
			);
			linePoints.push(newPoint);
		}
		var firstpolyline = new L.Polyline(linePoints, {
			color: '#bd0026',
			weight: 8,
			opacity: 0.8,
			smoothFactor: 1
		}
		);
		this.map.addLayer(firstpolyline);

		var currentPosition = positionList[positionList.length - 1];
		var circle = L.circle([currentPosition['latitude'], currentPosition['longitude']], {
			color: 'blue',
			fillColor: 'blue',
			fillOpacity: 1,
			radius: 100
		}).addTo(this.map);

		if (this.track) {
			this.map.panTo(new L.LatLng(currentPosition['latitude'], currentPosition['longitude']));
		}

	}

	clearMap() {
		for (var i in this.map._layers) {
			if (this.map._layers[i]._path != undefined) {
				try {
					this.map.removeLayer(this.map._layers[i]);
				}
				catch (e) {
					console.log("problem with " + e + this.map._layers[i]);
				}
			}
		}
	}

}
