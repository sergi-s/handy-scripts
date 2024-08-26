# Cron Job Setup Guide

This guide helps you schedule a cron job to run a Python script.

## Set Up the Cron Job

1. **Open Crontab:**

   ```bash
   crontab -e
   ```

2. **Add the Cron Job:**

   ```bash
   0 2 * * * /bin/bash -c 'source /path/to/your/env/bin/activate && /path/to/your/env/bin/python /path/to/your/main.py'
   ```

   - `0 2 * * *` - Runs daily at 2:00 AM.
   - Replace `/path/to/your/env` with your virtual environment path.
   - Replace `/path/to/your/main.py` with your script path.

3. **Save and Exit:**

   Save the file and exit the editor.

## Verify the Cron Job

List your cron jobs to confirm:

```bash
crontab -l
```