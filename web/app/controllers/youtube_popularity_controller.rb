class YoutubePopularityController < ApplicationController

  def index
  end

  def doAction
    start_date = params['start_date']

    conn = Mongo::Connection.new('localhost')
    db = conn['nicta']
    coll = db['predictions']

    top_videos = []
    coll.find({},
              {
                :sort => ['score', 'desc'],
                :limit => 100
              }).each do |result|
      top_videos << {
        'vid_id' => result['id'],
        'score' => result['score'],
        'actual' => result['actual']
      }
    end

    render json: {
      'status' => 'success',
      'top_videos' => top_videos
    }
  end
end
