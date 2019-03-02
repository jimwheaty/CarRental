import { TestBed } from '@angular/core/testing';

import { appService } from './app.service';

describe('appService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: appService = TestBed.get(appService);
    expect(service).toBeTruthy();
  });
});
