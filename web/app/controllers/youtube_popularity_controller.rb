class YoutubePopularityController < ApplicationController

  def index
  end

  def number_with_delimiter(number, delimiter=",")
    number.to_s.gsub(/(\d)(?=(\d\d\d)+(?!\d))/, "\\1#{delimiter}")
  end

  def doAction
    upload_date = params['upload_date']
    threshold = params['threshold'].to_i
    sort_by = params["sort_by"]

    filter = {}
    if threshold > 0
      filter['A_views'] = {'$lte' => threshold}
    end

    conn = Mongo::Connection.new('localhost')
    db = conn['nicta']
    coll = db['predictions_' + upload_date]
    w_coll = db['weights_' + upload_date]

    top_videos = []
    score_rank = 1
    coll.find(filter,
              {
                :sort => ['score', 'desc'],
                :limit => 100
              }).each do |result|
      top_videos << {
        'vid_id' => result['id'],
        'score' => result['score'],
        'actual' => result['actual'],
        'upload_date' => result['upload_date'],
        'a_views' => number_with_delimiter(result['A_views']),
        'b_views' => number_with_delimiter(result['B_views']),
        'a_count' => result['A_views'],
        'b_count' => result['B_views'],
        'features' => result['features'].inspect,
        'features_arr' => result['normalized_features'],
        'model_rank' => score_rank,
        'sample_tweets' => result['sample_tweets'],
        'sample_authors' => result['sample_authors'],
        'average_tweets' => result['average_tweets']
      }

      score_rank += 1
    end

    a_rank = 1
    top_videos.sort{|a,b| b['a_count'] <=> a['a_count']}.each do |v|
      v['a_rank'] = a_rank
      a_rank += 1
    end

    b_rank = 1
    top_videos.sort{|a,b| b['b_count'] <=> a['b_count']}.each do |v|
      v['b_rank'] = b_rank
      b_rank += 1
    end

    weights = w_coll.find_one()['weights']
    weights_map = {}
    weights_map['v.mention'] = weights[0]
    weights_map['v.hashtag'] = weights[1]
    weights_map['v.rt'] = weights[2]
    weights_map['v.nbc'] = weights[3]
    weights_map['v.tweet'] = weights[4]
    weights_map['v.a_views'] = weights[5]

    weights_map['u.mention:sum_log'] = weights[6]
    weights_map['u.mention:log_sum'] = weights[7]
    weights_map['u.mention:mean_log'] = weights[8]
    weights_map['u.mention:log_mean'] = weights[9]
    weights_map['u.mention:std_log'] = weights[10]
    weights_map['u.mention:log_std'] = weights[11]
    weights_map['u.mention_per_day:sum_log'] = weights[12]
    weights_map['u.mention_per_day:log_sum'] = weights[13]
    weights_map['u.mention_per_day:mean_log'] = weights[14]
    weights_map['u.mention_per_day:log_mean'] = weights[15]
    weights_map['u.mention_per_day:std_log'] = weights[16]
    weights_map['u.mention_per_day:log_std'] = weights[17]

    weights_map['u.hashtag:sum_log'] = weights[18]
    weights_map['u.hashtag:log_sum'] = weights[19]
    weights_map['u.hashtag:mean_log'] = weights[20]
    weights_map['u.hashtag:log_mean'] = weights[21]
    weights_map['u.hashtag:std_log'] = weights[22]
    weights_map['u.hashtag:log_std'] = weights[23]
    weights_map['u.hashtag_per_day:sum_log'] = weights[24]
    weights_map['u.hashtag_per_day:log_sum'] = weights[25]
    weights_map['u.hashtag_per_day:mean_log'] = weights[26]
    weights_map['u.hashtag_per_day:log_mean'] = weights[27]
    weights_map['u.hashtag_per_day:std_log'] = weights[28]
    weights_map['u.hashtag_per_day:log_std'] = weights[29]

    weights_map['u.rt:sum_log'] = weights[30]
    weights_map['u.rt:log_sum'] = weights[31]
    weights_map['u.rt:mean_log'] = weights[32]
    weights_map['u.rt:log_mean'] = weights[33]
    weights_map['u.rt:std_log'] = weights[34]
    weights_map['u.rt:log_std'] = weights[35]
    weights_map['u.rt_per_day:sum_log'] = weights[36]
    weights_map['u.rt_per_day:log_sum'] = weights[37]
    weights_map['u.rt_per_day:mean_log'] = weights[38]
    weights_map['u.rt_per_day:log_mean'] = weights[39]
    weights_map['u.rt_per_day:std_log'] = weights[40]
    weights_map['u.rt_per_day:log_std'] = weights[41]

    weights_map['u.nbc:sum_log'] = weights[42]
    weights_map['u.nbc:log_sum'] = weights[43]
    weights_map['u.nbc:mean_log'] = weights[44]
    weights_map['u.nbc:log_mean'] = weights[45]
    weights_map['u.nbc:std_log'] = weights[46]
    weights_map['u.nbc:log_std'] = weights[47]
    weights_map['u.nbc_per_day:sum_log'] = weights[48]
    weights_map['u.nbc_per_day:log_sum'] = weights[49]
    weights_map['u.nbc_per_day:mean_log'] = weights[50]
    weights_map['u.nbc_per_day:log_mean'] = weights[51]
    weights_map['u.nbc_per_day:std_log'] = weights[52]
    weights_map['u.nbc_per_day:log_std'] = weights[53]

    weights_map['u.tweet:sum_log'] = weights[54]
    weights_map['u.tweet:log_sum'] = weights[55]
    weights_map['u.tweet:mean_log'] = weights[56]
    weights_map['u.tweet:log_mean'] = weights[57]
    weights_map['u.tweet:std_log'] = weights[58]
    weights_map['u.tweet:log_std'] = weights[59]
    weights_map['u.tweet_per_day:sum_log'] = weights[60]
    weights_map['u.tweet_per_day:log_sum'] = weights[61]
    weights_map['u.tweet_per_day:mean_log'] = weights[62]
    weights_map['u.tweet_per_day:log_mean'] = weights[63]
    weights_map['u.tweet_per_day:std_log'] = weights[64]
    weights_map['u.tweet_per_day:log_std'] = weights[65]


    weights_map['u.mention_interaction:sum_log'] = weights[66]
    weights_map['u.mention_interaction:log_sum'] = weights[67]
    weights_map['u.mention_interaction:mean_log'] = weights[68]
    weights_map['u.mention_interaction:log_mean'] = weights[69]
    weights_map['u.mention_interaction:std_log'] = weights[70]
    weights_map['u.mention_interaction:log_std'] = weights[71]
    weights_map['u.mention_interaction_per_day:sum_log'] = weights[72]
    weights_map['u.mention_interaction_per_day:log_sum'] = weights[73]
    weights_map['u.mention_interaction_per_day:mean_log'] = weights[74]
    weights_map['u.mention_interaction_per_day:log_mean'] = weights[75]
    weights_map['u.mention_interaction_per_day:std_log'] = weights[76]
    weights_map['u.mention_interaction_per_day:log_std'] = weights[77]

    weights_map['u.hashtag_interaction:sum_log'] = weights[78]
    weights_map['u.hashtag_interaction:log_sum'] = weights[79]
    weights_map['u.hashtag_interaction:mean_log'] = weights[80]
    weights_map['u.hashtag_interaction:log_mean'] = weights[81]
    weights_map['u.hashtag_interaction:std_log'] = weights[82]
    weights_map['u.hashtag_interaction:log_std'] = weights[83]
    weights_map['u.hashtag_interaction_per_day:sum_log'] = weights[84]
    weights_map['u.hashtag_interaction_per_day:log_sum'] = weights[85]
    weights_map['u.hashtag_interaction_per_day:mean_log'] = weights[86]
    weights_map['u.hashtag_interaction_per_day:log_mean'] = weights[87]
    weights_map['u.hashtag_interaction_per_day:std_log'] = weights[88]
    weights_map['u.hashtag_interaction_per_day:log_std'] = weights[89]

    weights_map['u.rt_interaction:sum_log'] = weights[90]
    weights_map['u.rt_interaction:log_sum'] = weights[91]
    weights_map['u.rt_interaction:mean_log'] = weights[92]
    weights_map['u.rt_interaction:log_mean'] = weights[93]
    weights_map['u.rt_interaction:std_log'] = weights[94]
    weights_map['u.rt_interaction:log_std'] = weights[95]
    weights_map['u.rt_interaction_per_day:sum_log'] = weights[96]
    weights_map['u.rt_interaction_per_day:log_sum'] = weights[97]
    weights_map['u.rt_interaction_per_day:mean_log'] = weights[98]
    weights_map['u.rt_interaction_per_day:log_mean'] = weights[99]
    weights_map['u.rt_interaction_per_day:std_log'] = weights[100]
    weights_map['u.rt_interaction_per_day:log_std'] = weights[101]

    weights_map['u.nbc_interaction:sum_log'] = weights[102]
    weights_map['u.nbc_interaction:log_sum'] = weights[103]
    weights_map['u.nbc_interaction:mean_log'] = weights[104]
    weights_map['u.nbc_interaction:log_mean'] = weights[105]
    weights_map['u.nbc_interaction:std_log'] = weights[106]
    weights_map['u.nbc_interaction:log_std'] = weights[107]
    weights_map['u.nbc_interaction_per_day:sum_log'] = weights[108]
    weights_map['u.nbc_interaction_per_day:log_sum'] = weights[109]
    weights_map['u.nbc_interaction_per_day:mean_log'] = weights[110]
    weights_map['u.nbc_interaction_per_day:log_mean'] = weights[111]
    weights_map['u.nbc_interaction_per_day:std_log'] = weights[112]
    weights_map['u.nbc_interaction_per_day:log_std'] = weights[113]




    top_videos.each do |v|
      feature_dot = {}
      feature_dot['v.mention'] = v['features_arr'][0] * weights[0]
      feature_dot['v.hashtag'] = v['features_arr'][1] * weights[1]
      feature_dot['v.rt'] = v['features_arr'][2] * weights[2]
      feature_dot['v.nbc'] = v['features_arr'][3] * weights[3]
      feature_dot['v.tweet'] = v['features_arr'][4] * weights[4]
      feature_dot['v.a_views'] = v['features_arr'][5] * weights[5]
      
      feature_dot['u.mention'] = 0
      for i in 6..11
        feature_dot['u.mention'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.mention_per_day'] = 0
      for i in 12..17
        feature_dot['u.mention_per_day'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.hashtag'] = 0
      for i in 18..23
        feature_dot['u.hashtag'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.hashtag_per_day'] = 0
      for i in 24..29
        feature_dot['u.hashtag_per_day'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.rt'] = 0
      for i in 30..35
        feature_dot['u.rt'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.rt_per_day'] = 0
      for i in 36..41
        feature_dot['u.rt_per_day'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.nbc'] = 0
      for i in 42..47
        feature_dot['u.nbc'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.nbc_per_day'] = 0
      for i in 48..53
        feature_dot['u.nbc_per_day'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.tweet'] = 0
      for i in 54..59
        feature_dot['u.tweet'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.tweet_per_day'] = 0
      for i in 60..65
        feature_dot['u.tweet_per_day'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.mention_interaction'] = 0
      for i in 66..71
        feature_dot['u.mention_interaction'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.mention_interaction_per_day'] = 0
      for i in 72..77
        feature_dot['u.mention_interaction_per_day'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.hashtag_interaction'] = 0
      for i in 78..83
        feature_dot['u.hashtag_interaction'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.hashtag_interaction_per_day'] = 0
      for i in 84..89
        feature_dot['u.hashtag_interaction_per_day'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.rt_interaction'] = 0
      for i in 90..95
        feature_dot['u.rt_interaction'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.rt_interaction_per_day'] = 0
      for i in 96..101
        feature_dot['u.rt_interaction_per_day'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.nbc_interaction'] = 0
      for i in 102..107
        feature_dot['u.nbc_interaction'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.nbc_interaction_per_day'] = 0
      for i in 108..113
        feature_dot['u.nbc_interaction_per_day'] += v['features_arr'][i] * weights[i]
      end

      v['feature_dot'] = feature_dot
    end

    if sort_by != "model_rank"
      new_top_videos = []
      top_videos.each.sort{|a,b|
        a['feature_dot'][sort_by] <=> b['feature_dot'][sort_by]
      } do |v|
        new_top_videos << v
      end

      top_videos = new_top_videos
    end

    render json: {
      'status' => 'success',
      'top_videos' => top_videos[0, 100],
      'weights' => weights.inspect,
      'weights_map' => weights_map
    }
  end
end
