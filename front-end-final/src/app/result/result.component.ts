import { Component, OnInit, Input } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { KeywordService } from '../keyword.service';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {

  articleData: any = [];
  keywordShow: string;

  constructor(private httpClient: HttpClient, private keywordService: KeywordService, private spinner: NgxSpinnerService) { }

  ngOnInit() {
     this.keywordShow = this.getKeyword();
    this.spinner.show();
    setTimeout(() => {
      this.getArticle(this.getKeyword());
      this.spinner.hide();
    }, 1000);
    this.getArticle(this.getKeyword());
    
  }

  getKeyword(): string {
    console.log (this.keywordService.keyword);
    return this.keywordService.keyword;
  }
  getArticle(keyword: string): boolean {
    this.httpClient.get('http://127.0.0.1:5000/search?keyword='+keyword).subscribe(data => {
      this.articleData.push(data);
      console.log(this.articleData);
    });
    return true;
  }

}
