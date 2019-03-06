import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { mapPoint } from './mappoint';
import { User } from './user';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class appService {
  constructor(private http: HttpClient) { }

  // private API_END_POINT = 'http://localhost:3000/observatory/api/';
  // private uploadAPI_END_POINT = 'http://localhost:3000/observatory/api/upload';

  private loginAPI_END_POINT = 'http://localhost:8765/observatory/api/login';
  private signupAPI_END_POINT = 'http://localhost:8765/observatory/api/signup';
  private logoutAPI_END_POINT = 'http://localhost:8765/observatory/api/logout';
  private pricesAPI_END_POINT = 'http://localhost:8765/observatory/api/prices';
  private shopsAPI_END_POINT = 'http://localhost:8765/observatory/api/shops';
  private productsAPI_END_POINT = 'http://localhost:8765/observatory/api/products';
  //private url = '/assets/points.json'

  login(user: User): Observable<any>{
    //return this.http.get<Point[]>(this.API_END_POINT);
    return this.http.post<any>(this.loginAPI_END_POINT, user);
    //return this.http.get<Point[]>(this.url);
  }
  logout(): Observable<any>{
    let token = localStorage.getItem("token")
    
    var httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'X-OBSERVATORY-AUTH': token
      })
    }
    return this.http.post<any>(this.logoutAPI_END_POINT,{},httpOptions)
  }
  signup(user: any): Observable<any> {
    // console.log()
    return this.http.post<any>(this.signupAPI_END_POINT, JSON.stringify(user));
  }

  getPoints(data:any): Observable<any>{
    //return this.http.get<Point[]>(this.API_END_POINT);
    let httpParams = new HttpParams();
    Object.keys(data).forEach(function (key) {
      httpParams = httpParams.append(key, data[key]);
    });
    // console.log(httpParams.keys)
    return this.http.get<any>(this.pricesAPI_END_POINT,{params:httpParams});
    //return this.http.get<Point[]>(this.url);
  }
  getShops(data:any): Observable<any>{
    //return this.http.get<Point[]>(this.API_END_POINT);
    let httpParams = new HttpParams();
    Object.keys(data).forEach(function (key) {
      httpParams = httpParams.append(key, data[key]);
    });
    // console.log(httpParams.keys)
    return this.http.get<any>(this.shopsAPI_END_POINT,{params:httpParams});
    //return this.http.get<Point[]>(this.url);
  }
  getProducts(data:any): Observable<any>{
    //return this.http.get<Point[]>(this.API_END_POINT);
    let httpParams = new HttpParams();
    Object.keys(data).forEach(function (key) {
      httpParams = httpParams.append(key, data[key]);
    });
    // console.log(httpParams.keys)
    return this.http.get<any>(this.productsAPI_END_POINT,{params:httpParams});
    //return this.http.get<Point[]>(this.url);
  }
  getShopInfo(id:string): Observable<any>{
    // console.log(httpParams.keys)
    return this.http.get<any>(this.shopsAPI_END_POINT+'/'+id);
  }
  getProductInfo(id:string): Observable<any>{
    return this.http.get<any>(this.productsAPI_END_POINT+'/'+id);
  }
  uploadCar(data:any){
    let token = localStorage.getItem("token")
    var httpOptions = {
    headers: new HttpHeaders({
      'Content-Type':  'application/json',
      'X-OBSERVATORY-AUTH': token
    })
  }
    return this.http.post<any>(this.productsAPI_END_POINT, data,httpOptions);
  }
  uploadShop(data:any){
    let token = localStorage.getItem("token")
    var httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'X-OBSERVATORY-AUTH': token
      })
    }
    return this.http.post<any>(this.shopsAPI_END_POINT, data,httpOptions);
  }
  uploadPrice(data:any){
    let token = localStorage.getItem("token")
    var httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
        'X-OBSERVATORY-AUTH': token
      })
    }
    return this.http.post<any>(this.pricesAPI_END_POINT, data,httpOptions);
  }
}
