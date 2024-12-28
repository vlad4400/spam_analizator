import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpamCheckComponent } from './spam-check.component';

describe('SpamCheckComponent', () => {
  let component: SpamCheckComponent;
  let fixture: ComponentFixture<SpamCheckComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SpamCheckComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SpamCheckComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
