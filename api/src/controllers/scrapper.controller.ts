import { Controller, Get } from '@nestjs/common';
import { ScrapperService } from '../services/scrapper.service';

@Controller('scrap')
export class ScrapperController {
  constructor(private readonly scrapperService: ScrapperService) {}

  @Get()
  async scrap(): Promise<any> {
    return this.scrapperService.scrap();
  }
}
