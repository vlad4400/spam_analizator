import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-spam-check',
  standalone: true,
  imports: [CommonModule, FormsModule], 
  templateUrl: './spam-check.component.html'
})
export class SpamCheckComponent {
  emailText = '';
  spamResult: string | null = null;

  constructor(private http: HttpClient) {}

  checkSpam() {
    const payload = { email_text: this.emailText };
    this.http.post<any>('http://127.0.0.1:8000/api/check_spam/', payload)
      .subscribe({
        next: (response) => {
          this.spamResult = response.result;
        },
        error: (error) => {
          console.error('Błąd podczas sprawdzania spamu:', error);
        }
      });
  }
}
