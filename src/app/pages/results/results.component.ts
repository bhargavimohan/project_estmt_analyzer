import { Component, OnInit } from '@angular/core';
import { RouterModule , RouterOutlet, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';


@Component({
  selector: 'app-results',
  standalone: true,
  imports: [CommonModule, RouterOutlet , RouterLink, FormsModule],
  templateUrl: './results.component.html',
  styleUrl: './results.component.css'
})


export class ResultsComponent implements OnInit {
  fileNames: string[] = [];
  fileDescription: { key: string, value: string }[] = [];
  items: { [fileName: string]: any } = {}; // Dictionary to store file name and its corresponding JSON data
  excludedItems: { key: string, value: string }[] = [];
  fileSelected : string = ''
  excludedKeys: string[] = ['E-stmnt Analyzer Status', 'New Balance', 'Cost of ALL categories'];

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.getAllItems();
    this.fileSelected = ''

  }

  getAllItems() {
    this.http.get<any>('http://127.0.0.1:8001/analyzed-pdfs').subscribe(
      data => {
        this.items = data.items;
        this.fileNames = Object.keys(this.items).map(fileName => Object.keys(this.items[fileName])[0]);
      },

      error => {
        console.error('Error fetching items:', error);
      }
    );
  }

  onSelectFileName(fileName: string) {
    if (fileName != null) {
      const keys = Object.keys(this.items);
      for (let i = 0; i < keys.length; i++) {
        const key = keys[i];
        if (this.items[key].hasOwnProperty(fileName)) {
          const jsonString = this.items[key][fileName];
          if (jsonString) {
            this.fileDescription = JSON.parse(jsonString)
            console.log(Object.keys(JSON.parse(jsonString))
            .filter(key => this.excludedKeys.includes(key))
            .map(key => ({ key, value: JSON.parse(jsonString)[key]})));
            this.excludedItems = Object.keys(JSON.parse(jsonString))
            .filter(key => this.excludedKeys.includes(key))
            .map(key => ({ key, value: JSON.parse(jsonString)[key] }))
          } else {
            this.fileDescription = [];
            this.excludedItems = [];
          }
          return;
        }
      }
      this.fileDescription = [];
      this.excludedItems = [];
    } else {
      this.fileDescription = [];
      this.excludedItems = [];
    }
  }

  onReset(event: any) {
    this.fileDescription = [];
    this.excludedItems = [];
    this.fileSelected = '';
    const fileInput = document.getElementById('fileInput') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = ''; // Clear the selected file
  }
  }


}