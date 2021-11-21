# TermProject-Fa21-ECE382V
Algorithms for Planar Geometry - Rachelle David &amp; Juan Neri

## Instructions:

install git and pip and venv
```
sudo apt-get install git
sudo apt install python3-pip
sudo apt install python3-venv
```

clone the repo
```
git clone https://github.com/juanjoneri/TermProject-Fa21-ECE382V.git
```

init venv (takes a few minutes)
```
python3 -m venv testing
source testing/bin/activate
python3 -m pip install -r requirements.txt
```

go to code directory
```
cd convex_hull
```

execute the code
```
python3 quickhull.py datasets/circle-1000
```

exit the environment
```
deactivate
```