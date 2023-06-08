
controllers/api/vi/authentication_controller.rb

module Api
    module V1
     
    
        class AuthenticationController < ApplicationController
            skip_before_action :authorized, only: [:create]

            def create
                member = Memeber.find_by(email: params[:email])
                if member && member.authenticate(params[:password])
                  token = encode_token({ user_id: member.id })
                  render json: { token: token }
                else
                  render json: { error: 'Invalid email or password' }, status: :unauthorized
                end
            end





        end


    end

end    


  



controllers/api/vi/memebers_controller.rb


module Api
    module V1
  


       class MemebersController < ApplicationController
            skip_before_action :authorized, only: [:create]
            def create
                memeber = Memeber.new(memeber_params)
                if memeber.save
                  token = encode_token({ user_id: memeber.id })
                  render json: { user: memeber, token: token }
                else
                  render json: { error: memeber.errors.full_messages }, status: :unprocessable_entity
                end
            end

            private

            def memeber_params
                params.require(:memeber).permit(:email, :password)
            end

       end

    end  


end    








controllers/api/vi/application_controller.rb





class ApplicationController < ActionController::API
    before_action :authorized

    def encode_token(payload)
        JWT.encode(payload, ENV['JWT_SECRET'])
    end
    
    def decode_token(token)
        JWT.decode(token, ENV['JWT_SECRET'])[0]
    end

  
    def authorized
      render json: { error: 'Please log in' }, status: :unauthorized unless logged_in?
    end
  
    def logged_in?
      current_user.present?
    end
  
    def current_user
      if decoded_token
        memeber_id = decoded_token['memeber_id']
        @memeber ||= Memeber.find_by(id: memeber_id)
      end
    end
  
    def decoded_token
      token = request.headers['Authorization']
      begin
        decode_token(token)
      rescue JWT::DecodeError
        nil
      end
    end


end













nodels/memebr.rb


class Memeber < ApplicationRecord
    has_secure_password
    validates :email, presence: true, uniqueness: true
end







routes.rb


Rails.application.routes.draw do

  namespace :api do
    namespace :v1 do
      resources :memebers, only: [:create]
      post '/login', to: 'authentication#create'
     end
  end    



end


















































....
