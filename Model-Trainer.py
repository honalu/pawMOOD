
# model_trainer.py - Template for you and Likhitha
# Run this after collecting dataset
# Folder structure: dataset/dog/Labrador/happy/*.jpg etc.

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def train_pet(pet_type="dog", img_size=224, epochs=10):
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2, rotation_range=20, zoom_range=0.2)
    train = datagen.flow_from_directory(f"dataset/{pet_type}", target_size=(img_size,img_size), batch_size=32, subset="training", class_mode="categorical")
    val = datagen.flow_from_directory(f"dataset/{pet_type}", target_size=(img_size,img_size), batch_size=32, subset="validation", class_mode="categorical")
    
    base = tf.keras.applications.MobileNetV2(input_shape=(img_size,img_size,3), include_top=False, weights="imagenet")
    base.trainable = False
    model = tf.keras.Sequential([base, tf.keras.layers.GlobalAveragePooling2D(), tf.keras.layers.Dense(128, activation="relu"), tf.keras.layers.Dense(train.num_classes, activation="softmax")])
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    model.fit(train, validation_data=val, epochs=epochs)
    model.save(f"models/{pet_type}_emotion.h5")
    print(f"Saved models/{pet_type}_emotion.h5")

# Example: train_pet("dog")
