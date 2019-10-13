import { Component, OnInit } from '@angular/core';
import { KeywordService } from '../keyword.service';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['../app.component.css']
})
export class SearchComponent implements OnInit {

  set keyword(value: string) {
    this.keywordService.keyword = value;
  }

  ngOnInit() {
    this.spinner.show();
    setTimeout(() => {
      this.spinner.hide();
    }, 1000);
  }

  constructor(private keywordService: KeywordService, private spinner: NgxSpinnerService) {

  }
}
