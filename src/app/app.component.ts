import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { AnalyzerComponent } from './pages/analyzer/analyzer.component'; 
import { ResultsComponent } from './pages/results/results.component'; 
import { HttpClientModule } from '@angular/common/http';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HomeComponent, AnalyzerComponent, ResultsComponent ,HttpClientModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'estmt-analyzer';
}
