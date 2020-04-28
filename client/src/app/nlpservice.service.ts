import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class NlpserviceService {
  readonly baseUrl = "http://localhost:3000/nlp/getsentiment";
  readonly baseUrl1 = "http://localhost:3000/nlp/getsarcasm";
  constructor(private http:HttpClient) { }

  postsent(cont : any){
    return this.http.post(this.baseUrl,cont);
  }
  getsent(){
    return this.http.get(this.baseUrl);
  }
  postsarc(cont : any){
    return this.http.post(this.baseUrl1,cont);
  }
  getsarc(){
    return this.http.get(this.baseUrl1);
  }
}
