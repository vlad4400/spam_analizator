import { Component, AfterViewInit, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

import * as d3 from 'd3';
import { delay, of, switchMap } from 'rxjs';

@Component({
  selector: 'app-spam-check',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './spam-check.component.html',
  styleUrls: ['./spam-check.component.scss'],
})
export class SpamCheckComponent implements AfterViewInit {
  emailText = '';
  spamResult: string | null = null;
  loading = false;

  // Referencja do kontenera, w którym utworzymy SVG
  @ViewChild('d3background', { static: true }) d3Container!: ElementRef;

  constructor(private http: HttpClient) {}

  ngAfterViewInit(): void {
    this.initD3Animation();
  }

  checkSpam() {
    this.loading = true;
    this.spamResult = null;

    const payload = { email_text: this.emailText };

    this.http
      .post<any>('https://my-backend-service-955511185320.europe-west1.run.app/api/check_spam/', payload)
      .pipe(switchMap((response) => of(response).pipe(delay(1000)))) // min. 1 sekunda
      .subscribe({
        next: (response) => {
          this.loading = false;
          this.spamResult = response.result;
        },
        error: (error) => {
          this.loading = false;
          console.error('Błąd podczas sprawdzania spamu:', error);
        },
      });
  }

  private initD3Animation() {
    // Rozmiary "sceny"
    const width = window.innerWidth;
    const height = window.innerHeight;

    // Tworzymy SVG w elemencie #d3background
    const svg = d3
      .select(this.d3Container.nativeElement)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .style('position', 'fixed') // aby wypełniało okno
      .style('top', 0)
      .style('left', 0)
      .style('z-index', '-1'); // pod naszym kontentem

    // Tworzymy kilka kółek (np. 12)
    const circlesCount = 12;
    const circlesData = d3.range(circlesCount).map(() => {
      return {
        x: Math.random() * width,
        y: Math.random() * height,
        r: 40 + Math.random() * 60,
        color: d3.interpolateRainbow(Math.random()),
      };
    });

    // Dodajemy elementy <circle> do SVG
    const circles = svg
      .selectAll('circle')
      .data(circlesData)
      .enter()
      .append('circle')
      .attr('cx', (d) => d.x)
      .attr('cy', (d) => d.y)
      .attr('r', (d) => d.r)
      .attr('fill', (d) => d.color)
      .attr('fill-opacity', 0.3);

    // Funkcja animująca kółka – zmiana pozycji i koloru
    function animate() {
      circles
        .transition()
        .duration(3000) // 3 sekundy
        .ease(d3.easeQuadInOut)
        .attr('cx', () => Math.random() * width)
        .attr('cy', () => Math.random() * height)
        .attr('fill', () => d3.interpolateRainbow(Math.random()))
        .on('end', animate); // po skończeniu – znowu
    }

    // Start animacji
    animate();
  }
}
