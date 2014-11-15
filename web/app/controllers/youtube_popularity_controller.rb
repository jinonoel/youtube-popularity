class YoutubePopularityController < ApplicationController

  def index
  end

  def number_with_delimiter(number, delimiter=",")
    number.to_s.gsub(/(\d)(?=(\d\d\d)+(?!\d))/, "\\1#{delimiter}")
  end

  def doAction
    upload_date = params['upload_date']

    conn = Mongo::Connection.new('localhost')
    db = conn['nicta']
    coll = db['predictions_' + upload_date]

    top_videos = []
    coll.find({},
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
        'b_views' => number_with_delimiter(result['B_views'])
      }
    end

    render json: {
      'status' => 'success',
      'top_videos' => top_videos
    }
  end
end
