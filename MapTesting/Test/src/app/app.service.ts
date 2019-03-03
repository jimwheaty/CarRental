import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { mapPoint } from './mappoint';
import { User } from './user';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class appService {
  constructor(private http: HttpClient) { }

  private API_END_POINT = 'http://localhost:3000/observatory/api/';
  private uploadAPI_END_POINT = 'http://localhost:3000/observatory/api/upload';

  private loginAPI_END_POINT = 'http://localhost:3000/observatory/api/login';
  private signupAPI_END_POINT = 'http://localhost:3000/observatory/api/signup';
  //private url = '/assets/points.json'

  login(user: User): Observable<any>{
    //return this.http.get<Point[]>(this.API_END_POINT);
    return this.http.post<any>(this.loginAPI_END_POINT, user);
    //return this.http.get<Point[]>(this.url);
  }
  signup(user: User): Observable<any> {
    return this.http.post<any>(this.signupAPI_END_POINT, user);
  }

  getPoints(): Observable<mapPoint[]>{
    //return this.http.get<Point[]>(this.API_END_POINT);
    return this.http.get<any>(this.API_END_POINT);
    //return this.http.get<Point[]>(this.url);
  }
  upload(point: mapPoint): Observable<mapPoint> {
    let token = localStorage.getItem("token")
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'X-OBSERVATORY-AUTH': token
      })
    }
    return this.http.post<mapPoint>(this.uploadAPI_END_POINT, point, httpOptions);
  }
}
