import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';
import { SpamCheckComponent } from './app/spam-check/spam-check.component';

bootstrapApplication(SpamCheckComponent, appConfig)
  .catch((err) => console.error(err));
