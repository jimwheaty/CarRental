import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { mapPoint } from './mappoint';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class mapPointService {

  private API_END_POINT = 'http://localhost:3000';
  private uploadAPI_END_POINT = 'http://localhost:3000/upload';
  //private url = '/assets/points.json'
  constructor(private http: HttpClient) { }

  getPoints(): Observable<mapPoint[]>{
    //return this.http.get<Point[]>(this.API_END_POINT);
    return this.http.get<any>(this.API_END_POINT);
    //return this.http.get<Point[]>(this.url);
  }
  upload(point: mapPoint): Observable<mapPoint> {
    return this.http.post<mapPoint>(this.uploadAPI_END_POINT, point);
  }
}
