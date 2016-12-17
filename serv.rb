require 'sinatra'
require 'sinatra-websocket'

class Application < Sinatra::Base

  set :bind, '0.0.0.0'
  set :server, 'thin'
  set :sockets, []
  set :views, 'views'

  get '/' do
    if !request.websocket?
      erb :index
    else
      request.websocket do |ws|
        ws.onopen do
          puts("User connected")
          # ws.send("Hello World!")
        end
        ws.onmessage do |msg|
          EM.next_tick { settings.sockets.each{|s| s.send(msg) } }
        end
        ws.onclose do
          warn("websocket closed")
          settings.sockets.delete(ws)
        end
      end
    end
  end

  get '/esp' do
    if request.websocket?
      request.websocket do |ws|
        ws.onopen do
          puts("ESP connected")
          settings.sockets << ws
        end
        ws.onmessage do |msg|
          EM.next_tick { settings.sockets.each{|s| s.send(msg) } }
        end
        ws.onclose do
          warn("ESP websocket closed")
          settings.sockets.delete(ws)
        end
      end
    end
  end

  post '/' do
	   $stream_url = params[:stream_url]
	   redirect back
  end

end
