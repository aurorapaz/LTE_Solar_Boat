import { ViewChild } from '@angular/core';
import { ElementRef } from '@angular/core';
import { Component, OnInit } from '@angular/core';
import JSMpeg from '@cycjimmy/jsmpeg-player';

@Component({
  selector: 'app-video',
  templateUrl: './video.component.html',
  styleUrls: ['./video.component.css']
})
export class VideoComponent implements OnInit {

  @ViewChild('streaming', {static: true}) streamingcanvas: ElementRef;
 
  constructor() { }
 
  ngOnInit() {
    let player = new JSMpeg.Player('ws://solarboat.ddns.net:9999', {
      canvas: this.streamingcanvas.nativeElement, autoplay: true, audio: true, loop: true
    })
 
  }

}