import os
import tensorflow as tf
import numpy as np
import pandas as pd
# path의 excel file을 2차원 배열 numpy type으로 바꾸고, column의 수를 return 하는 function
def excel2Numpy(path):
    # 이곳에 들어가는 문서의 형식은 엑셀이며, 두번째 row부터 label이 존재해야하며, 첫번째 column에 기간을 넣어줘야한다.
    dataframe = pd.read_excel(path, header=1, thousands=',')
    dataframe = dataframe.dropna(axis=0)
    data = np.array(dataframe.drop(dataframe.columns[0], axis=1), dtype=np.float32)

    return data, data.shape[-1]

# 각 column의 데이터를 normalization 하고 결과를 return 하는 function
def normalization(data):
    for i in range(data.shape[-1]):
        mean = data[:, i].mean()
        std = data[:, i].std()
        data[:, i] = (data[:, i] - mean) / std

    return data

# 2차원 배열을 sequence length 만큼 row를 slicing 하여 3차원 배열로 return 하는 function
# Note. seperateData function에 종속된 function
def applyWindow(data, SL):
    result = []
    for i in range(len(data) - SL):
        result.append(data[i : i+SL])
    return np.array(result)

# 데이터를 slicing(applyWindow function)하고, 해당 3차원 배열을 x, y로 나누어 return 하는 function
# Note. applyWindow function을 내부적으로 사용한다.
def seperateData(data, SL):
    result = applyWindow(data, SL)

    x = result[:, :-1, :]
    y = result[:, -1, :]

    return x, y

# prediction.py module에 대한 최종 function
# prediction 값을 return 한다.
def predict(file_path):
    # All comments in function for debugging.
    data, columns_num = excel2Numpy(file_path)

    last_data = np.array([data[-1]])

    data = normalization(data)
    # print(data.shape)
    sequence_len = round(len(data) * 0.05)
    # print(applyWindow(data, sequence_len + 1).shape)
    x, y = seperateData(data, sequence_len+1)
    # print(x.shape, y.shape)
    
    dataset = tf.data.Dataset.from_tensor_slices((x, y)).\
        shuffle(buffer_size=len(x)).\
        batch(round(len(x) * 0.05), drop_remainder=False)
    
    model = tf.keras.models.Sequential([
        tf.keras.layers.Bidirectional(tf.keras.layers.GRU(32, return_sequences=True)),
        tf.keras.layers.TimeDistributed(tf.keras.layers.Dropout(rate=.2)),
        tf.keras.layers.GRU(32, return_sequences=False),
        tf.keras.layers.Dropout(rate=.2),
        tf.keras.layers.Dense(units=16),
        tf.keras.layers.Dense(units=columns_num)
    ])

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    model.compile(loss='mse', optimizer=optimizer)
    model.fit(dataset, epochs=30)

    # 예측에서의 증감을 구해 normalization 되지않은 값에 증감비율을 곱해 결과값으로 냄
    prediction_results = []
    for i in range(1, 3):
        prediction_results.append(model.predict(np.array([[data[-i]]])))
    increase_ratio = prediction_results[0] / prediction_results[1]
    results = increase_ratio * last_data

    # 1차원 배열로 변경
    results = np.squeeze(results)

    # Javascript는 "123465."과 같은 숫자 인식 못함
    # Javascript에 전송을 위해 list로 변환
    results = results.tolist()

    return results
