import { Injectable } from '@nestjs/common';
import { Options, PythonShell } from 'python-shell';

@Injectable()
export class PythonORService {
  async optimize(): Promise<any> {
    const options: Options = {
      mode: 'json',
      pythonPath: 'venv/Scripts/python.exe',
      pythonOptions: ['-u'],
      scriptPath: 'src/scripts',
    };

    const pythonFileName = 'python-ortools.py';

    const selectedPlayers = await new Promise((resolve) => {
      PythonShell.run(pythonFileName, options, async (err, results) => {
        if (err) throw err;

        return resolve(results[0]);
      });
    });

    return selectedPlayers;
  }
}
