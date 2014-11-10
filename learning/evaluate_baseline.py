import random
import argparse
import sys
import math
import pymongo

sys.path.append('/Users/jino/Code/liblinear-1.94/python')
sys.path.append('/Users/jino/Code/YTPopularity/learning')
import liblinearutil
import evaluate


def predict_baseline(test_data, test_features):
    predictions = {}

    for vid in test_data:
        predictions[vid] = {
            'class': 0,
            'score' : test_features[vid][0]
        }

    return predictions

def cross_validate(data, test_features):
    print 'Getting folds'
    folds = evaluate.get_folds(data)

    average_pr100 = 0
    for i in range(5):
        print 'Fold', (i+1)
        
        test_data = folds[i]

        print "Predict"
        predictions = predict_baseline(test_data, test_features)

        print "Evaluate"
        pr100 = evaluate.evaluate_map(predictions, test_data)

        print "Pr@100:", pr100
        print

        average_pr100 += pr100

    print "Average Pr@100:", average_pr100 / 5

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    parser.add_argument('feature_file')
    args = parser.parse_args()

    data = evaluate.read_data(args.data_file)
    features = evaluate.read_features(args.feature_file, False, data.keys())

    print 'data', len(data)
    print 'feat', len(features)
    #sys.exit()

    remove = set()
    for key in data:
        if key not in features:
            remove.add(key)
    for r in remove:
        del data[r]

    #print len(data), len(features)
    cross_validate(data, features)
