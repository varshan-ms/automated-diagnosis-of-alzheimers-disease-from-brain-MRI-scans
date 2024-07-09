
---

# Automated Diagnosis of Alzheimer's Disease from Brain MRI Scans

This project automates the diagnosis of Alzheimer's disease using brain MRI scans and a deep learning model. The system includes a web interface for user and doctor interactions, enabling users to predict their condition and book appointments with doctors.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Requirements](#requirements)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Acknowledgements](#acknowledgements)

## Introduction

This project leverages brain MRI scans and deep learning techniques to diagnose Alzheimer's disease. It includes a web application for users to upload MRI scans and receive predictions, and for doctors to provide feedback and book appointments.

## Installation

To set up the project, follow these steps:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/varshan-ms/automated-diagnosis-of-alzheimers-disease-from-brain-MRI-scans.git
    cd automated-diagnosis-alzheimers
    ```

2. **Extract the ZIP File:**

    Extract the contents of the provided ZIP file into the project directory.

## Requirements

Ensure you have the following software installed:

- **PyCharm**
- **Python**
- **WinRAR** (or any other extraction tool)
- **WampServer** (for hosting the website)

## Setup

1. **Set Up WampServer:**

    - Start WampServer.
    - Open `phpMyAdmin` and create a new database named `2doctorapdbpy`.
    - Import the SQL file provided in the ZIP into this database.

2. **Install Required Python Packages:**

    Open PyCharm, navigate to the project directory, and install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. **Start WampServer:**

    Ensure WampServer is running.

2. **Run the Main Application:**

    In PyCharm, open `App.py` located in the `CnnVgg` folder and run it.

3. **Access the Web Application:**

    After running `App.py`, a local host URL will be output in PyCharm. Click this URL to open the web application in your browser.

4. **Using the Web Application:**

    - **User Login:** Users can log in, upload an MRI scan, and receive a diagnosis (mild, non-demented, very mild dementia). Users can also book appointments with doctors for further consultation.
    - **Doctor Login:** Doctors can log in to view user data, provide precautions and remedies, and confirm appointments.

## Deep Learning Model

This project employs a Convolutional Neural Network (CNN) based on the VGG architecture for image classification tasks. The model is trained on MRI scan images to identify different stages of Alzheimer's disease.

### Model Architecture

- **Input Layer:** Preprocessed MRI scans
- **Convolutional Layers:** Multiple layers with ReLU activation
- **Pooling Layers:** Max pooling for downsampling
- **Fully Connected Layers:** Dense layers for classification
- **Output Layer:** Softmax activation for predicting the stage of Alzheimer's disease

## Acknowledgements

- The ADNI initiative for providing the dataset.
- Contributors to the open-source libraries and frameworks used in this project.
- The developers and researchers whose work inspired and supported this project.

---

Feel free to further customize this to better fit your project's specific needs.
