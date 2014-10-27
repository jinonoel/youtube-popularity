class YoutubePopularityController < ApplicationController

  def index
  end

  def doAction
    upload_date = params['upload_date']

    conn = Mongo::Connection.new('localhost')
    db = conn['nicta']
    coll = db['predictions']

    top_videos = []
    coll.find({'upload_date' => upload_date},
              {
                :sort => ['score', 'desc'],
                :limit => 100
              }).each do |result|
      top_videos << {
        'vid_id' => result['id'],
        'score' => result['score'],
        'actual' => result['actual'],
        'upload_date' => result['upload_date'],
        'a_views' => result['A_views'],
        'b_views' => result['B_views']
      }
    end

    render json: {
      'status' => 'success',
      'top_videos' => top_videos
    }
  end
end
