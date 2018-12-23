import { Component } from '@angular/core';
import {MapPoints} from './mappoints.service';

import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import XYZ from 'ol/source/XYZ';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {
  title = 'Test';
  map;
//  constructor( private _points:MapPoints){}
  public contrib=[];

  ngOnInit(){
    this.initializeMap();
  //  this._points.getPoints()
  //    .subscribe(data=>this.contrib=data);
  }

  initializeMap(){
      this.map=new Map({
      target: 'map',
      layers: [
        new TileLayer({
          source: new XYZ({
            url: 'https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png'
          })
        })
      ],
      view: new View({
        center: [2642275.193762,4577049.253716],
        zoom: 7
      })
    });
  }
}
