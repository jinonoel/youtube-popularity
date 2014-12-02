import random
import argparse
import sys
import math
import pymongo

sys.path.append('/Users/jino/Code/liblinear-1.94/python')
import liblinearutil

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

def sum_log(features):
    val = 0

    for f in features:
        val += math.log(f + 1)

    return val

def log_sum(features):
    val = 0

    for f in features:
        val += f + 1

    return math.log(val)

def mean_log(features):
    val = sum_log(features)
    return float(val) / len(features)

def log_mean(features):
    val = 0

    for f in features:
        val += f + 1

    val /= float(len(features))
    return math.log(val)

def std_log(features):
    vals = []
    val_sum = 0

    for f in features:
        log = math.log(f + 1)
        vals.append(log)
        val_sum += log

    val_mean = float(val_sum) / len(features)

    std = 0
    for v in vals:
        std += (val_mean - v) ** 2

    std /= float(len(vals))
    return math.sqrt(std)

def log_std(features):
    val_sum = 0

    for f in features:
        val_sum += f

    val_mean = float(val_sum) / len(features)

    std = 0
    for f in features:
        std += (val_mean - f) ** 2

    std /= float(len(features))
    return math.log(math.sqrt(std) + 1)

def read_features(filename, user_filename, baseline_file = False, valid = {}):
    feature_map = {}
    video_users = {}
    all_users = set()

    valid_set = set(valid)
    print "Reading features"
    for line in open(filename):
        #print line
        tokens = line.strip().split(',')
        if tokens[0] not in valid_set:# or len(tokens) != 6:
            continue

        if len(tokens) < 6:
            print line
            continue

        feature = []
        valid = True
        for i in range(1, 6):
            try:
                feature.append(float(tokens[i]))
            except ValueError:
                valid = False
                break

        if valid:
            feature_map[tokens[0]] = feature
            video_users[tokens[0]] = set();

            for i in range(6, len(tokens)):
                video_users[tokens[0]].add(tokens[i])
                all_users.add(tokens[i])

            if len(video_users[tokens[0]]) == 0:
                print "ZERO!"

    print "All users:", len(all_users)
    print "All videos:", len(feature_map)

    print "Reading baselines"
    if baseline_file:
        for line in open(baseline_file):
            tokens = line.strip().split(',')
            if tokens[0] not in valid_set or len(tokens) != 2:
                continue

            vid_id = tokens[0]
            views = tokens[1]
            if vid_id in feature_map:
                feature_map[vid_id].append(int(views))


    print "Read user features"
    user_map = {}
    for line in open(user_filename):
        tokens = line.strip().split(',')
        user_id = tokens[0]
        if user_id not in all_users:
            continue

        user_feature = []
        for i in range(1, 6):
            user_feature.append(float(tokens[i]))

        user_map[user_id] = user_feature


    print "user_map:", len(user_map)

    vid_count = 0
    remove = set()
    vid_active_features = {}
    for vid_id in feature_map:
        vid_count += 1
        if vid_count % 50000 == 0:
            print vid_count

        active_features = []

        for u in video_users[vid_id]:
            if u not in user_map:
                continue


            for i in range(len(user_map[u])):
                if len(active_features) == i:
                    active_features.append([])

                active_features[i].append(user_map[u][i])

            #print "yo:", len(active_features), len(user_map[u])

        if len(active_features) < 5:
            remove.add(vid_id)
            continue

        vid_active_features[vid_id] = active_features

        for i in range(len(active_features)):
            feature_map[vid_id].append(sum_log(active_features[i]))
            feature_map[vid_id].append(log_sum(active_features[i]))
            feature_map[vid_id].append(mean_log(active_features[i]))
            feature_map[vid_id].append(log_mean(active_features[i]))
            feature_map[vid_id].append(std_log(active_features[i]))
            feature_map[vid_id].append(log_std(active_features[i]))

            #print sum_log(active_features[i]), log_sum(active_features[i]), mean_log(active_features[i]), log_mean(active_features[i]), std_log(active_features[i]), log_std(active_features[i])
            #print

        #print feature_map[vid_id]


    for r in remove:
        del feature_map[r]

    print "final:", len(feature_map)

    return feature_map, vid_active_features


def read_data(filename):
    data = {}

    for line in open(filename):
        tokens = line.strip().split(',')
        if len(tokens) != 5:
            continue
        data[tokens[0]] = {
            'class' : int(tokens[1]),
            'views' : int(tokens[2]),
            'upload_date' : tokens[3]
        }

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
        y.append(train_data[key]['class'])
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
        #y.append(test_data[key]['class'])
        y.append(0);
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
    return evaluate_map(predictions, actual)

    #assume pos score counts as a positive label (assert checks above)
    sorted_preds = sorted(predictions.keys(), key=lambda vid: predictions[vid]['score'], reverse=True)

    correct = 0
    for i in range(100):
        #print predictions[sorted_preds[i]], actual[sorted_preds[i]]

        if actual[sorted_preds[i]]['class'] > 0:
            correct += 1


    return float(correct) / 100

def evaluate_map(predictions, actual):
    sorted_preds = sorted(predictions.keys(), key=lambda vid: predictions[vid]['score'], reverse=True)
    
    mean_ap = 0
    pos_count = 0
    print "Len:", len(sorted_preds)
    for i in range(len(sorted_preds)):
        if actual[sorted_preds[i]]['class'] > 0:
            pos_count += 1
            mean_ap += pos_count / float(i + 1)

    mean_ap /= float(pos_count)
    return mean_ap

def cross_validate(data, features):
    print 'Getting folds'
    folds = get_folds(data)

    average_pr100 = 0
    for i in range(5):
        print 'Fold', (i+1)
        
        train_data = {}
        for j in range(5):
            if i == j:
                continue

            train_data.update(folds[j])

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
        pr100 = evaluate_pr100(predictions, test_data)

        print "Score:", pr100
        print

        average_pr100 += pr100

    print "Average Score", average_pr100 / 5


def insert_predictions(data, features, active_features, baseline_file, date):
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
    pred_coll = db['predictions_' + date]
    vid_coll = db['videos']
    w_coll = db['weights_' + date]

    for line in open(baseline_file):
        tokens = line.strip().split(',')
        vid_id = tokens[0]
        if vid_id not in test_data:
            continue

        A_score = int(tokens[1])

        test_data[vid_id]['train_views'] = A_score


    pred_coll.drop()
    for vid_id in predictions:
        pred_coll.insert({
            'id' : vid_id,
            'score' : predictions[vid_id]['score'],
            'actual' : test_data[vid_id]['class'],
            'upload_date' : test_data[vid_id]['upload_date'],
            'B_views' : test_data[vid_id]['views'],
            'A_views' : test_data[vid_id]['train_views'],
            'features' : features[vid_id],
            'active_features' : active_features[vid_id]
        })

    pred_coll.ensure_index("A_views")

    liblinearutil.save_model('MODEL.DAT', model)
    weight_line = False
    weights = []
    for line in open('MODEL.DAT'):
        if not weight_line and line.strip() != 'w':
            continue
        elif line.strip() == 'w':
            weight_line = True
            continue
        else:
            weights.append(float(line.strip()))

    w_coll.remove()
    w_coll.insert({'weights' : weights})
            
        
    conn.close()
    print "Done"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action')
    parser.add_argument('data_file')
    parser.add_argument('feature_file')
    parser.add_argument('baseline_file')
    parser.add_argument('user_features_file')
    parser.add_argument('date')
    args = parser.parse_args()

    data = read_data(args.data_file)
    features, active_features = read_features(args.feature_file, args.user_features_file, args.baseline_file, data.keys())

    
    remove = set()
    for key in data:
        if key not in features:
            remove.add(key)
    for r in remove:
        del data[r]

    if args.action == 'cross_validate':
        cross_validate(data, features)
    elif args.action == 'insert':
        insert_predictions(data, features, active_features, args.baseline_file, args.date)
