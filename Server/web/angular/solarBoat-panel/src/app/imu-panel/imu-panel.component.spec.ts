import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImuPanelComponent } from './imu-panel.component';

describe('ImuPanelComponent', () => {
  let component: ImuPanelComponent;
  let fixture: ComponentFixture<ImuPanelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ImuPanelComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ImuPanelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
