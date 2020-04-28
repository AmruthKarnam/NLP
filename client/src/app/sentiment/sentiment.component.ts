import { Component, OnInit } from '@angular/core';
import { NlpserviceService } from '../nlpservice.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-sentiment',
  templateUrl: './sentiment.component.html',
  styleUrls: ['./sentiment.component.css']
})
export class SentimentComponent implements OnInit {

  constructor(public nlpService:NlpserviceService) { }
  outputsenti:string="";
  public un:String;
  ngOnInit(): void {
  }
  public selectedDetail :any={};

  onSubmit(){
    var tweet1 = "tweet";
    this.selectedDetail[tweet1]=this.un;
    console.log(this.selectedDetail);
    this.nlpService.postsent(this.selectedDetail).subscribe((res)=>{
      console.log(res);
      this.outputsenti=res+"!";
    });
    
  }

}
