import { Component } from '@angular/core';
import { Router, RouterOutlet, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-analyzer',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink],
  // providers : [HttpClient],
  templateUrl: './analyzer.component.html',
  styleUrl: './analyzer.component.css'
})


export class AnalyzerComponent {

  selectedTab = "Analyzer"
  selectedFile: File | null = null;
  uploadSuccessMessage: string = '';
  errorMessage: string = '';
  successMessage: string = '';
  uploadInProgress: boolean = false; 
  uploadFailMessage : string = '';
  analysisCompleteMessage : string = '';

  makeActive(tab: string) {
    this.selectedTab = tab;
  }
  

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (file && !file.type.includes('pdf')) {
      this.selectedFile = null;
      this.errorMessage = 'Error: Please select a PDF file';
    } else {
      this.selectedFile = file;
      this.errorMessage = '';
    }
  }

  constructor(private http: HttpClient) {}

  onUpload(event: any) {
    if (!this.selectedFile) {
      this.errorMessage = 'Error: No file selected';
      return;
    }
    this.uploadInProgress = true;
    this.analysisCompleteMessage = ''
    {
  
      const formData: FormData = new FormData();
      formData.append('file', this.selectedFile);
      // Handle sucess response here
      this.http.post('http://127.0.0.1:8001/receive', formData)
        .subscribe(response  => {
          console.log('File uploaded successfully:', response);
          console.log((response as any).message)
          this.successMessage = 'File was uploaded successfully, analysis has begun . . .';
          this.uploadInProgress = false;
          this.analysisCompleteMessage = (response as any).message
        }, (error : any) => {
          console.error('Error uploading file:', error);
          this.uploadFailMessage = 'Upload error, Try again after sometime . . .'
          this.successMessage = '';
          this.uploadInProgress = false; 
          // Handle error response here
        });
    }
}

onReset(event: any) {
  this.selectedFile = null;
  this.errorMessage = '';
  this.successMessage = '';
  this.uploadFailMessage = ''
  this.analysisCompleteMessage = ''
  const fileInput = document.getElementById('fileInput') as HTMLInputElement;
  if (fileInput) {
    fileInput.value = ''; // Clear the selected file
}
}
}