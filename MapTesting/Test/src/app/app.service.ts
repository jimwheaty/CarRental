import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { mapPoint } from './mappoint';
import { User } from './user';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class appService {
  constructor(private http: HttpClient) { }

  private API_END_POINT = 'http://localhost:3000';
  private uploadAPI_END_POINT = 'http://localhost:3000/upload';

  private loginAPI_END_POINT = 'http://localhost:3000/login';
  private signupAPI_END_POINT = 'http://localhost:3000/signup';
  //private url = '/assets/points.json'

  login(user: User): Observable<User>{
    //return this.http.get<Point[]>(this.API_END_POINT);
    return this.http.post<User>(this.loginAPI_END_POINT, user);
    //return this.http.get<Point[]>(this.url);
  }
  signup(user: User): Observable<User> {
    return this.http.post<User>(this.signupAPI_END_POINT, user);
  }

  getPoints(): Observable<mapPoint[]>{
    //return this.http.get<Point[]>(this.API_END_POINT);
    return this.http.get<any>(this.API_END_POINT);
    //return this.http.get<Point[]>(this.url);
  }
  upload(point: mapPoint): Observable<mapPoint> {
    return this.http.post<mapPoint>(this.uploadAPI_END_POINT, point);
  }
}
