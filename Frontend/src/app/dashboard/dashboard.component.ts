import { Component } from '@angular/core';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent {
  credentials: any;

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.authService.viewCredentials().subscribe(
      (data) => (this.credentials = data),
      (error) => console.error(error)
    );
  }
}
