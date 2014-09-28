import random
import liblinearutility

def read_features():
    return None

def get_folds(data):
    data_count = len(data)
    fold_cout = int(data_count / 5)
    data_keys = data.keys()
    added = set()
    folds = []

    for i in range(5):
        added_count = 0
        fold = {}

        while added_count < fold_count:
            rand_key = random.choice(data_keys)
            
            if rand_key not in added:
                added.add(rand_key)
                fold[rand_key] = data[rand_key]

        folds.append(fold)

    return folds

def train(train_data, features):
    x = []
    y = []

    for key in train_data:
        y.append(train_data[key])
        x.append(features[key])

    prob = liblinearutil.problem(y, x)
    param = liblinearutil.parameter('-c 0')
    model = liblinearutil.train(prob, param)
    return model

def predict(test_data, model):
    x = []
    y = []

    for key in test_data:
        y.append(test_data[key])
        x.append(test_data[key])

    p_label, p_acc, p_val = predict(y, x, m, '-b 1')
    return p_label

def evaluate(predictions, actual):
    return 0


data = None #Read this somehow

folds = get_folds(data)

for i in range(5):
    train_data = []
    for j in range(5):
        if i == j:
            next
        train_data.extend(data[j])
    
    test_data = data[i]

    model = train(train_data)
    predictions = predict(test_data, model)
