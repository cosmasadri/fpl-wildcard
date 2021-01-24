import { Controller, Get } from '@nestjs/common';
import { PythonORService } from '../services/python-or.service';

@Controller('optimize')
export class PythonORController {
  constructor(private readonly pythonORService: PythonORService) {}

  @Get()
  async optimize(): Promise<any> {
    return this.pythonORService.optimize();
  }
}
