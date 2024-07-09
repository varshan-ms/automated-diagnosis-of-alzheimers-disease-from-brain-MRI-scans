# importing libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import random
import glob  # to find files

# Seaborn library for bar chart
import seaborn as sns

# Libraries for TensorFlow
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing import image
from tensorflow.keras import models, layers

# Library for Transfer Learning
from tensorflow.keras.applications import VGG16
from keras.applications.vgg16 import preprocess_input

print("Importing libraries completed.")

path = 'Datas/'

train_folder = path + "train/"
train_normal_dir = train_folder + "MildDemented/"
train_pneu_dir = train_folder + "NonDemented/"
train_pneu_dir1 = train_folder + "VeryMildDemented/"

# test directory
test_folder = path + "test/"
test_normal_dir = test_folder + "MildDemented/"
test_pneu_dir = test_folder + "NonDemented/"
test_pneu_dir1 = test_folder + "VeryMildDemented/"

# validation directory
val_folder = path + "Val/"

val_normal_dir = val_folder + "MildDemented/"
val_pneu_dir = val_folder + "NonDemented/"
val_pneu_dir1 = val_folder + "VeryMildDemented/"

# variables for image size
img_width = 100
img_height = 100

# variable for model
batch_size = 64
epochs = 10

print("Variable declaration completed.")

# listing the folders containing images

# Train Dataset
train_class_names = os.listdir(train_folder)
print("Train class names: %s" % (train_class_names))
# print("\n")

# Test Dataset
test_class_names = os.listdir(test_folder)
print("Test class names: %s" % (test_class_names))
# print("\n")

# Validation Dataset
val_class_names = os.listdir(val_folder)
print("Validation class names: %s" % (val_class_names))

print("\nDataset class name listing completed.")


# declaration of functions

# Function get name of xray type
def Get_Xray_Type(argument):
    switcher = {
        "MildDemented": "MildDemented",
        "NonDemented": "NonDemented",
        "VeryMildDemented": "VeryMildDemented",
    }
    return switcher.get(argument, "Invalid image")


print("Declaration of functions completed.")

# Analysis of Train, Test and Validation directory

# find all files, our files has extension jpeg
train_normal_cases = glob.glob(train_normal_dir + '*jpg')
train_pneu_cases = glob.glob(train_pneu_dir + '*jpg')
train_pneu_cases1 = glob.glob(train_pneu_dir1 + '*jpg')

test_normal_cases = glob.glob(test_normal_dir + '*jpg')
test_pneu_cases = glob.glob(test_pneu_dir + '*jpg')
test_pneu_cases1 = glob.glob(test_pneu_dir1 + '*jpg')

val_normal_cases = glob.glob(val_normal_dir + '*jpg')
val_pneu_cases = glob.glob(val_pneu_dir + '*jpg')
val_pneu_cases1 = glob.glob(val_pneu_dir1 + '*jpg')
# create lists for train, test & validation cases, create labels as well
train_list = []
test_list = []
val_list = []

for x in train_normal_cases:
    train_list.append([x, "MildDemented"])

for x in train_pneu_cases:
    train_list.append([x, "NonDemented"])

for x in train_pneu_cases1:
    train_list.append([x, "VeryMildDemented"])

for x in test_normal_cases:
    test_list.append([x, "MildDemented"])

for x in test_pneu_cases:
    test_list.append([x, "NonDemented"])

for x in test_pneu_cases1:
    test_list.append([x, "VeryMildDemented"])

for x in val_normal_cases:
    val_list.append([x, "MildDemented"])

for x in val_pneu_cases:
    val_list.append([x, "NonDemented"])

for x in val_pneu_cases1:
    val_list.append([x, "VeryMildDemented"])

# create dataframes
train_df = pd.DataFrame(train_list, columns=['image', 'Diagnos'])
print(train_df.shape)
test_df = pd.DataFrame(test_list, columns=['image', 'Diagnos'])
print(test_df.shape)
val_df = pd.DataFrame(val_list, columns=['image', 'Diagnos'])
print(val_df.shape)

plt.figure(figsize=(20, 5))

plt.subplot(1, 3, 1)
# sns.countplot(train_df['Diagnos'])
# sns.distplot(train_df, y='Diagnos')

ax = sns.countplot(y=train_df['Diagnos'], data=train_df)
plt.title('Train data')

plt.subplot(1, 3, 2)
ax = sns.countplot(y=test_df['Diagnos'], data=train_df)
plt.title('Test data')

plt.subplot(1, 3, 3)

ax = sns.countplot(y=val_df['Diagnos'], data=train_df)
plt.title('Validation data')

plt.show()

plt.figure(figsize=(20, 8))
for i, img_path in enumerate(train_df[train_df['Diagnos'] == "MildDemented"][0:4]['image']):
    plt.subplot(2, 4, i + 1)
    plt.axis('off')
    img = plt.imread(img_path)
    plt.imshow(img, cmap='gray')
    plt.title('MildDemented')

for i, img_path in enumerate(train_df[train_df['Diagnos'] == "NonDemented"][0:4]['image']):
    plt.subplot(2, 4, 4 + i + 1)
    plt.axis('off')
    img = plt.imread(img_path)
    plt.imshow(img, cmap='gray')
    plt.title('Normal')
plt.show()
# Declaring variables
x = []  # to store array value of the images
y = []  # to store the labels of the images

for folder in os.listdir(train_folder):
    image_list = os.listdir(train_folder + "/" + folder)
    for img_name in image_list:
        # Loading images
        img = image.load_img(train_folder + "/" + folder + "/" + img_name, target_size=(img_width, img_height))

        # Converting to arrary
        img = image.img_to_array(img)

        # Transfer Learning: this is to apply preprocess of VGG16 model to our images before passing it to VGG16
        img = preprocess_input(img)  # Optional step

        # Appending the arrarys
        x.append(img)  # appending image array
        y.append(train_class_names.index(folder))  # appending class index to the array

print("Preparing Training Dataset Completed.")

# Preparing validation images data (image array and class name) for processing

# Declaring variables
val_images = []
val_images_Original = []
val_image_label = []  # to store the labels of the images

for folder in os.listdir(val_folder):
    image_list = os.listdir(val_folder + "/" + folder)
    for img_name in image_list:
        # Loading images
        img = image.load_img(val_folder + "/" + folder + "/" + img_name, target_size=(img_width, img_height))

        # Converting to arrarys
        img = image.img_to_array(img)

        # Saving original images, will be used just for display at the end
        val_images_Original.append(img.copy())

        # Transfer Learning: this is to apply preprocess of VGG16 to our images before passing it to VGG16
        img = preprocess_input(img)  # Optional step

        # Appending arrays
        val_images.append(img)  # appending image array
        val_image_label.append(val_class_names.index(folder))

print("Preparing Validation Dataset Completed.")

# Preparing validation images data (image array and class name) for processing

# Declaring variables
test_images = []
test_images_Original = []
test_image_label = []  # to store the labels of the images

for folder in os.listdir(test_folder):
    image_list = os.listdir(test_folder + "/" + folder)
    for img_name in image_list:
        # Loading images
        img = image.load_img(test_folder + "/" + folder + "/" + img_name, target_size=(img_width, img_height))

        # Converting to arrarys
        img = image.img_to_array(img)

        # Saving original images, will be used just for display at the end
        test_images_Original.append(img.copy())

        # Transfer Learning: this is to apply preprocess of VGG16 to our images before passing it to VGG16
        img = preprocess_input(img)  # Optional step

        # Appending arrays
        test_images.append(img)  # appending image array
        test_image_label.append(test_class_names.index(folder))

print("Preparing Test Dataset Completed.")

# Verifying the output

# Training Dataset
print("Training Dataset")

x = np.array(x)  # Converting to np arrary to pass to the model
print(x.shape)

y = to_categorical(y)  # onehot encoding of the labels
# print(y)
print(y.shape)

print("Test Dataset")

test_images = np.array(test_images)
print(test_images.shape)

test_image_label = to_categorical(test_image_label)  # onehot encoding of the labels)
print(test_image_label.shape)

# ===========

# Validation Dataset
print("Validation Dataset")

val_images = np.array(val_images)
print(val_images.shape)

val_image_label = to_categorical(val_image_label)  # onehot encoding of the labels)
print(val_image_label.shape)

print("Summary of default VGG16 model.\n")

# we are using VGG16 for transfer learnin here. So we have imported it
from tensorflow.keras.applications import VGG16

model_vgg16 = VGG16(weights='imagenet')
model_vgg16.summary()

print("Summary of Custom VGG16 model.\n")
input_layer = layers.Input(shape=(img_width, img_height, 3))
model_vgg16 = VGG16(weights='imagenet', input_tensor=input_layer, include_top=False)
model_vgg16.summary()
last_layer = model_vgg16.output
flatten = layers.Flatten()(last_layer)
output_layer = layers.Dense(3, activation='softmax')(flatten)
model = models.Model(inputs=input_layer, outputs=output_layer)

model.summary()
for layer in model.layers[:-1]:
    layer.trainable = False
model.summary()

from sklearn.model_selection import train_test_split

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=5)
print("Splitting data for train and test completed.")

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print("Model compilation completed.")

history2 = model.fit(xtrain, ytrain, epochs=epochs, batch_size=batch_size, verbose=True, validation_data=(xtrain, ytrain))

print("Fitting the model completed.")

model.save("Vggmodel")

acc = history2.history['accuracy']
val_acc = history2.history['val_accuracy']
epochs = range(len(acc))

plt.plot(epochs, acc, label='Training Accuracy')
plt.plot(epochs, val_acc, label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.show()

# Plot Model Loss
loss_train = history2.history['loss']
loss_val = history2.history['val_loss']
plt.plot(epochs, loss_train, label='Training Loss')
plt.plot(epochs, loss_val, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()


y_pred = model.predict(xtrain)
y_pred = np.argmax(y_pred, axis=1)
print(y_pred)
y_test = np.argmax(ytest, axis=1)
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
print(cm)

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix of VGg')
plt.show()