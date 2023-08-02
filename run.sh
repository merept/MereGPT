python3 ./src/checkModule.py
python3 ./src/main.py
if [ $? -eq 1 ]; then
  python3 ./src/update/update
  sh ./run.sh
fi