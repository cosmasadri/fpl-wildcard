import { Module } from '@nestjs/common';
import { PythonORController } from './controllers/python-or.controller';
import { ScrapperController } from './controllers/scrapper.controller';
import { PythonORService } from './services/python-or.service';
import { ScrapperService } from './services/scrapper.service';

@Module({
  imports: [],
  controllers: [ScrapperController, PythonORController],
  providers: [ScrapperService, PythonORService],
})
export class AppModule {}
