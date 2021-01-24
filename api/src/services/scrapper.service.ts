import { BadRequestException, Injectable } from '@nestjs/common';
import axios from 'axios';

@Injectable()
export class ScrapperService {
  async scrap(): Promise<any> {
    const res = await axios.get(
      'https://fantasy.premierleague.com/api/bootstrap-static/',
      {
        headers: {
          'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        },
      },
    );

    if (res.headers['content-length'] === 0) {
      throw new BadRequestException(
        'No places infromation found on the payload',
      );
    }

    return res.data;
  }
}
