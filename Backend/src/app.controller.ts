import { Controller, Get } from '@nestjs/common';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getAppStatus(): string {
    return 'NestJS Backend is running!';
  }

  @Get('hello')
  getHello(): string {
    return this.appService.getHello();
  }
}
