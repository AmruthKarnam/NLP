import { TestBed } from '@angular/core/testing';

import { NlpserviceService } from './nlpservice.service';

describe('NlpserviceService', () => {
  let service: NlpserviceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NlpserviceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
