import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { AppRoutingModule } from './app-routing.module';
import { HttpClientModule } from '@angular/common/http';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ToastrModule } from 'ngx-toastr';
import { CustomToast } from './home/custom.toast';
import { SocketIoModule, SocketIoConfig } from 'ngx-socket-io';
import { VideoComponent } from './video/video.component';
import { MapaLeafletComponent } from './mapa-leaflet/mapa-leaflet.component';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { FormsModule,ReactiveFormsModule  } from '@angular/forms';
import { ImuPanelComponent } from './imu-panel/imu-panel.component';
import { AlturaPanelComponent } from './altura-panel/altura-panel.component';
import {NgxChartsModule} from '@swimlane/ngx-charts';
import { SpeedPanelComponent } from './speed-panel/speed-panel.component';

//import { MatVideoModule } from 'mat-video';

const config: SocketIoConfig = { url: 'http://solarboat.ddns.net:5001', options: {} };

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    CustomToast,
    VideoComponent,
    MapaLeafletComponent,
    ImuPanelComponent,
    AlturaPanelComponent,
    SpeedPanelComponent,
    //VideoStreamingComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    MatButtonModule,
    //MatVideoModule,
    MatToolbarModule,
    BrowserAnimationsModule,
    MatSelectModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatCheckboxModule,
    FormsModule,
    ReactiveFormsModule,
    NgxChartsModule,
    SocketIoModule.forRoot(config),
    ToastrModule.forRoot({
      preventDuplicates: true,
      //toastComponent: CustomToast
    })
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
