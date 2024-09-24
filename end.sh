#!/bin/bash

# 'sleep' 프로세스 종료
echo "Terminating all 'sleep' processes..."
pgrep sleep | xargs -r sudo kill -9

# 'start_script.sh' 프로세스 종료
echo "Terminating all 'start_script.sh' processes..."
pgrep -f start_script.sh | xargs -r sudo kill -9

# 'uvicorn' 프로세스 종료
echo "Terminating all 'uvicorn' processes..."
pgrep -f uvicorn | xargs -r sudo kill -9

echo "All specified processes have been terminated."
