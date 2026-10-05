# 🌱 AI-Based Plant Health Monitoring for  Aquaponics

## 📌 Project Overview

Aquaponics is a sustainable farming system that combines aquaculture, the cultivation of aquatic organisms such as fish, with hydroponics, the soil-less cultivation of plants. In an aquaponics system, nutrient-rich water generated from fish waste is circulated to the plant-growing area, where plants utilize the available nutrients and help maintain water quality.

The **AI-Based Plant Health Monitoring** module is an intelligent extension of the Smart Aquaponics System. It introduces computer vision and deep learning techniques to monitor the visible health condition of plants using images captured by a camera.

Traditional plant monitoring mainly depends on manual observation. This can be time-consuming and may not identify early visual changes consistently. The proposed system uses a camera to capture plant images and a trained deep learning model to analyze these images and classify the plant according to the health categories used during model training.

The trained model is currently developed and tested using **Google Colab** and saved in Keras format. The next stage of implementation is to deploy the trained model on a **Raspberry Pi connected to a camera module**, enabling image-based plant health monitoring within the aquaponics setup.

The AI-based result can eventually be combined with sensor parameters such as **pH, water temperature, and ammonia level** to provide a more comprehensive assessment of plant and water conditions.

---

# 🎯 Objectives


- Develop an image-based plant health monitoring system.
- Capture and preprocess plant images for AI classification.
- Train a deep learning model to identify visible plant health conditions.
- Enable early detection of plant stress or disease symptoms.
- Reduce the need for continuous manual inspection.
- Integrate AI monitoring with aquaponics water-quality parameters.
- Provide a foundation for Raspberry Pi-based real-time monitoring.
---

# 🌿 Motivation

Plant health in an aquaponics system is influenced by several factors, including water quality, nutrient availability, temperature, pH, ammonia concentration, lighting, and possible diseases or environmental stress.

Although sensors can measure important water parameters, sensor readings alone cannot directly determine the visible condition of plant leaves.

For example:


Water Quality Sensors
        ↓
pH / Temperature / Ammonia
        ↓
Water Condition

These parameters provide information about the growing environment.
However:

**Camera
   ↓
Plant Image
   ↓
Leaf Appearance
   ↓
Visual Plant Condition**


provides complementary information about the plant itself.
Therefore, combining sensor-based monitoring with image-based AI analysis can provide a more complete understanding of the aquaponics ecosystem.

# 🧠 AI-Based Plant Health Monitoring

The proposed AI module follows the workflow:

**Plant Image → Image Preprocessing → Deep Learning Model → Plant Health Classification → Health Status → Dashboard**

---

## 1. 📷 Plant Image Acquisition

A camera module connected to the Raspberry Pi is used to capture images of the plants in the aquaponics system.

The camera continuously monitors the visible condition of the plants and provides images for AI-based analysis.

### Image Acquisition Process


**Plant
   ↓
Camera Module
   ↓
Raspberry Pi
   ↓
Captured Plant Image**

             
## 2. 🖼️ Image Preprocessing

Before sending the captured image to the trained AI model, the image is preprocessed.

The preprocessing steps include:

- Image resizing
- Pixel normalization
- Conversion into the required image format
- Preparation of the image as model input

The preprocessing ensures that the captured image is compatible with the trained deep learning model.

### Preprocessing Workflow


**Captured Image
      ↓
Resize Image
      ↓
Normalize Pixel Values
      ↓
Convert to Model Input**


## 3. 🧠 Deep Learning Model

A deep learning-based image classification model is used for plant health monitoring.

The model is trained using plant images representing different health conditions.

The trained model learns visual characteristics such as:

- Leaf colour
- Leaf shape
- Spots or abnormal patterns
- Discolouration
- Visible signs of stress or disease

The trained model is stored as:

plant_model.keras

The model can later be loaded into the Raspberry Pi for plant health prediction.

---

## 4. 📚 Model Training

The AI model is trained using a labelled plant image dataset.

The dataset is divided into training and validation data.


**Plant Image Dataset
        ↓
Dataset Preparation
        ↓
Training Images + Validation Images
        ↓
Deep Learning Model
        ↓
Model Training
        ↓
Trained Model**

## 5. 📊 Training and Validation

The dataset is divided into training and validation sets.

### Training Set

The training images are used to teach the model how to recognize different plant conditions.

### Validation Set

The validation images are used to evaluate how well the trained model performs on images that were not directly used for learning.

The model performance can be evaluated using:

- Training accuracy
- Validation accuracy
- Training loss
- Validation loss

These parameters help determine whether the model is learning effectively.

---

## 6. 🔍 Model Prediction

After training, a new plant image can be provided to the model.

The model processes the image and predicts the corresponding plant health class.

### Prediction Workflow



**New Plant Image
       ↓
Image Preprocessing
       ↓
Trained AI Model
       ↓
Prediction
       ↓
Plant Health Class
       ↓
Dashboard / Alert**



