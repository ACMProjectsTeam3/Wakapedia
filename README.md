# Wakapedia



First, download all the .txt files with the words 'wikipedia' in them, save them to a single directory, navigate to that directory in terminal, then run: 

cat *.txt > kimenet.txt

Then, download the .py program called LSTMRNN.py (or something), change the first file-path in the 'train' definition to match that of the text file, initialize the definition, and run it by just typing 

train()

in your python shell 


****TRY RUNNING JUST ONE EPOCH (nb_epoch) AT A TIME. THERE ARE SOMETIMES ISSUES WITH THE WEIGHT OF THE NEURONS DOWNLOADING, AND IT'S BETTER TO FIND OUT EARLY ON IF THERES A PROBLEM. ONCE YOU KNOW THAT THE WEIGHTS ARE DOWNLOADING AT LEAST SOMEWHERE, INCREASE nb_epoch TO SOMEWHERE BETWEEN 10-29*****
