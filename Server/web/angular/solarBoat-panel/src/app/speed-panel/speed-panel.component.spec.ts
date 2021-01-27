import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpeedPanelComponent } from './speed-panel.component';

describe('SpeedPanelComponent', () => {
  let component: SpeedPanelComponent;
  let fixture: ComponentFixture<SpeedPanelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SpeedPanelComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SpeedPanelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
