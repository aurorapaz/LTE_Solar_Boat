import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlturaPanelComponent } from './altura-panel.component';

describe('AlturaPanelComponent', () => {
  let component: AlturaPanelComponent;
  let fixture: ComponentFixture<AlturaPanelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AlturaPanelComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AlturaPanelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
