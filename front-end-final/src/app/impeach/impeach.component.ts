import { Component, OnInit, Input } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'app-impeach',
  templateUrl: './impeach.component.html',
  styleUrls: ['./impeach.component.css']
})
export class ImpeachComponent implements OnInit {

  articleData: any = [];
  keywordShow: string;

  constructor(private httpClient: HttpClient, private spinner: NgxSpinnerService) { }

  ngOnInit() {
    this.spinner.show();
    setTimeout(() => {
      this.getArticle();
      this.spinner.hide();
    }, 5000);
    // this.getArticle();
    
  }


  getArticle() {
    this.httpClient.get('http://127.0.0.1:5000/search?keyword=impeachment').subscribe(data => {
      this.articleData.push(data);
      console.log(this.articleData);
    })
  }

}
