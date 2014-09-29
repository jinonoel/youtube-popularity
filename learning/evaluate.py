import random
import argparse
import sys

sys.path.append('/Users/jino/Code/liblinear-1.94/python')
import liblinearutil

C_RANGE = [0.5, 1, 2]
random.seed(1)

def read_features(filename):
    feature_map = {}

    for line in open(filename):
        tokens = line.strip().split(',')
        feature = []

        for i in range(1, len(tokens)):
            feature.append(float(tokens[i]))

        feature_map[tokens[0]] = feature

    return feature_map

def read_data(filename):
    data = {}

    for line in open(filename):
        tokens = line.strip().split(',')
        data[tokens[0]] = int(tokens[1])

    return data

def get_folds(data):
    data_count = len(data)
    fold_count = int(data_count / 5)
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
                added_count += 1

        folds.append(fold)

    return folds

def train(train_data, features, c):
    x = []
    y = []

    for key in train_data:
        y.append(train_data[key])
        x.append(features[key])

    prob = liblinearutil.problem(y, x)
    param = liblinearutil.parameter('-c ' + str(c) + ' -s 0')
    model = liblinearutil.train(prob, param)
    return model

def predict(test_data, features, model):
    x = []
    y = []

    keys = test_data.keys()
    for key in keys:
        y.append(test_data[key])
        x.append(features[key])

    p_label, p_acc, p_val = liblinearutil.predict(y, x, model)
    predictions = {}
    for i in range(len(p_label)):
        predictions[keys[i]] = p_label[i]

    return predictions

def get_best_c(data, features):
    folds = get_folds(data)
    test_data = folds[0]
    train_data = {}
    train_data.update(folds[1])
    train_data.update(folds[2])
    train_data.update(folds[3])
    train_data.update(folds[4])

    best_c = 0
    best_score = -1

    for c in C_RANGE:
        c_model = train(train_data, features, c)
        predictions = predict(test_data, features, c_model)
        score = evaluate(predictions, test_data)
        
        print 'C: ' + str(c) + ' Score: ' + str(score)

        if score > best_score:
            best_c = c
            best_score = score

    print "Best C: " + str(best_c)
    return best_c

def evaluate(predictions, actual):
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for key in predictions:
        if predictions[key] > 0:
            if actual[key] > 0:
                tp += 1
            else:
                fp += 1
        else:
            if actual[key] > 0:
                fn += 1
            else:
                tn += 1

    return float(tp + tn) / float(tp + fp + tn + fn)


parser = argparse.ArgumentParser()
parser.add_argument('data_file')
parser.add_argument('feature_file')
args = parser.parse_args()

data = read_data(args.data_file)
features = read_features(args.feature_file)

print 'Getting folds'
folds = get_folds(data)

for i in range(5):
    train_data = {}
    for j in range(5):
        if i == j:
            next
        
        train_data.update(folds[j])
        
    best_c = get_best_c(train_data, features)

    test_data = folds[i]

    print 'fold', (i+1), len(train_data), len(test_data)

    model = train(train_data, features, best_c)

    predictions = predict(test_data, features, model)
    score = evaluate(predictions, test_data)

    print "Score: " + str(score)
