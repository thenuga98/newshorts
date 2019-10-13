import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ResultComponent } from './result/result.component';
import { SearchComponent } from './search/search.component';
import { ClimateComponent } from './climate/climate.component';
import { HkComponent } from './hk/hk.component';
import { ImpeachComponent } from './impeach/impeach.component';

const routes: Routes = [
  {path: '', component: SearchComponent },
  {path: 'result', component: ResultComponent },
  {path: 'result/climate', component: ClimateComponent },
  {path: 'result/hongkong', component: HkComponent },
  {path: 'result/impeachment', component: ImpeachComponent },

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
