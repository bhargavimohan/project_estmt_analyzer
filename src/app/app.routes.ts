import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { AnalyzerComponent } from './pages/analyzer/analyzer.component'; 
import { ResultsComponent } from './pages/results/results.component'; 

export const routes: Routes = [

    {
        path : '', redirectTo :'home', pathMatch : 'full'
    },
    {
        path : 'home',
        component : HomeComponent
    },
    {
        path : 'analyzer',
        component : AnalyzerComponent
    },
    {
        path : 'results',
        component : ResultsComponent
    }
];