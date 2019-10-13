import { Component } from '@angular/core';
import { Subject } from 'rxjs';
import { LoaderService } from '../../../services/loader-service.service';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'app-loader',
  templateUrl: './loader.component.html',
  styleUrls: ['./loader.component.css']
})
export class LoaderComponent {
  color = 'primary';
  mode = 'indeterminate';
  value = 50;
  isLoading: Subject<boolean> = this.loaderService.isLoading;
  constructor(private spinner: NgxSpinnerService, private loaderService: LoaderService){}
}