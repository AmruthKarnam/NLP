import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SarcasmComponent } from './sarcasm.component';

describe('SarcasmComponent', () => {
  let component: SarcasmComponent;
  let fixture: ComponentFixture<SarcasmComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SarcasmComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SarcasmComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
