#!/bin/bash
# Start Backend
source venv/bin/activate
uvicorn src.server:app --reload --port 8000 &
BACKEND_PID=$!

# Start Frontend
cd ui
npm start &
FRONTEND_PID=$!

echo "Career Hunter started!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "Press Ctrl+C to stop."

wait $BACKEND_PID $FRONTEND_PID
