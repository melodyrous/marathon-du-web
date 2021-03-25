## Ce repertoire contient les éléments web du projet


#### Installation pour la partie site/Base de donnée 

- conda create -n MarathonWeb python=3.8.3
- conda activate MarathonWeb
- cd ./branche_Concernée...
- conda install django==3.1.1
- conda install -c conda-forge django-debug-toolbar==3.1
- pip install mysqlclient

#### Installation pour la partie machine learning

- conda install pytorch torchvision cudatoolkit=10.0 -c pytorch
- pip install sentence-transformers
- pip install umap-learn
- pip install hdbscan
- pip install pandas
- pip install beautifulsoup4
- pip install protobuf