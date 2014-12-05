class YoutubePopularityController < ApplicationController

  def index
  end

  def number_with_delimiter(number, delimiter=",")
    number.to_s.gsub(/(\d)(?=(\d\d\d)+(?!\d))/, "\\1#{delimiter}")
  end

  def doAction
    upload_date = params['upload_date']
    threshold = params['threshold'].to_i

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
        'model_rank' => score_rank
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
    weights_map['u.hashtag:sum_log'] = weights[12]
    weights_map['u.hashtag:log_sum'] = weights[13]
    weights_map['u.hashtag:mean_log'] = weights[14]
    weights_map['u.hashtag:log_mean'] = weights[15]
    weights_map['u.hashtag:std_log'] = weights[16]
    weights_map['u.hashtag:log_std'] = weights[17]
    weights_map['u.rt:sum_log'] = weights[18]
    weights_map['u.rt:log_sum'] = weights[19]
    weights_map['u.rt:mean_log'] = weights[20]
    weights_map['u.rt:log_mean'] = weights[21]
    weights_map['u.rt:std_log'] = weights[22]
    weights_map['u.rt:log_std'] = weights[23]
    weights_map['u.nbc:sum_log'] = weights[24]
    weights_map['u.nbc:log_sum'] = weights[25]
    weights_map['u.nbc:mean_log'] = weights[26]
    weights_map['u.nbc:log_mean'] = weights[27]
    weights_map['u.nbc:std_log'] = weights[28]
    weights_map['u.nbc:log_std'] = weights[29]
    weights_map['u.tweet:sum_log'] = weights[30]
    weights_map['u.tweet:log_sum'] = weights[31]
    weights_map['u.tweet:mean_log'] = weights[32]
    weights_map['u.tweet:log_mean'] = weights[33]
    weights_map['u.tweet:std_log'] = weights[34]
    weights_map['u.tweet:log_std'] = weights[35]

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

      feature_dot['u.hashtag'] = 0
      for i in 12..17
        feature_dot['u.hashtag'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.rt'] = 0
      for i in 18..23
        feature_dot['u.rt'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.nbc'] = 0
      for i in 24..29
        feature_dot['u.nbc'] += v['features_arr'][i] * weights[i]
      end

      feature_dot['u.tweet'] = 0
      for i in 30..35
        feature_dot['u.tweet'] += v['features_arr'][i] * weights[i]
      end

      v['feature_dot'] = feature_dot
    end

    render json: {
      'status' => 'success',
      'top_videos' => top_videos[0, 100],
      'weights' => weights.inspect,
      'weights_map' => weights_map.inspect
    }
  end
end
