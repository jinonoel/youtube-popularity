import random
import argparse
import sys
import math
import pymongo

sys.path.append('/Users/jino/Code/liblinear-1.94/python')
import liblinearutil

#C_RANGE = [
#    0.0000001,
#    0.000001, 
#    0.00001, 
#    .0001, 
#    0.001, 
#    0.01, 
#    0.1, 
#    0.5, 
#    1, 
 #   2, 
#    10,
#    100,
#    1000,
#    10000,
#    100000
#]

C_RANGE = [
    2e-15,
    2e-13,
    2e-11,
    2e-9,
    2e-7,
    2e-5,
    2e-3,
    2e-1,
    2e0,
    2e1,
    2e3,
    2e5,
    2e7,
    2e9,
    2e11,
    2e13,
    2e15
]

#C_RANGE = [1]

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
    param = liblinearutil.parameter('-q -c ' + str(c) )
    model = liblinearutil.train(prob, param)

    return model

def predict(test_data, features, model):
    x = []
    y = []

    keys = test_data.keys()
    for key in keys:
        y.append(test_data[key])
        x.append(features[key])

    p_label, p_acc, p_val = liblinearutil.predict(y, x, model, '-q')
    
    predictions = {}
    reverse = False
    for i in range(len(p_label)):
        predictions[keys[i]] = {
            'class' : p_label[i],
            'score' : p_val[i][0]
        }

        if (p_label[i] <= 0 and p_val[i][0] > 0):
            reverse = True

        if (p_label[i] > 0 and p_val[i][0] < 0):
            reverse = True
            
    if reverse:
        print 'REVERSING SCORE!'

        for key in predictions:
            predictions[key]['score'] *= -1

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
        metrics = evaluate_pr100(predictions, test_data)
        print metrics, c

        score = metrics
        
        if score > best_score:
            best_c = c
            best_score = score

    print "Best C: " + str(best_c)
    return best_c

def normalize_train(train_data, features):
    feature_sum = []
    feature_mean = []
    
    count = 0
    feature_max = []
    feature_min = []

    for vid_id in features:
        if vid_id not in train_data:
            continue

        feat = features[vid_id]
        count += 1

        for f in range(len(feat)):
            if len(feature_sum) == f:
                feature_sum.append(feat[f])
                feature_max.append(feat[f])
                feature_min.append(feat[f])
            else:
                feature_sum[f] += feat[f]
                if feat[f] > feature_max[f]:
                    feature_max[f] = feat[f]
                if feat[f] < feature_min[f]:
                    feature_min[f] = feat[f]


    for f in range(len(feature_sum)):
        feature_mean.append(feature_sum[f] / float(count))

    feature_std = []
    for vid_id in features:
        if vid_id not in train_data:
            continue

        feat = features[vid_id]

        for f in range(len(feat)):
            val = (feat[f] - feature_sum[f]) ** 2
            if len(feature_std) == f:
                feature_std.append(val)
            else:
                feature_std[f] += val
    
    for f in range(len(feature_std)):
        feature_std[f] = math.sqrt(feature_std[f] / float(count))


    normalized_features = {}
    for vid_id in features:
        if vid_id not in train_data:
            continue
            
        feat = features[vid_id]
        normalized = []

        for f in range(len(feat)):
            n = float(feat[f] - feature_mean[f]) / feature_std[f] 
            normalized.append(n)

        normalized_features[vid_id] = normalized

    #print feature_sum
    #print feature_max
    #print feature_min
    return normalized_features, feature_mean, feature_std

def normalize_test(test_data, features, feature_mean, feature_std):
    normalized_features = {}

    for vid_id in features:
        if vid_id not in test_data:
            #print 'WHAT'
            continue

        feat = features[vid_id]
        normalized = []

        for f in range(len(feat)):
            n = float(feat[f] - feature_mean[f]) / feature_std[f]
            normalized.append(n)

        normalized_features[vid_id] = normalized

    return normalized_features

def evaluate_pr100(predictions, actual):
    #assume pos score counts as a positive label (assert checks above)
    sorted_preds = sorted(predictions.keys(), key=lambda vid: predictions[vid]['score'], reverse=True)

    correct = 0
    for i in range(100):
        #print predictions[sorted_preds[i]], actual[sorted_preds[i]]

        if actual[sorted_preds[i]] > 0:
            correct += 1


    return float(correct) / 100

def evaluate_aprf(predictions, actual):
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for key in predictions:
        if predictions[key]['class'] > 0:
            if actual[key] > 0:
                tp += 1
            else:
                fp += 1
        else:
            if actual[key] > 0:
                fn += 1
            else:
                tn += 1

    
    return (float(tp + tn) / float(tp + fp + tn + fn)), tp, tn, fp, fn



def cross_validate(data, features):
    print 'Getting folds'
    folds = get_folds(data)

    average_acc = 0
    average_pr100 = 0
    for i in range(5):
        print 'Fold', (i+1)
        
        train_data = {}
        for j in range(5):
            if i == j:
                continue

            train_data.update(folds[j])
        continue

        test_data = folds[i]

        print "Normalize"
        normalized_train_features, mean, std = normalize_train(train_data, features)
        normalized_test_features = normalize_test(test_data, features, mean, std)

        print "Tune"
        best_c = get_best_c(train_data, normalized_train_features)

        print "Train"
        model = train(train_data, normalized_train_features, best_c)

        print "Predict"
        predictions = predict(test_data, normalized_test_features, model)

        print "Evaluate"
        score = evaluate_aprf(predictions, test_data)
        pr100 = evaluate_pr100(predictions, test_data)
        accr = score[0]

        #print score[1], score[2], score[3], score[4]
        print "Accuracy:", accr
        print "Pr@100:", pr100
        print

        average_acc += accr
        average_pr100 += pr100

    print "Average Accuracy:", average_acc / 5
    print "Average Pr@100:", average_pr100 / 5


def insert_predictions(data, features):
    folds = get_folds(data)
    test_data = folds[0]
    train_data = {}
    train_data.update(folds[1])
    train_data.update(folds[2])
    train_data.update(folds[3])
    train_data.update(folds[4])

    print "Normalize"
    normalized_train_features, mean, std = normalize_train(train_data, features)
    normalized_test_features = normalize_test(test_data, features, mean, std)

    print "Tune"
    best_c = get_best_c(train_data, normalized_train_features)
    
    print "Train"
    model = train(train_data, normalized_train_features, best_c)

    print "Predict"
    predictions = predict(test_data, normalized_test_features, model)

    print "Insert"
    conn = pymongo.MongoClient('localhost')
    db = conn['nicta']
    coll = db['predictions']

    for vid_id in predictions:
        coll.insert({
            'id' : vid_id,
            'score' : predictions[vid_id]['score'],
            'actual' : test_data[vid_id]
        })

    conn.close()
    print "Done"

parser = argparse.ArgumentParser()
parser.add_argument('data_file')
parser.add_argument('feature_file')
args = parser.parse_args()

data = read_data(args.data_file)
features = read_features(args.feature_file)

#cross_validate(data, features)
insert_predictions(data, features)
