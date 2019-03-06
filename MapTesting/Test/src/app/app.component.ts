import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import * as ol from 'openlayers';
import { stringify } from 'querystring';
import { appService } from './app.service';
import { mapPoint } from './mappoint';
import { User } from './user';
import {getLength} from 'ol/sphere.js';
import { I18nContext } from '@angular/compiler/src/render3/view/i18n/context';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  takishome:any;
  key:any;
  // tokenValue:any;
  loggedIn:boolean=false;
  searchButton:boolean=true;

  geolocationPosition:any;
  locationOptions = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
  };
  secondWindow:boolean=false;
  entryInfoProducts:{
    Name:string,
    Description:string,
    Category:string,
    Tags:string[],
    Price:number,
    Date:string
  }[]=[];
  errorWindow:boolean=false;
  entryInfoShopName:string='';
  entryInfoShopAddress:string='';
  entryInfoShopTags:string[]=[];
  // entryInfoProductPrice:number[];
  // entryInfoProductDate:string[]=[];
  // entryInfoProductName:string[]=[];
  // entryInfoProductDescription:string[]=[];
  // entryInfoProductCategory:string[]=[];
  // entryInfoProductTags:string[][]=[];
  // entryInfoK:number=0;

  checkbox1:boolean=false;
  checkbox2:boolean=false;
  checkbox3:boolean=false;
  checkbox4:boolean=false;
  checkbox5:boolean=false;
  checkbox6:boolean=false;
  checkbox7:boolean=false;
  checkbox8:boolean=false;
  checkbox11:boolean=false;
  checkbox12:boolean=false;
  checkbox13:boolean=false;
  checkbox14:boolean=false;
  checkbox15:boolean=false;
  checkbox16:boolean=false;
  checkbox17:boolean=false;
  checkbox18:boolean=false;
  checkbox21:boolean=false;
  checkbox22:boolean=false;
  checkbox23:boolean=false;
  checkbox24:boolean=false;
  checkbox25:boolean=false;
  checkbox26:boolean=false;
  checkbox27:boolean=false;
  checkbox28:boolean=false;
  
  errorMessageWindow:boolean=false;
  public infoWindow:boolean=false;
  public uploadWindow:boolean=false;
  public tagListWindow:boolean=false;
  public profileWindow:boolean=false;
  public loginWindow:boolean=false;
  public uploadWindowCarTagList:boolean=false;
  
  // public uploadResponse = [];
  // public signupResponse = [];
  // public loginResponse:{success: Boolean, message: string, token:string}[]=[];
  // response:{success: Boolean, message: string, token:string}

  public entryInfo:any;
  select:any;
  //point = new Point(38.050855, 23.819017);

  hello:string
  map: ol.Map;
  vectorLayer: ol.layer.Vector;
  vectorSource: ol.source.Vector;

  onEntryInfoUploadCar:boolean=false;
  uploadWindowCarName: string = "";
  uploadWindowCarDescription: string = "";
  uploadWindowCarCategory: string = "";
  uploadWindowCarTags: string[] = [];
  uploadWindowCarWithdrawn: boolean;
  uploadWindowCarExtradata: string = "";

  entryInfoWindowCarName: string = "";
  entryInfoWindowCarDescription: string = "";
  entryInfoWindowCarCategory: string = "";
  entryInfoWindowCarTags: string[] = [];
  entryInfoWindowCarWithdrawn: boolean;
  entryInfoWindowCarExtradata: string = "";

  uploadWindowShopWithdrawn:boolean=false;
  uploadWindowShopAddress='';
  uploadWindowShopName='';
  uploadWindowShopTags: string[] = [];

  uploadWindowDateFrom:string='';
  uploadWindowDateTo:string='';
  uploadWindowPrice:number;
  

  username: string = "";
  password: string = "";

  display_name:string='';
  display_rating:string='';
  display_count:number;


  shopCarsCount:number=0;
  shopRating:string='';
  totalPreviewPrices:number=0;

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
        center: ol.proj.fromLonLat([24, 38.3]),
        zoom: 7
      })
    });

    //Display name when hovering over a point on the map.
    this.map.on('pointermove', (evt: any) => {
        let found = false;
        this.map.forEachFeatureAtPixel(evt.pixel,(feature=>{
          let p = feature.getProperties();
          this.display_name = p.name;
          this.display_count=p.count;
          this.display_rating=p.rating;
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
    let distanceBetweenPoints = function(latlng1, latlng2){
      var line = new ol.geom.LineString([latlng1, latlng2]);
      return Math.round(line.getLength() * 100) / 100;
    };
    let formatDistance = function(length) {
      if (length >= 1000) {
          length = (Math.round(length / 1000 * 100) / 100);
      } else {
          length =  Math.round(length);
      }
      return length;
    }
    console.log("adding...")
    var feature = event.target.item(0);
    feature.setStyle(this.selectedStyle)
    this.entryInfo=feature.getProperties();
    console.log("entryInfo.name=",this.entryInfo.name)
    //open the info
    let coordinates:ol.Coordinate = this.map.getView().getCenter();
    let lonlat4326 = ol.proj.toLonLat(coordinates,'EPSG:4326');
    // let lonlat3857 = ol.proj.toLonLat(coordinates,'EPSG:3857');
    let ourLonlat4326=[this.entryInfo.lng,this.entryInfo.lat];
    let geoDist=formatDistance(distanceBetweenPoints(lonlat4326,ourLonlat4326))
    this.previewEntry(this.entryInfo.lng,this.entryInfo.lat);
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
    // this.pointService.getPoints()
    //   .subscribe(data => this.points = data)
    let distanceBetweenPoints = function(latlng1, latlng2){
      var line = new ol.geom.LineString([latlng1, latlng2]);
      return Math.round(line.getLength() * 100) / 100;
    };
    let formatDistance = function(length) {
      if (length >= 1000) {
          length = (Math.round(length / 1000 * 100) / 100);
      } else {
          length =  Math.round(length);
      }
      return length;
    }
    let map=this.map
    
    let start=0;
    let count=30;
    let geoDist:any;
    let geoLng:any;
    let geoLat:any;
    let dateFrom="2019-03-04";
    let dateTo=new Date().toISOString().slice(0,10);
    let shops=null;
    let products=null;
    let tags:any;
    let sort="date";
    let appservice =this.appservice;
    let vectorSource=this.vectorSource;
    let defaultStyle=this.defaultStyle
    map.once('postrender', function() {
      let coordinates:ol.Coordinate = map.getView().getCenter();
      let lonlat4326 = ol.proj.toLonLat(coordinates,'EPSG:4326');
      let lonlat3857 = ol.proj.toLonLat(coordinates,'EPSG:3857');
      geoLng=lonlat3857[0];
      geoLat=lonlat3857[1];
      let pixel=map.getPixelFromCoordinate(coordinates);
      let ourPixel:[number,number] = [pixel[0],0];
      let ourCoordinates = map.getCoordinateFromPixel(ourPixel);
      // long, lat of the top-center pixel
      let ourLonlat4326 = ol.proj.toLonLat(ourCoordinates,'EPSG:4326');
      // let geoDist=Math.sqrt(Math.pow(coordinates[0]-ourCoordinates[0],2)+Math.pow(coordinates[1]-ourCoordinates[1],2));
      // ol.proj.transform([pos.longitude, pos.latitude], 'EPSG:4326', 'EPSG:3857'))
      geoDist=formatDistance(distanceBetweenPoints(lonlat4326,ourLonlat4326))
      console.log("distance in km from top pixel=",geoDist);
      appservice.getPoints({start:start,count:count,geoDist:geoDist,geoLng:geoLng,geoLat:geoLat,dateFrom:dateFrom,dateTo:dateTo,shops:shops,products:products,tags:tags,sort:sort})
        .subscribe((datum: {start:number, count:number, total:number, prices:
          {price:number,date:string, productName:string,productId:number,
            productTags:string[],shopId:string,shopName:string,
            shopTags:string[],shopAddress:string}[]}) => {
        
        // d.forEach(datum => {
          // console.log(datum.start,datum.count,datum.total,datum.prices)
          let p=datum.prices
          let carCount=datum.total;
          p.forEach(priceInfo => {
            console.log(priceInfo.price,priceInfo.date,priceInfo.productName,priceInfo.productId,priceInfo.productTags,priceInfo.shopAddress,priceInfo.shopId,priceInfo.shopName,priceInfo.shopTags)
            appservice.getShopInfo(priceInfo.shopId).subscribe(
              (shop:{id:number,name:string,address:string,lng:number,
                  lat:number,tags:string[],withdrawn:boolean})=>{
                    // console.log(d)
                      // console.log("lng,lat=",shop.lng,shop.lat)
                      let feature = new ol.Feature(
                        new ol.geom.Point(ol.proj.fromLonLat([+shop.lng, +shop.lat]))
                      );
                      let t=shop.tags;
                      let carRating=t.toString();
                    feature.setStyle(defaultStyle);
                    vectorSource.addFeature(feature);
                    feature.setProperties({name:shop.name,count:carCount,rating:carRating,lng:shop.lng,lat:shop.lat});
              })
          })
        })
        // });
      })
  }

  onSave() {
    if(this.uploadWindowPrice==null || this.uploadWindowCarName==null ||
      this.uploadWindowDateFrom==null || this.uploadWindowDateTo==null ||
      this.uploadWindowCarCategory==null || this.uploadWindowShopName==null) {
        // APLO =
        this.errorWindow=true;
        this.uploadWindowPrice=null
        this.uploadWindowCarName=null
        this.uploadWindowDateFrom=null
        this.uploadWindowDateTo=null
        this.uploadWindowShopName=null
        this.uploadWindowCarCategory=null
        return;
      }
      else {
        this.errorWindow=false;
      }
    // alert('poi save request');
    if (this.checkbox1===true) {
      this.uploadWindowCarTags.push("GPS-navigation");
    }
    if (this.checkbox2===true) {
      this.uploadWindowCarTags.push("Bluetooth connectivity");
    }
    if (this.checkbox3===true) {
      this.uploadWindowCarTags.push("USB for phones/sticks");
    }
    if (this.checkbox4===true) {
      this.uploadWindowCarTags.push("Χιονολάστιχα");
    }
    if (this.checkbox5===true) {
      this.uploadWindowCarTags.push("Diesel");
    }
    if (this.checkbox6===true) {
      this.uploadWindowCarTags.push("Παραλαβή+Παράδοση γεμάτο ρεζερβουάρ");
    }
    if (this.checkbox7===true) {
      this.uploadWindowCarTags.push("4x4");
    }
    if (this.checkbox8===true) {
      this.uploadWindowCarTags.push("Auto");
    }
    let vectorSource=this.vectorSource
    let coordinates = this.map.getView().getCenter();
    let lonlat = ol.proj.toLonLat(coordinates,'EPSG:3857');
    let myShopId:any;
    let myProductId:any;
    this.errorMessageWindow=false;
    this.appservice.uploadCar({id:0,name:this.uploadWindowCarName,
      description:this.uploadWindowCarDescription,category:this.uploadWindowCarCategory,
      tags:this.uploadWindowCarTags,withdrawn:this.uploadWindowCarWithdrawn,extraData:this.uploadWindowCarExtradata})
      .subscribe((m:{message:string})=>{
        console.log(m.message)
        if (m.message!="OK") {
          this.errorMessageWindow=true;
          return
        }
      })
    this.errorMessageWindow=false
    this.appservice.uploadShop({id:0,name:this.uploadWindowShopName,
      address:this.uploadWindowShopAddress,lng:lonlat[0],lat:lonlat[1],
      tags:this.uploadWindowShopTags,withdrawn:this.uploadWindowShopWithdrawn})
      .subscribe((m:{message:string})=>{
        console.log(m.message)
        if(m.message!="OK"){
          this.errorMessageWindow=true;
          return
        }
      })
    this.appservice.getShops({start:0,count:1,status:"ACTIVE",sort:"id|DESC"})
    .subscribe((datum:{start:Number,count:Number,total:Number,shops:
      {id:Number,name:String,address:String,lng:Number,lat:Number,tags:String[],withdrawn:Boolean}[]
    })=>{
      // console.log(d)
      // d.forEach(datum => {
        let s=datum.shops;
        s.forEach(shop => {
          myShopId=shop.id;
          console.log(myShopId)
        })
      // })
    })
    this.appservice.getProducts({start:0,count:1,status:"ACTIVE",sort:"id|DESC"})
    .subscribe((datum:{start:Number,count:Number,total:Number,products:
      {id:Number,name:String,description:String,category:string,tags:String[],withdrawn:Boolean}[]
    })=>{      
      // console.log(d)
      // d.forEach(datum => {
        let p=datum.products;
        p.forEach(product => {
          myProductId=product.id;
          console.log(myProductId)
        })
      // })
    })
    let dateFrom=this.uploadWindowDateFrom;
    let dateTo=this.uploadWindowDateTo;
    let price=this.uploadWindowPrice;
    this.errorMessageWindow=false
    this.appservice.uploadPrice({price:price,dateFrom:dateFrom,
      dateTo:dateTo,productId:myProductId,shopId:myShopId})
      .subscribe((d:{message:string})=>{
        console.log(d.message)
        if(d.message!="OK"){
          this.errorMessageWindow=true
          return
        }
      })
    
    let point = new mapPoint(lonlat[0], lonlat[1]);
    // getPriceentryInfoWindowCarName
    let shopId:any;
    this.appservice.getPoints({start:0,count:0,geoDist:0,geoLng:lonlat[0],geoLat:lonlat[1],dateFrom:dateFrom,dateTo:dateTo,shops:[],products:[],tags:[],sort:null})
    .subscribe((datum: {start:number, count:number, total:number, prices:
      {price:number,date:string, productName:string,productId:number,
        productTags:string[],shopId:string,shopName:string,
        shopTags:string[],shopAddress:string}[]}) => {
    
        // d.forEach(datum => {
          // console.log(datum.start,datum.count,datum.total,datum.prices)
          this.shopCarsCount=datum.total;
          console.log("total=",this.shopCarsCount)
//????????????test
          let p=datum.prices;
          p.forEach(price => {
            shopId=price.shopId;
          })
        // })
    console.log("shopid",shopId)
    this.appservice.getShopInfo(shopId).subscribe(
      (shop:{id:number,name:string,address:string,lng:number,
          lat:number,tags:string[],withdrawn:boolean})=>{
            // console.log(d)
            // s.forEach(shop => {
              console.log("lng,lat=",shop.lng,shop.lat)
              let t=shop.tags
//????????????test
              t.forEach(tag => {
                this.shopRating=t.toString();
                console.log("rating=",this.shopRating)
                let f = new ol.Feature(new ol.geom.Point(ol.proj.fromLonLat([lonlat[0], lonlat[1]])))
                f.setStyle(this.defaultStyle);
                // console.log("name,rating,count",this.uploadWindowShopName,this.shopRating,this.shopCarsCount)
                f.setProperties({name:this.uploadWindowShopName,rating:this.shopRating,count:this.shopCarsCount,lng:shop.lng,lat:shop.lat});
                this.vectorSource.addFeature(f);
                this.uploadWindow=false;
              })
            // })
      });
      
    // console.log("rating",this.shopRating);
    // this.vectorSource.clear();
    
    // this.appservice.upload(point).subscribe(point => this.uploadResponse.push(point));
    // console.log("response from server=", this.uploadResponse)
    console.log("ATROMHTOI")
    this.uploadWindowPrice=null
    this.uploadWindowCarName=null
    this.uploadWindowDateFrom=null
    this.uploadWindowDateTo=null
    this.uploadWindowShopName=null
    this.uploadWindowCarCategory=null 
 
  })}
  onSaveCar(event){
    let distanceBetweenPoints = function(latlng1, latlng2){
      var line = new ol.geom.LineString([latlng1, latlng2]);
      return Math.round(line.getLength() * 100) / 100;
    };
    let formatDistance = function(length) {
      if (length >= 1000) {
          length = (Math.round(length / 1000 * 100) / 100);
      } else {
          length =  Math.round(length);
      }
      return length;
    }
  // entryInfoWindowCarName string = "";
  // entryInfoWindowCarDescription: string = "";
  // entryInfoWindowCarCategory: string = "";
  // entryInfoWindowCarTags: string[] = [];
  // entryInfoWindowCarWithdrawn: boolean;
  // entryInfoWindowCarExtradata: string = "";
  this.errorMessageWindow=false
  this.appservice.uploadCar({id:0,name:this.entryInfoWindowCarName,
    description:this.entryInfoWindowCarDescription,category:this.entryInfoWindowCarCategory,
    tags:this.entryInfoWindowCarTags,withdrawn:this.entryInfoWindowCarWithdrawn,extraData:this.entryInfoWindowCarWithdrawn})
    .toPromise().then((m:{message:string})=>{
      console.log(m.message)
      if(m.message!="OK") {
        this.errorMessageWindow=true
        return
      }
      //κανε refresh to preview window για ανανέωση των χαρακτηριστικών του 
      //???????????/
      var feature = event.target.item(0);
      feature.setStyle(this.selectedStyle)
      this.entryInfo=feature.getProperties();
      console.log("entryInfo.name=",this.entryInfo.name)
      //open the info
      let coordinates:ol.Coordinate = this.map.getView().getCenter();
      let lonlat4326 = ol.proj.toLonLat(coordinates,'EPSG:4326');
      console.log("lonlat4326=",lonlat4326)
      // let lonlat3857 = ol.proj.toLonLat(coordinates,'EPSG:3857');
      let ourLonlat4326=[this.entryInfo.lng,this.entryInfo.lat];
      // let geoDist=formatDistance(distanceBetweenPoints(lonlat4326,ourLonlat4326))
      this.previewEntry(this.entryInfo.lng,this.entryInfo.lat);
    })
  }
  previewEntry(lng:number,lat:number){
    let dateFrom="2019-03-04";
    let dateTo=new Date().toISOString().slice(0,10);
    let total:any;
    this.appservice.getPoints({start:0,count:1,geoDist:0.001,geoLng:lng,geoLat:lat,dateFrom:dateFrom,dateTo:dateTo,shops:[],products:[],tags:[],sort:"date|DESC"})
    .subscribe((datum: {start:number, count:number, total:number, prices:
      {price:number,date:string, productName:string,productId:number,
        productTags:string[],shopId:string,shopName:string,
        shopTags:string[],shopAddress:string}[]}) => {
          // d.forEach(datum => {
            console.log("geia sou maria")
            total=datum.total;
          // });
          console.log("totalllll:",total)
          this.appservice.getPoints({start:0,count:total-1,geoDist:0.001,geoLng:lng,geoLat:lat,dateFrom:dateFrom,dateTo:dateTo,shops:[],products:[],tags:[],sort:"date|DESC"})
          .subscribe((dd: {start:number, count:number, total:number, prices:
            {price:number,date:string, productName:string,productId:number,
              productTags:string[],shopId:string,shopName:string,
              shopTags:string[],shopAddress:string}[]}) => {
                
                // d.dforEach(datum => {
                  let p=dd.prices
                  let carCount=dd.total;
                  let k=0;
                  p.forEach(priceInfo => {
                    if (k==0) {
                      this.entryInfoShopName = priceInfo.shopName;
                      this.entryInfoShopTags = priceInfo.shopTags;
                      this.entryInfoShopAddress = priceInfo.shopAddress;
                    } 
                    let Price = priceInfo.price;
                    let Date = priceInfo.date;
                    let Name = priceInfo.productName;
                    let Tags = priceInfo.productTags;
                    console.log("id...=",priceInfo.productId)
                    this.appservice.getProductInfo(priceInfo.productId.toString())
                    .subscribe((productInfo:{id:number,name:string,description:string,category:string,tags:string[],withdrawn:boolean})=>{      
                      // console.log(d)
                      // l.forEach(productInfo => {
                        let Description=productInfo.description;
                        let Category= productInfo.category;
                        this.entryInfoProducts.push({Name,Description,Category,Tags,Price,Date})
                      // })
                    })
                    // let shopId = priceInfo.shopId;
                    k++
                  })
                  // this.entryInfoK=k;
                // })
                console.log("entryInfoProducts",this.entryInfoProducts)
                this.infoWindow=true;
              });
              
            })
          }
          onCloseInfo() {
            this.infoWindow = false;
          }
          onCloseUploadWindow(){
    this.uploadWindow = false;
  }
  
  onProfile() {
    this.profileWindow = !this.profileWindow;
  }
  onOpenUploadWindow() {
    this.uploadWindow = true;
  }
  onLogout() {
    // profileWindow=false; tokenValue=null;
    this.errorMessageWindow=false
    this.appservice.logout()
    .subscribe((datum:{message: string}) => {
      // d.forEach(datum => {
        if (datum.message=="OK") {
          // console.log("logout message=",datum.message);
          localStorage.removeItem('token');
          document.getElementById("profileWindow").innerHTML = "<span style='color:green;font-weight: bold;font-size:large'>Success</span>";
          setTimeout(function() {document.getElementById('profileWindow').innerHTML='';},4000);
          this.loggedIn=false; 
        }
        else {
          document.getElementById("profileWindow").innerHTML = "<span style='color:red;font-weight: bold;font-size:large'>Error. Please try again</span>";
          setTimeout(function() {document.getElementById('profileWindow').innerHTML='';},4000);
        }
      // })
    })
  }
  onSignUpButton() {
    // loggedIn=true; loginWindow=false; 
    let user = new User(this.username, this.password);
    // this.appservice.login(user).subscribe(user => this.loginResponse.push(user));
    this.appservice.signup(user)
    .subscribe((d:{"X-OBSERVATORY-AUTH":string}) => {
      // d.forEach(datum => {
        // if (datum.success=="true") {
          // console.log("token=",datum.token);
          this.key = "token"
          localStorage.setItem(this.key, d["X-OBSERVATORY-AUTH"])
          let item = localStorage.getItem(this.key)
          console.log("saved token=",item);
          document.getElementById("loginWindow").innerHTML = "<span style='color:green;font-weight: bold;font-size:large'>Success</span>";
          setTimeout(function() {document.getElementById('loginWindow').innerHTML='';},4000);
          this.loggedIn=true; 
          // this.loginWindow=false; 
        // }
        // else {
          // document.getElementById("loginWindow").innerHTML = "<span style='color:red;font-weight: bold;font-size:large'>Error. Please try again</span>";
          // setTimeout(function() {document.getElementById('loginWindow').innerHTML='';},4000);
        // }
      // });
    })
  }
  onLogInButton() {
    // loggedIn=true; loginWindow=false; 
    let user = new User(this.username, this.password);
    // this.appservice.login(user).subscribe(user => this.loginResponse.push(user));
    this.appservice.login(user)
    .subscribe((d:{"X-OBSERVATORY-AUTH":string}) => {
      // d.forEach(datum => {
        // if (d.success=="true") {
          // console.log("token=",datum.token);
          this.key = "token"
          localStorage.setItem(this.key, d["X-OBSERVATORY-AUTH"])
          let item = localStorage.getItem(this.key)
          console.log("saved token=",item);
          document.getElementById("loginWindow").innerHTML = "<span style='color:green;font-weight: bold;font-size:large'>Success</span>";
          setTimeout(function() {document.getElementById('loginWindow').innerHTML='';},4000);
          this.loggedIn=true; 
          // this.loginWindow=false; 
        // })
        // else {
        //   document.getElementById("loginWindow").innerHTML = "<span style='color:red;font-weight: bold;font-size:large'>Error. Please try again</span>";
        //   setTimeout(function() {document.getElementById('loginWindow').innerHTML='';},4000);
        // }
      // });
    })
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
  onFilter(){
    // this.form_filter_name
    // this.form_filter_category
    
  }
  onOffersButton(){
    document.getElementById('onOffersButton').innerHTML="<span style='color:red;margin-left:200px;font-weight: bold;font-size:large'>Άουτς</span>";
    setTimeout(function() {document.getElementById('onOffersButton').innerHTML='';},500);
  }
}
