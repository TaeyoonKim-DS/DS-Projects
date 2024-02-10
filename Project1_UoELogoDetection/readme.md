# University of Edinburgh Logo Detection using YOLOv8

This repository contains a custom YOLOv8 model trained to detect the University of Edinburgh logo in images.

## Introduction
The University of Edinburgh logo detection model is built using the YOLOv8 architecture, which is a state-of-the-art deep learning algorithm for object detection tasks. This model is trained to accurately locate and classify instances of the University of Edinburgh logo within images.

## Dataset
The dataset used for training this model consists of a collection of images containing various instances of the University of Edinburgh logo. These images were manually annotated with bounding boxes specifying the location of the logo within each image.

## Model Training
The YOLOv8 model was trained using the annotated dataset mentioned above. The training process involved optimizing the model's parameters to minimize the detection loss and improve its accuracy in identifying the University of Edinburgh logo.

## Evaluation
The trained model's performance was evaluated on a separate validation set to assess its ability to accurately detect the University of Edinburgh logo in unseen images. Evaluation metrics such as precision, recall, and mean Average Precision (mAP) were computed to measure the model's performance.

## Results
The trained YOLOv8 model demonstrates robust performance in detecting the University of Edinburgh logo across a variety of images. Sample results and visualizations of the model's predictions are provided in the repository.

## Usage
To use the trained model for logo detection, follow the instructions provided in the `UoE_training%prediction.ipynb` notebook. This notebook contains code examples demonstrating how to load the model and perform logo detection on custom images.

## Dependencies
- Python 3
- PyTorch
- OpenCV
- NumPy

## Contact
For any inquiries or feedback, please contact [Taeyoon Kim](taeyoon.kim.ds@gmail.com).
