import cv2
import numpy as np
from keras.applications import VGG19
from keras.models import Model
from keras.layers import Dense, Flatten

# Load the pre-trained VGG19 model
base_model = VGG19(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze the layers in the base model
for layer in base_model.layers:
    layer.trainable = False

# Add a new output layer on top of the pre-trained model
x = base_model.output
x = Flatten()(x)
predictions = Dense(1, activation='sigmoid')(x)
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Load the small set of labeled fake video samples
train_videos = "/content/drive/MyDrive/dfdc/traini"
validation_videos = ['/content/drive/MyDrive/dfdc/dfdc/train/fake/Copy of abarnvbtwb.mp4', '/content/drive/MyDrive/dfdc/dfdc/train/fake/Copy of abofeumbvv.mp4']
train_labels = np.array([0, 1])  # Replace with the actual labels
validation_labels = np.array([0, 1])  # Replace with the actual labels

# Define the function to extract frames from the video
def extract_frames(video_path, num_frames=10):
    frames = []
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % (cap.get(cv2.CAP_PROP_FRAME_COUNT) // num_frames) == 0:
            frame = cv2.resize(frame, (224, 224))
            frame = np.expand_dims(frame, axis=0)
            frames.append(frame)
        frame_count += 1
    cap.release()
    frames = np.concatenate(frames, axis=0)
    return frames

train_frames = []
for video_path in train_videos:
    frames = extract_frames(video_path)
    train_frames.append(frames)
train_frames = np.concatenate(train_frames, axis=0)
train_labels = np.repeat(train_labels, 10)

validation_frames = []
for video_path in validation_videos:
    frames = extract_frames(video_path)
    validation_frames.append(frames)
validation_frames = np.concatenate(validation_frames, axis=0)
validation_labels = np.repeat(validation_labels, 10)

# Train the model
model.fit(
        train_frames,
        train_labels,
        batch_size=32,
        epochs=10,
        validation_data=(validation_frames, validation_labels))

# Evaluate the model on a separate set of validation data
score = model.evaluate(validation_frames, validation_labels)
print('Validation loss:', score[0])
print('Validation accuracy:', score[1])
