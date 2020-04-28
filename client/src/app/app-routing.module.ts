import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { SentimentComponent } from './sentiment/sentiment.component';
import { SarcasmComponent } from './sarcasm/sarcasm.component';


const routes: Routes = [
  {path : "",component:HomeComponent},
  {path : "home",component:HomeComponent},
  {path:"sentiment",component:SentimentComponent},
  {path : "sarcasm",component:SarcasmComponent}

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
