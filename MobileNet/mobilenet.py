# -*- coding: utf-8 -*-
"""MobileNet.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1UzeWnj_iMIJJ-Dr-Y0UUTn5INqs-sukW
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, GlobalAveragePooling2D, Dropout, Dense
from tensorflow.keras.applications import MobileNet

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalize pixel values to range [0, 1]
x_train, x_test = x_train / 255.0, x_test / 255.0

# Resize images to match MobileNet input size
x_train_resized = tf.image.resize(x_train[..., np.newaxis], (32, 32))
x_test_resized = tf.image.resize(x_test[..., np.newaxis], (32, 32))

# Convert labels to one-hot encoding
y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)

# Define MobileNet model without top (classification) layers
base_model = MobileNet(input_shape=(32, 32, 1), include_top=False, weights=None)

# Add new classification layers on top of MobileNet
x = GlobalAveragePooling2D()(base_model.output)
x = Dropout(0.5)(x)
x = Dense(128, activation='relu')(x)
predictions = Dense(10, activation='softmax')(x)

# Combine base MobileNet model with new layers
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(x_train_resized, y_train, epochs=5, batch_size=32, validation_data=(x_test_resized, y_test))

# Evaluate the model
test_loss, test_acc = model.evaluate(x_test_resized, y_test)
print("Test accuracy:", test_acc)

"""Includin Precision and Plotting over epochs"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, GlobalAveragePooling2D, Dropout, Dense
from tensorflow.keras.applications import MobileNet

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalize pixel values to range [0, 1]
x_train, x_test = x_train / 255.0, x_test / 255.0

# Resize images to match MobileNet input size
x_train_resized = tf.image.resize(x_train[..., np.newaxis], (32, 32))
x_test_resized = tf.image.resize(x_test[..., np.newaxis], (32, 32))

# Convert labels to one-hot encoding
y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)

# Define MobileNet model without top (classification) layers
base_model = MobileNet(input_shape=(32, 32, 1), include_top=False, weights=None)

# Add new classification layers on top of MobileNet
x = GlobalAveragePooling2D()(base_model.output)
x = Dropout(0.5)(x)
x = Dense(128, activation='relu')(x)
predictions = Dense(10, activation='softmax')(x)

# Combine base MobileNet model with new layers
model = Model(inputs=base_model.input, outputs=predictions)

# Compile the model with precision in metrics
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy', tf.keras.metrics.Precision()])

model.summary()

# Train the model
history = model.fit(x_train_resized, y_train, epochs=5, batch_size=32, validation_data=(x_test_resized, y_test))

# Evaluate the model
test_loss, test_acc, test_precision = model.evaluate(x_test_resized, y_test)
print("Test accuracy:", test_acc)
print("Test precision:", test_precision)

# Plot training and validation accuracy, precision, and loss over epochs
plt.figure(figsize=(12, 6))

# Plot training & validation accuracy
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')

# Plot training & validation precision
plt.subplot(1, 2, 2)
plt.plot(history.history['precision'])
plt.plot(history.history['val_precision'])
plt.title('Model Precision')
plt.ylabel('Precision')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')

plt.tight_layout()
plt.show()

# Plot training & validation loss
plt.figure(figsize=(6, 4))
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

"""Improved Model"""

import tensorflow as tf
import numpy as np

from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, GlobalAveragePooling2D, Dropout, Dense
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.metrics import Precision, Recall

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalize pixel values

# Resize images to match MobileNet's minimum input size requirement
x_train_resized = tf.image.resize(x_train[..., np.newaxis], (32, 32))
x_test_resized = tf.image.resize(x_test[..., np.newaxis], (32, 32))

# Convert labels to one-hot encoding
y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)

base_model = MobileNet(input_shape=(32, 32, 1), include_top=False, weights=None, alpha=0.5)

# Add new classification layers on top of MobileNet
inputs = Input(shape=(32, 32, 1))
x = base_model(inputs)
x = GlobalAveragePooling2D()(x)
x = Dropout(0.5)(x)
x = Dense(128, activation='relu')(x)
outputs = Dense(10, activation='softmax')(x)

model = Model(inputs=inputs, outputs=outputs)

# Compile the model with additional metrics
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy', Precision(), Recall()])

# Train the model
history = model.fit(x_train_resized, y_train, epochs=5, batch_size=64, validation_data=(x_test_resized, y_test))

# Evaluate the model on test data
test_loss, test_accuracy, test_precision, test_recall = model.evaluate(x_test_resized, y_test)
print(f"Test Loss: {test_loss}")
print(f"Test Accuracy: {test_accuracy}")
print(f"Test Precision: {test_precision}")
print(f"Test Recall: {test_recall}")

# Print model summary
model.summary()

# Convert to TensorFlow Lite with post-training quantization
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

# Save the TensorFlow Lite model
with open('mnist_mobilenet.tflite', 'wb') as f:
    f.write(tflite_model)

print("TensorFlow Lite model is saved.")

!pip install tensorflow_model_optimization
import tensorflow as tf
from tensorflow_model_optimization.sparsity import keras as sparsity

# Define pruning schedule
pruning_schedule = sparsity.PolynomialDecay(initial_sparsity=0.0,
                                            final_sparsity=0.5,
                                            begin_step=0,
                                            end_step=np.ceil(len(x_train) / 64).astype(np.int32) * 5,  # Number of training steps to complete 5 epochs
                                            frequency=100)

# Apply pruning to the model
pruned_model = sparsity.prune_low_magnitude(model, pruning_schedule=pruning_schedule)

# Recompile the pruned model
pruned_model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])

# Add callback for pruning
callbacks = [
    sparsity.UpdatePruningStep(),
    sparsity.PruningSummaries(log_dir='./pruning_summaries'),
]

# Train the pruned model
pruned_model.fit(x_train_resized, y_train, batch_size=64, epochs=5,
                 validation_data=(x_test_resized, y_test),
                 callbacks=callbacks)

# Remove pruning wrappers to finalize the model
final_model = sparsity.strip_pruning(pruned_model)

# Convert the pruned model to TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(final_model)
tflite_model = converter.convert()

# Save the TensorFlow Lite model
with open('mnist_mobilenet_pruned.tflite', 'wb') as f:
    f.write(tflite_model)

print("Model has been pruned, quantized, and converted to TensorFlow Lite.")

# Convert the model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(final_model)
tflite_model = converter.convert()

# Save the TensorFlow Lite model to file
with open('mnist_MB_model.tflite', 'wb') as f:
    f.write(tflite_model)

"""Final Model with precision and recall"""

!pip install tensorflow_model_optimization
import tensorflow as tf
import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, GlobalAveragePooling2D, Dropout, Dense
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.metrics import Precision, Recall
from tensorflow_model_optimization.sparsity import keras as sparsity

# Load and preprocess the MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalize pixel values

# Resize images to match MobileNet's minimum input size requirement
x_train_resized = tf.image.resize(x_train[..., np.newaxis], (32, 32))
x_test_resized = tf.image.resize(x_test[..., np.newaxis], (32, 32))

# Convert labels to one-hot encoding
y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)

# Define a MobileNet model with reduced width (alpha parameter)
base_model = MobileNet(input_shape=(32, 32, 1), include_top=False, weights=None, alpha=0.5)  # alpha reduces the number of filters

# Add new classification layers on top of MobileNet
inputs = Input(shape=(32, 32, 1))
x = base_model(inputs)
x = GlobalAveragePooling2D()(x)
x = Dropout(0.5)(x)
x = Dense(128, activation='relu')(x)
outputs = Dense(10, activation='softmax')(x)

model = Model(inputs=inputs, outputs=outputs)

# Define pruning schedule and wrap the model
pruning_schedule = sparsity.PolynomialDecay(initial_sparsity=0.0,
                                            final_sparsity=0.5,
                                            begin_step=0,
                                            end_step=np.ceil(len(x_train) / 64).astype(np.int32) * 5,
                                            frequency=100)

pruned_model = sparsity.prune_low_magnitude(model, pruning_schedule=pruning_schedule)

# Recompile the model with additional metrics
pruned_model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy', Precision(), Recall()])

# Add callback for pruning and training the model
callbacks = [
    sparsity.UpdatePruningStep(),
    sparsity.PruningSummaries(log_dir='./pruning_summaries'),
]

# Train the model
history = pruned_model.fit(x_train_resized, y_train, epochs=5, batch_size=64,
                           validation_data=(x_test_resized, y_test), callbacks=callbacks)

# Remove pruning wrappers to finalize the model
final_model = sparsity.strip_pruning(pruned_model)

# Convert to TensorFlow Lite with post-training quantization
converter = tf.lite.TFLiteConverter.from_keras_model(final_model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

# Save the TensorFlow Lite model
with open('mnist_mobilenet_compressed.tflite', 'wb') as f:
    f.write(tflite_model)

# Print model summary
final_model.summary()

"""Redo"""

!pip install tensorflow_model_optimization
import tensorflow as tf
import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, GlobalAveragePooling2D, Dropout, Dense
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.metrics import Precision, Recall
from tensorflow_model_optimization.sparsity import keras as sparsity

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0  # Normalize pixel values

# Resize images to match MobileNet's minimum input size requiremen
x_train_resized = tf.image.resize(x_train[..., np.newaxis], (32, 32))
x_test_resized = tf.image.resize(x_test[..., np.newaxis], (32, 32))

# Convert labels to one-hot encoding
y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)

base_model = MobileNet(input_shape=(32, 32, 1), include_top=False, weights=None, alpha=0.5)  # alpha reduces the number of filters

# Add new classification layers on top of MobileNet
inputs = Input(shape=(32, 32, 1))
x = base_model(inputs)
x = GlobalAveragePooling2D()(x)
x = Dropout(0.5)(x)
x = Dense(128, activation='relu')(x)
outputs = Dense(10, activation='softmax')(x)

model = Model(inputs=inputs, outputs=outputs)

# Define pruning schedule and wrap the model
pruning_schedule = sparsity.PolynomialDecay(initial_sparsity=0.0,
                                            final_sparsity=0.5,
                                            begin_step=0,
                                            end_step=np.ceil(len(x_train) / 64).astype(np.int32) * 5,
                                            frequency=100)

pruned_model = sparsity.prune_low_magnitude(model, pruning_schedule=pruning_schedule)

# Recompile the model with additional metrics
pruned_model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy', Precision(), Recall()])

# Add callback for pruning and training the model
callbacks = [
    sparsity.UpdatePruningStep(),
    sparsity.PruningSummaries(log_dir='./pruning_summaries'),
]

# Train the model
history = pruned_model.fit(x_train_resized, y_train, epochs=5, batch_size=64,
                           validation_data=(x_test_resized, y_test), callbacks=callbacks)

# Evaluate the pruned model
pruned_eval = pruned_model.evaluate(x_test_resized, y_test)
print("Pruned Model Evaluation:")
print(f"Loss: {pruned_eval[0]}, Accuracy: {pruned_eval[1]}, Precision: {pruned_eval[2]}, Recall: {pruned_eval[3]}")

# Remove pruning wrappers to finalize the model
final_model = sparsity.strip_pruning(pruned_model)

# Recompile the final model
final_model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy', Precision(), Recall()])

# Evaluate the final stripped model
final_eval = final_model.evaluate(x_test_resized, y_test)
print("Final Model Evaluation after Stripping Pruning:")
print(f"Loss: {final_eval[0]}, Accuracy: {final_eval[1]}, Precision: {final_eval[2]}, Recall: {final_eval[3]}")

# Convert to TensorFlow Lite with post-training quantization
converter = tf.lite.TFLiteConverter.from_keras_model(final_model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

# Save the TensorFlow Lite model
with open('mnist_mobilenet_compressed.tflite', 'wb') as f:
    f.write(tflite_model)

# Print model summary
final_model.summary()