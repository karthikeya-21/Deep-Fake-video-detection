import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB7, ResNet50, VGG19
from tensorflow.keras.layers import Dense, Dropout, Flatten, Input
from tensorflow.keras.models import Model

train_dir = '/content/drive/MyDrive/dfdc/traini'
validation_dir = '/content/drive/MyDrive/dfdc/dfdc/vali'


# Set batch size and image dimensions
batch_size = 32
img_height = 224
img_width = 224

# Function to extract frames from videos using OpenCV
def extract_frames(video_path):
    frames = []
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (img_height, img_width))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
        else:
            break
    cap.release()
    return frames

train_videos = [os.path.join(train_dir, f) for f in os.listdir(train_dir)]
train_labels = [1] * len(train_videos)  # All videos are fake
train_frames = [extract_frames(v) for v in train_videos]
train_frames = np.array(train_frames) / 255.0
train_labels = np.array(train_labels)

validation_videos = [os.path.join(validation_dir, f) for f in os.listdir(validation_dir)]
validation_labels = [1] * len(validation_videos)  # All videos are fake
validation_frames = [extract_frames(v) for v in validation_videos]
validation_frames = np.array(validation_frames) / 255.0
validation_labels = np.array(validation_labels)

train_ds = tf.data.Dataset.from_tensor_slices((train_frames, train_labels)).shuffle(len(train_frames)).batch(batch_size)
validation_ds = tf.data.Dataset.from_tensor_slices((validation_frames, validation_labels)).batch(batch_size)
input_shape = (img_height, img_width, 3)
inputs = Input(shape=input_shape)

vgg_model = VGG19(weights='imagenet', include_top=False, input_tensor=inputs)
resnet_inputs = Input(shape=input_shape)
resnet_model = ResNet50(weights='imagenet', include_top=False, input_tensor=resnet_inputs)
efficientnet_inputs = Input(shape=input_shape)
efficientnet_model = EfficientNetB7(weights='imagenet', include_top=False, input_tensor=efficientnet_inputs)

vgg_output = Flatten()(vgg_model.output)
vgg_output = Dense(256, activation='relu')(vgg_output)
vgg_output = Dropout(0.5)(vgg_output)
vgg_output = Dense(1, activation='sigmoid')(vgg_output)
vgg_model = Model(inputs=inputs, outputs=vgg_output)

resnet_output = Flatten()(resnet_model.output)
resnet_output = Dense(256, activation='relu')(resnet_output)
resnet_output = Dropout(0.5)(resnet_output)
resnet_output = Dense(1, activation='sigmoid')(resnet_output)
resnet_model = Model(inputs=resnet_inputs, outputs=resnet_output)

efficientnet_output = Flatten()(efficientnet_model.output)
efficientnet_output = Dense(256, activation='relu')(efficientnet_output)
efficientnet_output = Dropout(0.5)(efficientnet_output)
efficientnet_output = Dense(1, activation='sigmoid')(efficientnet_output)
efficientnet_model = Model(inputs=efficientnet_inputs, outputs=efficientnet_output)



for layer in vgg_model.layers:
  layer.trainable = False
for layer in resnet_model.layers:
  layer.trainable = False
for layer in efficientnet_model.layers:
  layer.trainable = False

merged = tf.keras.layers.concatenate([vgg_model.output, resnet_model.output, efficientnet_model.output])
merged_output = Dense(256, activation='relu')(merged)
merged_output = Dropout(0.5)(merged_output)
merged_output = Dense(1, activation='sigmoid')(merged_output)

model = Model(inputs=[inputs, resnet_inputs, efficientnet_inputs], outputs=merged_output)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
