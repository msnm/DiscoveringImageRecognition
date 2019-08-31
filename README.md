# DiscoveringImageRecognition
In this repo I'm exploring how to recognise CAPTCHA's. I started with one character 'a-z' and I'm now training a model for two digits (0-9). My goal is to have model for captchas with atleast 2 characters 'a-z', but I have to take into account limited hardware resources.

In the output folder there is another readme with my notes why I decided to change the network architecture after each run. 
In the output folder every run contains the test_acc in its foldername + numbers or character and how many. In each folder the model.json can be found + the python code + the pyplot image of the test train acc and loss. 
The weights are not uploaded in this repo because these files where to large.

# Setup
Create your own virtual environment by running the following commands:


```
python3 -m venv env-deeplearning
source env-deeplearning/bin/activate
pip install keras
pip install tensorflow
pip install matplotlib
pip install keras.preprocessing
pip install sklearn
Pip install ImageCaptcha
```

The setup can be tested by running the scripts in the MNIST folder:
```
python helloKeras.py
python mnist_keras.py
```

To reset the source env-deeplearning to the global env type:
```
deactivate
```

# Resources

https://realpython.com/python-virtual-environments-a-primer/
