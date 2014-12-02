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
    w_coll = db['predictions_' + upload_date]

    top_videos = []
    score_rank = 1
    coll.find(filter,
              {
                :sort => ['score', 'desc'],
              }).each do |result|
      top_videos << {
        'vid_id' => result['id'],
        'score' => result['score'],
        'actual' => result['actual'],
        'upload_date' => result['upload_date'],
        'a_views' => number_with_delimiter(result['A_views']),
        'b_views' => number_with_delimiter(result['B_views']),
        'features' => result['features'].inspect,
        'model_rank' => score_rank
      }

      score_rank += 1
    end

    a_rank = 1
    top_videos.sort{|a,b| b['a_views'] <=> a['a_views']}.each do |v|
      v['a_rank'] = a_rank
      a_rank += 1
    end

    b_rank = 1
    top_videos.sort{|a,b| b['b_views'] <=> a['b_views']}.each do |v|
      v['b_rank'] = b_rank
      b_rank += 1
    end

    weights = w_coll.find_one()

    render json: {
      'status' => 'success',
      'top_videos' => top_videos[0, 100]
      'weights' => weights['weights'].inspect
    }
  end
end
