class YoutubePopularityController < ApplicationController

  def index
  end

  def doAction
    start_date = params['start_date']

    render json: {'hello' => 'world', 'foo' => params[:start_date]}
  end
end
