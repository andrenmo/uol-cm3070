# uol-cm3070
UOL - CM3070 Final Project

This repository has the Jupyter notebook and python script files to generate the predictions for the CM3070 final project.

The training data must be downloaded from [Kaggle competition page](https://www.kaggle.com/competitions/planet-understanding-the-amazon-from-space/).

The notebook `multi_label_resnet50` generate the Kaggle competition file.

The notebook `parse_data` transform the input data from Kaggle to a single label classification training dataset.

The  script `split_images` script rotate and split the Earth Explorer images to be predicted in the new model.

The notebook `single_label_resnet50` train the model in the new dataset and predict the data for the external data.