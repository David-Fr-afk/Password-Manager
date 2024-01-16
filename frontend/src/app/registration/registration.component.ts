// registration.component.ts
import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})
export class RegistrationComponent {
  email: string;
  password: string;

  constructor(private http: HttpClient) {}

  onSubmit() {
    const registrationData = {
      email: this.email,
      password: this.password
    };

    // Replace 'YOUR_API_ENDPOINT' with the actual registration API endpoint
    this.http.post('YOUR_API_ENDPOINT', registrationData)
      .subscribe(response => {
        // Handle the response from the server
        console.log('Registration successful:', response);
      }, error => {
        // Handle errors
        console.error('Registration failed:', error);
      });
  }
}
