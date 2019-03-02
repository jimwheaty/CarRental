import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import * as ol from 'openlayers';
import { stringify } from 'querystring';
import { appService } from './app.service';
import { mapPoint } from './mappoint';
import { User } from './user';
import { I18nContext } from '@angular/compiler/src/render3/view/i18n/context';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  takishome:any;
  loggedIn:boolean=false;

  geolocationPosition:any;
  locationOptions = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
  };

  public infoWindow:boolean=false;
  public uploadWindow:boolean=false;
  public tagListWindow:boolean=false;
  public profileWindow:boolean=false;
  public loginWindow:boolean=false;
  
  public uploadResponse = [];
  public signupResponse = [];
  public loginResponse = [];

  public entryInfo:any;
  select:any;
  //point = new Point(38.050855, 23.819017);

  hello:string
  map: ol.Map;
  vectorLayer: ol.layer.Vector;
  vectorSource: ol.source.Vector;


  form_name: string = "";
  form_value: string = "";
  username: string = "";
  password: string = "";

  display_name:string='';
  display_value:string='';
  display_info:string='';

  form_left:number;
  form_top:number;

  defaultStyle = new ol.style.Style({
    image: new ol.style.Circle({
      radius:8,
        fill: new ol.style.Fill({
          color:'blue'
        }),
        stroke:new ol.style.Stroke({
          color:'blue'
        })
    })
  })
  selectedStyle = new ol.style.Style({
    image: new ol.style.Circle({
      radius:10,
        fill: new ol.style.Fill({
          color:'green'
        }),
        stroke:new ol.style.Stroke({
          color:'green'
        })
      })
    })
    
    // constructor(private httmp: HttpClient) {}
    constructor(private appservice: appService){}
    
    ngOnInit() {
    this.isLoggedIn();
      
    this.vectorSource = new ol.source.Vector();

    this.vectorLayer = new ol.layer.Vector({
      source: this.vectorSource
    });

    this.map = new ol.Map({
      target: "map",
      layers: [
        new ol.layer.Tile({ source: new ol.source.OSM() }),
        this.vectorLayer
      ],
      view: new ol.View({
        center: ol.proj.fromLonLat([23.68, 38]),
        zoom: 7
      })
    });

    //Display name when hovering over a point on the map.
    this.map.on('pointermove', (evt: any) => {
        let found = false;
        this.map.forEachFeatureAtPixel(evt.pixel,(feature=>{
          let p = feature.getProperties();
          this.display_name = p.name;
          //this.display_value = p.value;
          this.form_left = evt.pixel[0]+10;
          this.form_top = evt.pixel[1]+10;
          found = true;
        }))
        if(!found){
          this.form_left = -9999;
        }
    })
  
  // create a Select interaction and add it to the map
    this.select = new ol.interaction.Select({
      layers: [this.vectorLayer],
      style: this.selectedStyle
    });

    this.map.addInteraction(this.select);
    
    // use the features Collection to detect when a feature is selected,
    // the collection will emit the add event
    var selectedFeatures = this.select.getFeatures();
    selectedFeatures.on('add', event=>this.addSelectedFeatures(event));
    // when a feature is removed, clear the photo-info div
    selectedFeatures.on('remove', event=>this.removeSelectedFeatures(event));
    
    this.getMyPois();
  }
  isLoggedIn() {
    let tokenValue = localStorage.getItem("token");
    if (tokenValue ===null) {
      this.loggedIn=false;
    } 
    else {
      this.loggedIn=true;
    }
  }

  addSelectedFeatures(event) {
    console.log("adding...")
    var feature = event.target.item(0);
    feature.setStyle(this.selectedStyle)
    this.entryInfo=feature.getProperties();
    console.log("entryInfo.name=",this.entryInfo.name)
    //open the info
    this.infoWindow = true
    return feature;
    // var url = feature.get('url');
    // put the url of the feature into the photo-info div
    // $('#photo-info').html(url);
  }
  removeSelectedFeatures(event) {
    var d=this.vectorSource.getFeatures()
    d.forEach(datum=>{
      if(datum != this.select.getFeatures()){
        datum.setStyle(this.defaultStyle)
      }
    })
    this.onCloseInfo();
  }
  
  getMyPois() {
    console.log("42-5");
    // this.pointService.getPoints()
    //   .subscribe(data => this.points = data)
    this.appservice.getPoints()
      .toPromise()
      .then((d: {x:number, y:number, name:string, info:string}[]) => {
        console.log("42");
      
      //let max = Math.max(...d.map(dd=>parseFloat(dd.value)));
      d.forEach(datum => {
        console.log("1");
        console.log(datum.x,datum.y);
        let feature = new ol.Feature(
          new ol.geom.Point(ol.proj.fromLonLat([+datum.x, +datum.y]))
        );
        feature.setStyle(this.defaultStyle);
        this.vectorSource.addFeature(feature);
        feature.setProperties({name:datum.name,info:datum.info});

    });
    })
  }
  // getMyPois() {
  //   this.pointService.enroll(this.point).subscribe(data => console.log("Success",data))
  // }
//       /*.catch((err: HttpErrorResponse) => {
//         // simple logging, but you can do a lot more, see below
//         console.error('An error occurred:', err.error);
//       })*/;
//   }

  onSave() {
    // alert('poi save request');

    let coordinates = this.map.getView().getCenter();
    let lonlat = ol.proj.toLonLat(coordinates);
    // let object = {
    //   x: lonlat[0],
    //   y: lonlat[1],
    //   name: this.form_name,
    //   value: this.form_value
    // }
    let point = new mapPoint(lonlat[0], lonlat[1]);

    // this.vectorSource.clear();
    let f = new ol.Feature(new ol.geom.Point(ol.proj.fromLonLat([lonlat[0], lonlat[1]])))
    f.setStyle(this.defaultStyle);
    f.setProperties({name:this.form_name,info:this.form_value});
    this.vectorSource.addFeature(f);
    
    this.appservice.upload(point).subscribe(point => this.uploadResponse.push(point));
    console.log("response from server=", this.uploadResponse)
    this.uploadWindow=false;
  }

  onCloseInfo() {
    this.infoWindow = false;
  }
  onCloseUploadWindow(){
    this.uploadWindow = false;
  }
  onTagList() {
    this.tagListWindow = !this.tagListWindow;
  }
  onProfile() {
    this.profileWindow = !this.profileWindow;
  }
  onSignUpButton() {
    //check if username is unique
    let user = {username:this.username, password:this.password};
    this.appservice.signup(user).subscribe(user => this.signupResponse.push(user));
  }
  onLogInButton() {
    let user = {username:this.username, password:this.password};
    this.appservice.login(user).subscribe(user => this.loginResponse.push(user));
  }

  ongetlocation() {
    if (window.navigator && window.navigator.geolocation) {
      window.navigator.geolocation.getCurrentPosition(
          position => {
              this.geolocationPosition = position,
              console.log(position)
              var pos=this.geolocationPosition.coords;
              this.map.getView().setCenter(ol.proj.transform([pos.longitude, pos.latitude], 'EPSG:4326', 'EPSG:3857'));
              this.map.getView().setZoom(16);
              this.uploadWindow = true;
          }
      );
      
    }
  }
  onOpenUploadWindow() {
    this.uploadWindow = true;
  }
}
