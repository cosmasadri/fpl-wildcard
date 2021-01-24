import { Module } from '@nestjs/common';
import { ScrapperController } from './controllers/scrapper.controller';
import { ScrapperService } from './services/scrapper.service';

@Module({
  imports: [],
  controllers: [ScrapperController],
  providers: [ScrapperService],
})
export class AppModule {}
