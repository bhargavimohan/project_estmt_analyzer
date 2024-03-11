import { Component, OnInit } from '@angular/core';
import { Router, RouterOutlet, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-results',
  standalone: true,
  imports: [CommonModule, RouterOutlet , RouterLink],
  templateUrl: './results.component.html',
  styleUrl: './results.component.css'
})
export class ResultsComponent{
}