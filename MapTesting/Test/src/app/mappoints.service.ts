import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Contrib} from './contrib';
import {Observable} from 'rxjs';
@Injectable()
export class MapPoints{
private _url: string = "/samplecoords.json";

  constructor(private http: HttpClient){

  }
  getPoints():Observable<Contrib[]>{
    return this.http.get<Contrib[]>(this._url);

  }
}
