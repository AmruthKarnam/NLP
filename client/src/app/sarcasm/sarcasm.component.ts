import { NlpserviceService } from './../nlpservice.service';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-sarcasm',
  templateUrl: './sarcasm.component.html',
  styleUrls: ['./sarcasm.component.css']
})
export class SarcasmComponent implements OnInit {

  constructor(public nlpService:NlpserviceService) { }
  outputsarc:string="";
  public un:String;
  ngOnInit(): void {
  }
  public selectedDetail :any={};
  
  
  onSubmit(){
    var tweet1 = "tweet";
    this.selectedDetail[tweet1]=this.un;
    console.log(this.selectedDetail);
    this.nlpService.postsarc(this.selectedDetail).subscribe((res)=>{
    console.log(res);
    if(res=='0'){
      this.outputsarc="No";
    }
    else{
      this.outputsarc="Yes";
      console.log(this.outputsarc);
    }
    });
    
  }

}
