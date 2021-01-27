import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MapaLeafletComponent } from './mapa-leaflet.component';

describe('MapaLeafletComponent', () => {
  let component: MapaLeafletComponent;
  let fixture: ComponentFixture<MapaLeafletComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MapaLeafletComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MapaLeafletComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
