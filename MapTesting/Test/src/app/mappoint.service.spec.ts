import { TestBed } from '@angular/core/testing';

import { mapPointService } from './mappoint.service';

describe('PointService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: mapPointService = TestBed.get(mapPointService);
    expect(service).toBeTruthy();
  });
});
