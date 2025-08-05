#README


In the same folder as the run-tk-chatbot.sh run the following:

#install virtual environments in pip named tk-chatbot-venv:
python3 -m venv tk-chatbot-venv

source tk-chatbot-venv/bin/activate

#install packages:
pip install ollama secrets tk

#deactivate venv:
deactivate

#modify permissions for chatbot script w/ sudo chroot +x on the run-tk-chatbot.sh script:
sudo chroot +x run-tk-chatbot.sh

#run script to activate chatbot:
./run-tk-chatbot.sh


